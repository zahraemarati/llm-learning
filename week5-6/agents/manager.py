from dataclasses import dataclass


@dataclass
class MultiAgentResult:
    research_notes: str
    draft: str
    review: str
    final_answer: str


class ManagerAgent:
    def __init__(
        self,
        researcher,
        writer,
        reviewer,
    ):
        self.researcher = researcher
        self.writer = writer
        self.reviewer = reviewer

    def execute(
        self,
        task: str,
        verbose: bool = True,
    ) -> MultiAgentResult:
        if verbose:
            print("\nManager: Delegating research")

        research_notes = self.researcher.research(
            task=task,
            verbose=verbose,
        )

        if verbose:
            print("\nManager: Delegating writing")

        draft = self.writer.create_draft(
            task=task,
            research_notes=research_notes,
            verbose=verbose,
        )

        if verbose:
            print("\nManager: Delegating review")

        review = self.reviewer.review(
            task=task,
            draft=draft,
            verbose=verbose,
        )

        if verbose:
            print("\nManager: Delegating revision")

        final_answer = self.writer.revise(
            task=task,
            draft=draft,
            review=review,
            verbose=verbose,
        )

        return MultiAgentResult(
            research_notes=research_notes,
            draft=draft,
            review=review,
            final_answer=final_answer,
        )

    def run(
        self,
        task: str,
        verbose: bool = True,
    ) -> str:
        result = self.execute(
            task=task,
            verbose=verbose,
        )

        return result.final_answer


_default_manager = None


def get_default_manager():
    global _default_manager

    if _default_manager is None:
        from agents.researcher import ResearcherAgent
        from agents.reviewer import ReviewerAgent
        from agents.writer import WriterAgent
        from llm_client import model

        researcher = ResearcherAgent(
            model=model
        )

        writer = WriterAgent(
            model=model
        )

        reviewer = ReviewerAgent(
            model=model
        )

        _default_manager = ManagerAgent(
            researcher=researcher,
            writer=writer,
            reviewer=reviewer,
        )

    return _default_manager


def run_multi_agent(
    task: str,
    verbose: bool = True,
) -> str:
    manager = get_default_manager()

    return manager.run(
        task=task,
        verbose=verbose,
    )