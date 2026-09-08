from langchain_core.prompts import ChatPromptTemplate


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI research assistant. "
            "Explain technical concepts clearly and accurately."
        ),
        (
            "human",
            "{question}"
        )
    ]
)