from retrieve.context_builder import *
from retrieve.query_router import route, GREETING_RESPONSE, OFF_TOPIC_RESPONSE
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path
import time
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

LLM_NAME = "llama-3.3-70b-versatile"
CONTEXT_RETRIEVED_NUM = 3
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
        stream = client.chat.completions.create(
            model=LLM_NAME,
            messages=messages,
            temperature=0.2,
            stream=True
        )

        for chunk in stream:
            token = chunk.choices[0].delta.content
            if token:
                yield token
    finally:
        t2 = time.time()
        print(f"Generation: {t2 - t1:.3f}s")
        print(f"Total: {t2 - t0:.3f}s")
        print("-" * 16)
