from agents.research_agent import research_agent


def test_agent_uses_tool():

    result = research_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Calculate 25 * 25"
                }
            ]
        }
    )


    answer = result["messages"][-1].content


    assert answer

    assert "625" in answer