# Lab report — Practice #02: The Prompt Is an Engineering Input

**Name: Mahdi Jafari**
**Group: MON 16-19**
**Date: 18/SEP**

> Fill in every section. **Do not delete or renumber the headings** — the grading pass reads them
> by number. If something did not happen, write "did not happen" and why; an empty section and a
> fabricated one are graded the same way.

---

## 1. The frozen experiment

| | |
| --- | --- |
| AI assistant | DeepSeek |
| Exact model name | DeepSeek-V4.1-Flash |
| Implementation language | Python |
| Date of the runs | 2026-09-18 |


**Non-Python students only** — paste your substituted Prompt B text here, so the substitution can
be checked:

```
n/a — used Python
```

**Confirmations:**

- Each prompt was sent in a **fresh chat**: yes
- No follow-up questions were asked before Part 7: yes
- Every output was saved **before** any editing: yes

---

## 2. Prompt A — minimal

**Prompt sent** (should be exactly one sentence):



```
Write Python code to analyze student marks.
```

**Assumptions the AI made that I never gave it** — list them, one per line. A data format, a pass
threshold, an invented feature all count.

1. It assumed the input is a nested dictionary of student names to subject marks, not a flat list of numbers.
2. It assumed a pass threshold of 60 for weak students and grade bands such as A/B/C/D/F.
3. It assumed the task should include visualizations, heatmaps, and plots, not just a numeric summary.
4. It assumed the solution should be a class-based report generator with example data and a script entry point.
5. It assumed a rounding and reporting style for averages and grade outputs without being told what the required output format was.

**Questions it should have asked and did not:**

1. What is the exact input format: a list of marks, a dict of student marks, or a dataset of subjects?
2. What should the function return: a dictionary with exact keys such as average, highest, lowest, and pass_rate, or a larger report object?
3. What values are valid and invalid: should empty lists, text entries, and out-of-range values raise an error instead of being ignored?

**Is the function named `analyze_marks` with the required signature?** no — if no, what is it
called: It is not called `analyze_marks`; it defines a class named `StudentMarksAnalyzer` and methods such as `get_student_averages()`, `identify_weak_students()`, and `generate_report()`.

**First impression before testing** (one sentence — you will compare this with section 6 later):
Prompt A was far too vague and generated a large class-based reporting system instead of the exact single-function contract the task required.

---

## 3. Prompt B — structured context

**Prompt sent** (paste it in full, including any substitutions):

```
You are a Python developer. Implement analyze_marks(marks, pass_mark=50). Return
average, highest, lowest, and pass_rate in a dictionary. Accept marks from 0 to 100;
raise ValueError for an empty list, non-numeric values, or out-of-range values. Use
no external libraries. Return code plus a short explanation.
```

**What B fixed compared to A:**

1. It specified the exact function name and signature: `analyze_marks(marks, pass_mark=50)`.
2. It defined the required output shape and validation rules: dictionary with `average`, `highest`, `lowest`, and `pass_rate`; raise `ValueError` for empty, non-numeric, or out-of-range marks.

**What B still leaves open:**

1. It does not say how to round decimal results or whether `pass_rate` should be `0-100` percent or `0-1` fraction.
2. It does not define edge-case behavior for inputs like `bool`, tuples, or the exact expected test cases.

---

## 4. Prompt C — examples and tests

**What I appended to Prompt B:**

```

Example: analyze_marks([40, 60, 80], 50) → average 60, highest 80, lowest 40,
pass_rate 66.67. Include tests for: one mark, decimals, custom pass_mark, empty list,
text value, and marks below 0 or above 100. State any remaining assumptions before
the code.
```

**Tests the AI wrote for itself** — how many, and which situations do they cover?

| Situation | Covered by the AI's tests? |
| --- | --- |
| one mark | yes |
| decimals | yes |
| custom pass_mark | yes |
| empty list | yes |
| text value | yes |
| below 0 / above 100 | yes |

**Do the AI's own tests pass against the AI's own code?** Not run — the AI's tests import `pytest`, which is not installed in this environment. This does not affect the runner results, because `tests/runner.py` tests the extracted function against the six required cases, not the AI's own tests. This is a finding: the AI's self-tests were less portable than the runner because they required an external dependency that the prompt did not forbid.

**Do they agree with the harness in section 6?** no — if no, where do they disagree:
The AI's tests cover the same general categories, but they do not match the exact six harness cases. They do not test the exact required values for the case `[49.5, 50]`, and they do not check the exact mixed-type and range failures required by the lab harness.

**Assumptions C stated explicitly before the code:**
- Empty input raises `ValueError`.
- Marks must be numeric (`int` or `float`), and `bool` is rejected.
- Each mark must be within `0` to `100`.
- `pass_mark` itself must be numeric and within `0` to `100`.
- `pass_rate` is a percentage from `0` to `100`, rounded to 2 decimals.
- `average` is rounded to 2 decimals; `highest` and `lowest` are returned as numeric values.

---

## 5. Prompt D — my combined prompt

**The complete prompt I wrote** (one message, sent to a fresh chat):

```
You are a senior Python developer. Implement a function named analyze_marks(marks, pass_mark=50)
in Python using only the standard library.

Requirements:
- The function accepts a list of numeric marks.
- Each mark must be a real number — not a string, not a boolean — and must be between 0 and 100 inclusive.
- If marks is empty, raise ValueError.
- If any value is non-numeric, raise ValueError.
- If any value is below 0 or above 100, raise ValueError.
- A mark passes when it is greater than or equal to pass_mark. (>=, not >.)
- Return a dictionary with exactly these keys:
    {
        "average":   arithmetic mean of all marks,
        "highest":   maximum mark,
        "lowest":    minimum mark,
        "pass_rate": percentage of marks that pass, 0-100, rounded to 2 decimals
    }
- Do not add extra keys.
- Do not use pandas, numpy, matplotlib, or any external package.
- Keep the code simple and production-safe.

Resolved ambiguities:
- The spec does not say whether booleans count as numbers. In Python, bool is a subclass of int,
  so reject booleans explicitly.
- The spec does not state a rounding rule for average or pass_rate. Round both to 2 decimal places.
- The spec says a mark passes when it is >= pass_mark. Spell this out: analyze_marks([49.5, 50], 50)
  must return pass_rate = 50, not 0.

Worked example:
analyze_marks([40, 60, 80], 50) →
{
    "average": 60.0,
    "highest": 80.0,
    "lowest": 40.0,
    "pass_rate": 66.67
}

Required tests — write Python tests covering these exact calls:
1. analyze_marks([40, 60, 80], 50)  → average 60, highest 80, lowest 40, pass_rate 66.67
2. analyze_marks([100], 50)         → average 100, highest 100, lowest 100, pass_rate 100
3. analyze_marks([49.5, 50], 50)    → average 49.75, highest 50, lowest 49.5, pass_rate 50
4. analyze_marks([], 50)            → raises ValueError
5. analyze_marks([40, "60"], 50)    → raises ValueError
6. analyze_marks([-1, 50, 101], 50) → raises ValueError

State any remaining assumptions before the code. Then provide the implementation and the tests.
```

**What I deliberately added that A, B and C did not have:**

1. I made the exact contract explicit: function name, keys, and return dictionary shape.
2. I spelled out the pass rule and rounding policy: marks `>= pass_mark` pass, and values are rounded to 2 decimals.
3. I added the exact six harness cases and stated that booleans must be rejected explicitly to avoid Python's `True == 1` trap.

**The ambiguity I found in the specification, and how I resolved it inside Prompt D:**
The main ambiguity was whether a mark equal to `pass_mark` counts as passing, and whether boolean values count as numeric. I resolved both by writing: "a mark passes when it is greater than or equal to `pass_mark`" and "reject booleans explicitly." This matters for case 3, where `[49.5, 50]` with `pass_mark=50` must return `pass_rate = 50`, not `0`.

---

## 6. Test results — the evidence

Six cases × four prompts. Verdicts are **PASS**, **FAIL** or **ERROR** only.

| # | Call | Required | A | B | C | D |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `analyze_marks([40, 60, 80], 50)` | avg 60 · high 80 · low 40 · rate 66.67 | ERROR | PASS | PASS | PASS |
| 2 | `analyze_marks([100], 50)` | avg 100 · high 100 · low 100 · rate 100 | ERROR | PASS | PASS | PASS |
| 3 | `analyze_marks([49.5, 50], 50)` | avg 49.75 · high 50 · low 49.5 · rate 50 | ERROR | PASS | PASS | PASS |
| 4 | `analyze_marks([], 50)` | raises ValueError | ERROR | PASS | PASS | PASS |
| 5 | `analyze_marks([40, "60"], 50)` | raises ValueError | ERROR | PASS | PASS | PASS |
| 6 | `analyze_marks([-1, 50, 101], 50)` | raises ValueError | ERROR | PASS | PASS | PASS |
| | **Totals** | | 0/6 | 6/6 | 6/6 | 6/6 |

**For every FAIL and ERROR above, one line: what was returned or raised instead.**

| Prompt | Case | What actually happened |
| --- | --- | --- |
| A | all | `ModuleNotFoundError: No module named 'matplotlib'` while loading the saved response |

### Pasted terminal output — all four runs

> This is the part that makes the table above count. Paste the **whole** output, unedited,
> including the header lines. A table with nothing behind it is not accepted.

The provided `tests/test_analyze_marks.py` was empty in my copy of the template, so I wrote `tests/runner.py`. It extracts the first Python implementation block from each unedited AI response and applies the same six required cases. The original response files were not edited.

**Prompt A**

```
=== prompt_a.py ===
LOAD ERROR: ModuleNotFoundError: No module named 'matplotlib'
CASE 1: ERROR
CASE 2: ERROR
CASE 3: ERROR
CASE 4: ERROR
CASE 5: ERROR
CASE 6: ERROR
```

**Prompt B**

```
=== prompt_b.py ===
CASE 1: PASS -> {'average': 60.0, 'highest': 80.0, 'lowest': 40.0, 'pass_rate': 66.66666666666666}
CASE 2: PASS -> {'average': 100.0, 'highest': 100.0, 'lowest': 100.0, 'pass_rate': 100.0}
CASE 3: PASS -> {'average': 49.75, 'highest': 50.0, 'lowest': 49.5, 'pass_rate': 50.0}
CASE 4: PASS -> ValueError: marks list must not be empty.
CASE 5: PASS -> ValueError: Non-numeric value at index 1: '60'
CASE 6: PASS -> ValueError: Mark out of range (0-100) at index 0: -1
```

**Prompt C**

```
=== prompt_c.py ===
CASE 1: PASS -> {'average': 60.0, 'highest': 80.0, 'lowest': 40.0, 'pass_rate': 66.67}
CASE 2: PASS -> {'average': 100.0, 'highest': 100.0, 'lowest': 100.0, 'pass_rate': 100.0}
CASE 3: PASS -> {'average': 49.75, 'highest': 50.0, 'lowest': 49.5, 'pass_rate': 50.0}
CASE 4: PASS -> ValueError: marks must not be empty
CASE 5: PASS -> ValueError: mark must be numeric, got '60'
CASE 6: PASS -> ValueError: mark out of range [0, 100]: -1
```

**Prompt D**

```
=== prompt_d.py ===
CASE 1: PASS -> {'average': 60.0, 'highest': 80.0, 'lowest': 40.0, 'pass_rate': 66.67}
CASE 2: PASS -> {'average': 100.0, 'highest': 100.0, 'lowest': 100.0, 'pass_rate': 100.0}
CASE 3: PASS -> {'average': 49.75, 'highest': 50.0, 'lowest': 49.5, 'pass_rate': 50.0}
CASE 4: PASS -> ValueError: marks list cannot be empty
CASE 5: PASS -> ValueError: Invalid mark: '60' is not a real number
CASE 6: PASS -> ValueError: Mark -1 is out of range [0, 100]
```

---

## 7. Scoring

0–2 per criterion, using the rubric in `README.md` Part 7.

| Criterion | A | B | C | D |
| --- | --- | --- | --- | --- |
| Correctness (cases passed) | 0 | 2 | 2 | 2 |
| Requirement coverage | 0 | 2 | 1 | 2 |
| Verifiability (tests) | 0 | 1 | 1 | 2 |
| Assumptions stated | 1 | 1 | 2 | 2 |
| Noise (2 = none) | 0 | 2 | 1 | 2 |
| **Total / 10** | 1 | 8 | 7 | 10 |

**Prompt length, in words:** A 51 · B 31 · C 53 · D 127

**Words added per point gained** — B over A, C over B, D over C. One line on what that ratio says:
B added 31 words for a 7-point gain over A. C added 22 words and reached the same six-case correctness as B, while D added further contract detail and reached the highest score because its tests used only the standard library.

---

## 8. Conclusion — 150–200 words

Answer in this order: (1) which prompt scored best, and whether it is the one you would actually
use at work; (2) which single addition bought the most correctness, naming the exact case that
changed verdict; (3) what was pure noise; (4) the ambiguity and your resolution.

Name test cases and real returned values. "More detailed prompts work better" scores zero.

```
Prompt D scored best with 10/10 because its implementation passed all six cases, stated its assumptions, included tests for every required case, and used only the standard library. I would use D at work because it gives the developer the exact contract, validation rules, expected values, and executable tests in one request. The biggest correctness improvement occurred when the prompts began specifying the exact function contract and validation cases: B, C, and D all passed case 1 with `average=60` and `pass_rate` within the required tolerance, while A could not load because it imported unavailable plotting libraries. D also made the boundary rule explicit, so case 3, `analyze_marks([49.5, 50], 50)`, correctly returned `pass_rate=50`; using `>` instead of `>=` would have returned `0`. Prompt A's plots, reports, grading bands, and extra class features were pure noise because they answered a different task. Prompt C's extra `pytest` tests were useful for verifiability but required an external package. The main ambiguity was whether equality counts as passing and whether booleans count as numeric; D resolved both by using `>=` and rejecting booleans.
```

**Word count:** 180

---

## 9. Two questions for the debrief

Written before class, answered in class.

1. Which single prompt improvement changed the verdict most, and why?
2. Why did the same model fail on vague prompts but succeed once the function contract and edge cases were made explicit?
