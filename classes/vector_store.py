import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim, index_path=None):

        if (index_path):
            self.index = faiss.read_index(index_path)
            self.dim = self.index.d

        else:
            base_index = faiss.IndexFlatIP(dim)
            self.index = faiss.IndexIDMap(base_index)
            self.dim = dim

    def search(self, query_embedding, k=5):
        query_embedding = np.array([query_embedding], dtype=np.float32)
        faiss.normalize_L2(query_embedding)

        D, I = self.index.search(query_embedding, k)

        return D[0], I[0]        

    def add_with_ids(self, embeddings, ids):
        ids = np.array(ids, dtype=np.int64)

        assert len(embeddings) == len(ids), "Embeddings and IDs mismatch"
        
        faiss.normalize_L2(embeddings)
        self.index.add_with_ids(embeddings, ids)

    def save_db(self, path):
        faiss.write_index(self.index, str(path / "faiss_index.index"))