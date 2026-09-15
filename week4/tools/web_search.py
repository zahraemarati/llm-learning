from langchain_core.tools import tool
from ddgs import DDGS


@tool
def web_search(query: str) -> str:
    """
    Search the web for up-to-date information.

    Input:
    A search query.

    Output:
    Top search results with title, URL, and snippet.
    """

    try:
        results = DDGS().text(
            query,
            max_results=5,
        )

        if not results:
            return "No search results found."

        formatted_results = []

        for index, result in enumerate(results, start=1):
            title = result.get("title", "No title")
            url = result.get("href", "")
            body = result.get("body", "")

            formatted_results.append(
                f"{index}. {title}\n"
                f"URL: {url}\n"
                f"Snippet: {body}"
            )

        return "\n\n".join(formatted_results)

    except Exception as e:
        return f"Search error: {str(e)}"