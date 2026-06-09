from ingest.indexer import *

documents = load_documents()

build_dense_indices(documents)
build_sparse_corpus(documents)