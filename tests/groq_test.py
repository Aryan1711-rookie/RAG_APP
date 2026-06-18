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

from llm.groq_client import GroqClient

llm = GroqClient()

response = llm.invoke(
    "What is artificial intelligence?"
)

print(response.content)