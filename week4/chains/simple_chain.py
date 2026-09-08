from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from prompts.basic_prompt import prompt

from dotenv import load_dotenv
import os


load_dotenv()


model = ChatOpenAI(
    model=os.getenv("CHAT_MODEL"),
    api_key=os.getenv("BAI_API_KEY"),
    base_url="https://api.b.ai/v1",
    temperature=0
)


output_parser = StrOutputParser()


chain = (
    prompt
    |
    model
    |
    output_parser
)


response = chain.invoke(
    {
        "question": "Explain Hybrid Retrieval in RAG"
    }
)


print(response)