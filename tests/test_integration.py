import pytest
from calculator.parser import parse
from calculator.evaluator import evaluate

def test_parser_and_eval():
    assert evaluate(parse("1+1")) == 2

def test_parser_error():
    with pytest.raises(ValueError):
        parse("1 /")

def test_eval_error():
    with pytest.raises(ZeroDivisionError):
        evaluate(parse("1/0"))

def test_integration_parentheses_exponent_mix():
    expr = "(2 + 3)^(1 + 1)"
    assert evaluate(parse(expr)) == 25

def test_complex():
    expr = "3.375e+09^(1/3)"
    result = evaluate(parse(expr))
    assert round(result) == 1500

def test_negative_exponent_with_parentheses():
    expr = parse("4^(-2)")
    assert evaluate(expr) == 0.0625

def test_nested_functions():
    assert abs(evaluate(parse("sin(cos(0))")) - 0.841) < 0.01
    assert abs(evaluate(parse("sqrt(cos(0))")) - 1) < 0.01
    assert abs(evaluate(parse("tg(cos(0))")) - 1.557) < 0.01
    assert abs(evaluate(parse("ln(exp(1)) - 1"))) < 0.01
    assert abs(evaluate(parse("exp(ln(e))")) - 2.718) < 0.01
    assert abs(evaluate(parse("sqrt(ln(exp(1)))")) - 1) < 0.01
    assert abs(evaluate(parse("cos(tg(0))")) - 1) < 0.01