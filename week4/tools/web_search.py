from langchain_core.tools import tool
from ddgs import DDGS


@tool
def web_search(query: str) -> str:
    """
    Search the web for research papers and latest information.
    """

    results = DDGS().text(
        query,
        max_results=5
    )

    output = []

    for item in results:

        output.append(
            f"""
Title:
{item.get('title')}

URL:
{item.get('href')}

Summary:
{item.get('body')}
"""
        )

    return "\n\n".join(output)