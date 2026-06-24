from typing import List
import numpy as np
import requests
import os


class EmbeddingManager:
   
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None

        self.embedding_dim = 384  # all-MiniLM-L6-v2 outputs 384 dims

    def _load_model(self):
        """Load embedding model."""

        try:
            print(f"Loading model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)

            print(f"Embedding dimensions: {self.model.get_embedding_dimension()}")

        except Exception as e:
            print(f"Failed to load model. {e}")
            raise
            
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts (batched in chunks of 32)."""
        all_embeddings = []
        for i in range(0, len(texts), 32):
            batch = texts[i:i+32]
            print(f"Embedding batch {i//32 + 1} ({len(batch)} texts)...")
            all_embeddings.append(self._call_api(batch))
        return np.vstack(all_embeddings)

    def generate_query_embeddings(self, query: str) -> np.ndarray:
        """Generate query embedding."""
        prefixed = f"Represent this sentence for searching relevant passages: {query}"
        result = self._call_api([prefixed])
        return result[0]  # return 1D array
    
    def get_embedding_dimension(self) -> int:

        if self.model is None:
            raise ValueError("Model not loaded")

        return self.model.get_sentence_embedding_dimension()
