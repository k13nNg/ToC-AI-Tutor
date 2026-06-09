from retrieve.context_builder import *
import ollama

def ask_llm(query):
    context = build_context(query)

    with open("retrieve/prompt.txt", "r", encoding="utf-8") as f:
        system_prompt = f.read()

    user_message = f"""
QUESTION:
{query}

CONTEXT:
{context}
"""

    response = ollama.chat(
        model="llama3.1",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        stream = True
    )

    return response["message"]["content"]