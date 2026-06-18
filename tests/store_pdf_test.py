from pathlib import Path
import sys

project_root = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

sys.path.insert(
    0,
    str(project_root)
)

from loaders.pdf_loader import PDFLoader
from rag.ingestion import IngestionPipeline
from vector_db.vector_store import VectorStore


loader = PDFLoader()

docs = loader.load(str(project_root / "data" / "pdf" / "Attention is all you need.pdf") )

pipeline = IngestionPipeline()

store = VectorStore()

pipeline.ingest_to_store(
    docs,
    store
)

print(
    store.get_document_count()
)