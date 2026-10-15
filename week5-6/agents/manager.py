from agents.workflow_state import WorkflowState


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
    ) -> WorkflowState:
        state = WorkflowState(
            task=task
        )

        if not task.strip():
            state.fail(
                "validation",
                ValueError(
                    "Task cannot be empty."
                ),
            )

            return state

        if not self._run_research(
            state,
            verbose,
        ):
            return state

        if not self._run_writing(
            state,
            verbose,
        ):
            return state

        if not self._run_review(
            state,
            verbose,
        ):
            return state

        if not self._run_revision(
            state,
            verbose,
        ):
            return state

        state.finish()

        if verbose:
            print(
                "\nManager: Workflow completed"
            )

        return state

    def _run_research(
        self,
        state: WorkflowState,
        verbose: bool,
    ) -> bool:
        stage = "research"

        try:
            state.start_stage(
                stage
            )

            if verbose:
                print(
                    "\nManager: Delegating research"
                )

            state.research_notes = (
                self.researcher.research(
                    task=state.task,
                    verbose=verbose,
                )
            )

            if not state.research_notes.strip():
                raise ValueError(
                    "Researcher returned empty output."
                )

            state.complete_stage(
                stage
            )

            return True

        except Exception as error:
            state.fail(
                stage,
                error,
            )

            self._print_error(
                stage,
                error,
                verbose,
            )

            return False

    def _run_writing(
        self,
        state: WorkflowState,
        verbose: bool,
    ) -> bool:
        stage = "writing"

        try:
            state.start_stage(
                stage
            )

            if verbose:
                print(
                    "\nManager: Delegating writing"
                )

            state.draft = (
                self.writer.create_draft(
                    task=state.task,
                    research_notes=state.research_notes,
                    verbose=verbose,
                )
            )

            if not state.draft.strip():
                raise ValueError(
                    "Writer returned empty draft."
                )

            state.complete_stage(
                stage
            )

            return True

        except Exception as error:
            state.fail(
                stage,
                error,
            )

            self._print_error(
                stage,
                error,
                verbose,
            )

            return False

    def _run_review(
        self,
        state: WorkflowState,
        verbose: bool,
    ) -> bool:
        stage = "review"

        try:
            state.start_stage(
                stage
            )

            if verbose:
                print(
                    "\nManager: Delegating review"
                )

            state.review = (
                self.reviewer.review(
                    task=state.task,
                    research_notes=state.research_notes,
                    draft=state.draft,
                    verbose=verbose,
                )
            )

            if not state.review.strip():
                raise ValueError(
                    "Reviewer returned empty feedback."
                )

            state.complete_stage(
                stage
            )

            return True

        except Exception as error:
            state.fail(
                stage,
                error,
            )

            self._print_error(
                stage,
                error,
                verbose,
            )

            return False

    def _run_revision(
        self,
        state: WorkflowState,
        verbose: bool,
    ) -> bool:
        stage = "revision"

        try:
            state.start_stage(
                stage
            )

            if verbose:
                print(
                    "\nManager: Delegating revision"
                )

            state.final_answer = (
                self.writer.revise(
                    task=state.task,
                    research_notes=state.research_notes,
                    draft=state.draft,
                    review=state.review,
                    verbose=verbose,
                )
            )

            if not state.final_answer.strip():
                raise ValueError(
                    "Writer returned empty final answer."
                )

            state.complete_stage(
                stage
            )

            return True

        except Exception as error:
            state.fail(
                stage,
                error,
            )

            self._print_error(
                stage,
                error,
                verbose,
            )

            return False

    def _print_error(
        self,
        stage: str,
        error: Exception,
        verbose: bool,
    ) -> None:
        if verbose:
            print(
                f"\nManager error in {stage}: "
                f"{error}"
            )

    def run(
        self,
        task: str,
        verbose: bool = True,
    ) -> str:
        state = self.execute(
            task=task,
            verbose=verbose,
        )

        if state.success:
            return state.final_answer

        error_message = (
            state.errors[-1]
            if state.errors
            else "Unknown workflow error."
        )

        return (
            "The multi-agent workflow failed. "
            f"{error_message}"
        )


_default_manager = None


def get_default_manager():
    global _default_manager

    if _default_manager is None:
        from agents.researcher import (
            ResearcherAgent,
        )
        from agents.reviewer import (
            ReviewerAgent,
        )
        from agents.writer import (
            WriterAgent,
        )
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


def run_multi_agent_with_state(
    task: str,
    verbose: bool = True,
) -> WorkflowState:
    manager = get_default_manager()

    return manager.execute(
        task=task,
        verbose=verbose,
    )