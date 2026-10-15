from langchain_core.messages import AIMessage

import agents.research_agent as research_agent
import tools.rag_tool as rag_tool_module


class FakeToolDecisionModel:
    def invoke(
        self,
        messages,
    ):
        user_input = messages[-1].content.lower()

        if "calculate" in user_input:
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "calculator",
                        "args": {
                            "a": 10,
                            "b": 5,
                            "operation": "multiply",
                        },
                        "id": "call-calculator",
                        "type": "tool_call",
                    }
                ],
            )

        if "read the pdf" in user_input:
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "pdf_reader",
                        "args": {
                            "file_path": "uploads/report.pdf",
                        },
                        "id": "call-pdf",
                        "type": "tool_call",
                    }
                ],
            )

        if "search the web" in user_input:
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "web_search",
                        "args": {
                            "query": "latest Python release",
                        },
                        "id": "call-web",
                        "type": "tool_call",
                    }
                ],
            )

        if "paper.pdf" in user_input:
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

        return AIMessage(
            content="No tool needed."
        )


def test_agent_selects_calculator(
    monkeypatch,
):
    monkeypatch.setattr(
        research_agent,
        "model_with_tools",
        FakeToolDecisionModel(),
    )

    response = research_agent.decide(
        "Calculate 10 multiplied by 5"
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
        FakeToolDecisionModel(),
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
        FakeToolDecisionModel(),
    )

    response = research_agent.decide(
        "Search the web for the latest Python release"
    )

    assert response.tool_calls
    assert (
        response.tool_calls[0]["name"]
        == "web_search"
    )


def test_agent_selects_rag(
    monkeypatch,
):
    monkeypatch.setattr(
        research_agent,
        "model_with_tools",
        FakeToolDecisionModel(),
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


def test_rag_retrieval_returns_context(
    monkeypatch,
):
    documents = [
        {
            "id": "doc-1",
            "content": (
                "Retrieval-Augmented Generation combines "
                "retrieval with language generation."
            ),
            "metadata": {
                "source": "paper.pdf",
                "page": 1,
            },
        },
        {
            "id": "doc-2",
            "content": (
                "Retrieved context can improve grounded answers."
            ),
            "metadata": {
                "source": "paper.pdf",
                "page": 2,
            },
        },
    ]

    def fake_hybrid_search(
        query,
        top_k=15,
        source=None,
    ):
        return documents

    def fake_rerank_documents(
        query,
        documents,
        top_k=5,
    ):
        return documents[:top_k]

    monkeypatch.setattr(
        rag_tool_module,
        "hybrid_search",
        fake_hybrid_search,
    )

    monkeypatch.setattr(
        rag_tool_module,
        "rerank_documents",
        fake_rerank_documents,
    )

    result = rag_tool_module.rag_search.invoke(
        {
            "query": "What is RAG?",
            "source": "paper.pdf",
        }
    )

    assert isinstance(
        result,
        str,
    )

    assert (
        "Retrieval-Augmented Generation"
        in result
    )

    assert (
        "grounded answers"
        in result
    )