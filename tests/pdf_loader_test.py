import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from loaders.pdf_loader import PDFLoader

# Always build absolute paths relative to this file
PROJECT_ROOT = Path(__file__).resolve().parent.parent

loader = PDFLoader()

documents = loader.load(
    str(PROJECT_ROOT / "data" / "pdf" / "Attention is all you need.pdf") 
)

documents = loader.load(str(PROJECT_ROOT / "data" / "pdf" / "Attention is all you need.pdf"))

print(documents[0].metadata)

docs = loader.load(str(PROJECT_ROOT / "data" / "pdf" / "Attention is all you need.pdf"))

print(docs[0].metadata)

print(f"Loaded {len(documents)} pages")  
print(documents[0].page_content[:1000])    