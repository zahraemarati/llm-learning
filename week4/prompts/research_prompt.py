from langchain_core.prompts import ChatPromptTemplate


research_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant.
            Provide accurate and structured answers.
            """
        ),
        (
            "human",
            """
            Question:

            {question}

            Provide:

            - Summary
            - Key points
            - Sources
            """
        )
    ]
)