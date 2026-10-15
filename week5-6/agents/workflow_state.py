from dataclasses import dataclass, field


@dataclass
class WorkflowState:
    task: str
    research_notes: str = ""
    draft: str = ""
    review: str = ""
    final_answer: str = ""

    current_stage: str = "pending"
    completed_stages: list[str] = field(
        default_factory=list
    )
    errors: list[str] = field(
        default_factory=list
    )

    success: bool = False

    def start_stage(
        self,
        stage: str,
    ) -> None:
        self.current_stage = stage

    def complete_stage(
        self,
        stage: str,
    ) -> None:
        if stage not in self.completed_stages:
            self.completed_stages.append(
                stage
            )

    def fail(
        self,
        stage: str,
        error: Exception,
    ) -> None:
        self.current_stage = "failed"

        self.errors.append(
            f"{stage}: {error}"
        )

        self.success = False

    def finish(
        self,
    ) -> None:
        self.current_stage = "completed"
        self.success = True