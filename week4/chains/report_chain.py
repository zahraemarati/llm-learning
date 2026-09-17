from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import settings


model = ChatOpenAI(
    model=settings.chat_model,
    api_key=settings.openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
)

report_prompt = ChatPromptTemplate.from_template(
"""
You are a research report generator.

Create a structured Markdown research report
based on the analysis and sources.

Do not invent sources.
Use only the provided sources.

The report must contain:

# Title

## Abstract

## Main Findings

## Comparison

## Conclusion

## Sources


Research Analysis:

{analysis}


Real Sources:

{sources}
"""
)


report_chain = (
    report_prompt
    |
    model
    |
    StrOutputParser()
)