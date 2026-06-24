from typing import List, Tuple
import numpy as np

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from embeddings.embedding_manager import EmbeddingManager

class IngestionPipeline:
    
    """
    Handles:
    1. Chunking documents
    2. Generating embeddings
    """

    def __init__(self, embedding_manager, chunk_size: int = 1000, chunk_overlap: int = 200):
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        # self.embedding_manager = EmbeddingManager(
        #     model_name = embedding_model
        # )
        self.embedding_manager = embedding_manager
    def chunk_documents(self,documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks.
        """

        chunks = self.text_splitter.split_documents(documents)

        print(f"Created {len(chunks)} chunks of the document.")

        return chunks
    
    def extract_texts(self, chunks: List[Document]) -> List[str]:
        """
        Extract plain text from Langchain Documents.
        """

        return [chunk.page_content for chunk in chunks]
    
    def generate_embeddings(self, chunks: List[Document]) -> np.ndarray:
        """
        Generate embeddings of chunks.
        """
        texts = self.extract_texts(chunks)
        embeddings = self.embedding_manager.generate_embeddings(texts)

        return embeddings
    
    def process_documents(self, documents: List[Document]) -> Tuple[List[Document], np.ndarray]:
        """
        Full injestion pipeline.
        
        Returns:
            Chunks
            embeddings
        
        """

        chunks = self.chunk_documents(documents)
        embeddings = self.generate_embeddings(chunks)

        # chunks, embeddings = pipeline.process_documents(documents)
        # vector_store.add_documents(chunks,embeddings)

        print("Injestion process completed.")

        return chunks, embeddings
    
    def ingest_to_store(self, documents, vector_store):
        if not documents:
            print("No documents found.")
            return 0

        file_hash = documents[0].metadata.get("file_hash")

        if (file_hash and vector_store.document_exists(file_hash)):
            
            print("Document already exists.")

            return 0

        chunks = self.chunk_documents(documents)

        embeddings = self.generate_embeddings(chunks)
    

        vector_store.add_documents(
        chunks,
        embeddings
        )

        print(
        f"Stored {len(chunks)} chunks."
        )

        return len(chunks)