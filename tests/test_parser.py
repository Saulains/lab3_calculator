import pytest
from calculator.parser import parse, Number, BinaryOp, UnaryOp
from calculator.evaluator import evaluate

def test_single_number():
    expr = parse("42")
    assert isinstance(expr, Number)
    assert expr.value == 42

@pytest.mark.parametrize("expr_str, expected_type", [
    ("1+2", BinaryOp),
    ("3-4", BinaryOp),
    ("5*6", BinaryOp),
    ("7/8", BinaryOp),
])
def test_basic_operations(expr_str, expected_type):
    expr = parse(expr_str)
    assert isinstance(expr, expected_type)

def test_combined_expression():
    expr = parse("2+3*4")
    assert isinstance(expr, BinaryOp)
    assert expr.op == '+'
    assert isinstance(expr.right, BinaryOp)
    assert expr.right.op == '*'

def test_multi_digit_numbers():
    expr = parse("123+456")
    assert isinstance(expr, BinaryOp)
    assert expr.left.value == 123
    assert expr.right.value == 456

@pytest.mark.parametrize("bad_expr", ["2 /", "1 + 4j", "0; import os", "2 ** 2"])
def test_invalid_expressions(bad_expr):
    with pytest.raises(ValueError):
        parse(bad_expr)

def test_spaces_handling():
    expr = parse("  1 +  2 * 3 ")
    assert isinstance(expr, BinaryOp)

def test_unbalanced_parentheses():
    with pytest.raises(ValueError):
        parse("(1 + 2")

def test_extra_tokens():
    with pytest.raises(ValueError):
        parse("1 + 2 3")

def test_scientific_notation():
    expr = parse("1.25e+2")
    assert isinstance(expr, Number)
    assert expr.value == 125.0

def test_exponentiation():
    expr = parse("2^3")
    assert isinstance(expr, BinaryOp)
    assert expr.op == '^'
    assert isinstance(expr.left, Number) and expr.left.value == 2
    assert isinstance(expr.right, Number) and expr.right.value == 3

def test_unary_minus():
    expr = parse("-42")
    assert isinstance(expr, UnaryOp)
    assert expr.op == '-'
    assert isinstance(expr.operand, Number)
    assert expr.operand.value == 42

    expr = parse("-1 + 2")
    assert isinstance(expr, BinaryOp)
    assert isinstance(expr.left, UnaryOp)
    assert expr.left.op == '-'
    assert isinstance(expr.left.operand, Number)
    assert expr.left.operand.value == 1
    assert expr.op == '+'
    assert isinstance(expr.right, Number)
    assert expr.right.value == 2


def test_unary_minus_without_parentheses_should_fail():
    with pytest.raises(ValueError):
        parse("2 * -3")

def test_parse():
    expr = parse("1.5 + 2.5")
    assert isinstance(expr, BinaryOp)  
    assert isinstance(expr.left, Number)  
    assert expr.left.value == 1.5  

def test_parentheses():
    expr = parse("1 + 2 / (3 + 4)")
    assert isinstance(expr, BinaryOp)

def test_deeply_nested_parentheses():
    expr = parse("1 + (2 * (3 + (4 / 2)))") 
    # Проверяем, что выражение является операцией сложения (BinaryOp)
    assert isinstance(expr, BinaryOp)
    assert expr.op == '+'
    assert isinstance(expr.left, Number)  # Левый операнд должен быть числом (1)
    assert expr.left.value == 1
    # Проверяем правый операнд, который является операцией умножения (BinaryOp)
    assert isinstance(expr.right, BinaryOp)
    assert expr.right.op == '*'  
    # Проверяем операнды умножения
    assert isinstance(expr.right.left, Number)  # Левый операнд для * (2)
    assert expr.right.left.value == 2 
    # Проверяем правый операнд умножения, который является операцией сложения
    assert isinstance(expr.right.right, BinaryOp)
    assert expr.right.right.op == '+'  
    # Проверяем операнды сложения
    assert isinstance(expr.right.right.left, Number)  # Левый операнд для + (3)
    assert expr.right.right.left.value == 3 
    # Проверяем правый операнд сложения, который является операцией деления
    assert isinstance(expr.right.right.right, BinaryOp)
    assert expr.right.right.right.op == '/'
    # Проверяем операнды деления
    assert isinstance(expr.right.right.right.left, Number)  # Левый операнд для / (4)
    assert expr.right.right.right.left.value == 4
    assert isinstance(expr.right.right.right.right, Number)  # Правый операнд для / (2)
    assert expr.right.right.right.right.value == 2



def test_negative_exponent_without_parentheses():
    with pytest.raises(ValueError):
        parse("4^-2")  


def test_missing_operator():
    expr = "2 3"
    with pytest.raises(ValueError):
        evaluate(parse(expr))  


def test_repeated_operators():
    expr = "1 ++ 2"
    with pytest.raises(ValueError):
        parse(expr)  
    expr = "1 -(- 2"
    with pytest.raises(ValueError):
        parse(expr)  
    expr = "1 +- 2"
    with pytest.raises(ValueError):
        parse(expr)  
    expr = "1 **+ 2"
    with pytest.raises(ValueError):
        parse(expr) 

def test_unexpected_operator_after_parenthesis():
    invalid_expressions = [
        "(+3 + 2)",   
        "(*4 + 1)",   
        "(/5 - 2)",  
        "(^2 + 1)"  
    ]
    
    for expr in invalid_expressions:
        with pytest.raises(ValueError, match=r"Unexpected operator '.*' after '\('"):
            parse(expr)

def test_sin():
    expr = parse("-3 + sin(0)")
    assert expr is not None

def test_sqrt():
    expr = parse("sqrt(4)")
    assert expr is not None

def test_cos():
    expr = parse("cos(0)")
    assert expr is not None

def test_tg():
    expr = parse("tg(0)")
    assert expr is not None

def test_ctg():
    expr = parse("ctg(1)")
    assert expr is not None

def test_ln():
    expr = parse("ln(e)")
    assert expr is not None

def test_exp():
    expr = parse("exp(1)")
    assert expr is not None

def test_pi_constant():
    expr = parse("pi")
    assert expr is not None

def test_e_constant():
    expr = parse("e")
    assert expr is not None

def test_combined_expression():
    expr = parse("sqrt(ln(e))")
    assert expr is not None