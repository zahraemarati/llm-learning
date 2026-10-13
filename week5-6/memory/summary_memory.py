from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage


class SummaryMemory:
    def __init__(self, summarizer):
        self.summarizer = summarizer
        self.summary = ""

    def update(
        self,
        messages: list[BaseMessage],
    ) -> str:
        if not messages:
            return self.summary

        conversation = self._format_messages(
            messages
        )

        prompt = [
            SystemMessage(
                content=(
                    "Summarize the conversation while preserving "
                    "important facts, decisions, preferences, "
                    "and project details."
                )
            ),
            HumanMessage(
                content=(
                    f"Previous summary:\n{self.summary}\n\n"
                    f"New conversation:\n{conversation}"
                )
            ),
        ]

        response = self.summarizer.invoke(
            prompt
        )

        self.summary = response.content

        return self.summary

    def get_summary(self) -> str:
        return self.summary

    def clear(self) -> None:
        self.summary = ""

    def _format_messages(
        self,
        messages: list[BaseMessage],
    ) -> str:
        formatted = []

        for message in messages:
            formatted.append(
                f"{message.type}: {message.content}"
            )

        return "\n".join(formatted)