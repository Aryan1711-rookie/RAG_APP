from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from loaders.pdf_loader import PDFLoader
from rag.ingestion import IngestionPipeline


loader = PDFLoader()

documents = loader.load(str(PROJECT_ROOT / "data" / "pdf" / "Attention is all you need.pdf") )

pipeline = IngestionPipeline()

chunks, embeddings = pipeline.process_documents(
    documents
)

print(f"Chunks: {len(chunks)}")
print(f"Embeddings Shape: {embeddings.shape}")