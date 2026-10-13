from langchain_core.messages import AIMessage

import agents.research_agent as research_agent


class FakeModelWithTools:
    def invoke(self, messages):
        current_message = messages[-1].content

        if current_message == "My project is about RAG":
            return AIMessage(
                content="Got it.",
                tool_calls=[],
            )

        if current_message == "What is my project about?":
            has_project_context = any(
                message.content == "My project is about RAG"
                for message in messages[:-1]
            )

            if has_project_context:
                return AIMessage(
                    content="Your project is about RAG.",
                    tool_calls=[],
                )

            return AIMessage(
                content="I do not know.",
                tool_calls=[],
            )

        return AIMessage(
            content="OK",
            tool_calls=[],
        )


def test_agent_remembers_previous_message(
    monkeypatch,
):
    research_agent.clear_memory()

    monkeypatch.setattr(
        research_agent,
        "model_with_tools",
        FakeModelWithTools(),
    )

    research_agent.run_agent(
        "My project is about RAG",
        verbose=False,
    )

    answer = research_agent.run_agent(
        "What is my project about?",
        verbose=False,
    )

    assert "RAG" in answer