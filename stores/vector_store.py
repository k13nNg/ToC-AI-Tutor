import numpy as np
import faiss

class VectorStore:
    def __init__(self, dim=-1, index_path=None):

        if (index_path):
            self.index = faiss.read_index(index_path)
            self.dim = self.index.d

        else:
            base_index = faiss.IndexFlatIP(dim)
            self.index = faiss.IndexIDMap(base_index)
            self.dim = dim

    def search(self, query_embedding, k=5):
        """
        Return k most relevant documents using FAISS
        """
        query_embedding = np.array(query_embedding, dtype=np.float32)

        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        faiss.normalize_L2(query_embedding)

        D, I = self.index.search(query_embedding, k)

        return D[0], I[0]        

    def add_with_ids(self, embeddings, ids):
        """
        Add embeddings with ids to the index
        """
        ids = np.array(ids, dtype=np.int64)

        assert len(embeddings) == len(ids), "Embeddings and IDs mismatch"
        
        faiss.normalize_L2(embeddings)

        self.index.add_with_ids(embeddings, ids)

    def save_db(self, path):
        """
        Save the db in the specified path
        """
        faiss.write_index(self.index, str(path / "faiss_index.index"))