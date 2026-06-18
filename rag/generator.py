from typing import Dict, Any


def rag_pipeline(
    query: str,
    retriever,
    llm,
    top_k: int = 3,
    min_score: float = 0.2,
    return_context: bool = False
) -> Dict[str, Any]:

    results = retriever.retrieve(
        query=query,
        top_k=top_k,
        score_threshold=min_score
    )

    if not results:

        return {
            "answer":
                "No relevant context found.",
            "sources": [],
            "confidence": 0.0,
            "context": ""
        }

    context = "\n\n".join(
        doc["content"]
        for doc in results
    )

    sources = [
        {
            "source":
                doc["metadata"].get(
                    "source_file",
                    "unknown"
                ),

            "page":
                doc["metadata"].get(
                    "page",
                    "unknown"
                ),

            "score":
                doc["similarity_score"],

            "preview":
                doc["content"][:120]
        }
        for doc in results
    ]

    confidence = max(
        doc["similarity_score"]
        for doc in results
    )

    prompt = f"""
You are a helpful RAG assistant.

Use ONLY the provided context.

If the answer cannot be found in the context,
say so clearly.

Context:
{context}

Question:
{query}

Answer:
"""

    response = llm.invoke(prompt)

    output = {
        "answer": response.content,
        "sources": sources,
        "confidence": confidence
    }

    if return_context:
        output["context"] = context

    return output