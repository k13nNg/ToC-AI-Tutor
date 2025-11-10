from collections import defaultdict
import pickle
import heapq
import ollama
import numpy as np
import chromadb

client = chromadb.PersistentClient(path="./chroma_data")

collection = client.get_collection(name="lessons")

RRF_K = 60
BM25_WEIGHT = 1.0    
DENSE_WEIGHT = 2.0   

with open("bm25_index.pickle", "rb") as f:
    bm25 = pickle.load(f)

with open("all_chunks.pickle", "rb") as f:
    all_chunks = pickle.load(f)

with open("id_map.pickle", "rb") as f: 
    id_map = pickle.load(f)

def calculate_rrf(rank):
    return 1.0 / (RRF_K + rank)

def hybrid_search(query_text, top_k = 5):
    # Sparse search
    tokenized_query= query_text.split(" ")

    bm25_scores = np.array(bm25.get_scores(tokenized_query))
    bm25_int_ranks = np.argsort(bm25_scores)[::-1][:top_k * 2].tolist()

    # CRITICAL FIX: Convert integer indices to string UUIDs for fusion
    bm25_uuid_ranks = [id_map[i] for i in bm25_int_ranks]

    # Dense search
    query_embedding = ollama.embed("embeddinggemma", query_text)

    results = collection.query(
        query_embeddings=query_embedding["embeddings"],
        n_results=top_k * 2
    )

    dense_ranks = results["ids"][0]

    # Initialize the fusion dictionary
    fused_scores = defaultdict(float)

    # Process Sparse (BM25) Ranks
    for rank, doc_id in enumerate(bm25_uuid_ranks, 1):
        rrf_score = BM25_WEIGHT * calculate_rrf(rank)
        fused_scores[doc_id] += rrf_score
        
    # Process Dense ranks
    for rank, doc_id in enumerate(dense_ranks, 1):
        rrf_score = DENSE_WEIGHT * calculate_rrf(rank)
        fused_scores[doc_id] += rrf_score
        
    # Sort and Return final list of UUIDs
    sorted_fused_items = sorted(
        fused_scores.items(), 
        key=lambda item: item[1], 
        reverse=True
    )[:top_k] 
    
    return [doc_id for doc_id, _ in sorted_fused_items]

results = hybrid_search("What is a set?")

for r in range(len(results)):
    print("Result", r)
    print("--------")
    if isinstance(results[r], int):
        print(all_chunks[results[r]])
    else:
        print(collection.get(ids=[results[r]])["documents"][0])
    print("--------")
    
