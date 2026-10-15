from agents.base_agent import (
    AgentConfig,
    BaseAgent,
)
from agents.prompts import (
    REVIEWER_AGENT_PROMPT,
)


class ReviewerAgent(BaseAgent):
    def __init__(
        self,
        model,
    ):
        config = AgentConfig(
            name="reviewer_agent",
            system_prompt=REVIEWER_AGENT_PROMPT,
            max_steps=3,
        )

        super().__init__(
            model=model,
            config=config,
        )

    def review(
        self,
        task: str,
        research_notes: str,
        draft: str,
        verbose: bool = True,
    ) -> str:
        instruction = (
            f"Original task:\n{task}\n\n"
            f"Research notes:\n{research_notes}\n\n"
            f"Draft:\n{draft}\n\n"
            "Review the draft against both the original "
            "task and the research notes. "
            "Check correctness, relevance, completeness, "
            "clarity, structure, and unsupported claims. "
            "Return concrete feedback for the writer."
        )

        return self.run(
            user_input=instruction,
            verbose=verbose,
            save_memory=False,
        )