from ddgs import DDGS
from langchain_core.tools import tool


@tool
def web_search(query: str) -> str:
    """
    Search the web for up-to-date information.

    Use this tool when the user asks about recent events,
    current information, or information that may not be
    available in the model's internal knowledge.
    """

    results = DDGS().text(
        query,
        max_results=5,
    )

    if not results:
        return "No search results found."

    formatted_results = []

    for result in results:
        formatted_results.append(
            (
                f"Title: {result.get('title', '')}\n"
                f"URL: {result.get('href', '')}\n"
                f"Snippet: {result.get('body', '')}"
            )
        )

    return "\n\n".join(formatted_results)