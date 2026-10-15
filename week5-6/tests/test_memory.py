from langchain_core.messages import (
    AIMessage,
    HumanMessage,
)

from context.context_manager import (
    ContextManager,
)
from memory.buffer_memory import (
    BufferMemory,
)
from memory.summary_memory import (
    SummaryMemory,
)


class FakeResponse:
    def __init__(
        self,
        content: str,
    ):
        self.content = content


class FakeSummarizer:
    def invoke(
        self,
        messages,
    ):
        return FakeResponse(
            "The user is building a RAG project."
        )


def test_buffer_memory_stores_messages():
    memory = BufferMemory(
        max_messages=10
    )

    memory.add_user_message(
        "Hello"
    )

    memory.add_ai_message(
        "Hi"
    )

    messages = memory.get_messages()

    assert len(messages) == 2

    assert isinstance(
        messages[0],
        HumanMessage,
    )

    assert isinstance(
        messages[1],
        AIMessage,
    )

    assert messages[0].content == "Hello"
    assert messages[1].content == "Hi"


def test_buffer_memory_respects_limit():
    memory = BufferMemory(
        max_messages=2
    )

    memory.add_user_message(
        "Message 1"
    )

    memory.add_ai_message(
        "Message 2"
    )

    memory.add_user_message(
        "Message 3"
    )

    messages = memory.get_messages()

    assert len(messages) == 2

    assert messages[0].content == (
        "Message 2"
    )

    assert messages[1].content == (
        "Message 3"
    )


def test_summary_memory_creates_summary():
    summary_memory = SummaryMemory(
        summarizer=FakeSummarizer()
    )

    messages = [
        HumanMessage(
            content="My project uses RAG."
        ),
        AIMessage(
            content="Understood."
        ),
    ]

    summary = summary_memory.update(
        messages
    )

    assert summary == (
        "The user is building a RAG project."
    )

    assert (
        summary_memory.get_summary()
        == summary
    )


def test_context_manager_includes_memory():
    buffer_memory = BufferMemory(
        max_messages=None
    )

    summary_memory = SummaryMemory(
        summarizer=FakeSummarizer()
    )

    manager = ContextManager(
        buffer_memory=buffer_memory,
        summary_memory=summary_memory,
        system_prompt="Test assistant.",
        summary_threshold=10,
        recent_messages=4,
    )

    manager.update_memory(
        user_input="My project is about RAG.",
        assistant_output="Got it.",
    )

    messages = manager.build_messages(
        "What is my project about?"
    )

    contents = [
        message.content
        for message in messages
    ]

    assert (
        "My project is about RAG."
        in contents
    )

    assert "Got it." in contents

    assert (
        "What is my project about?"
        in contents
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
        system_prompt="Test assistant.",
        summary_threshold=2,
        recent_messages=2,
    )

    manager.update_memory(
        user_input="My project uses RAG.",
        assistant_output="Understood.",
    )

    manager.update_memory(
        user_input="I am adding agents.",
        assistant_output="Great.",
    )

    assert (
        summary_memory.get_summary()
        == "The user is building a RAG project."
    )

    recent_messages = (
        buffer_memory.get_messages()
    )

    assert len(recent_messages) == 2

    assert recent_messages[0].content == (
        "I am adding agents."
    )

    assert recent_messages[1].content == (
        "Great."
    )


def test_context_contains_summary():
    buffer_memory = BufferMemory(
        max_messages=None
    )

    summary_memory = SummaryMemory(
        summarizer=FakeSummarizer()
    )

    manager = ContextManager(
        buffer_memory=buffer_memory,
        summary_memory=summary_memory,
        system_prompt="Test assistant.",
        summary_threshold=2,
        recent_messages=2,
    )

    manager.update_memory(
        user_input="My project uses RAG.",
        assistant_output="Understood.",
    )

    manager.update_memory(
        user_input="I am building agents.",
        assistant_output="Great.",
    )

    messages = manager.build_messages(
        "What am I building?"
    )

    combined = "\n".join(
        message.content
        for message in messages
    )

    assert (
        "The user is building a RAG project."
        in combined
    )