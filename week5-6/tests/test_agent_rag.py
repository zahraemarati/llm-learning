from agents.research_agent import decide


def test_agent_selects_rag_for_indexed_document():
    response = decide(
        "Summarize paper.pdf"
    )

    assert response.tool_calls

    tool_call = response.tool_calls[0]

    assert tool_call["name"] == "rag_search"
    assert tool_call["args"]["source"] == "paper.pdf"