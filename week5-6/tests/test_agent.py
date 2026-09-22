from agents.research_agent import decide


def test_agent_selects_calculator():
    response = decide("Calculate 20*5")

    assert response.tool_calls
    assert response.tool_calls[0]["name"] == "calculator"