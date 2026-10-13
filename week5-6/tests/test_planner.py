from langchain_core.messages import AIMessage

from agents.planner import Planner


class FakePlannerModel:
    def invoke(
        self,
        messages,
    ):
        return AIMessage(
            content=(
                "{"
                '"goal": "Analyze the paper", '
                '"steps": ['
                '"Read the PDF", '
                '"Retrieve important sections", '
                '"Summarize the findings", '
                '"Create a report"'
                "]"
                "}"
            )
        )


def test_planner_creates_steps():
    planner = Planner(
        model=FakePlannerModel()
    )

    plan = planner.create_plan(
        "Analyze this paper and create a report"
    )

    assert plan.goal == (
        "Analyze the paper"
    )

    assert len(plan.steps) == 4

    assert plan.steps[0] == (
        "Read the PDF"
    )