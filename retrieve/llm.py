from retrieve.context_builder import *
import ollama
import time 

LLM_NAME = "llama3.2"

def ask_llm(query, chat_history):
    # context = build_context(query)

    t0 = time.time()

    context = build_context(query, k = 2)
    print("Context build:", time.time() - t0)


    with open("retrieve/prompt.txt", "r", encoding="utf-8") as f:
        system_prompt = f.read()

#     user_message = f"""
# Student Question:
# {query}

# Course Material:
# {context}
# """
    messages = [
    {"role": "system", "content": system_prompt},
    *chat_history[-4:],   # cap history
    {
        "role": "user",
        "content": f"""Question: {query}

Context:
{context}"""
    }
]
    messages.extend(chat_history)


    t1 = time.time()
    
    response = ollama.chat(
        model=LLM_NAME,
        messages=messages
    )

    # response = ollama.chat(
    #     model="llama3.2",
    #     messages=[
    #         {"role": "system", "content": system_prompt},
    #         {"role": "user", "content": user_message},
    #     ]
    # )
    print("Generation:", time.time() - t1)
    print("Total:", time.time() - t0)
    print("-" * 16)
    return response["message"]["content"]
