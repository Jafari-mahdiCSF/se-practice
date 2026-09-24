# ```python
def analyze_marks(marks, pass_mark=50):
    """
    Analyze a list of marks and return summary statistics.

    Args:
        marks (list): A list of numeric marks, each between 0 and 100.
        pass_mark (float/int): Minimum mark to be considered a pass. Default 50.

    Returns:
        dict: {
            'average': float,
            'highest': float,
            'lowest': float,
            'pass_rate': float   # percentage of marks >= pass_mark
        }

    Raises:
        ValueError: If marks is empty, contains non-numeric values,
                    or contains values outside the 0-100 range.
    """
    if not isinstance(marks, (list, tuple)):
        raise ValueError("marks must be a list or tuple of numbers.")
    if len(marks) == 0:
        raise ValueError("marks list must not be empty.")

    cleaned = []
    for i, m in enumerate(marks):
        # Reject booleans (bool is a subclass of int in Python)
        if isinstance(m, bool) or not isinstance(m, (int, float)):
            raise ValueError(f"Non-numeric value at index {i}: {m!r}")
        if m < 0 or m > 100:
            raise ValueError(f"Mark out of range (0-100) at index {i}: {m}")
        cleaned.append(float(m))

    total = 0.0
    highest = cleaned[0]
    lowest = cleaned[0]
    passed = 0

    for m in cleaned:
        total += m
        if m > highest:
            highest = m
        if m < lowest:
            lowest = m
        if m >= pass_mark:
            passed += 1

    n = len(cleaned)
    return {
        "average": total / n,
        "highest": highest,
        "lowest": lowest,
        "pass_rate": (passed / n) * 100.0,
    }


# ---- Quick demo / self-test ----
if __name__ == "__main__":
    print(analyze_marks([45, 78, 92, 50, 33, 88]))
    # {'average': 64.333..., 'highest': 92.0, 'lowest': 33.0, 'pass_rate': 66.666...}

    for bad in ([], [101], [-1], ["80"], [None], [True, 60]):
        try:
            analyze_marks(bad)
        except ValueError as e:
            print(f"OK -> {e}")
# ```

# ### Explanation

# **Validation first, then a single pass.**
# 1. **Type & emptiness checks** — The input must be a non-empty list/tuple. `bool` is explicitly rejected because in Python `True == 1`, which would silently corrupt the stats. Non-`int`/`float` entries raise `ValueError` with the offending index.
# 2. **Range check** — Each mark must satisfy `0 <= m <= 100`; otherwise `ValueError` is raised. Valid marks are converted to `float` once so the rest of the code works with a uniform type.
# 3. **Single-pass aggregation** — Instead of calling `sum`, `max`, `min` (which would each loop separately), the loop accumulates `total`, tracks `highest`/`lowest` starting from the first element, and counts how many marks meet `pass_mark`. This is O(n) time and O(n) extra space (for the cleaned copy); you could drop the copy and validate inline for O(1) extra space.
# 4. **Results** — `average = total / n`, `pass_rate` is a percentage (`passed / n * 100`), and `highest`/`lowest` are returned as floats for consistency.

# **Edge cases handled:** empty list, non-numeric entries (`"80"`, `None`), out-of-range values (`-1`, `101`), booleans, and a custom `pass_mark` (e.g., `analyze_marks([40, 60], pass_mark=60)` yields `pass_rate = 50.0`).