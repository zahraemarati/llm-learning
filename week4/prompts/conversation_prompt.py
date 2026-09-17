from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


conversation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful AI assistant.

Use the conversation history to answer
the user's question.
"""
        ),

        MessagesPlaceholder(
            variable_name="history"
        ),

        (
            "human",
            "{input}"
        ),
    ]
)