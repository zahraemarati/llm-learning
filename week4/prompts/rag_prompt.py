from langchain_core.prompts import ChatPromptTemplate


rag_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a research assistant.

Answer only using the provided context.

If the answer is not available in the context,
say:

"I couldn't find this information in the document."

Do not use outside knowledge.
Do not invent sources.
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
        ),
    ]
)