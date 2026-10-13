from langchain_core.messages import HumanMessage

from context.context_manager import ContextManager
from memory.buffer_memory import BufferMemory
from memory.summary_memory import SummaryMemory


class FakeResponse:
    def __init__(self, content: str):
        self.content = content


class FakeSummarizer:
    def invoke(self, messages):
        return FakeResponse(
            "The user's project is about RAG."
        )


def test_context_manager_includes_buffer():
    buffer_memory = BufferMemory()
    summary_memory = SummaryMemory(
        summarizer=FakeSummarizer()
    )

    buffer_memory.add_user_message(
        "My project is about RAG"
    )

    manager = ContextManager(
        buffer_memory=buffer_memory,
        summary_memory=summary_memory,
        system_prompt="You are a research assistant.",
    )

    messages = manager.build_messages(
        "What is my project about?"
    )

    assert len(messages) == 3
    assert messages[0].content == (
        "You are a research assistant."
    )
    assert messages[1].content == (
        "My project is about RAG"
    )
    assert messages[2].content == (
        "What is my project about?"
    )


def test_context_manager_includes_summary():
    buffer_memory = BufferMemory()

    summary_memory = SummaryMemory(
        summarizer=FakeSummarizer()
    )

    summary_memory.update(
        [
            HumanMessage(
                content="My project is about RAG"
            )
        ]
    )

    manager = ContextManager(
        buffer_memory=buffer_memory,
        summary_memory=summary_memory,
        system_prompt="You are a research assistant.",
    )

    messages = manager.build_messages(
        "What is my project about?"
    )

    assert len(messages) == 3

    assert "Conversation summary" in (
        messages[1].content
    )

    assert "RAG" in messages[1].content