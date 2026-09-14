from langchain_core.prompts import ChatPromptTemplate


report_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a research assistant.

Create a clear and structured research report
based only on the provided content.
"""
        ),
        (
            "human",
            """
Content:
{content}

Generate a report with exactly these sections:

Title
Summary
Insights
Conclusion
"""
        )
    ]
)