from langchain_core.messages import AIMessage

import agents.research_agent as research_agent


class FakeRagDecisionModel:
    def invoke(self, messages):
        return AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "rag_search",
                    "args": {
                        "query": "summarize",
                        "source": "paper.pdf",
                    },
                    "id": "call-rag",
                    "type": "tool_call",
                }
            ],
        )


def test_agent_selects_rag_for_indexed_document(
    monkeypatch,
):
    monkeypatch.setattr(
        research_agent,
        "model_with_tools",
        FakeRagDecisionModel(),
    )

    response = research_agent.decide(
        "Summarize paper.pdf"
    )

    assert response.tool_calls

    tool_call = response.tool_calls[0]

    assert tool_call["name"] == "rag_search"
    assert (
        tool_call["args"]["source"]
        == "paper.pdf"
    )