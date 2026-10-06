from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from llm_client import model
from tools.calculator import calculator
from tools.pdf_reader import pdf_reader
from tools.web_search import web_search
from tools.rag_tool import rag_search


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


def build_messages(user_input: str):
    return [
        SystemMessage(
            content=(
                "You are a research assistant. "
                "Use rag_search whenever the user's question depends on "
                "uploaded or indexed documents. "
                "When the user mentions a filename such as paper.pdf, "
                "pass that filename in the source argument. "
                "Use pdf_reader only when the user explicitly asks to read "
                "a PDF file directly from a file path. "
                "Use web_search for current public information."
            )
        ),
        HumanMessage(content=user_input),
    ]


def decide(user_input: str):
    messages = build_messages(user_input)
    return model_with_tools.invoke(messages)


def run_agent(
    user_input: str,
    verbose: bool = True,
) -> str:
    messages = build_messages(user_input)

    max_steps = 5

    for step in range(max_steps):
        response = model_with_tools.invoke(messages)

        messages.append(response)

        if not response.tool_calls:
            return response.content

        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            if verbose:
                print(f"\nStep: {step + 1}")
                print(f"Selected tool: {tool_name}")
                print(f"Tool args: {tool_args}")

            selected_tool = tools_by_name[tool_name]

            result = selected_tool.invoke(
                tool_args
            )

            if verbose:
                print(f"Observation: {result}")

            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"],
                )
            )

    raise RuntimeError(
        "Agent exceeded maximum number of steps."
    )