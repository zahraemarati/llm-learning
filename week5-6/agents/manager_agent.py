from langchain_core.messages import HumanMessage, SystemMessage

from agents.assistant_agent import assistant_agent
from agents.base_agent import AgentConfig, BaseAgent
from agents.prompts import MANAGER_AGENT_PROMPT
from agents.research_agent import research_agent
from llm_client import model


class ManagerAgent(BaseAgent):
    def __init__(
        self,
        model,
        research_agent,
        assistant_agent,
    ):
        config = AgentConfig(
            name="manager_agent",
            system_prompt=MANAGER_AGENT_PROMPT,
            max_steps=1,
        )

        super().__init__(
            model=model,
            config=config,
        )

        self.research_agent = research_agent
        self.assistant_agent = assistant_agent

    def route(
        self,
        user_input: str,
    ) -> str:
        messages = [
            SystemMessage(
                content=MANAGER_AGENT_PROMPT
            ),
            HumanMessage(
                content=user_input
            ),
        ]

        response = self.model.invoke(
            messages
        )

        route = (
            response.content
            .strip()
            .lower()
        )

        if route not in {
            "research",
            "assistant",
        }:
            return "assistant"

        return route

    def run(
        self,
        user_input: str,
        verbose: bool = True,
        save_memory: bool = True,
    ) -> str:
        route = self.route(
            user_input
        )

        if verbose:
            print(
                f"Manager selected: {route}"
            )

        if route == "research":
            return self.research_agent.run(
                user_input=user_input,
                verbose=verbose,
                save_memory=save_memory,
            )

        return self.assistant_agent.run(
            user_input=user_input,
            verbose=verbose,
            save_memory=save_memory,
        )


manager_agent = ManagerAgent(
    model=model,
    research_agent=research_agent,
    assistant_agent=assistant_agent,
)


def run_manager(
    user_input: str,
    verbose: bool = True,
) -> str:
    return manager_agent.run(
        user_input=user_input,
        verbose=verbose,
    )