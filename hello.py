import logging

def greet(name: str) -> str:
    """
    Greet a person by name.

    Args:
        name (str): The name of the person to greet.

    Returns:
        str: A greeting message.
    """
    logging.info(f"Greeting {name}")
    return f"Hello, {name}!"


if __name__ == "__main__":
    # Example usage
    print(greet("Alice"))
    print(greet("Bob"))
