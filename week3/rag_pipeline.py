from typing import Any

from retrieval.hybrid_retriever import HybridRetriever
from context.context_manager import manage_context
from generation.answer_generator import generate_answer


retriever = HybridRetriever()


def ask_question(
    question: str,
    where: dict[str, Any] | None = None,
):

    retrieved_chunks = retriever.retrieve(
        question,
        n_results=10
    )


    context = manage_context(
        retrieved_chunks,
        max_chunks=5,
    )


    answer = generate_answer(
        question,
        [context],
    )


    sources = []


    for chunk in retrieved_chunks[:5]:

        metadata = chunk.get(
            "metadata"
        )

        if metadata:
            sources.append(metadata)


    return {
        "answer": answer,
        "sources": sources,
    }