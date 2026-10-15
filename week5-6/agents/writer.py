from agents.base_agent import (
    AgentConfig,
    BaseAgent,
)
from agents.prompts import (
    WRITER_AGENT_PROMPT,
)


class WriterAgent(BaseAgent):
    def __init__(
        self,
        model,
    ):
        config = AgentConfig(
            name="writer_agent",
            system_prompt=WRITER_AGENT_PROMPT,
            max_steps=3,
        )

        super().__init__(
            model=model,
            config=config,
        )

    def create_draft(
        self,
        task: str,
        research_notes: str,
        verbose: bool = True,
    ) -> str:
        instruction = (
            f"Original task:\n{task}\n\n"
            f"Research notes:\n{research_notes}\n\n"
            "Create a complete and structured draft "
            "that answers the original task. "
            "Use only information supported by the "
            "research notes."
        )

        return self.run(
            user_input=instruction,
            verbose=verbose,
            save_memory=False,
        )

    def revise(
        self,
        task: str,
        research_notes: str,
        draft: str,
        review: str,
        verbose: bool = True,
    ) -> str:
        instruction = (
            f"Original task:\n{task}\n\n"
            f"Research notes:\n{research_notes}\n\n"
            f"Current draft:\n{draft}\n\n"
            f"Reviewer feedback:\n{review}\n\n"
            "Revise the draft using the review feedback. "
            "Preserve supported information from the "
            "research notes. "
            "Return only the improved final answer."
        )

        return self.run(
            user_input=instruction,
            verbose=verbose,
            save_memory=False,
        )