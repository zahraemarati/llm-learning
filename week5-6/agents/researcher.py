from agents.base_agent import (
    AgentConfig,
    BaseAgent,
)
from agents.prompts import (
    RESEARCHER_AGENT_PROMPT,
)
from tools.pdf_reader import pdf_reader
from tools.rag_tool import rag_search
from tools.web_search import web_search


class ResearcherAgent(BaseAgent):
    def __init__(
        self,
        model,
        tools: list | None = None,
    ):
        config = AgentConfig(
            name="researcher_agent",
            system_prompt=RESEARCHER_AGENT_PROMPT,
            max_steps=5,
        )

        if tools is None:
            tools = [
                rag_search,
                web_search,
                pdf_reader,
            ]

        super().__init__(
            model=model,
            config=config,
            tools=tools,
        )

    def research(
        self,
        task: str,
        verbose: bool = True,
    ) -> str:
        instruction = (
            f"Original task:\n{task}\n\n"
            "Gather the information needed to complete "
            "the original task. "
            "Return clear research notes for the writer. "
            "Do not write the final answer."
        )

        return self.run(
            user_input=instruction,
            verbose=verbose,
            save_memory=False,
        )