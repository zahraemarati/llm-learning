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


summarizer_prompt = ChatPromptTemplate.from_template(
"""
You are an expert research assistant.

Analyze the following paper and extract:

1. Summary
2. Method
3. Results
4. Limitations


Paper:

{paper}
"""
)


summarizer_chain = (
    summarizer_prompt
    |
    model
    |
    StrOutputParser()
)