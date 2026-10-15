from agents.base_agent import AgentConfig, BaseAgent
from agents.prompts import ASSISTANT_AGENT_PROMPT
from llm_client import model
from tools.calculator import calculator


class AssistantAgent(BaseAgent):
    def __init__(
        self,
        model,
        tools: list | None = None,
        context_manager=None,
    ):
        config = AgentConfig(
            name="assistant_agent",
            system_prompt=ASSISTANT_AGENT_PROMPT,
            max_steps=5,
        )

        super().__init__(
            model=model,
            config=config,
            tools=tools,
            context_manager=context_manager,
        )


assistant_agent = AssistantAgent(
    model=model,
    tools=[
        calculator,
    ],
)