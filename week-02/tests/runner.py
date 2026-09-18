import re
import sys
from pathlib import Path


CASES = [
    ("1", [40, 60, 80], 50),
    ("2", [100], 50),
    ("3", [49.5, 50], 50),
    ("4", [], 50),
    ("5", [40, "60"], 50),
    ("6", [-1, 50, 101], 50),
]


def load_first_python_block(file_path):
    source = file_path.read_text(encoding="utf-8")
    match = re.search(r"```python\s*(.*?)```", source, re.DOTALL | re.IGNORECASE)
    return match.group(1) if match else source


def expected_result(case_number):
    expected = {
        "1": {"average": 60, "highest": 80, "lowest": 40, "pass_rate": 66.67},
        "2": {"average": 100, "highest": 100, "lowest": 100, "pass_rate": 100},
        "3": {"average": 49.75, "highest": 50, "lowest": 49.5, "pass_rate": 50},
    }
    return expected.get(case_number)


def result_matches(result, expected):
    return (
        set(result) == set(expected)
        and all(abs(result[key] - value) <= 0.01 for key, value in expected.items())
    )


def run_file(file_path):
    print(f"=== {file_path.name} ===")
    namespace = {}
    try:
        exec(load_first_python_block(file_path), namespace)
    except Exception as error:
        print(f"LOAD ERROR: {type(error).__name__}: {error}")
        for case_number, _, _ in CASES:
            print(f"CASE {case_number}: ERROR")
        return

    analyze_marks = namespace.get("analyze_marks")
    if analyze_marks is None:
        print("LOAD ERROR: analyze_marks function not found")
        for case_number, _, _ in CASES:
            print(f"CASE {case_number}: ERROR")
        return

    for case_number, marks, pass_mark in CASES:
        try:
            result = analyze_marks(marks, pass_mark)
            expected = expected_result(case_number)
            verdict = "PASS" if expected is not None and result_matches(result, expected) else "FAIL"
            print(f"CASE {case_number}: {verdict} -> {result}")
        except ValueError as error:
            verdict = "PASS" if case_number in {"4", "5", "6"} else "ERROR"
            print(f"CASE {case_number}: {verdict} -> ValueError: {error}")
        except Exception as error:
            print(f"CASE {case_number}: ERROR -> {type(error).__name__}: {error}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python tests/runner.py code/prompt_a.py")
    run_file(Path(sys.argv[1]))