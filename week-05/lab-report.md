# Week 05 — Lab report

**Name:** Mahdi Jafari  
**Group:** Not provided  
**Date:** 2026-10-08

## 1. Setup

| | |
| --- | --- |
| Assistant (tool) | Copilot SDK in VS Code |
| **Exact** model name | GPT-5 (Copilot SDK) |
| Language and version | Python 3 |
| Path | A |
| My Week 04 declaration for touching bookings | allowed |

The Week 04 touching-booking declaration already agrees with AC4, which allows endpoint
touching, so no diagram change is required.

## 2. Task 1 — the plan

**The assistant's plan, pasted unedited:**

```text
1. Check the room status and reject immediately if blocked.
2. Validate that 0 <= start < end <= 1440 and that start is strictly after now.
3. Reject requests longer than 120 minutes; exactly 120 minutes is allowed.
4. Check every existing interval for a strict overlap using start < existing_end
   and end > existing_start, which allows touching endpoints.
5. Return the Boolean True only after all checks pass, without changing existing.
Assumption: non-integer times are outside the contract and are not specially handled.
Boundary cases: touching at either endpoint, exact 120 minutes, 121 minutes, start
equal to now, zero length, reversed times, day end 1440, each overlap shape, an
empty list, and an unsorted list with more than one booking.
```

**What the plan invented or changed.**

| # | What the plan said | What the contract or the AC says | What I did |
| --- | --- | --- | --- |
| 1 | Non-integer times are not specially handled. | The contract says times are integers but does not specify non-integer behavior. | Kept this as an explicit assumption and documented the resulting error behavior in §9.2. |

**Boundary cases the assistant suggested that I kept as tests:**

- Endpoint touching, overlap shapes, exact and over-two-hour durations, start equal to now,
  zero-length and reversed intervals, day bounds, empty and unsorted multiple bookings,
  and unchanged input.

## 3. Task 2 — the first version (v1), read before it was run

v1 is saved as `code/original/booking_v1.py`, exactly as the assistant returned it: yes

| # | Line in v1 | AC it implements | Correct as written? If not, why |
| --- | --- | --- | --- |
| 1 | `if blocked:` | AC3 | Yes. |
| 2 | `if not (0 <= start < end <= 1440):` | AC1 | Yes. |
| 3 | `if start <= now:` | AC1 | Yes; the request must start strictly after now. |
| 4 | `if end - start > 120:` | AC2 | Yes; 120 is allowed. |
| 5 | `if start <= b and end >= a:` | AC4 | No. The inclusive comparisons reject bookings that only touch an endpoint. |
| 6 | `return False` inside the loop | AC4 | Yes when a real overlap is found. |
| 7 | `return True` | AC5 | Yes after all checks pass. |

Anything in v1 that no AC asks for: none. It does not sort, store, log, add a buffer, or
change the return type.

## 4. Task 3 — my tests

| # | Test name | Request (start, end) | What differs from the base input | Expected | AC | Result on v1 | Result on final |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `test_touching_end_is_allowed` | (660, 720) | none | True | AC4 | False | True |
| 2 | `test_partial_overlap_over_end_is_rejected` | (630, 690) | none | False | AC4 | False | False |
| 3 | `test_partial_overlap_over_start_is_rejected` | (570, 630) | none | False | AC4 | False | False |
| 4 | `test_inside_existing_booking_is_rejected` | (615, 645) | none | False | AC4 | False | False |
| 5 | `test_containing_existing_booking_is_rejected` | (570, 690) | none | False | AC4 | False | False |
| 6 | `test_blocked_room_is_rejected` | (660, 720) | `blocked=True` | False | AC3 | False | False |
| 7 | `test_exactly_two_hours_is_allowed` | (720, 840) | none | True | AC2 | True | True |
| 8 | `test_over_two_hours_is_rejected` | (720, 841) | none | False | AC2 | False | False |
| 9 | `test_starts_now_is_rejected` | (540, 570) | none | False | AC1 | False | False |
| 10 | `test_zero_length_is_rejected` | (700, 700) | empty existing | False | AC1 | False | False |
| 11 | `test_reversed_interval_is_rejected` | (720, 700) | empty existing | False | AC1 | False | False |
| 12 | `test_day_end_is_allowed` | (1320, 1440) | empty existing | True | AC1 | True | True |
| 13 | `test_after_day_end_is_rejected` | (1320, 1441) | empty existing | False | AC1 | False | False |
| 14 | `test_empty_existing_allows_valid_request` | (600, 660) | empty existing | True | AC4 | True | True |
| 15 | `test_second_booking_is_checked` | (720, 780) | existing has two bookings | False | AC4 | False | False |
| 16 | `test_existing_input_is_unchanged` | (780, 840) | unsorted existing list | True | AC5 | True | True |

## 5. Task 4 — debugging with evidence

| # | Input (the full call) | Expected | Actual | Cause (quote the line) | Fix | Who proposed the fix |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `can_book(660, 720, 540, False, [(600, 660)])` | True | False | v1 used `if start <= b and end >= a`, so equality at the existing end counted as overlap. | Use strict comparisons: `start < b and end > a`. | Copilot SDK in VS Code, checked and accepted by me against AC4. |

**The debug prompt I sent, and the assistant's answer**

```text
The expected result is True, but I get False. Here are my code and failing test. Explain the cause and propose the smallest fix without changing the contract.

The inclusive overlap comparisons treat an endpoint touch as an overlap. Replace
start <= b and end >= a with start < b and end > a. This rejects only intervals
that share actual interior time and allows an interval ending at a or starting at b.
```

## 6. Task 5 — the critique

**The assistant's critique, pasted unedited:**

```text
1. The overlap condition uses strict comparisons, which matches AC4 because
   endpoint-touching bookings are allowed.
2. The function returns only True or False on all contract-valid inputs and never
   mutates existing.
3. The contract does not define non-integer inputs. The current implementation
   may raise TypeError for such values; that is an explicit out-of-contract
   assumption rather than a required acceptance criterion.
```

| # | Suggestion | accept / reject | Reason — cite the AC or the contract line | Suite after the change |
| --- | --- | --- | --- | --- |
| 1 | Keep strict overlap comparisons. | accept | AC4 says touching endpoints are allowed, so `start < b and end > a` is required. | 16 tests, OK |
| 2 | Do not add non-integer validation. | accept | The contract only specifies integer times and AC5 requires False for failed contract conditions; adding an exception policy would invent behavior. | 16 tests, OK |

## 7. Change log — v1 to final

| # | What changed (the line, before → after) | Why | Evidence: the test or check that moved |
| --- | --- | --- | --- |
| 1 | `start <= b and end >= a` → `start < b and end > a` | Allow endpoint-touching bookings while rejecting actual overlap. | `test_touching_end_is_allowed` changed from False on v1 to True; F7 passed. |

## 8. Evidence — real output

### 8.1 My suite, final run

```text
test_after_day_end_is_rejected (test_booking.BookingTests.test_after_day_end_is_rejected) ... ok
test_blocked_room_is_rejected (test_booking.BookingTests.test_blocked_room_is_rejected) ... ok
test_containing_existing_booking_is_rejected (test_booking.BookingTests.test_containing_existing_booking_is_rejected) ... ok
test_day_end_is_allowed (test_booking.BookingTests.test_day_end_is_allowed) ... ok
test_empty_existing_allows_valid_request (test_booking.BookingTests.test_empty_existing_allows_valid_request) ... ok
test_exactly_two_hours_is_allowed (test_booking.BookingTests.test_exactly_two_hours_is_allowed) ... ok
test_existing_input_is_unchanged (test_booking.BookingTests.test_existing_input_is_unchanged) ... ok
test_inside_existing_booking_is_rejected (test_booking.BookingTests.test_inside_existing_booking_is_rejected) ... ok
test_over_two_hours_is_rejected (test_booking.BookingTests.test_over_two_hours_is_rejected) ... ok
test_partial_overlap_over_end_is_rejected (test_booking.BookingTests.test_partial_overlap_over_end_is_rejected) ... ok
test_partial_overlap_over_start_is_rejected (test_booking.BookingTests.test_partial_overlap_over_start_is_rejected) ... ok
test_reversed_interval_is_rejected (test_booking.BookingTests.test_reversed_interval_is_rejected) ... ok
test_second_booking_is_checked (test_booking.BookingTests.test_second_booking_is_checked) ... ok
test_starts_now_is_rejected (test_booking.BookingTests.test_starts_now_is_rejected) ... ok
test_touching_end_is_allowed (test_booking.BookingTests.test_touching_end_is_allowed) ... ok
test_zero_length_is_rejected (test_booking.BookingTests.test_zero_length_is_rejected) ... ok

----------------------------------------------------------------------
Ran 16 tests in 0.001s

OK
```

### 8.2 The checker, final run

```text
PASS   F1-F10  final function checks
PASS   O1      assistant v1 is kept
PASS   S1-S2   16 tests and suite is green
PASS   M1      caught by test_starts_now_is_rejected
FAIL   M2      NOT caught - an AC1 fault passed all 16 tests
PASS   M3      caught by test_zero_length_is_rejected
PASS   M4      caught by test_day_end_is_allowed, test_exactly_two_hours_is_allowed
PASS   M5      caught by test_blocked_room_is_rejected
PASS   M6      caught by test_touching_end_is_allowed
PASS   M7      caught by test_second_booking_is_checked
PASS   M8      caught by test_containing_existing_booking_is_rejected
PASS   M9      caught by test_existing_input_is_unchanged
PASS   M10     caught by test_existing_input_is_unchanged
PASS   L1-L9   report sections are filled
SUMMARY pass=31 fail=1 error=0 (32 checks)
```

### 8.3 Path B only — three faults I planted myself

```text
Not applicable: this is Path A.
```

## 9. What still fails, and what the contract does not say

### 9.1 Checks I am keeping as FAIL or ERROR

| Check | Why it stays |
| --- | --- |
| M2 | The checker’s AC1 fault is not distinguishable with a contract-valid test: a negative start is always not strictly after valid `now` (0–1439), so AC1’s `start > now` rule rejects it even if the separate lower-bound comparison is faulty. I do not add a contradictory expected result. |

### 9.2 Outside the contract

The implementation does not specially validate non-integer inputs. For a value such as
`600.5` or `"600"`, Python comparison or arithmetic raises `TypeError`. This is
`raise-error` in `submission.yml`. The contract states that times are integers and does not
define behavior for values outside that domain, so adding a new rejection policy would be
inventing a rule rather than implementing AC1–AC5.

### 9.3 A bound that never decides

The lower bound `0 <= start` can never be the only reason for rejection when `now` is valid.
Any negative `start` is also not greater than `now`, so the separate AC1 condition `start > now`
rejects it. Therefore no contract-valid test can isolate that lower-bound comparison.

## 10. Conclusion (120–180 words)

The final code rejects an overlap when `start < b and end > a`, where `(a, b)` is an existing
booking. Both comparisons are strict because the intervals include their starts and exclude
their ends. If a new booking starts exactly at `b`, the first comparison is false; if it ends
exactly at `a`, the second comparison is false. In either case the bookings only touch and are
allowed. The fault my tests missed longest was M2, the lower-day-bound variant of AC1. A negative
start is already rejected by the required `start > now` rule because `now` is always non-negative,
so a test for the lower bound cannot isolate that fault without contradicting the contract. The
assistant’s v1 also exposed the important endpoint mistake: inclusive comparisons rejected a
booking that started at the existing end. I had to decide the behavior for non-integer inputs,
because the contract says times are integers but gives no runtime policy. I chose to leave those
out-of-contract values unhandled, resulting in Python’s TypeError, and documented that decision.
