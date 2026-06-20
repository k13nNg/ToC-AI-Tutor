import sys
from pathlib import Path

# Add RAG/ to path so its internal imports (stores, etc.) resolve correctly
sys.path.insert(0, str(Path(__file__).resolve().parent / "RAG"))

from RAG.ingest.indexer import load_documents, build_dense_indices, build_sparse_corpus, clear_artifacts

if __name__ == "__main__":
    print("Clearing old artifacts...")
    clear_artifacts()
    print()

    print("Loading documents...")
    documents = load_documents()
    print(f"Loaded {len(documents)} chunks.\n")

    print("Building dense indices (FAISS + SQLite)...")
    result = build_dense_indices(documents)
    print(result, "\n")

    print("Building sparse corpus (BM25)...")
    result = build_sparse_corpus(documents)
    print(result, "\n")

    print("Done.")
