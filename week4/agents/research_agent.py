from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from config import settings

from tools.calculator import calculator
from tools.web_search import web_search
from tools.rag_tool import rag_search


model = ChatOpenAI(
    model=settings.chat_model,
    api_key=settings.openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
)


tools = [
    web_search,
    rag_search,
    calculator,
]


research_agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="""
You are an AI research assistant.

You have access to these tools:

- web_search:
  Use this when you need current information
  or external research papers.

- rag_search:
  Use this when answering questions about
  uploaded papers and internal documents.

- calculator:
  Use this for exact mathematical calculations.

Rules:

1. Choose tools only when necessary.
2. For questions about research papers,
   prefer rag_search over guessing.
3. For latest information,
   use web_search.
4. Provide clear answers and mention sources
   when available.
"""
)


if __name__ == "__main__":

    result = research_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "According to the uploaded paper,"
                        "what are the major development trends of intelligent technologies?"
                    ),
                }
            ]
        }
    )


    print(
        result["messages"][-1].content
    )