from langchain_core.tools import tool

from rag_pipeline import ask_question


@tool
def rag_search(question: str) -> dict:
    """
    Search internal research documents using RAG.

    Use this tool when the answer should come from
    uploaded papers or indexed documents.
    """

    result = ask_question(question)

    return {
        "answer": result["answer"],
        "sources": result["sources"],
    }