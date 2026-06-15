from retrieve.context_builder import *
from groq import Groq
from dotenv import load_dotenv
import time
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# LLM_NAME = "llama-3.1-8b-instant"  # or "llama-3.3-70b-versatile"
LLM_NAME = "llama-3.3-70b-versatile"

def ask_llm(query, chat_history):
    t0 = time.time()

    context = build_context(query, k=2)
    print("Context build:", time.time() - t0)

    with open("retrieve/prompt.txt", "r", encoding="utf-8") as f:
        system_prompt = f.read()

    messages = [
        {"role": "system", "content": system_prompt},
        *chat_history[:-1],  # cap history
        {
            "role": "user",
            "content": f"""Question: {query}

Context:
{context}"""
        }
    ]

    t1 = time.time()

    response = client.chat.completions.create(
        model=LLM_NAME,
        messages=messages,
        temperature=0.2
    )

    print("Generation:", time.time() - t1)
    print("Total:", time.time() - t0)
    print("-" * 16)

    return response.choices[0].message.content