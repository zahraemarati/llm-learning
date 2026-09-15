from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """
    Useful for mathematical calculations.

    Input should be a mathematical expression.
    Example:
    25 * 4
    """

    try:
        result = eval(expression)

        return str(result)

    except Exception:
        return "Invalid calculation"