from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from config import settings

from prompts.conversation_prompt import (
    conversation_prompt
)

from memory.buffer_memory import (
    buffer_memory
)


model = ChatOpenAI(
    model=settings.chat_model,
    api_key=settings.openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
)


conversation_chain = (
    conversation_prompt
    | model
    | StrOutputParser()
)
