import json
from dataclasses import dataclass

from langchain_core.messages import HumanMessage, SystemMessage

from agents.planner import Plan


@dataclass
class StepResult:
    step: str
    output: str
    successful: bool


@dataclass
class ExecutionResult:
    results: list[StepResult]
    final_answer: str


class Executor:
    def __init__(
        self,
        step_runner,
        model,
        max_retries: int = 1,
    ):
        self.step_runner = step_runner
        self.model = model
        self.max_retries = max_retries

    def execute(
        self,
        plan: Plan,
        verbose: bool = True,
    ) -> ExecutionResult:
        results = []

        for index, step in enumerate(
            plan.steps,
            start=1,
        ):
            if verbose:
                print(
                    f"\nPlanning Step {index}: {step}"
                )

            output = self._execute_step(
                plan=plan,
                step=step,
                previous_results=results,
            )

            reflection = self._reflect(
                step=step,
                output=output,
            )

            retries = 0

            while (
                not reflection["sufficient"]
                and retries < self.max_retries
            ):
                retries += 1

                if verbose:
                    print(
                        "Reflection requested retry: "
                        f"{reflection['feedback']}"
                    )

                output = self._execute_step(
                    plan=plan,
                    step=step,
                    previous_results=results,
                    feedback=reflection["feedback"],
                )

                reflection = self._reflect(
                    step=step,
                    output=output,
                )

            result = StepResult(
                step=step,
                output=output,
                successful=reflection[
                    "sufficient"
                ],
            )

            results.append(
                result
            )

            if verbose:
                print(
                    f"Step result: {output}"
                )

        final_answer = self._synthesize(
            plan=plan,
            results=results,
        )

        return ExecutionResult(
            results=results,
            final_answer=final_answer,
        )

    def _execute_step(
        self,
        plan: Plan,
        step: str,
        previous_results: list[StepResult],
        feedback: str | None = None,
    ) -> str:
        previous_context = "\n\n".join(
            (
                f"Step: {result.step}\n"
                f"Result: {result.output}"
            )
            for result in previous_results
        )

        instruction = (
            f"Overall goal:\n{plan.goal}\n\n"
            f"Current step:\n{step}\n\n"
        )

        if previous_context:
            instruction += (
                "Previous step results:\n"
                f"{previous_context}\n\n"
            )

        if feedback:
            instruction += (
                "Reflection feedback:\n"
                f"{feedback}\n\n"
            )

        instruction += (
            "Execute only the current step."
        )

        return self.step_runner(
            instruction
        )

    def _reflect(
        self,
        step: str,
        output: str,
    ) -> dict:
        messages = [
            SystemMessage(
                content=(
                    "Evaluate whether the result sufficiently "
                    "completes the requested step. "
                    "Return only JSON: "
                    '{"sufficient": true, "feedback": ""}. '
                    "If insufficient, set sufficient to false "
                    "and explain what is missing in feedback."
                )
            ),
            HumanMessage(
                content=(
                    f"Step:\n{step}\n\n"
                    f"Result:\n{output}"
                )
            ),
        ]

        response = self.model.invoke(
            messages
        )

        return self._parse_json(
            response.content
        )

    def _synthesize(
        self,
        plan: Plan,
        results: list[StepResult],
    ) -> str:
        execution_text = "\n\n".join(
            (
                f"Step: {result.step}\n"
                f"Result: {result.output}"
            )
            for result in results
        )

        messages = [
            SystemMessage(
                content=(
                    "Create the final answer for the user "
                    "using the completed execution steps. "
                    "Do not mention internal planning unless "
                    "it is useful to the user."
                )
            ),
            HumanMessage(
                content=(
                    f"Goal:\n{plan.goal}\n\n"
                    f"Execution results:\n"
                    f"{execution_text}"
                )
            ),
        ]

        response = self.model.invoke(
            messages
        )

        return response.content

    def _parse_json(
        self,
        content: str,
    ) -> dict:
        content = content.strip()

        if content.startswith("```"):
            content = content.strip("`")

            if content.startswith("json"):
                content = content[4:].strip()

        return json.loads(content)