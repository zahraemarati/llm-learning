from langchain_core.tools import tool

from context.context_builder import build_context
from retrieval.hybrid_retriever import hybrid_search
from retrieval.reranker import rerank_documents


def prepare_query(query: str) -> str:
    normalized_query = query.strip().lower()

    summary_queries = {
        "summarize",
        "summary",
        "summarize this document",
        "summarize the document",
    }

    if normalized_query in summary_queries:
        return (
            "main topics purpose scope chapter overview "
            "key ideas and important concepts"
        )

    return query


@tool
def rag_search(
    query: str,
    source: str | None = None,
) -> str:
    """
    Search indexed documents and return relevant context.

    Use this tool when the user's question depends on uploaded
    or indexed documents.

    If the user mentions a specific filename, pass that filename
    in the source argument.
    """
    retrieval_query = prepare_query(query)

    documents = hybrid_search(
        query=retrieval_query,
        top_k=15,
        source=source,
    )

    if not documents:
        return "No relevant documents found."

    ranked_documents = rerank_documents(
        query=retrieval_query,
        documents=documents,
        top_k=5,
    )

    return build_context(
        ranked_documents
    )