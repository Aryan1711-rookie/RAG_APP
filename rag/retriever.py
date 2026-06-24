from typing import List, Dict, Any

from embeddings.embedding_manager import EmbeddingManager
from vector_db.vector_store import VectorStore
from database.supabase_client import supabase

class RAGRetriever:
    """Handles query-based retrieval from the vector_Store"""

    def __init__(self, vector_store: VectorStore, embedding_manager: EmbeddingManager):
        """
        Init the retriever
        
        Args:
            vector_store: Vector store containing documents embeddings
            embedding_manager: Manager for generating query embeddings
        """
        self.vector_store = vector_store
        self.embedding_manager = embedding_manager

    # def retrieve(self, query:str, top_k: int = 5, score_threshold: float = 0.0) -> List[Dict[str, Any]]:
    #     """
    #     Retrieve relevant documents for a query
    #
    #     Args:
    #         query: The search query
    #         top_k = Number of top results to return
    #         score_threshold = Minimum similarity score threshold
    #
    #     Return:
    #         List of dictionaries containing retireved documents and metadata
    #     """
    #     print(f"Retrieving documents for query: {query}")
    #     print(f"Top_k: {top_k}, score_threshold: {score_threshold}")
    #
    #     # Generate query embedding
    #     query_embedding = self.embedding_manager.generate_query_embeddings(query)
    #     # search in vector store
    #
    #     try:
    #         results = self.vector_store.collection.query(
    #             query_embeddings=[query_embedding.tolist()],
    #             n_results=top_k
    #         )
    #
    #         retrieved_docs = []
    #         if results['documents'] and results['documents'][0]:
    #             documents = results['documents'][0]
    #             metadatas = results['metadatas'][0]
    #             distances = results['distances'][0]
    #             ids = results['ids'][0]
    #
    #             for i, (doc_id, document, metadata, distance) in enumerate(zip(ids, documents, metadatas, distances)):
    #                 # convert distance to similarity score(ChromaDB uses cosine distances)
    #                 similarity_score = 1 - distance
    #
    #                 print(
    #                     f"Doc {i+1}: "
    #                     f"distance={distance:.4f}, "
    #                     f"similarity={similarity_score:.4f}"
    #                 )
    #                 if similarity_score >= score_threshold:
    #                     retrieved_docs.append({
    #                         'id': doc_id,
    #                         'content': document,
    #                         'metadata': metadata,
    #                         'similarity_score': similarity_score,
    #                         'distance': distance,
    #                         'rank': i + 1
    #                     })
    #
    #             print(f"Retrieved {len(retrieved_docs)} documents (after filtering)")
    #         else:
    #             print("No documents found")
    #
    #         return retrieved_docs
    #
    #     except Exception as e:
    #         print(f"Error during retrieval: {e}")
    #         return [] 

    def retrieve(self, query: str, top_k: int = 5, score_threshold: float = 0.2):
        print(f"Retrieving documents for query: {query}")

        query_embedding = self.embedding_manager.generate_query_embeddings(query)

        try:
            response = (
                supabase.rpc(
                    "match_documents",
                    {
                        "query_embedding": query_embedding.tolist(),
                        "match_threshold": score_threshold,
                        "match_count": top_k
                    }
                )
                .execute()
            )

            retrieved_docs = []

            for i, row in enumerate(response.data):
                retrieved_docs.append({
                    "id": row["id"],
                    "content": row["content"],
                    "metadata": row["metadata"],
                    "similarity_score": row["similarity"],
                    "rank": i + 1
                })

            print(f"Retrieved {len(retrieved_docs)} documents")
            return retrieved_docs

        except Exception as e:
            print(f"Error during retrieval: {e}")
            return []