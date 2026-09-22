from tools.calculator import calculator


def test_multiply():
    result = calculator.invoke(
        {
            "a": 20,
            "b": 5,
            "operation": "multiply",
        }
    )

    assert result == 100