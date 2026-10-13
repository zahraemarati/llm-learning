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


def test_summary_is_included_in_context():
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
        summary_threshold=2,
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

    messages = manager.build_messages(
        "What is my project about?"
    )

    contents = [
        message.content
        for message in messages
    ]

    assert any(
        "The user's project is about RAG."
        in content
        for content in contents
    )