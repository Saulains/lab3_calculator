import pytest
from calculator.parser import Number, BinaryOp, UnaryOp
from calculator.evaluator import evaluate

@pytest.mark.parametrize("expr, result", [
    (BinaryOp(Number(1), '+', Number(2)), 3),
    (BinaryOp(Number(4), '-', Number(2)), 2),
    (BinaryOp(Number(3), '*', Number(5)), 15),
    (BinaryOp(Number(10), '/', Number(2)), 5),
])
def test_simple_evaluations(expr, result):
    assert evaluate(expr) == result

def test_nested_expression():
    expr = BinaryOp(Number(2), '+', BinaryOp(Number(3), '*', Number(4)))  
    assert evaluate(expr) == 14

def test_division_by_zero():
    expr = BinaryOp(Number(1), '/', Number(0))
    with pytest.raises(ZeroDivisionError):
        evaluate(expr)

def test_large_division():
    expr = BinaryOp(Number(1e300), '/', Number(1e-300))
    with pytest.raises(OverflowError):
        evaluate(expr)

def test_unknown_operator():
    expr = BinaryOp(Number(1), '%', Number(2))  
    with pytest.raises(ValueError):
        evaluate(expr)

def test_unary_minus():
    expr = UnaryOp('-', Number(5))
    assert evaluate(expr) == -5

def test_nested_unary():
    expr = BinaryOp(UnaryOp('-', Number(3)), '+', Number(7))
    assert evaluate(expr) == 4