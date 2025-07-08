def run_math_agent(expression):
    if "+" in expression:
        a, b = expression.split("+")
        return f"{expression} = {float(a) + float(b)}"
    elif "-" in expression:
        a, b = expression.split("-")
        return f"{expression} = {float(a) - float(b)}"
    else:
        return "Only + and - are supported."

if __name__ == "__main__":
    print(run_math_agent("2+3"))
    print(run_math_agent("100-9"))

