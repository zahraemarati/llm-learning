from agents.base_agent import AgentConfig, BaseAgent
from agents.prompts import REVIEWER_AGENT_PROMPT


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
        draft: str,
        verbose: bool = True,
    ) -> str:
        instruction = (
            f"Original task:\n{task}\n\n"
            f"Draft:\n{draft}\n\n"
            "Review this draft and provide concrete feedback "
            "for the writer agent."
        )

        return self.run(
            user_input=instruction,
            verbose=verbose,
            save_memory=False,
        )