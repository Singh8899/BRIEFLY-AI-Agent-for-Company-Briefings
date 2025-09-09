from langchain_core.tools import tool

@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

@tool
def get_temperature(city: str) -> str:
    """Fake weather tool."""
    data = {"Berlin": "19°C", "Bologna": "27°C"}
    return data.get(city, "No data")