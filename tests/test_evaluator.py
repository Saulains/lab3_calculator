import pytest
from calculator.parser import parse, Number, BinaryOp, UnaryOp
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

# Добавление тестов с вещественными числами:
@pytest.mark.parametrize("expr_str, expected", [
    ("1.5+2.5", 4.0),
    ("3.0-1.2", 1.8),
    ("2.5*4", 10.0),
    ("5.0/2", 2.5),
])
def test_float_operations(expr_str, expected):
    result = evaluate(parse(expr_str))
    assert result == pytest.approx(expected, rel=1e-15)  # Допустимая погрешность