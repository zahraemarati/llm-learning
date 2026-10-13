from langchain_core.messages import AIMessage, HumanMessage

from memory.buffer_memory import BufferMemory


def test_buffer_memory_stores_messages():
    memory = BufferMemory()

    memory.add_user_message(
        "My project is about RAG"
    )

    memory.add_ai_message(
        "Got it."
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

    assert messages[0].content == (
        "My project is about RAG"
    )


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
    assert messages[0].content == "Message 2"
    assert messages[1].content == "Message 3"


def test_buffer_memory_clear():
    memory = BufferMemory()

    memory.add_user_message(
        "My project is about RAG"
    )

    memory.clear()

    assert memory.get_messages() == []