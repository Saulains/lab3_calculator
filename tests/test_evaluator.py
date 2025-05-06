import pytest
import math
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
    assert evaluate(parse("-(3+4)")) == -7

def test_nested_unary():
    expr = BinaryOp(UnaryOp('-', Number(3)), '+', Number(7))
    assert evaluate(expr) == 4

def test_scientific():
    assert evaluate(parse("1.25e2")) == 125.0

def test_parentheses():
    result = evaluate(parse("1 + 2 / (3 + 4)"))
    assert abs(result - 1.2857142857142856) < 1e-10

def test_near_zero_division():
    expr = "1 / 1e-300"
    result = evaluate(parse(expr))
    assert result > 1e+299

def test_negative_exponent():
    assert evaluate(parse("4^(-2)")) == 0.0625

def test_negative_base_non_integer_exponent():
    expr = BinaryOp(Number(-2), '^', Number(0.5))  
    with pytest.raises(ValueError):
        evaluate(expr)

def test_exponentiation():
    assert evaluate(parse("2^3")) == 8
    assert evaluate(parse("3^2")) == 9
    assert evaluate(parse("2.5^2")) == 6.25
    assert evaluate(parse("(-2)^2")) == 4
    assert evaluate(parse("2^(-3)")) == 0.125


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

def test_operation_order():
    assert evaluate(parse("1 + 2 * 3")) == 7  # 1 + (2 * 3)
    assert evaluate(parse("3 + 2 * 3")) == 9  # 3 + (2 * 3)
    assert evaluate(parse("(1 + 2) * 3")) == 9  # (1 + 2) * 3
    assert evaluate(parse("1 + (2 * 3)")) == 7  # 1 + (2 * 3)

def test_incomplete_expression():
    expr = "1 + (2 * 3"
    with pytest.raises(ValueError):
        evaluate(parse(expr))  

def test_constants():
    assert abs(evaluate(parse("pi")) - math.pi) < 0.01
    assert abs(evaluate(parse("e")) - math.e) < 0.01

def test_functions():
    assert abs(evaluate(parse("sin(pi / 2)")) - 1) < 0.01
    assert abs(evaluate(parse("cos(0)")) - 1) < 0.01
    assert abs(evaluate(parse("tg(pi / 4)")) - 1) < 0.01
    assert abs(evaluate(parse("ctg(pi / 4)")) - 1) < 0.01
    assert abs(evaluate(parse("ln(e)")) - 1) < 0.01
    assert abs(evaluate(parse("exp(1)")) - 2.718281828459045) < 0.01
    assert abs(evaluate(parse("sqrt(4)")) - 2) < 0.01
    assert abs(evaluate(parse("pi")) - 3.141592653589793) < 0.01
    assert abs(evaluate(parse("e")) - 2.718281828459045) < 0.01
    assert abs(evaluate(parse("sqrt(ln(e))")) - 1) < 0.01