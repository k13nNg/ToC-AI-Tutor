from collections import defaultdict
import pickle
import ollama
import numpy as np
import chromadb

client = chromadb.PersistentClient(path="./chroma_data")

notes_collection = client.get_collection(name="lessons")
exercises_collection = client.get_collection(name="exercises")

# weight the dense search ranks more as we are working with highly technical documents, 
# which might results in contextual/ conceptual questions. For example: "What's a PDA?"
RRF_K = 60
BM25_WEIGHT = 1.0    
DENSE_WEIGHT = 2.0   

# load the saved BM25 model and the uuid map
with open("bm25_index.pickle", "rb") as f:
    bm25 = pickle.load(f)

with open("notes_id_map.pickle", "rb") as f: 
    id_map = pickle.load(f)

def calculate_rrf(rank):
    return 1.0 / (RRF_K + rank)


def exercises_search(query_embedding, top_k = 5):
    retrieved_docs = exercises_collection.query(
        query_embeddings=query_embedding["embeddings"],
        n_results=top_k
    )

    results = []

    for doc in retrieved_docs["documents"]:
        results += doc

    return '\n\n'.join(results)

def notes_search(query_text, query_embedding, top_k = 5):
    # Sparse search
    tokenized_query= query_text.split(" ")

    bm25_scores = np.array(bm25.get_scores(tokenized_query))
    bm25_int_ranks = np.argsort(bm25_scores)[::-1][:top_k * 2].tolist()
    bm25_uuid_ranks = [id_map[i] for i in bm25_int_ranks]

    # Dense search
    results = notes_collection.query(
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
    
    retrieved_docs = [notes_collection.get(ids=[doc_id]) for doc_id, _ in sorted_fused_items]

    output = []

    for doc in retrieved_docs:
        output += doc["documents"]

    return '\n\n'.join(output)