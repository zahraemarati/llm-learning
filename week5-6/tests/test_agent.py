from agents.research_agent import decide


def test_agent_selects_calculator():
    response = decide(
        "Calculate 20 * 5"
    )

    assert response.tool_calls
    assert response.tool_calls[0]["name"] == "calculator"


def test_agent_selects_pdf_reader():
    response = decide(
        "Read the PDF file directly from uploads/report.pdf"
    )

    assert response.tool_calls
    assert response.tool_calls[0]["name"] == "pdf_reader"


def test_agent_selects_web_search():
    response = decide(
        "Search the web for the latest Python release"
    )

    assert response.tool_calls
    assert response.tool_calls[0]["name"] == "web_search"