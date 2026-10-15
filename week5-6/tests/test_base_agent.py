from langchain_core.messages import (
    AIMessage,
    ToolMessage,
)

from agents.base_agent import (
    AgentConfig,
    BaseAgent,
)


class FakeTool:
    name = "echo"

    def invoke(
        self,
        args,
    ):
        return args["text"]


class FakeModel:
    def __init__(
        self,
    ):
        self.bound_tools = []

    def bind_tools(
        self,
        tools,
    ):
        self.bound_tools = tools

        return self

    def invoke(
        self,
        messages,
    ):
        has_tool_result = any(
            isinstance(
                message,
                ToolMessage,
            )
            for message in messages
        )

        if has_tool_result:
            return AIMessage(
                content="Finished."
            )

        return AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "echo",
                    "args": {
                        "text": "hello"
                    },
                    "id": "call-1",
                    "type": "tool_call",
                }
            ],
        )


def test_base_agent_tool_injection():
    model = FakeModel()
    tool = FakeTool()

    config = AgentConfig(
        name="test_agent",
        system_prompt="Test prompt",
    )

    agent = BaseAgent(
        model=model,
        config=config,
        tools=[tool],
    )

    result = agent.run(
        "Run echo",
        verbose=False,
    )

    assert model.bound_tools == [
        tool
    ]

    assert result == "Finished."