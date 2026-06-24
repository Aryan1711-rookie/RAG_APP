from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

class EmbeddingManager:
    """
    Handles embedding generation using SentenceTransformer.
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None

        # self._load_model()
    
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
        """Generate embeddings"""

        if self.model is None:
            raise ValueError("Model not loaded.")

        embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            normalize_embeddings=True
        )

        return embeddings
    
    def generate_query_embeddings(self, query: str) -> np.ndarray:
        """Generate query embeddings."""

        if self.model is None:
            raise ValueError("Model not loaded.")

        query = (
            "Represent this sentence for searching."
            f"relevant passages: {query}"
        )

        embedding = self.model.encode(query, normalize_embeddings=True)

        return embedding
    
    def get_embedding_dimension(self) -> int:

        if self.model is None:
            raise ValueError("Model not loaded")

        return self.model.get_sentence_embedding_dimension()
