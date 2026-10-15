from agents.manager import ManagerAgent


class FakeResearcher:
    def __init__(self):
        self.received_task = None

    def research(
        self,
        task: str,
        verbose: bool = True,
    ) -> str:
        self.received_task = task

        return "Research notes about the paper."


class FakeWriter:
    def __init__(self):
        self.draft_task = None
        self.draft_research = None
        self.revision_review = None

    def create_draft(
        self,
        task: str,
        research_notes: str,
        verbose: bool = True,
    ) -> str:
        self.draft_task = task
        self.draft_research = research_notes

        return "Initial report draft."

    def revise(
        self,
        task: str,
        draft: str,
        review: str,
        verbose: bool = True,
    ) -> str:
        self.revision_review = review

        return "Improved final report."


class FakeReviewer:
    def __init__(self):
        self.received_draft = None

    def review(
        self,
        task: str,
        draft: str,
        verbose: bool = True,
    ) -> str:
        self.received_draft = draft

        return "Improve structure and clarity."


def test_manager_delegates_between_agents():
    researcher = FakeResearcher()
    writer = FakeWriter()
    reviewer = FakeReviewer()

    manager = ManagerAgent(
        researcher=researcher,
        writer=writer,
        reviewer=reviewer,
    )

    result = manager.execute(
        "Write a report about paper.pdf",
        verbose=False,
    )

    assert researcher.received_task == (
        "Write a report about paper.pdf"
    )

    assert writer.draft_research == (
        "Research notes about the paper."
    )

    assert reviewer.received_draft == (
        "Initial report draft."
    )

    assert writer.revision_review == (
        "Improve structure and clarity."
    )

    assert result.final_answer == (
        "Improved final report."
    )


def test_manager_returns_final_answer():
    manager = ManagerAgent(
        researcher=FakeResearcher(),
        writer=FakeWriter(),
        reviewer=FakeReviewer(),
    )

    result = manager.run(
        "Write a report about paper.pdf",
        verbose=False,
    )

    assert result == (
        "Improved final report."
    )