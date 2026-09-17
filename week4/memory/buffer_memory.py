from langchain_classic.memory import ConversationBufferMemory


buffer_memory = ConversationBufferMemory(
    memory_key="history",
    return_messages=True,
)


if __name__ == "__main__":

    buffer_memory.save_context(
        {"input": "Explain transformers"},
        {"output": "Transformers are neural network architectures."},
    )

    buffer_memory.save_context(
        {"input": "What about attention?"},
        {"output": "Attention is a mechanism used by transformers."},
    )

    history = buffer_memory.load_memory_variables({})

    print(history)