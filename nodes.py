import re
from tools import add, sub

def decide_and_calculate(expression: str) -> str:
    if "+" in expression:
        a, b = map(float, expression.split("+"))
        result = add(a, b)
        return f"{expression} = {result}"
    elif "-" in expression:
        a, b = map(float, expression.split("-"))
        result = sub(a, b)
        return f"{expression} = {result}"
    else:
        return "Only + and - operations are supported."
