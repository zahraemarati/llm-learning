from agents.base_agent import AgentConfig, BaseAgent
from agents.prompts import WRITER_AGENT_PROMPT


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
            "Create a complete draft that answers the original task."
        )

        return self.run(
            user_input=instruction,
            verbose=verbose,
            save_memory=False,
        )

    def revise(
        self,
        task: str,
        draft: str,
        review: str,
        verbose: bool = True,
    ) -> str:
        instruction = (
            f"Original task:\n{task}\n\n"
            f"Current draft:\n{draft}\n\n"
            f"Reviewer feedback:\n{review}\n\n"
            "Revise the draft using the reviewer feedback. "
            "Return only the improved final response."
        )

        return self.run(
            user_input=instruction,
            verbose=verbose,
            save_memory=False,
        )