from langchain_core.messages import AIMessage

import agents.research_agent as research_agent


class FakeDecisionModel:
    def invoke(self, messages):
        user_input = messages[-1].content.lower()

        if "calculate" in user_input:
            tool_name = "calculator"
            args = {
                "a": 20,
                "b": 5,
                "operation": "multiply",
            }

        elif "read the pdf" in user_input:
            tool_name = "pdf_reader"
            args = {
                "file_path": "uploads/report.pdf",
            }

        elif "search the web" in user_input:
            tool_name = "web_search"
            args = {
                "query": "latest Python release",
            }

        else:
            return AIMessage(
                content="No tool needed."
            )

        return AIMessage(
            content="",
            tool_calls=[
                {
                    "name": tool_name,
                    "args": args,
                    "id": "call-test",
                    "type": "tool_call",
                }
            ],
        )


def test_agent_selects_calculator(
    monkeypatch,
):
    monkeypatch.setattr(
        research_agent,
        "model_with_tools",
        FakeDecisionModel(),
    )

    response = research_agent.decide(
        "Calculate 20 * 5"
    )

    assert response.tool_calls
    assert (
        response.tool_calls[0]["name"]
        == "calculator"
    )


def test_agent_selects_pdf_reader(
    monkeypatch,
):
    monkeypatch.setattr(
        research_agent,
        "model_with_tools",
        FakeDecisionModel(),
    )

    response = research_agent.decide(
        "Read the PDF file directly from uploads/report.pdf"
    )

    assert response.tool_calls
    assert (
        response.tool_calls[0]["name"]
        == "pdf_reader"
    )


def test_agent_selects_web_search(
    monkeypatch,
):
    monkeypatch.setattr(
        research_agent,
        "model_with_tools",
        FakeDecisionModel(),
    )

    response = research_agent.decide(
        "Search the web for the latest Python release"
    )

    assert response.tool_calls
    assert (
        response.tool_calls[0]["name"]
        == "web_search"
    )