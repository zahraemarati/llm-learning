from agents.workflow_state import WorkflowState


def test_workflow_state_tracks_stages():
    state = WorkflowState(
        task="Write report"
    )

    state.start_stage(
        "research"
    )

    assert state.current_stage == (
        "research"
    )

    state.complete_stage(
        "research"
    )

    assert "research" in (
        state.completed_stages
    )

    state.finish()

    assert state.success is True
    assert state.current_stage == (
        "completed"
    )


def test_workflow_state_tracks_errors():
    state = WorkflowState(
        task="Write report"
    )

    state.fail(
        "research",
        ValueError("Research failed"),
    )

    assert state.success is False
    assert state.current_stage == "failed"

    assert (
        "research: Research failed"
        in state.errors
    )