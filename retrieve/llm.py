from retrieve.context_builder import *
import ollama
import time

LLM_NAME = "llama3.2"


def ask_llm(query, chat_history):
    """
    Generator that yields text chunks as they stream from Ollama.
    st.write_stream() in app.py collects and renders them incrementally.
    """
    t0 = time.time()

    context = build_context(query, k=2)
    print("Context build:", time.time() - t0)

    with open("retrieve/prompt.txt", "r", encoding="utf-8") as f:
        system_prompt = f.read()

    messages = [
        {"role": "system", "content": system_prompt},
        *chat_history[-4:],
        {"role": "user", "content": f"{query}\n\n{context}"}
    ]

    t1 = time.time()

    for chunk in ollama.chat(model=LLM_NAME, messages=messages, stream=True):
        token = chunk["message"]["content"]
        if token:
            yield token

    print("Generation:", time.time() - t1)
    print("Total:", time.time() - t0)
    print("-" * 16)
