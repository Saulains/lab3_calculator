import sys
from calculator.parser import parse
from calculator.evaluator import evaluate

def main():
    try:
        expr = parse(sys.argv[1])
        result = evaluate(expr)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    main()
