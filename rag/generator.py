from typing import Dict, Any


def rag_pipeline(
    query: str,
    retriever,
    llm,
    top_k: int = 3,
    min_score: float = 0.2,
    return_context: bool = False
) -> Dict[str, Any]:
    
    # print("QUERY RECEIVED:", query)
    query_lower = query.lower().strip()

    greetings = [
        "hi",
        "hello",
        "hey",
        "how are you"
    ]

    if query_lower in greetings:
        return {
            "answer": "Hi, how are you today? Is there something I can help you with or would you like to chat?",
            "sources": [],
            "confidence": 1.0
        }

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
You are Smriti.AI.

If the question is a greeting, casual conversation,
or does not require document retrieval,
answer naturally.

Use the provided context ONLY when it is relevant
to answering the question.

If the context does not contain the answer,
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