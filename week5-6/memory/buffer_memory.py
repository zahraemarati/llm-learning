from langchain_core.messages import AIMessage, BaseMessage, HumanMessage


class BufferMemory:
    def __init__(
        self,
        max_messages: int | None = 10,
    ):
        self.max_messages = max_messages
        self.messages: list[BaseMessage] = []

    def add_message(
        self,
        message: BaseMessage,
    ) -> None:
        self.messages.append(message)
        self._trim()

    def add_user_message(
        self,
        content: str,
    ) -> None:
        self.add_message(
            HumanMessage(content=content)
        )

    def add_ai_message(
        self,
        content: str,
    ) -> None:
        self.add_message(
            AIMessage(content=content)
        )

    def get_messages(
        self,
    ) -> list[BaseMessage]:
        return list(self.messages)

    def clear(
        self,
    ) -> None:
        self.messages.clear()

    def _trim(
        self,
    ) -> None:
        if self.max_messages is None:
            return

        if len(self.messages) > self.max_messages:
            self.messages = self.messages[
                -self.max_messages:
            ]