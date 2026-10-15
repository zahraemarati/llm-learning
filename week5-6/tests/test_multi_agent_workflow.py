from agents.manager import ManagerAgent


class FakeResearcher:
    def research(
        self,
        task: str,
        verbose: bool = True,
    ) -> str:
        return "Research notes."


class FakeWriter:
    def create_draft(
        self,
        task: str,
        research_notes: str,
        verbose: bool = True,
    ) -> str:
        assert research_notes == (
            "Research notes."
        )

        return "Draft report."

    def revise(
        self,
        task: str,
        research_notes: str,
        draft: str,
        review: str,
        verbose: bool = True,
    ) -> str:
        assert research_notes == (
            "Research notes."
        )

        assert draft == (
            "Draft report."
        )

        assert review == (
            "Review feedback."
        )

        return "Final report."


class FakeReviewer:
    def review(
        self,
        task: str,
        research_notes: str,
        draft: str,
        verbose: bool = True,
    ) -> str:
        assert research_notes == (
            "Research notes."
        )

        assert draft == (
            "Draft report."
        )

        return "Review feedback."


class FailingResearcher:
    def research(
        self,
        task: str,
        verbose: bool = True,
    ) -> str:
        raise RuntimeError(
            "Research service unavailable"
        )


def test_complete_multi_agent_pipeline():
    manager = ManagerAgent(
        researcher=FakeResearcher(),
        writer=FakeWriter(),
        reviewer=FakeReviewer(),
    )

    state = manager.execute(
        "Write a report",
        verbose=False,
    )

    assert state.success is True

    assert state.research_notes == (
        "Research notes."
    )

    assert state.draft == (
        "Draft report."
    )

    assert state.review == (
        "Review feedback."
    )

    assert state.final_answer == (
        "Final report."
    )

    assert state.completed_stages == [
        "research",
        "writing",
        "review",
        "revision",
    ]


def test_pipeline_handles_agent_error():
    manager = ManagerAgent(
        researcher=FailingResearcher(),
        writer=FakeWriter(),
        reviewer=FakeReviewer(),
    )

    state = manager.execute(
        "Write a report",
        verbose=False,
    )

    assert state.success is False
    assert state.current_stage == "failed"

    assert state.completed_stages == []

    assert len(
        state.errors
    ) == 1

    assert (
        "Research service unavailable"
        in state.errors[0]
    )


def test_run_returns_final_answer():
    manager = ManagerAgent(
        researcher=FakeResearcher(),
        writer=FakeWriter(),
        reviewer=FakeReviewer(),
    )

    answer = manager.run(
        "Write a report",
        verbose=False,
    )

    assert answer == (
        "Final report."
    )


def test_empty_task_is_rejected():
    manager = ManagerAgent(
        researcher=FakeResearcher(),
        writer=FakeWriter(),
        reviewer=FakeReviewer(),
    )

    state = manager.execute(
        "",
        verbose=False,
    )

    assert state.success is False

    assert (
        "Task cannot be empty"
        in state.errors[0]
    )