from agents.manager import ManagerAgent


class FakeResearcher:
    def __init__(
        self,
        should_fail: bool = False,
    ):
        self.should_fail = should_fail
        self.received_task = None

    def research(
        self,
        task: str,
        verbose: bool = True,
    ) -> str:
        self.received_task = task

        if self.should_fail:
            raise RuntimeError(
                "Research failed"
            )

        return (
            "Research notes about the paper."
        )


class FakeWriter:
    def __init__(self):
        self.received_research = None
        self.received_draft = None
        self.received_review = None

    def create_draft(
        self,
        task: str,
        research_notes: str,
        verbose: bool = True,
    ) -> str:
        self.received_research = (
            research_notes
        )

        return (
            "Initial report draft."
        )

    def revise(
        self,
        task: str,
        research_notes: str,
        draft: str,
        review: str,
        verbose: bool = True,
    ) -> str:
        self.received_draft = draft
        self.received_review = review

        return (
            "Improved final report."
        )


class FakeReviewer:
    def __init__(self):
        self.received_research = None
        self.received_draft = None

    def review(
        self,
        task: str,
        research_notes: str,
        draft: str,
        verbose: bool = True,
    ) -> str:
        self.received_research = (
            research_notes
        )

        self.received_draft = draft

        return (
            "Improve structure and clarity."
        )


def test_multi_agent_communication():
    researcher = FakeResearcher()
    writer = FakeWriter()
    reviewer = FakeReviewer()

    manager = ManagerAgent(
        researcher=researcher,
        writer=writer,
        reviewer=reviewer,
    )

    state = manager.execute(
        "Write a report about paper.pdf",
        verbose=False,
    )

    assert researcher.received_task == (
        "Write a report about paper.pdf"
    )

    assert writer.received_research == (
        "Research notes about the paper."
    )

    assert reviewer.received_research == (
        "Research notes about the paper."
    )

    assert reviewer.received_draft == (
        "Initial report draft."
    )

    assert writer.received_draft == (
        "Initial report draft."
    )

    assert writer.received_review == (
        "Improve structure and clarity."
    )

    assert state.final_answer == (
        "Improved final report."
    )


def test_multi_agent_state():
    manager = ManagerAgent(
        researcher=FakeResearcher(),
        writer=FakeWriter(),
        reviewer=FakeReviewer(),
    )

    state = manager.execute(
        "Write a report about paper.pdf",
        verbose=False,
    )

    assert state.success is True

    assert state.current_stage == (
        "completed"
    )

    assert state.completed_stages == [
        "research",
        "writing",
        "review",
        "revision",
    ]

    assert state.research_notes == (
        "Research notes about the paper."
    )

    assert state.draft == (
        "Initial report draft."
    )

    assert state.review == (
        "Improve structure and clarity."
    )

    assert state.final_answer == (
        "Improved final report."
    )


def test_multi_agent_error_handling():
    manager = ManagerAgent(
        researcher=FakeResearcher(
            should_fail=True
        ),
        writer=FakeWriter(),
        reviewer=FakeReviewer(),
    )

    state = manager.execute(
        "Write a report about paper.pdf",
        verbose=False,
    )

    assert state.success is False

    assert state.current_stage == (
        "failed"
    )

    assert len(state.errors) == 1

    assert (
        "Research failed"
        in state.errors[0]
    )

    assert state.draft == ""
    assert state.review == ""
    assert state.final_answer == ""


def test_multi_agent_returns_final_answer():
    manager = ManagerAgent(
        researcher=FakeResearcher(),
        writer=FakeWriter(),
        reviewer=FakeReviewer(),
    )

    answer = manager.run(
        "Write a report about paper.pdf",
        verbose=False,
    )

    assert answer == (
        "Improved final report."
    )