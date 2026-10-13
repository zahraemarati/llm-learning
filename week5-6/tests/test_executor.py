from langchain_core.messages import AIMessage

from agents.executor import Executor
from agents.planner import Plan


class FakeExecutorModel:
    def invoke(
        self,
        messages,
    ):
        system_message = messages[0].content

        if "Evaluate whether" in system_message:
            return AIMessage(
                content=(
                    '{"sufficient": true, '
                    '"feedback": ""}'
                )
            )

        return AIMessage(
            content="Final report generated."
        )


def fake_step_runner(
    instruction: str,
) -> str:
    return (
        "Completed step successfully."
    )


def test_executor_runs_all_steps():
    plan = Plan(
        goal="Analyze the paper",
        steps=[
            "Read the PDF",
            "Summarize important sections",
            "Create a report",
        ],
    )

    executor = Executor(
        step_runner=fake_step_runner,
        model=FakeExecutorModel(),
    )

    result = executor.execute(
        plan,
        verbose=False,
    )

    assert len(result.results) == 3

    assert all(
        step.successful
        for step in result.results
    )

    assert result.final_answer == (
        "Final report generated."
    )