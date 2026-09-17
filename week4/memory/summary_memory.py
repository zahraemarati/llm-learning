from langchain_classic.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI

from config import settings


model = ChatOpenAI(
    model=settings.chat_model,
    api_key=settings.openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
)


summary_memory = ConversationSummaryMemory(
    llm=model,
    memory_key="history",
    return_messages=True,
)


if __name__ == "__main__":

    summary_memory.save_context(
        {
            "input": "Explain transformers"
        },
        {
            "output": (
                "Transformers are neural networks "
                "that use attention mechanisms."
            )
        },
    )


    summary_memory.save_context(
        {
            "input": "What about attention?"
        },
        {
            "output": (
                "Attention helps models focus "
                "on relevant parts of the input."
            )
        },
    )


    history = summary_memory.load_memory_variables({})

    print(history)