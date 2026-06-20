from retrieve.hybrid_retriever import HybridRetriever
from stores.metadata_store import MetadataStore
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
METADATA_FILE_PATH = PROJECT_ROOT / "data" / "dense" / "sql" / "docs_metadata.db"

def format_chunk(chunk, score):
    """
    Return the chunk in the format:

    ---
    [Week | Section | Subsection | Score]
    Text
    ---

    Note: Input chunk is a 5 tuple (doc_id, text, section, subsection, week)

    """
    _, text, section, subsection, week = chunk

    return f"""[Week: {week} | Section: {section} | Subsection: {subsection} | Score: {score} ]\n\n{text}
    """

def build_context(query, k = 5, DENSE_TO_SPARSE_RATIO = 0.5):
    retriever = HybridRetriever()
    retrieved_docs =  retriever.retrieve(query, k, DENSE_TO_SPARSE_RATIO)
    metadata_store = MetadataStore(METADATA_FILE_PATH)
    output = []

    for doc_id, doc_score in retrieved_docs:
        chunk = metadata_store.fetch(doc_id)
        if chunk is None:
            print(f"Warning: doc_id {doc_id} not found in metadata store, skipping.")
            continue
        output.append(format_chunk(chunk, doc_score))

    metadata_store.close_connection()

    return "\n\n---\n\n".join(output)





