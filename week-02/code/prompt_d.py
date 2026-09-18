# Looking at this task, I need to implement a mark analysis function with specific validation requirements. Let me identify the key points:

# **Assumptions:**
# 1. `pass_mark` should also be validated as a real number (not bool) between 0-100, since it's used in comparison
# 2. "Real number" means `int` or `float`, but explicitly **not** `bool`
# 3. For the average and pass_rate, I'll use `round()` to 2 decimal places
# 4. The pass_rate formula: `(number of marks >= pass_mark) / total_marks * 100`, rounded to 2 decimals
# 5. If `marks` is not a list (e.g., a string or None), raise `ValueError`

# Here's my implementation:

# ```python
def analyze_marks(marks, pass_mark=50):
    """
    Analyze a list of numeric marks.
    
    Args:
        marks: List of numeric marks (int or float, not bool), each 0-100 inclusive.
        pass_mark: Threshold for passing (>=), must be numeric 0-100, not bool.
    
    Returns:
        dict with keys: average, highest, lowest, pass_rate (all rounded to 2 decimals).
    
    Raises:
        ValueError: If marks is empty, not a list, contains non-numeric/boolean values,
                    or values outside [0, 100]. Also if pass_mark is invalid.
    """
    # Validate pass_mark
    if isinstance(pass_mark, bool) or not isinstance(pass_mark, (int, float)):
        raise ValueError("pass_mark must be a real number, not a boolean")
    if pass_mark < 0 or pass_mark > 100:
        raise ValueError("pass_mark must be between 0 and 100 inclusive")
    
    # Validate marks is a non-empty list
    if not isinstance(marks, list):
        raise ValueError("marks must be a list")
    if len(marks) == 0:
        raise ValueError("marks list cannot be empty")
    
    # Validate each mark
    for mark in marks:
        if isinstance(mark, bool) or not isinstance(mark, (int, float)):
            raise ValueError(f"Invalid mark: {mark!r} is not a real number")
        if mark < 0 or mark > 100:
            raise ValueError(f"Mark {mark} is out of range [0, 100]")
    
    n = len(marks)
    total = sum(marks)
    average = round(total / n, 2)
    highest = float(max(marks))
    lowest = float(min(marks))
    
    pass_count = sum(1 for m in marks if m >= pass_mark)
    pass_rate = round(pass_count / n * 100, 2)
    
    return {
        "average": average,
        "highest": highest,
        "lowest": lowest,
        "pass_rate": pass_rate,
    }
# ```

# And the required tests:

# ```python
import unittest


class TestAnalyzeMarks(unittest.TestCase):
    
    def test_case_1_standard(self):
        result = analyze_marks([40, 60, 80], 50)
        self.assertEqual(result["average"], 60.0)
        self.assertEqual(result["highest"], 80.0)
        self.assertEqual(result["lowest"], 40.0)
        self.assertEqual(result["pass_rate"], 66.67)
        self.assertEqual(set(result.keys()), {"average", "highest", "lowest", "pass_rate"})
    
    def test_case_2_single_mark(self):
        result = analyze_marks([100], 50)
        self.assertEqual(result["average"], 100.0)
        self.assertEqual(result["highest"], 100.0)
        self.assertEqual(result["lowest"], 100.0)
        self.assertEqual(result["pass_rate"], 100.0)
    
    def test_case_3_boundary_pass(self):
        result = analyze_marks([49.5, 50], 50)
        self.assertEqual(result["average"], 49.75)
        self.assertEqual(result["highest"], 50.0)
        self.assertEqual(result["lowest"], 49.5)
        self.assertEqual(result["pass_rate"], 50.0)
    
    def test_case_4_empty_list(self):
        with self.assertRaises(ValueError):
            analyze_marks([], 50)
    
    def test_case_5_string_in_list(self):
        with self.assertRaises(ValueError):
            analyze_marks([40, "60"], 50)
    
    def test_case_6_out_of_range(self):
        with self.assertRaises(ValueError):
            analyze_marks([-1, 50, 101], 50)
    
    # Additional edge-case tests
    def test_bool_rejected(self):
        with self.assertRaises(ValueError):
            analyze_marks([True, 50], 50)
        with self.assertRaises(ValueError):
            analyze_marks([50, False], 50)
    
    def test_none_rejected(self):
        with self.assertRaises(ValueError):
            analyze_marks(None, 50)
    
    def test_all_fail(self):
        result = analyze_marks([10, 20, 30], 50)
        self.assertEqual(result["pass_rate"], 0.0)
    
    def test_all_pass(self):
        result = analyze_marks([50, 60, 70], 50)
        self.assertEqual(result["pass_rate"], 100.0)
    
    def test_default_pass_mark(self):
        result = analyze_marks([40, 60, 80])
        self.assertEqual(result["pass_rate"], 66.67)
    
    def test_bool_pass_mark_rejected(self):
        with self.assertRaises(ValueError):
            analyze_marks([50, 60], True)
    
    def test_out_of_range_pass_mark(self):
        with self.assertRaises(ValueError):
            analyze_marks([50, 60], -1)
        with self.assertRaises(ValueError):
            analyze_marks([50, 60], 101)
    
    def test_rounding(self):
        # 1/3 pass rate → 33.33
        result = analyze_marks([40, 60, 80], 70)
        self.assertEqual(result["pass_rate"], 33.33)


if __name__ == "__main__":
    unittest.main()
# ```

# **Key implementation details:**

# 1. **Boolean rejection**: `isinstance(mark, bool)` is checked *before* `isinstance(mark, (int, float))` because `bool` is a subclass of `int`. Without this check, `True` would pass as `1`.

# 2. **Pass condition**: `m >= pass_mark` correctly treats 50 as passing when `pass_mark=50`, giving `pass_rate = 50.0` for `[49.5, 50]`.

# 3. **Return types**: `max()`/`min()` on a list of ints return ints; I wrap them in `float()` so `highest`/`lowest` are always floats, consistent with the worked example.

# 4. **Rounding**: `round(x, 2)` applied to both `average` and `pass_rate`. Note `round(66.666..., 2)` → `66.67`, matching the example.

# 5. **No extra keys**: The dict literal contains exactly the four required keys.

# 6. **Standard library only**: No imports needed at all for the implementation.