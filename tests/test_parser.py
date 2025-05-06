import pytest
from calculator.parser import parse, Number, BinaryOp, UnaryOp

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

@pytest.mark.parametrize("bad_expr", ["2 ^ 4", "2 /", "1 + 4j", "0; import os", "2 ** 2"])
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