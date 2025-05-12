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

class Function(Expression):
    def __init__(self, name: str, arg: Expression):
        self.name = name
        self.arg = arg

CONSTANTS = {
    'pi': 3.141592653589793,
    'e': 2.718281828459045,
}

FUNCTIONS = {'sqrt', 'sin', 'cos', 'tg', 'ctg', 'ln', 'exp', 'arctg'}

def tokenize(expression: str):
    token_pattern = re.compile(r'\d+\.\d+(e[+-]?\d+)?|\d+(e[+-]?\d+)?|[+\-*/^()]|[a-zA-Z_][a-zA-Z_0-9]*')
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
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

        def parse_term():
            if not tokens:
                raise ValueError("Unexpected end of expression")
            token = tokens.pop(0)
            
            if token in FUNCTIONS:
                if not tokens or tokens.pop(0) != '(':
                    raise ValueError("Expected '(' after function name")
                arg = parse_expr(tokens)
                if not tokens or tokens.pop(0) != ')':
                    raise ValueError("Missing closing parenthesis after function argument")
                return Function(token, arg)

            elif token in CONSTANTS:
                return Number(CONSTANTS[token])
            if token == '-':
                if not tokens:
                    raise ValueError("Invalid syntax after unary minus")
                if tokens[0] == '(':
                    tokens.pop(0)
                    expr = parse_expr(tokens)
                    if not tokens or tokens.pop(0) != ')':
                        raise ValueError("Missing closing parenthesis after unary minus")
                    return UnaryOp('-', expr)
                elif re.match(r'\d+(\.\d+)?(e[+-]?\d+)?', tokens[0]):
                    return UnaryOp('-', Number(float(tokens.pop(0))))
                else:
                    raise ValueError("Invalid token after unary minus")

            if token == '(':
                if tokens and tokens[0] in '+*/^':
                    raise ValueError(f"Unexpected operator '{tokens[0]}' after '(' — expected number or unary minus in parentheses")
                expr = parse_expr(tokens)
                if not tokens or tokens.pop(0) != ')':
                    raise ValueError("Missing closing parenthesis")
                return expr


            if re.match(r'\d+(\.\d+)?(e[+-]?\d+)?', token):
                return Number(float(token))

            raise ValueError(f"Unexpected token: {token}")

        def parse_binop_rhs(lhs, min_prec):
            while tokens and tokens[0] in precedence:
                op = tokens[0]
                prec = precedence[op]
                if prec < min_prec:
                    break
                tokens.pop(0)
                rhs = parse_term()
                next_min_prec = prec + 1 if op == '^' else prec
                while tokens and tokens[0] in precedence and precedence[tokens[0]] > next_min_prec:
                    rhs = parse_binop_rhs(rhs, precedence[tokens[0]])

                lhs = BinaryOp(lhs, op, rhs)
            return lhs

        lhs = parse_term()

        if tokens and re.match(r'\d+(\.\d+)?(e[+-]?\d+)?', tokens[0]):
            raise ValueError(f"Missing operator before: {tokens[0]}")
        
        expr = parse_binop_rhs(lhs, 0)
        return expr

    expr = parse_expr(tokens)

    if tokens:
        raise ValueError(f"Unexpected tokens remaining: {tokens}")

    return expr
