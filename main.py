import argparse
import sys
from calculator.parser import parse
from calculator.evaluator import evaluate

def main():
    parser = argparse.ArgumentParser(description="CLI Calculator")
    parser.add_argument("expression", help="Mathematical expression to evaluate, e.g., 'sin(90)'")
    parser.add_argument("--degrees", action="store_true", help="Interpret angles in degrees")

    args = parser.parse_args()

    try:
        expr = parse(args.expression)
        result = evaluate(expr, degrees=args.degrees)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    main()
