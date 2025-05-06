import math
from calculator.parser import UnaryOp, BinaryOp, Number, Function

def evaluate(expr, degrees=False):
    if isinstance(expr, Number):
        return expr.value
    elif isinstance(expr, UnaryOp):
        if expr.op == '-':
            return -evaluate(expr.operand, degrees)
        else:
            raise ValueError(f"Unknown unary operator: {expr.op}")
    elif isinstance(expr, BinaryOp):
        left = evaluate(expr.left, degrees)
        right = evaluate(expr.right, degrees)
        if expr.op == '+':
            return left + right
        elif expr.op == '-':
            return left - right
        elif expr.op == '*':
            return left * right
        elif expr.op == '/':
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            if math.isinf(left / right):
                raise OverflowError("Result is infinite")
            return left / right
        elif expr.op == '^':
            # Проверка на отрицательную степень и некорректный синтаксис
            if left < 0 and not right.is_integer():
                raise ValueError("A negative number cannot be raised to a non-integer power")
            return left ** right
        else:
            raise ValueError(f"Unknown operator: {expr.op}")

    elif isinstance(expr, Function):
        arg = evaluate(expr.arg, degrees)
        if degrees and expr.name in {'sin', 'cos', 'tg', 'ctg'}:
            arg = math.radians(arg)
        match expr.name:
            case 'sqrt':
                return math.sqrt(arg)
            case 'sin':
                return math.sin(arg)
            case 'cos':
                return math.cos(arg)
            case 'tg':
                return math.tan(arg)
            case 'ctg':
                return 1 / math.tan(arg)
            case 'ln':
                return math.log(arg)
            case 'exp':
                return math.exp(arg)
            case _:
                raise ValueError(f"Unsupported function: {expr.name}")

    else:
        raise TypeError("Invalid expression type")
