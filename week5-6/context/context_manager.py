from langchain_core.messages import HumanMessage, SystemMessage

from memory.buffer_memory import BufferMemory
from memory.summary_memory import SummaryMemory


class ContextManager:
    def __init__(
        self,
        buffer_memory: BufferMemory,
        summary_memory: SummaryMemory,
        system_prompt: str,
        summary_threshold: int = 10,
        recent_messages: int = 4,
    ):
        self.buffer_memory = buffer_memory
        self.summary_memory = summary_memory
        self.system_prompt = system_prompt
        self.summary_threshold = summary_threshold
        self.recent_messages = recent_messages

    def build_messages(
        self,
        user_input: str,
    ):
        messages = [
            SystemMessage(
                content=self.system_prompt
            )
        ]

        summary = self.summary_memory.get_summary()

        if summary:
            messages.append(
                SystemMessage(
                    content=(
                        "Conversation summary:\n"
                        f"{summary}"
                    )
                )
            )

        messages.extend(
            self.buffer_memory.get_messages()
        )

        messages.append(
            HumanMessage(
                content=user_input
            )
        )

        return messages

    def update_memory(
        self,
        user_input: str,
        assistant_output: str,
    ) -> None:
        self.buffer_memory.add_user_message(
            user_input
        )

        self.buffer_memory.add_ai_message(
            assistant_output
        )

        self._summarize_if_needed()

    def _summarize_if_needed(
        self,
    ) -> None:
        messages = self.buffer_memory.get_messages()

        if len(messages) <= self.summary_threshold:
            return

        old_messages = messages[
            :-self.recent_messages
        ]

        recent_messages = messages[
            -self.recent_messages:
        ]

        self.summary_memory.update(
            old_messages
        )

        self.buffer_memory.clear()

        for message in recent_messages:
            self.buffer_memory.add_message(
                message
            )