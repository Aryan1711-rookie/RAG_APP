import os
import uuid
from typing import List, Any, Dict

import chromadb
import numpy as np


class VectorStore:
    """
    Manages document embeddings in a ChromaDB vector store.
    """

    def __init__(
        self,
        collection_name: str = "pdf_documents",
        persist_directory: str = "data/vector_store"
    ):

        self.collection_name = collection_name
        self.persist_directory = persist_directory

        self.client = None
        self.collection = None

        self._initialize_store()

    def _initialize_store(self):
        """
        Initialize ChromaDB client and collection.
        """

        try:

            os.makedirs(
                self.persist_directory,
                exist_ok=True
            )

            self.client = chromadb.PersistentClient(
                path=self.persist_directory
            )

            self.collection = (
                self.client.get_or_create_collection(
                    name=self.collection_name,
                    metadata={
                        "description":
                        "PDF document embeddings for RAG"
                    }
                )
            )

            print(
                f"Vector store initialized: "
                f"{self.collection_name}"
            )

            print(
                f"Existing documents: "
                f"{self.collection.count()}"
            )

        except Exception as e:

            print(
                f"Error initializing vector store: {e}"
            )

            raise

    def add_documents(
        self,
        documents: List[Any],
        embeddings: np.ndarray
    ):
        """
        Add documents and embeddings.
        """

        if len(documents) != len(embeddings):

            raise ValueError(
                "Number of documents must match "
                "number of embeddings"
            )

        print(
            f"Adding {len(documents)} "
            f"documents to vector store..."
        )

        ids = []
        metadatas = []
        documents_text = []
        embeddings_list = []

        for i, (
            doc,
            embedding
        ) in enumerate(zip(documents, embeddings)):

            doc_id = (
                f"doc_{uuid.uuid4().hex[:8]}_{i}"
            )

            ids.append(doc_id)

            metadata = dict(doc.metadata)

            metadata["doc_index"] = i

            metadata["content_length"] = (
                len(doc.page_content)
            )

            metadatas.append(metadata)

            documents_text.append(
                doc.page_content
            )

            embeddings_list.append(
                embedding.tolist()
            )

        try:

            self.collection.add(
                ids=ids,
                embeddings=embeddings_list,
                metadatas=metadatas,
                documents=documents_text
            )

            print(
                f"Successfully added "
                f"{len(documents)} documents."
            )

            print(
                f"Total documents: "
                f"{self.collection.count()}"
            )

        except Exception as e:

            print(
                f"Error adding documents: {e}"
            )

            raise

    def get_document_count(self) -> int:
        """
        Get total documents stored.
        """

        return self.collection.count()

    def delete_all_documents(self):
        """
        Clear collection.
        """

        try:

            self.client.delete_collection(
                self.collection_name
            )

            self.collection = (
                self.client.get_or_create_collection(
                    name=self.collection_name
                )
            )

            print(
                "Collection cleared successfully."
            )

        except Exception as e:

            print(
                f"Error clearing collection: {e}"
            )

            raise

    def get_collection_info(self) -> Dict:
        """
        Collection information.
        """

        return {
            "collection_name":
                self.collection_name,

            "document_count":
                self.collection.count(),

            "persist_directory":
                self.persist_directory
        }
    
    def document_exists(self,file_hash: str) -> bool:
        results = self.collection.get(where={"file_hash": file_hash})

        return len(results["ids"]) > 0

    def peek(self, limit=5):
        return self.collection.peek(limit=limit)
    
    def get_all_sources(self):
        results = self.collection.get()

        for metadata in results["metadatas"]:
            print(
            metadata.get("source_file"),
            metadata.get("page"),
            metadata.get("doc_index")
            )
    def get_document_summary(self):
        results = self.collection.get()

        docs = {}

        for metadata in results["metadatas"]:
            source = metadata.get(
            "source_file",
            "unknown")

            docs[source] = docs.get(source,0) + 1

        return docs