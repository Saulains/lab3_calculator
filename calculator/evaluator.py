import math

from calculator.parser import UnaryOp, BinaryOp, Number


def evaluate(expr):
    if isinstance(expr, Number):
        return expr.value
    elif isinstance(expr, UnaryOp):
        if expr.op == '-':
            return -evaluate(expr.operand)
        else:
            raise ValueError(f"Unknown unary operator: {expr.op}")
    elif isinstance(expr, BinaryOp):
        left = evaluate(expr.left)
        right = evaluate(expr.right)
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
        else:
            raise ValueError(f"Unknown operator: {expr.op}")
    else:
        raise TypeError("Invalid expression type")
