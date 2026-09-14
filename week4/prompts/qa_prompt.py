from langchain_core.prompts import ChatPromptTemplate


qa_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a question answering assistant.

Answer the question using only the provided context.

If the answer is not available in the context,
say that you do not have enough information.
"""
        ),
        (
            "human",
            """
Context:
{context}

Question:
{question}
"""
        )
    ]
)