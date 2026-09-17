from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)

from dotenv import load_dotenv
import os


load_dotenv()


model = ChatOpenAI(
    model=os.getenv("CHAT_MODEL"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0
)


messages = [

    SystemMessage(
        content="""
        You are an AI research assistant.
        Answer clearly and technically.
        """
    ),

    HumanMessage(
        content="Explain Retrieval Augmented Generation"
    )

]


response = model.invoke(messages)


print(response.content)