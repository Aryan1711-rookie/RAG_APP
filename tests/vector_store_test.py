from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from vector_db.vector_store import VectorStore

store = VectorStore()

print(store.get_collection_info())
results = store.peek(1)

print(results["metadatas"])

# print("\n ===All sources===")
# store.get_all_sources()

print("\n=== Documents in Knowledge Base ===")

for doc, count in store.get_document_summary().items():

    print(f"{doc}: {count} chunks")