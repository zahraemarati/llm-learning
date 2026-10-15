from langchain_core.messages import AIMessage

from agents.manager_agent import ManagerAgent


class FakeManagerModel:
    def __init__(
        self,
        route: str,
    ):
        self.route = route

    def invoke(
        self,
        messages,
    ):
        return AIMessage(
            content=self.route
        )


class FakeAgent:
    def __init__(
        self,
        response: str,
    ):
        self.response = response

    def run(
        self,
        user_input: str,
        verbose: bool = True,
        save_memory: bool = True,
    ):
        return self.response


def test_manager_routes_to_research():
    manager = ManagerAgent(
        model=FakeManagerModel(
            "research"
        ),
        research_agent=FakeAgent(
            "Research result"
        ),
        assistant_agent=FakeAgent(
            "Assistant result"
        ),
    )

    result = manager.run(
        "Analyze paper.pdf",
        verbose=False,
    )

    assert result == "Research result"


def test_manager_routes_to_assistant():
    manager = ManagerAgent(
        model=FakeManagerModel(
            "assistant"
        ),
        research_agent=FakeAgent(
            "Research result"
        ),
        assistant_agent=FakeAgent(
            "Assistant result"
        ),
    )

    result = manager.run(
        "Hello",
        verbose=False,
    )

    assert result == "Assistant result"