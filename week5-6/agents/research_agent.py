from agents.base_agent import (
    AgentConfig,
    BaseAgent,
)
from agents.prompts import (
    RESEARCH_AGENT_PROMPT,
)
from context.context_manager import ContextManager
from llm_client import model
from memory.buffer_memory import BufferMemory
from memory.summary_memory import SummaryMemory
from tools.calculator import calculator
from tools.pdf_reader import pdf_reader
from tools.rag_tool import rag_search
from tools.web_search import web_search


class ResearchAgent(BaseAgent):
    def __init__(
        self,
        model,
        tools: list,
        context_manager=None,
    ):
        config = AgentConfig(
            name="research_agent",
            system_prompt=RESEARCH_AGENT_PROMPT,
            max_steps=5,
        )

        super().__init__(
            model=model,
            config=config,
            tools=tools,
            context_manager=context_manager,
        )


tools = [
    calculator,
    pdf_reader,
    web_search,
    rag_search,
]


buffer_memory = BufferMemory(
    max_messages=None
)


summary_memory = SummaryMemory(
    summarizer=model
)


context_manager = ContextManager(
    buffer_memory=buffer_memory,
    summary_memory=summary_memory,
    system_prompt=RESEARCH_AGENT_PROMPT,
    summary_threshold=10,
    recent_messages=4,
)


research_agent = ResearchAgent(
    model=model,
    tools=tools,
    context_manager=context_manager,
)


model_with_tools = (
    research_agent.model_with_tools
)


tools_by_name = (
    research_agent.tools_by_name
)


def build_messages(
    user_input: str,
):
    return research_agent.build_messages(
        user_input
    )


def decide(
    user_input: str,
):
    research_agent.model_with_tools = (
        model_with_tools
    )

    return research_agent.decide(
        user_input
    )


def run_agent(
    user_input: str,
    verbose: bool = True,
    save_memory: bool = True,
) -> str:
    research_agent.model_with_tools = (
        model_with_tools
    )

    return research_agent.run(
        user_input=user_input,
        verbose=verbose,
        save_memory=save_memory,
    )


def clear_memory() -> None:
    research_agent.clear_memory()