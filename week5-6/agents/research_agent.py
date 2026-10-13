from langchain_core.messages import ToolMessage

from context.context_manager import ContextManager
from llm_client import model
from memory.buffer_memory import BufferMemory
from memory.summary_memory import SummaryMemory
from tools.calculator import calculator
from tools.pdf_reader import pdf_reader
from tools.rag_tool import rag_search
from tools.web_search import web_search


tools = [
    calculator,
    pdf_reader,
    web_search,
    rag_search,
]

tools_by_name = {
    tool.name: tool
    for tool in tools
}

model_with_tools = model.bind_tools(tools)


buffer_memory = BufferMemory(
    max_messages=None
)

summary_memory = SummaryMemory(
    summarizer=model
)

context_manager = ContextManager(
    buffer_memory=buffer_memory,
    summary_memory=summary_memory,
    system_prompt=(
        "You are a research assistant. "
        "Use conversation context when answering follow-up questions. "
        "Use rag_search whenever the user's question depends on "
        "uploaded or indexed documents. "
        "When the user mentions a filename such as paper.pdf, "
        "pass that filename in the source argument. "
        "Use pdf_reader only when the user explicitly asks to read "
        "a PDF file directly from a file path. "
        "Use web_search for current public information."
    ),
    summary_threshold=10,
    recent_messages=4,
)


def build_messages(
    user_input: str,
):
    return context_manager.build_messages(
        user_input
    )


def decide(
    user_input: str,
):
    messages = build_messages(
        user_input
    )

    return model_with_tools.invoke(
        messages
    )


def run_agent(
    user_input: str,
    verbose: bool = True,
    save_memory: bool = True,
) -> str:
    messages = build_messages(
        user_input
    )

    max_steps = 5

    for step in range(max_steps):
        response = model_with_tools.invoke(
            messages
        )

        messages.append(response)

        if not response.tool_calls:
            final_answer = response.content

            if save_memory:
                context_manager.update_memory(
                    user_input=user_input,
                    assistant_output=final_answer,
                )

            return final_answer

        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            if verbose:
                print(f"\nStep: {step + 1}")
                print(f"Selected tool: {tool_name}")
                print(f"Tool args: {tool_args}")

            selected_tool = tools_by_name[
                tool_name
            ]

            result = selected_tool.invoke(
                tool_args
            )

            if verbose:
                print(
                    f"Observation: {result}"
                )

            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"],
                )
            )

    raise RuntimeError(
        "Agent exceeded maximum number of steps."
    )


def clear_memory() -> None:
    buffer_memory.clear()
    summary_memory.clear()