from context.context_manager import ContextManager
from memory.buffer_memory import BufferMemory
from memory.summary_memory import SummaryMemory


class FakeResponse:
    def __init__(self, content: str):
        self.content = content


class FakeSummarizer:
    def invoke(self, messages):
        return FakeResponse(
            "The user is working on a RAG project."
        )


def test_old_messages_are_summarized():
    buffer_memory = BufferMemory(
        max_messages=None
    )

    summary_memory = SummaryMemory(
        summarizer=FakeSummarizer()
    )

    manager = ContextManager(
        buffer_memory=buffer_memory,
        summary_memory=summary_memory,
        system_prompt="You are a research assistant.",
        summary_threshold=4,
        recent_messages=2,
    )

    manager.update_memory(
        user_input="My project is about RAG",
        assistant_output="Got it.",
    )

    manager.update_memory(
        user_input="I use Chroma",
        assistant_output="Understood.",
    )

    manager.update_memory(
        user_input="I also have an agent",
        assistant_output="Great.",
    )

    assert summary_memory.get_summary() == (
        "The user is working on a RAG project."
    )

    messages = buffer_memory.get_messages()

    assert len(messages) == 2
    assert messages[0].content == (
        "I also have an agent"
    )
    assert messages[1].content == "Great."