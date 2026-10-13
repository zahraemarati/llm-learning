from agents.executor import Executor
from agents.planner import Planner
from agents.research_agent import (
    context_manager,
    run_agent,
)
from llm_client import model


planner = Planner(
    model=model
)


def run_planned_agent(
    user_input: str,
    verbose: bool = True,
) -> str:
    plan = planner.create_plan(
        user_input
    )

    if verbose:
        print(
            f"\nGoal: {plan.goal}"
        )

        print("\nPlan:")

        for index, step in enumerate(
            plan.steps,
            start=1,
        ):
            print(
                f"{index}. {step}"
            )

    executor = Executor(
        model=model,
        step_runner=lambda instruction: run_agent(
            instruction,
            verbose=verbose,
            save_memory=False,
        ),
        max_retries=1,
    )

    execution = executor.execute(
        plan=plan,
        verbose=verbose,
    )

    context_manager.update_memory(
        user_input=user_input,
        assistant_output=execution.final_answer,
    )

    return execution.final_answer