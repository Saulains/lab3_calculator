import re

class Expression:
    pass

class Number(Expression):
    def __init__(self, value: float):
        self.value = value

class BinaryOp(Expression):
    def __init__(self, left: Expression, op: str, right: Expression):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp(Expression):
    def __init__(self, op: str, operand: Expression):
        self.op = op
        self.operand = operand


def tokenize(expression: str):
    token_pattern = re.compile(r'\d+\.\d+|\d+|[+\-*/]')
    pos = 0
    tokens = []

    matches = re.findall(r'\d+ \d+', expression)
    if matches:
        raise ValueError("Unexpected expression: there should be no spaces between the numbers.")

    expression = expression.replace(" ", "")
    while pos < len(expression):
        match = token_pattern.match(expression, pos)
        if match:
            tokens.append(match.group())
            pos = match.end()
        else:
            raise ValueError(f"Unexpected character: {expression[pos]}")
    for i in range(1, len(tokens)):
        if tokens[i] in '+-*/^' and tokens[i-1] in '+-*/^':
            raise ValueError(f"Two operators in a row: '{tokens[i-1]}{tokens[i]}'")

    return tokens

def parse(expression: str) -> Expression:
    tokens = tokenize(expression)
    if not tokens:
        raise ValueError("Empty or invalid expression")

    def parse_expr(tokens):
        def parse_term():
            if not tokens:
                raise ValueError("Unexpected end of expression")
            token = tokens.pop(0)
            if token == '-':
                if not tokens or not re.match(r'\d+(\.\d+)?', tokens[0]):
                    raise ValueError("Invalid syntax after unary minus")
                operand = Number(float(tokens.pop(0)))
                return UnaryOp('-', operand)

            if re.match(r'\d+(\.\d+)?', token):
                return Number(float(token))
            else:
                raise ValueError(f"Unexpected token: {token}")


        def parse_binop_rhs(lhs, min_prec):
            while tokens and tokens[0] in "+-*/":
                op = tokens[0]
                prec = {'+': 1, '-': 1, '*': 2, '/': 2}[op]
                if prec < min_prec:
                    break
                tokens.pop(0)
                if not tokens:
                    raise ValueError("Missing right-hand side of binary operation")
                # ❗ Запрет на унарный минус без скобок
                if tokens[0] == '-':
                    raise ValueError("Unary minus after operator must be in parentheses")
                rhs = parse_term()
                
                if tokens and re.match(r'\d+(\.\d+)?', tokens[0]):
                    raise ValueError(f"Missing operator before: {tokens[0]}")
                    
                while tokens and tokens[0] in "+-*/" and {'+': 1, '-': 1, '*': 2, '/': 2}[tokens[0]] > prec:
                    rhs = parse_binop_rhs(rhs, {'+': 1, '-': 1, '*': 2, '/': 2}[tokens[0]])
                lhs = BinaryOp(lhs, op, rhs)
            return lhs

        lhs = parse_term()
        
        if tokens and re.match(r'\d+(\.\d+)?', tokens[0]):
            raise ValueError(f"Missing operator before: {tokens[0]}")
            
        expr = parse_binop_rhs(lhs, 0)
        return expr

    expr = parse_expr(tokens)

    if tokens:
        raise ValueError(f"Unexpected tokens remaining: {tokens}")

    return expr