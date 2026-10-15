from dataclasses import dataclass

from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    ToolMessage,
)


@dataclass
class AgentConfig:
    name: str
    system_prompt: str
    max_steps: int = 5


class BaseAgent:
    def __init__(
        self,
        model,
        config: AgentConfig,
        tools: list | None = None,
        context_manager=None,
    ):
        self.model = model
        self.config = config
        self.tools = tools or []
        self.context_manager = context_manager

        self.tools_by_name = {
            tool.name: tool
            for tool in self.tools
        }

        if self.tools:
            self.model_with_tools = self.model.bind_tools(
                self.tools
            )
        else:
            self.model_with_tools = self.model

    def build_messages(
        self,
        user_input: str,
    ):
        if self.context_manager:
            return self.context_manager.build_messages(
                user_input
            )

        return [
            SystemMessage(
                content=self.config.system_prompt
            ),
            HumanMessage(
                content=user_input
            ),
        ]

    def decide(
        self,
        user_input: str,
    ):
        messages = self.build_messages(
            user_input
        )

        return self.model_with_tools.invoke(
            messages
        )

    def run(
        self,
        user_input: str,
        verbose: bool = True,
        save_memory: bool = True,
    ) -> str:
        messages = self.build_messages(
            user_input
        )

        for step in range(
            self.config.max_steps
        ):
            response = self.model_with_tools.invoke(
                messages
            )

            messages.append(
                response
            )

            tool_calls = getattr(
                response,
                "tool_calls",
                [],
            )

            if not tool_calls:
                final_answer = response.content

                if (
                    save_memory
                    and self.context_manager
                ):
                    self.context_manager.update_memory(
                        user_input=user_input,
                        assistant_output=final_answer,
                    )

                return final_answer

            for tool_call in tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                if verbose:
                    print(
                        f"\nStep: {step + 1}"
                    )
                    print(
                        f"Selected tool: {tool_name}"
                    )
                    print(
                        f"Tool args: {tool_args}"
                    )

                if tool_name not in self.tools_by_name:
                    raise ValueError(
                        f"Unknown tool: {tool_name}"
                    )

                selected_tool = self.tools_by_name[
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
            f"{self.config.name} exceeded maximum number of steps."
        )

    def clear_memory(
        self,
    ) -> None:
        if not self.context_manager:
            return

        self.context_manager.buffer_memory.clear()
        self.context_manager.summary_memory.clear()