## Assumptions

# - **Non-empty input required** — an empty `marks` list raises `ValueError`.
# - **Elements must be numeric** — `int` or `float` (bools are rejected despite being `int` subclasses; `Decimal`/`Fraction` are rejected to keep it simple).
# - **Range** — each mark must satisfy `0 <= mark <= 100`.
# - **`pass_mark`** — must itself be numeric and in `[0, 100]`, otherwise `ValueError`.
# - **`pass_rate`** — percentage (`0–100`) of marks `>= pass_mark`, rounded to 2 decimals.
# - **`average`** — rounded to 2 decimals; `highest`/`lowest` returned as-is.

# ```python
def analyze_marks(marks, pass_mark=50):
    if not isinstance(marks, (list, tuple)):
        raise ValueError("marks must be a list or tuple")
    if len(marks) == 0:
        raise ValueError("marks must not be empty")

    if isinstance(pass_mark, bool) or not isinstance(pass_mark, (int, float)):
        raise ValueError("pass_mark must be a number")
    if not (0 <= pass_mark <= 100):
        raise ValueError("pass_mark must be between 0 and 100")

    cleaned = []
    for m in marks:
        if isinstance(m, bool) or not isinstance(m, (int, float)):
            raise ValueError(f"mark must be numeric, got {m!r}")
        if not (0 <= m <= 100):
            raise ValueError(f"mark out of range [0, 100]: {m!r}")
        cleaned.append(float(m))

    average = round(sum(cleaned) / len(cleaned), 2)
    highest = max(cleaned)
    lowest = min(cleaned)
    passed = sum(1 for m in cleaned if m >= pass_mark)
    pass_rate = round(passed / len(cleaned) * 100, 2)

    return {
        "average": average,
        "highest": highest,
        "lowest": lowest,
        "pass_rate": pass_rate,
    }
# ```

# ## Explanation

# 1. **Input guards first** — validate the container type, reject empty lists, and validate `pass_mark` before touching the marks.
# 2. **Per-mark validation** — reject `bool` explicitly (since `True == 1` would sneak through `isinstance(..., int)`), reject non-numerics, and enforce `[0, 100]`.
# 3. **Compute** — cast to `float` for consistent math, then take `sum/len`, `max`, `min`, and count marks `>= pass_mark`.
# 4. **Round `pass_rate` and `average`** to 2 decimals to match the example (`66.67`).

# ## Tests

# ```python
import pytest

def test_single_mark():
    assert analyze_marks([75]) == {
        "average": 75.0, "highest": 75.0, "lowest": 75.0, "pass_rate": 100.0
    }

def test_decimals():
    r = analyze_marks([33.3, 66.6, 99.9], 50)
    assert r["average"] == 66.6
    assert r["highest"] == 99.9
    assert r["lowest"] == 33.3
    assert r["pass_rate"] == 66.67

def test_custom_pass_mark():
    r = analyze_marks([40, 60, 80], pass_mark=70)
    assert r["pass_rate"] == 33.33  # only 80 passes

def test_example_from_prompt():
    r = analyze_marks([40, 60, 80], 50)
    assert r == {"average": 60.0, "highest": 80.0, "lowest": 40.0, "pass_rate": 66.67}

def test_empty_list():
    with pytest.raises(ValueError):
        analyze_marks([])

def test_text_value():
    with pytest.raises(ValueError):
        analyze_marks([50, "sixty"])

def test_below_zero():
    with pytest.raises(ValueError):
        analyze_marks([-1, 50])

def test_above_hundred():
    with pytest.raises(ValueError):
        analyze_marks([50, 101])

def test_bool_rejected():
    with pytest.raises(ValueError):
        analyze_marks([True, 50])

def test_invalid_pass_mark():
    with pytest.raises(ValueError):
        analyze_marks([50], pass_mark=150)
# ```

# Run with `pytest`. All tests should pass.