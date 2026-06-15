# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaEmbeddings
from pathlib import Path
from rank_bm25 import BM25Okapi
from collections import defaultdict
from stores.vector_store import VectorStore

import pickle
import numpy as np


QUERY_EXPANSIONS = {
    "dfa": [
        "deterministic finite automaton"
    ],

    "nfa": [
        "nondeterministic finite automaton",
        "non deterministic finite automaton"
    ],

    "tm": [
        "turing machine"
    ],

    "pda": [
        "pushdown automaton"
    ],

    "cfg": [
        "context free grammar"
    ]
}

def expand_query(query):
    expanded = query

    words = query.lower().split()

    for word in words:
        if word in QUERY_EXPANSIONS:
            expansions = QUERY_EXPANSIONS[word]
            expanded += " " + " ".join(expansions)

    return expanded


PROJECT_ROOT = Path(__file__).resolve().parent.parent

EMBEDDING_MODEL_NAME = "nomic-embed-text"
FAISS_INDEX_FILE_PATH = PROJECT_ROOT / "data" / "dense" / "faiss" / "faiss_index.index"
BM25_CORPUS_FILE_PATH = PROJECT_ROOT / "data" / "sparse" / "bm25_corpus.pkl"

class HybridRetriever:
    def __init__(self):
        self.embedding_model = OllamaEmbeddings(model=EMBEDDING_MODEL_NAME)
        self.vector_db = VectorStore(index_path=str(FAISS_INDEX_FILE_PATH))

        with open(BM25_CORPUS_FILE_PATH, "rb") as f:
            corpus = pickle.load(f)

        self.bm25 = BM25Okapi(corpus)

    def dense_retrieve(self, query, k = 5):
        """
        Retrieve k nearest documents using FAISS index
        """
        query_embedding = self.embedding_model.embed_query(expand_query(query))

        _, ids = self.vector_db.search(query_embedding, k)

        return ids

    def sparse_retrieve(self, query, k=5):
        """
        Retrieve k nearest documents using BM25
        """
        def preprocess(text):
            """
            Convert all words to lowercase and split by blank space
            Necessary for BM25 corpus building phase
            """
            return text.lower().split()

        scores = self.bm25.get_scores(preprocess(expand_query(query)))
        ranked_ids = np.argsort(scores)[::-1][:k]

        return ranked_ids

    def rrf(self, rank_lists, weights = None, k=60):
        """
        Return weighted fusioned scores of documents in rank_lists
        """

        # initialize equal weights for each component if no weights is given
        if weights is None:
            weights = [1] * len(rank_lists)

        scores = defaultdict(float)

        for ranked_list, weight in zip(rank_lists, weights):
            for rank, doc_id in enumerate(ranked_list, start=1):
                scores[int(doc_id)] += weight * (1 / (k + rank))

        return sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
    
    def retrieve(self, query, k=5, DENSE_TO_SPARSE_RATIO = 0.5):
        """
        Return k most relevant documents, ranked by RRF
        """
        dense_ranked = self.dense_retrieve(query, k)
        sparse_ranked = self.sparse_retrieve(query, k)

        dense_weights = DENSE_TO_SPARSE_RATIO
        sparse_weights = 1.0 - DENSE_TO_SPARSE_RATIO

        results = self.rrf([dense_ranked, sparse_ranked],
                           weights = [dense_weights, sparse_weights])

        return results
            

