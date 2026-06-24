from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for
)
from database.supabase_client import supabase

from rag import retriever
from rag.retriever import RAGRetriever
from rag.generator import rag_pipeline
from llm.groq_client import GroqClient
from vector_db.vector_store import VectorStore
from embeddings.embedding_manager import EmbeddingManager
from loaders.pdf_loader import PDFLoader
from rag.ingestion import IngestionPipeline
from flask import Response
import hashlib
import uuid
from flask import session
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
#vector_store = VectorStore() // for chromadb

from vector_db.supabase_store import (
    SupabaseVectorStore
)
embedding_manager = EmbeddingManager()
vector_store = SupabaseVectorStore()
ingestion_pipeline = IngestionPipeline(embedding_manager=embedding_manager)
pdf_loader = PDFLoader()



retriever = RAGRetriever(
    vector_store,
    embedding_manager
)

llm = GroqClient()

@app.route("/")
def home():

    files = vector_store.get_document_summary()

    return render_template(
        "index.html",
        files=files
    )


@app.route("/chat")
def chat():

    files = vector_store.get_document_summary()

    history = (
        supabase
        .table("chats")
        .select("*")
        .eq(
            "session_id",
            session["session_id"]
        )
        .order(
            "created_at",
            desc=True
        )
        .execute()
    )

    return render_template(
        "chat.html",
        files=files,
        history=history.data
    )

# @app.route("/upload", methods=["POST"])
# def upload():

#     file = request.files["file"]

#     save_path = f"data/pdf/{file.filename}"

#     file.save(save_path)

#     print(f"Uploaded: {save_path}")

#     documents = pdf_loader.load(save_path)

#     chunks, embeddings = (
#         ingestion_pipeline.process_documents(
#             documents
#         )
#     )

#     vector_store.add_documents(
#         chunks,
#         embeddings
#     )

#     return redirect(
#         url_for("chat")
#     )

@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["file"]

    save_path = f"data/pdf/{file.filename}"

    file.save(save_path)

    with open(save_path, "rb") as f:
        file_hash = hashlib.md5(
            f.read()
        ).hexdigest()

    print("File Hash:", file_hash)

    # CHECK DUPLICATE FIRST
    existing = (
        supabase
        .table("documents")
        .select("id")
        .eq("file_hash", file_hash)
        .execute()
    )

    if existing.data:

        return render_template(
            "index.html",
            files=vector_store.get_document_summary(),
            error=f'"{file.filename}" already exists in the knowledge base.'
        )

    documents = pdf_loader.load(save_path)

    # Insert metadata
    response = (
        supabase
        .table("documents")
        .insert({
            "file_name": file.filename,
            "file_hash": file_hash,
            "file_type": "pdf"
        })
        .execute()
    )

    document_id = response.data[0]["id"]

    chunks, embeddings = (
        ingestion_pipeline.process_documents(
            documents
        )
    )

    vector_store.add_documents(
        chunks,
        embeddings,
        document_id
    )

    (
        supabase
        .table("documents")
        .update({
            "chunk_count": len(chunks)
        })
        .eq("id", document_id)
        .execute()
    )

    return redirect(
        url_for("chat")
    )
@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()

    question = data["question"]

    # Later:
    result = rag_pipeline(query=question,retriever=retriever,llm=llm)
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    chat = (
    supabase
    .table("chats")
    .insert({
        "session_id": session["session_id"],
        "title": question[:50]
    })
    .execute()
    )

    chat_id = chat.data[0]["id"]

    # Save chat history
    # supabase.table("chat_history").insert({
    #     "session_id": session["session_id"],
    #     "question": question,
    #     "answer": result["answer"]
    # }).execute()

    supabase.table("messages").insert([
    {
        "chat_id": chat_id,
        "role": "user",
        "content": question
    },
    {
        "chat_id": chat_id,
        "role": "assistant",
        "content": result["answer"]
    }
    ]).execute()

    # result = {
    #     "answer":
    #     f"You asked: {question}"
    # }

    return jsonify(result)

# @app.route("/ask", methods=["POST"])
# def ask():

#     def generate():

#         for token in llm.stream(
#             prompt
#         ):
#             yield token

#     return Response(
#         generate(),
#         mimetype="text/plain"
#     )
@app.route("/chat/<chat_id>")
def open_chat(chat_id):

    files = vector_store.get_document_summary()

    messages = (
        supabase
        .table("messages")
        .select("*")
        .eq("chat_id", chat_id)
        .order("created_at")
        .execute()
    )
    print(messages.data)
    history = (
        supabase
        .table("chats")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    return render_template(
        "chat.html",
        files=files,
        history=history.data,
        messages=messages.data
    )
@app.route("/new-chat")
def new_chat():

    session.pop("current_chat_id", None)

    return redirect(url_for("chat"))

@app.route("/delete-chat/<chat_id>", methods=["POST"])
def delete_chat(chat_id):

    supabase.table("chats")\
        .delete()\
        .eq("id", chat_id)\
        .execute()

    return redirect(url_for("chat"))
    
if __name__ == "__main__":

    app.run(
        debug=True
    )