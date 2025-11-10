from google import genai
from dotenv import load_dotenv
from retriever import hybrid_search
import os
import time

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

query = input("Ask me a question! ")

context = hybrid_search(query)

prompt = ""

with open("prompt.txt", "r") as f:
    for line in f.readlines():
        prompt += line

prompt += f"""
### Retrieved context:
{context}
"""

print("\nGenerating response, just a second!", end="", flush=True)
for _ in range(3): 
    time.sleep(0.4)
    print(".", end="", flush=True)
print("\n")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=query,
)

print()

print (response)