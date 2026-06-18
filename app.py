from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for
)

from rag import retriever
from rag.retriever import RAGRetriever
from rag.generator import rag_pipeline
from llm.groq_client import GroqClient
from vector_db.vector_store import VectorStore
from embeddings.embedding_manager import EmbeddingManager
from loaders.pdf_loader import PDFLoader
from rag.ingestion import IngestionPipeline
from flask import Response

app = Flask(__name__)
vector_store = VectorStore()
ingestion_pipeline = IngestionPipeline()
pdf_loader = PDFLoader()

embedding_manager = EmbeddingManager()

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

    return render_template(
        "chat.html",
        files=files
    )


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["file"]

    save_path = f"data/pdf/{file.filename}"

    file.save(save_path)

    print(f"Uploaded: {save_path}")

    documents = pdf_loader.load(save_path)

    chunks, embeddings = (
        ingestion_pipeline.process_documents(
            documents
        )
    )

    vector_store.add_documents(
        chunks,
        embeddings
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

if __name__ == "__main__":

    app.run(
        debug=True
    )