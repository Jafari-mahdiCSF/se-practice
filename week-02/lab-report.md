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
n/a
```

**Confirmations:**

- Each prompt was sent in a **fresh chat**: yes / no
- No follow-up questions were asked before Part 7: yes / no
- Every output was saved **before** any editing: yes / no

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

```

**Tests the AI wrote for itself** — how many, and which situations do they cover?

| Situation | Covered by the AI's tests? |
| --- | --- |
| one mark | |
| decimals | |
| custom pass_mark | |
| empty list | |
| text value | |
| below 0 / above 100 | |

**Do the AI's own tests pass against the AI's own code?** yes / no

**Do they agree with the harness in section 6?** yes / no — if no, where do they disagree:

**Assumptions C stated explicitly before the code:**

---

## 5. Prompt D — my combined prompt

**The complete prompt I wrote** (one message, sent to a fresh chat):

```

```

**What I deliberately added that A, B and C did not have:**

1.
2.
3.

**The ambiguity I found in the specification, and how I resolved it inside Prompt D:**

---

## 6. Test results — the evidence

Six cases × four prompts. Verdicts are **PASS**, **FAIL** or **ERROR** only.

| # | Call | Required | A | B | C | D |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `analyze_marks([40, 60, 80], 50)` | avg 60 · high 80 · low 40 · rate 66.67 | | | | |
| 2 | `analyze_marks([100], 50)` | avg 100 · high 100 · low 100 · rate 100 | | | | |
| 3 | `analyze_marks([49.5, 50], 50)` | avg 49.75 · high 50 · low 49.5 · rate 50 | | | | |
| 4 | `analyze_marks([], 50)` | raises ValueError | | | | |
| 5 | `analyze_marks([40, "60"], 50)` | raises ValueError | | | | |
| 6 | `analyze_marks([-1, 50, 101], 50)` | raises ValueError | | | | |
| | **Totals** | | /6 | /6 | /6 | /6 |

**For every FAIL and ERROR above, one line: what was returned or raised instead.**

| Prompt | Case | What actually happened |
| --- | --- | --- |
| | | |
| | | |
| | | |

### Pasted terminal output — all four runs

> This is the part that makes the table above count. Paste the **whole** output, unedited,
> including the header lines. A table with nothing behind it is not accepted.

**Prompt A**

```

```

**Prompt B**

```

```

**Prompt C**

```

```

**Prompt D**

```

```

---

## 7. Scoring

0–2 per criterion, using the rubric in `README.md` Part 7.

| Criterion | A | B | C | D |
| --- | --- | --- | --- | --- |
| Correctness (cases passed) | | | | |
| Requirement coverage | | | | |
| Verifiability (tests) | | | | |
| Assumptions stated | | | | |
| Noise (2 = none) | | | | |
| **Total / 10** | | | | |

**Prompt length, in words:** A ____ · B ____ · C ____ · D ____

**Words added per point gained** — B over A, C over B, D over C. One line on what that ratio says:

---

## 8. Conclusion — 150–200 words

Answer in this order: (1) which prompt scored best, and whether it is the one you would actually
use at work; (2) which single addition bought the most correctness, naming the exact case that
changed verdict; (3) what was pure noise; (4) the ambiguity and your resolution.

Name test cases and real returned values. "More detailed prompts work better" scores zero.

```
(150–200 words)



```

**Word count:**

---

## 9. Two questions for the debrief

Written before class, answered in class.

1.
2.
