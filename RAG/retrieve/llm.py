from retrieve.context_builder import *
from retrieve.query_router import route, GREETING_RESPONSE, OFF_TOPIC_RESPONSE
import ollama
import time
from pathlib import Path

LLM_NAME = "llama3.2"
CONTEXT_RETRIEVED_NUM = 2
PROMPT_PATH = Path(__file__).resolve().parent / "prompt.txt"

def ask_llm(query, chat_history):
    t0 = time.time()

    decision = route(query, chat_history)

    if decision == "greeting":
        yield GREETING_RESPONSE
        return

    if decision == "off_topic":
        yield OFF_TOPIC_RESPONSE
        return

    context = build_context(query, k=CONTEXT_RETRIEVED_NUM)
    t1 = time.time()
    print(f"Context Build: {t1 - t0:.3f}s")

    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    messages = [
        {"role": "system", "content": system_prompt},
        *chat_history[-4:],
        {
            "role": "user",
            "content": f"Question: {query}\n\nContext:\n{context}"
        }
    ]

    try:
        for chunk in ollama.chat(model=LLM_NAME, messages=messages, stream=True):
            token = chunk["message"]["content"]
            if token:
                yield token
    finally:
        t2 = time.time()
        print(f"Generation: {t2 - t1:.3f}s")
        print(f"Total: {t2 - t0:.3f}s")
        print("-" * 16)
