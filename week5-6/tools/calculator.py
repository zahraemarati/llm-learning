from typing import Literal

from langchain_core.tools import tool


@tool
def calculator(
    a: float,
    b: float,
    operation: Literal["add", "subtract", "multiply", "divide"],
) -> float:
    """
    Perform a mathematical calculation on two numbers.

    Use this tool when the user asks for arithmetic calculations
    such as addition, subtraction, multiplication, or division.
    """

    if operation == "add":
        return a + b

    if operation == "subtract":
        return a - b

    if operation == "multiply":
        return a * b

    if operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero.")

        return a / b

    raise ValueError(f"Unsupported operation: {operation}")