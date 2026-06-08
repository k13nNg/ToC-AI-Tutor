from ingest.indexer import *

documents = load_documents()

print(build_sparse_corpus(documents))
print(build_dense_indices(documents))
