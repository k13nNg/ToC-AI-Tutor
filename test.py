import chromadb
import ollama

client = chromadb.PersistentClient(path="./chroma_data")

collection = client.get_collection(name="lessons")

query_texts=[
    "What is a set?",
    "What is a PDA?",
    "What is a mathematical set?"
]

query_embeddings = ollama.embed("embeddinggemma", query_texts)

results= collection.query(
    query_embeddings=query_embeddings["embeddings"],
    n_results=5
)

for i, query_results in enumerate(results["documents"]):
    print(f"\nQuery {i}")
    print("\n-----\n".join(query_results))
