from typing import Any

from retrieval.hybrid_retriever import HybridRetriever
from context.context_manager import manage_context
from generation.answer_generator import generate_answer

from query.query_rewriter import QueryRewriter
from query.multi_query import MultiQueryGenerator


retriever = HybridRetriever()

query_rewriter = QueryRewriter()
multi_query_generator = MultiQueryGenerator()


def ask_question(
    question: str,
    where: dict[str, Any] | None = None,
):

    rewritten_query = query_rewriter.rewrite(
        question
    )


    queries = multi_query_generator.generate(
        rewritten_query,
        number_of_queries=3
    )


    queries.insert(
        0,
        rewritten_query
    )


    all_chunks = []


    for query in queries:

        chunks = retriever.retrieve(
            query,
            n_results=10
        )

        all_chunks.extend(chunks)



    unique_chunks = []

    seen = set()


    for chunk in all_chunks:

        chunk_key = str(
            chunk.get("page_content")
            or chunk.get("content")
            or chunk
        )


        if chunk_key not in seen:

            unique_chunks.append(chunk)
            seen.add(chunk_key)



    retrieved_chunks = unique_chunks[:10]


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