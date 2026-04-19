"""
Utility functions for the package.
"""


def greet(name: str) -> str:
    """
    Greet a person by name.

    Args:
        name (str): The name of the person to greet.

    Returns:
        str: A greeting message.
    """
    return f"Hello, {name}!"


def add(a: int, b: int) -> int:
    """
    Add two numbers together.

    Args:
        a (int): First number.
        b (int): Second number.

    Returns:
        int: The sum of a and b.
    """
    return a + b


def multiply(a: int, b: int) -> int:
    """
    Multiply two numbers together.

    Args:
        a (int): First number.
        b (int): Second number.

    Returns:
        int: The product of a and b.
    """
    return a * b
