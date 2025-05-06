from calculator.evaluator import evaluate
from calculator.parser import parse
import pytest
import time

def test_large_number_expression():
    large_expr = "1" + "0" * 100  
    expr = f"{large_expr} + 1"
    start = time.time()
    result = evaluate(parse(expr))
    end = time.time()
    assert result > 10**100
    assert (end - start) < 0.2, "Execution time exceeded 200ms for large numbers"

def test_deeply_nested_expression():
    expr = "sin(" * 100 + "pi/2" + ")" * 100
    start = time.time()
    result = evaluate(parse(expr))
    end = time.time()
    assert -1 <= result <= 1  
    assert (end - start) < 0.2, "Execution time exceeded 200ms for deeply nested expression"


@pytest.mark.parametrize("expression", [
    " + ".join(["1"] * 1000),
    "1.000000000000001 ^ 36893488147419103232",  
    "1 ^ 36893488147419103232",  
    " + ".join(["10000000000000000000000000000000"] * 50), 
    "1 + (2 + (3 + (4 + (5 + (6 + (7 + (8 + (9 + (10))))))))",  
])
def test_heavy_expression_performance(expression):
    start = time.time()
    try:
        result = evaluate(parse(expression))
    except Exception:
        result = None
    end = time.time()
    assert (end - start) < 0.2
