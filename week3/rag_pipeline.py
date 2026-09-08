from typing import Any

from retrieval.hybrid_retriever import HybridRetriever
from retrieval.reranker import Reranker

from context.context_manager import manage_context
from generation.answer_generator import generate_answer

from query.query_rewriter import QueryRewriter
from query.multi_query import MultiQueryGenerator


retriever = HybridRetriever()
reranker = Reranker()

query_rewriter = QueryRewriter()
multi_query_generator = MultiQueryGenerator()


def retrieve_chunks(
    question: str,
    candidate_count: int = 10,
    top_k: int = 5,
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
            n_results=candidate_count
        )

        all_chunks.extend(chunks)


    unique_chunks = []

    seen = set()


    for chunk in all_chunks:

        chunk_key = chunk.get("text")


        if chunk_key and chunk_key not in seen:

            unique_chunks.append(chunk)

            seen.add(chunk_key)


    candidate_chunks = unique_chunks[
        :candidate_count
    ]


    reranked_chunks = reranker.rerank(
        question,
        candidate_chunks,
        top_k=top_k
    )


    return reranked_chunks



def ask_question(
    question: str,
    where: dict[str, Any] | None = None,
):

    retrieved_chunks = retrieve_chunks(
        question,
        candidate_count=10,
        top_k=5
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


    for chunk in retrieved_chunks:

        metadata = chunk.get(
            "metadata"
        )

        if metadata:

            sources.append(
                metadata
            )


    return {
        "answer": answer,
        "sources": sources,
    }