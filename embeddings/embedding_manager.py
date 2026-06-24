from typing import List
import numpy as np
import requests
import os

HF_API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

class EmbeddingManager:
    """
    Handles embedding generation using HuggingFace Inference API.
    No local model loaded — zero memory overhead.
    """
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_name}"
        self.headers = {"Authorization": f"Bearer {os.environ['HF_API_TOKEN']}"}
        self.embedding_dim = 384  # all-MiniLM-L6-v2 outputs 384 dims

    def _call_api(self, texts: List[str]) -> np.ndarray:
        """Call HF Inference API and return normalized embeddings."""
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json={"inputs": texts, "options": {"wait_for_model": True}}
        )
        if response.status_code != 200:
            raise ValueError(f"HF API error {response.status_code}: {response.text}")
        
        embeddings = np.array(response.json(), dtype=np.float32)
        
        # Normalize (L2)
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        return embeddings / np.maximum(norms, 1e-10)

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
