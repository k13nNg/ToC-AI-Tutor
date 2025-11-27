from google import genai
from dotenv import load_dotenv
from retriever import notes_search, exercises_search
import ollama
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

system_instruction = ""

with open("prompt.txt", "r") as f:
    system_instruction = f.read()

chat = client.chats.create(
    model="gemini-2.5-flash",
    config={"system_instruction": system_instruction}
)
 
while True:
    query = input("Student: ")

    query_embeddings = ollama.embed("embeddinggemma", query)

    retrieved_context = f"\n\nNotes:\n\n{
        notes_search(query, query_embeddings)
    }\n\nExercises:\n\n{
        exercises_search(query_embeddings)
    }"

    full_prompt = f"""
    ### Retrieved context:
    {retrieved_context}

    ### User Query:
    {query}
    """

    response = chat.send_message(full_prompt)

    print()
    print("AI Tutor:", response.text)
    print("-" * 20)