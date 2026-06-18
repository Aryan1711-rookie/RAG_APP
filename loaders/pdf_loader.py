from pathlib import Path
import hashlib

from langchain_community.document_loaders import PyPDFLoader

from loaders.base_loader import BaseLoader


class PDFLoader(BaseLoader):

    def load(self, file_path):

        loader = PyPDFLoader(file_path)

        documents = loader.load()

        filename = Path(file_path).name

        with open(file_path, "rb") as f:

            file_hash = hashlib.sha256(
                f.read()
            ).hexdigest()

        for doc in documents:

            doc.metadata["source_file"] = filename

            doc.metadata["file_type"] = "pdf"

            doc.metadata["file_hash"] = file_hash

        return documents