import json
from dataclasses import dataclass

from langchain_core.messages import HumanMessage, SystemMessage


@dataclass
class Plan:
    goal: str
    steps: list[str]


class Planner:
    def __init__(self, model):
        self.model = model

    def create_plan(
        self,
        task: str,
    ) -> Plan:
        messages = [
            SystemMessage(
                content=(
                    "You are a planning agent. "
                    "Break the user's task into clear, actionable "
                    "research and analysis steps. "
                    "Return between 2 and 5 steps. "

                    "For uploaded or indexed documents such as paper.pdf, "
                    "use retrieval-oriented steps instead of opening "
                    "the file directly. "

                    "For document analysis, first retrieve the document's "
                    "main topics, purpose, scope, and structure. "
                    "Then retrieve important sections, themes, findings, "
                    "or concepts needed for the task. "
                    "Then analyze and organize the retrieved information. "

                    "Avoid vague retrieval instructions such as "
                    "'retrieve key findings' when a more descriptive "
                    "retrieval objective can be used. "

                    "Do not include writing the final answer or final report "
                    "as a planning step. "
                    "The executor will synthesize the final answer after "
                    "all steps are complete. "

                    "Use direct PDF reading only when the user provides "
                    "an explicit filesystem path such as uploads/file.pdf. "

                    "Return only valid JSON with this exact structure: "
                    '{"goal": "...", "steps": ["step 1", "step 2"]}.'
                )
            ),
            HumanMessage(
                content=task
            ),
        ]

        response = self.model.invoke(
            messages
        )

        data = self._parse_response(
            response.content
        )

        steps = data.get(
            "steps",
            []
        )

        if not steps:
            raise ValueError(
                "Planner returned no steps."
            )

        return Plan(
            goal=data.get(
                "goal",
                task,
            ),
            steps=steps,
        )

    def _parse_response(
        self,
        content: str,
    ) -> dict:
        content = content.strip()

        if content.startswith("```"):
            content = content.strip("`")

            if content.startswith("json"):
                content = content[4:].strip()

        return json.loads(content)