from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from config import settings

from tools.calculator import calculator
from tools.pdf_reader import pdf_reader
from tools.web_search import web_search


model = ChatOpenAI(
    model=settings.chat_model,
    api_key=settings.bai_api_key,
    base_url="https://api.b.ai/v1",
    temperature=0,
)


tools = [
    web_search,
    pdf_reader,
    calculator,
]


research_agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="""
You are an AI research assistant.

You have access to these tools:

- web_search: use it when current or external information is needed.
- pdf_reader: use it when the user asks about a PDF file.
- calculator: use it for calculations that should be exact.

Choose tools only when necessary.

If you can answer reliably without a tool, answer directly.
"""
)


if __name__ == "__main__":

    result = research_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Read the file ./paper.pdf and summarize it"
                }
            ]
        }
    )

    print(result["messages"][-1].content)