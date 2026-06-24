from database.supabase_client import supabase

class SupabaseVectorStore:

    def add_documents(
        self,
        chunks,
        embeddings,
        document_id
    ):

        rows = []

        for i, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):

            rows.append({
                "document_id": document_id,
                "page": chunk.metadata.get("page"),
                "chunk_index": i,
                "content": chunk.page_content,
                "metadata": chunk.metadata,
                "embedding": embedding.tolist()
            })

        supabase.table(
            "document_chunks"
        ).insert(
            rows
        ).execute()
    
    def get_document_summary(self):

        response = (
        supabase
        .table("documents")
        .select("file_name, chunk_count")
        .execute()
        )

        docs = {}

        for row in response.data:
            docs[row["file_name"]] = row["chunk_count"]

        return docs