import chromadb
import ollama

client = chromadb.PersistentClient(path="./chroma_data")

collection = client.get_collection(name="exercises")

query_texts=[
    "Exercises on Turing Machine"
]

query_embeddings = ollama.embed("embeddinggemma", query_texts)

results= collection.query(
    query_embeddings=query_embeddings["embeddings"],
    n_results=5,
    include=['distances', 'documents']
)

# Assuming query_texts is your original list: ["What is a set?", "What is a PDA?", ...]
for i, (query_docs, query_dists) in enumerate(zip(results["documents"], results["distances"])):
    query_text = query_texts[i]
    print(f"\n--- Query {i + 1}: {query_text} ---")

    # This loop iterates through the individual retrieved items and their distances
    for rank, (doc_text, distance) in enumerate(zip(query_docs, query_dists)):
        # Lower distance means higher similarity/relevance
        print(f"Rank {rank + 1} (Distance: {distance:.4f}):")
        print(f"  {doc_text[:100]}...") # Print first 100 characters of the document
        print("-----")