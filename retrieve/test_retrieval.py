"""
Retrieval test script.

Usage:
    # Run the default test queries
    python retrieve/test_retrieval.py

    # Pass a custom query directly
    python retrieve/test_retrieval.py "what is the pumping lemma?"

    # Interactive mode — type queries one by one
    python retrieve/test_retrieval.py --interactive
"""

import sys
from retrieve.hybrid_retriever import HybridRetriever
from stores.metadata_store import MetadataStore
from pathlib import Path

PROJECT_ROOT       = Path(__file__).resolve().parent.parent
METADATA_FILE_PATH = PROJECT_ROOT / "data" / "dense" / "sql" / "docs_metadata.db"

# Default queries that cover a range of ToC topics
DEFAULT_QUERIES = [
    "what is the formal definition of a DFA?",
    "pumping lemma for regular languages",
    "context free grammar",
    "Turing machine halting problem",
    "NP completeness and polynomial time reduction",
    "pushdown automaton stack",
]

K                   = 5     # number of chunks to retrieve
DENSE_TO_SPARSE     = 0.5   # 50/50 dense vs sparse


def retrieve(query: str) -> list[tuple]:
    """Return list of (score, week, section, subsection, text) for a query."""
    retriever      = HybridRetriever()
    retrieved_docs = retriever.retrieve(query, K, DENSE_TO_SPARSE)
    metadata_store = MetadataStore(METADATA_FILE_PATH)

    results = []
    for doc_id, score in retrieved_docs:
        _, text, section, subsection, week = metadata_store.fetch(doc_id)
        results.append((score, week, section, subsection, text))

    metadata_store.close_connection()
    return results


def print_results(query: str, results: list[tuple]) -> None:
    print("\n" + "=" * 70)
    print(f"QUERY: {query}")
    print("=" * 70)

    if not results:
        print("  No results returned.")
        return

    for i, (score, week, section, subsection, text) in enumerate(results, 1):
        print(f"\n  [{i}] Score: {score:.4f} | Week: {week} | {section} > {subsection}")
        print(f"  {'-' * 60}")
        # Print first 300 chars of the chunk so output stays readable
        preview = text.strip().replace("\n", " ")
        print(f"  {preview[:300]}{'...' if len(preview) > 300 else ''}")

    print()


def run_queries(queries: list[str]) -> None:
    for query in queries:
        results = retrieve(query)
        print_results(query, results)


if __name__ == "__main__":
    args = sys.argv[1:]

    if "--interactive" in args:
        print("Retrieval test — interactive mode. Type 'quit' to exit.\n")
        while True:
            try:
                query = input("Query: ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if query.lower() in ("quit", "exit", "q"):
                break
            if query:
                results = retrieve(query)
                print_results(query, results)

    elif args:
        # Single query passed as CLI argument
        run_queries([" ".join(args)])

    else:
        # Run all default queries
        print(f"Running {len(DEFAULT_QUERIES)} default queries (k={K}, dense/sparse={DENSE_TO_SPARSE})...")
        run_queries(DEFAULT_QUERIES)
