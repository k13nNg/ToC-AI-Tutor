from langchain_text_splitters import MarkdownHeaderTextSplitter
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from stores.metadata_store import MetadataStore
from stores.vector_store import VectorStore

import numpy as np
import pickle
import shutil

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

MARKDOWN_FILE_PATH = PROJECT_ROOT / "data" / "markdown_latex"
FAISS_INDEX_FILE_PATH = PROJECT_ROOT / "data" / "dense" / "faiss"
BM25_INDEX_FILE_PATH = PROJECT_ROOT / "data" / "sparse"

HEADERS_TO_SPLIT = [("#", "Section"),
                      ("##", "Subsection")]

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

METADATA_CONNECTION_PATH = PROJECT_ROOT / "data" / "dense" / "sql" / "docs_metadata.db"


def clear_artifacts():
    """Delete all previously built index artifacts."""
    # FAISS index
    faiss_file = FAISS_INDEX_FILE_PATH / "faiss_index.index"
    if faiss_file.exists():
        faiss_file.unlink()
        print(f"Deleted: {faiss_file.relative_to(PROJECT_ROOT)}")

    # SQLite metadata DB
    if METADATA_CONNECTION_PATH.exists():
        METADATA_CONNECTION_PATH.unlink()
        print(f"Deleted: {METADATA_CONNECTION_PATH.relative_to(PROJECT_ROOT)}")

    # BM25 corpus
    bm25_file = BM25_INDEX_FILE_PATH / "bm25_corpus.pkl"
    if bm25_file.exists():
        bm25_file.unlink()
        print(f"Deleted: {bm25_file.relative_to(PROJECT_ROOT)}")

def preprocess(text):
    """
    Convert all words to lowercase and split by blank space
    Necessary for BM25 corpus building phase
    """
    return text.lower().split()

def load_documents():
    """
    Create a list of Document objects from the Markdown files
    """
    documents = []

    markdown_splitter = MarkdownHeaderTextSplitter(HEADERS_TO_SPLIT)

    # iterate through the weeks
    for i in range(0, 12):
        # skip Week 7, since it's Reading Week and no content exist
        if (i != 7):
            # open the markdown file
            with open(MARKDOWN_FILE_PATH / f"Week_{i}" / f"Week_{i}_content.md", "r", encoding="utf-8") as file:
                # split the file
                markdown_content = file.read()
                docs = markdown_splitter.split_text(markdown_content)

                # add week to the chunks (useful for later citations)
                for doc in docs:
                    doc.metadata["Week"] = i
                
                # add docs to faiss_corpus
                documents += docs

    return documents

def build_dense_indices(documents):
    """
    Create and save: 
        - a FAISS index
        - a SQLite local database
    """
    try:
        # initiate connection to SQLite
        metadata_store = MetadataStore(str(METADATA_CONNECTION_PATH))

        # embed documents using HuggingFace model
        embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME
        )
        docs_content = [doc.page_content for doc in documents]

        embedded_docs = embedding_model.embed_documents(docs_content)
        embedded_docs = np.array(embedded_docs, dtype=np.float32)

        vector_store = VectorStore(embedded_docs.shape[1])
        ids = np.arange(len(documents), dtype=np.int64)

        vector_store.add_with_ids(embedded_docs, ids)
        vector_store.save_db(FAISS_INDEX_FILE_PATH)

        for i, doc in enumerate(documents):
            if ("Section" in doc.metadata and "Subsection" in doc.metadata):
                metadata_store.insert(i, 
                                    doc.page_content, 
                                    doc.metadata["Section"], 
                                    doc.metadata["Subsection"],
                                    doc.metadata["Week"])
            else:
                metadata_store.insert(i, 
                                    doc.page_content, 
                                    "", 
                                    "",
                                    doc.metadata["Week"])
        vector_store.save_db(FAISS_INDEX_FILE_PATH)
        metadata_store.close_connection()
        return "Dense indices built succesfully"
    
    except Exception as e:
        return f"Failed to build dense indices.\n\n Error: {e}"


def build_sparse_corpus(documents):
    """
    Return a BM25 index
    """
    try:
        corpus = []

        for doc in documents:
            section = doc.metadata.get("Section", "")
            subsection = doc.metadata.get("Subsection", "")
            week = doc.metadata.get("Week", "")

            text = f"""
            Section: {section}
            Subsection: {subsection}
            Week: {week}

            {doc.page_content}
            """

            corpus.append(preprocess(text))

        with open(BM25_INDEX_FILE_PATH / "bm25_corpus.pkl", "wb") as f:
            pickle.dump(corpus, f)

        return "BM25 index built successfully"
    
    except Exception as e:
        return f"Failed to build BM25 index.\n\n Error: {e}"
