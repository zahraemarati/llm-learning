from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from prompts.research_prompt import research_prompt
from config import settings


model = ChatOpenAI(
    model=settings.chat_model,
    api_key=settings.bai_api_key,
    base_url="https://api.b.ai/v1",
    temperature=0,
)


output_parser = StrOutputParser()


simple_chain = (
    research_prompt
    | model
    | output_parser
)


if __name__ == "__main__":
    response = simple_chain.invoke(
        {
            "question": "What is Retrieval Augmented Generation?"
        }
    )

    print(response)