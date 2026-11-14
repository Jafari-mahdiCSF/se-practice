# SIS #03 — Report: Smart Campus Room Availability Checker

## 1. Setup and reuse

| Item | Value |
| --- | --- |
| Coding assistant (tool) | Grok |
| Coding assistant model | grok 4.6 |
| Bolt.new model | not displayed |
| Bolt project link | not-shared |
| Language | python |
| Path | A |
| Python v1 from | week-05 |
| Web v1 from | week-06 |

## 2. Baseline — before any new AI exchange

### 2.1 Scope in my own words

**Scope:** One page and one Python function that only check whether a student can use a room in a chosen window. The room is already selected. Bookings on the page are made-up sample data. The check never creates, saves or confirms a booking. Login, a database, a backend, an external API and payments are out of scope.

### 2.2 The acceptance criteria in my own words

| AC | In my own words |
| --- | --- |
| AC1 | Start and end are whole minutes after midnight. Start is less than end, both sit in 0 to 1440, and start is strictly later than the given current time. |
| AC2 | The window may be at most 120 minutes long. A window of exactly 120 minutes is still allowed. |
| AC3 | If the selected room is marked blocked, every request for that room is refused. |
| AC4 | A request that shares interior time with any existing booking is refused. Two intervals that only meet at an endpoint are not an overlap. |
| AC5 | The answer is a clear Available or Unavailable (True or False in Python). Existing bookings are not changed by the check. |
| AC6 | Invalid input gets a readable reason. The page stays usable on a narrow phone-width layout. |

### 2.3 Likely failure points

| # | Failure point | AC | How I will check it |
| --- | --- | --- | --- |
| 1 | Treating a touch at an endpoint as overlap, so 660-720 against (600, 660) is refused | AC4 | Call can_book(660, 720, 540, False, [(600, 660)]) and enter 11:00-12:00 after 10:00-11:00 on the page (T1) |
| 2 | Allowing a window that starts at the supplied now, so 540-570 is accepted | AC1 | Call can_book(540, 570, 540, False, [(600, 660)]) and set current time 09:00 with start 09:00 on the page (T6) |

### 2.4 The contract

| Parameter | Meaning | Type and allowed values |
| --- | --- | --- |
| `start` | Candidate start, minutes after midnight | integer; must satisfy 0 <= start < end |
| `end` | Candidate end, minutes after midnight | integer; must satisfy start < end <= 1440 |
| `now` | Current time used for the "strictly after now" rule | integer, assumed valid in 0-1439 |
| `blocked` | Whether the selected room rejects every request | boolean True or False |
| `existing` | Bookings already on that room, each a (start, end) pair | collection of integer pairs; not mutated |
| returns | Whether the request is allowed | boolean True only when AC1-AC4 all hold, else False |

### 2.5 Initial assumptions and manual checks

**Assumptions:**

1. Times on the contract are integers; non-integer values are outside the contract and need no extra policy.
2. Intervals include their start minute and exclude their end minute, which is why touching at an endpoint is allowed.
3. `now` is already valid (0-1439), so the function does not re-validate it.

**Checked manually:**

- I will walk every if-branch in the first Python version against AC1-AC4 before I trust a generated True or False.
- I will run T1 and T6 by hand on both the function and the page so endpoint-touch and starts-now are not only assumed.

## 3. Python v1 review

| Branch in v1 (quoted) | AC | Satisfies it? | Why |
| --- | --- | --- | --- |
| `if blocked:` | AC3 | Yes | Any True blocked value returns False before times are even read. |
| `if not (0 <= start < end <= 1440):` | AC1 | Yes | Zero-length, reversed, negative start and end after 1440 all fail this chain. |
| `if start <= now:` | AC1 | Yes | Start equal to now is refused, so the start must be strictly after now. |
| `if end - start > 120:` | AC2 | Yes | 121 minutes is refused; 120 minutes does not enter this branch. |
| `if start <= b and end >= a:` | AC4 | No | Equality at an endpoint counts as overlap, so T1 (660-720 against 600-660) returns False. |
| `return True` | AC5 | Yes | After the checks pass, the function returns a Boolean and never writes into `existing`. |

## 4. Prototype v1 in Bolt.new

**Prompt as sent:**

~~~~text
Build a small responsive Smart Campus Room Availability Checker. Requirements:
AC1: Accept a candidate interval only when 0 <= start < end <= 1440 and start is after the supplied current time.
AC2: Reject a booking longer than 120 minutes.
AC3: Reject the request when the selected room is blocked.
AC4: Reject any interval that overlaps an existing booking; touching endpoints are allowed.
AC5: Show a clear Available / Unavailable decision without changing the existing booking data.
AC6: The page remains usable at desktop and narrow/mobile width and gives understandable validation feedback.
Use fictional sample data only. Keep the implementation simple and within one-page scope. Do not add authentication, backend services, analytics, or unrelated features. After building, briefly list the main files/components you created.
~~~~

| Generated file or component | Path | Its role |
| --- | --- | --- |
| Page shell | index.html | Room select, start and end time inputs, Check availability, Book this slot, result box and bookings list |
| First-version logic | app.js | Sample rooms and bookings, overlap check, localStorage read/write, Check that appends a hold |

**What v1 does:**

- Shows A-101 with one sample booking 10:00-11:00 and answers Available for 11:00-12:00 on the first check (T1).
- Does not compare start with a supplied now, does not read `blocked`, writes the checked window into bookings and localStorage, and uses a fixed 960 px column.

## 5. Test cases — executed on both artifacts

| Case | Name | Input | Expected | Python v1 | Python final | Page v1 | Page final |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | Touching | 660–720 | Available | False | True | Available | Available |
| T2 | Overlap | 630–690 | Unavailable | False | False | Unavailable | Unavailable |
| T3 | Blocked | 660–720, blocked | Unavailable | False | False | Available | Unavailable |
| T4 | Exactly 120 min | 720–840 | Available | True | True | Available | Available |
| T5 | 121 min | 720–841 | Unavailable | False | False | Unavailable | Unavailable |
| T6 | Starts now | 540–570 | Unavailable | False | False | Not testable | Unavailable |
| T7 | Reversed | 720–660 | Unavailable | False | False | Available | Unavailable |
| T8 | Ends at midnight | 1380–1440 | Available | True | True | Not testable | Available |
| T9 | Past midnight | 1380–1441 | Unavailable | False | False | Not testable | Not testable |
| T10 | Second booking | 720–780, existing (600–660), (700–760) | Unavailable | False | False | Available | Unavailable |
| T11 | Same check twice | 660–720, twice | Available | False | True | Unavailable | Available |
| T12 | Narrow screen | T1 at ~375 px wide | Available | n/a | n/a | Available | Available |

Python columns are what `can_book` actually returned when the checker and a direct call ran `code/original/booking_v1.py` and `code/booking.py`. Page columns are what the browser showed: v1 at `web/original/index.html`, final at `web/final/index.html`. T8 on the final page used the "ends at 24:00" checkbox. T9 on both pages cannot be typed into `<input type="time">` (the control stops at 23:59).

## 6. Traceability

| AC | Implementation / file | Test input | Expected | v1 actual | Final actual |
| --- | --- | --- | --- | --- | --- |
| AC1 | booking.py lines 5-8; final `decideAvailability` order and now field | T6, T7, T8, T9 | T6/T7/T9 Unavailable, T8 Available | Python T6-T9 correct; page T6 Not testable, T7 Available | Python correct; page T6/T7 Unavailable, T8 Available, T9 Not testable |
| AC2 | booking.py lines 9-10; availability.js duration check | T4, T5 | T4 Available, T5 Unavailable | Both artifacts matched | Both artifacts matched |
| AC3 | booking.py lines 3-4; room.blocked in availability.js | T3 | Unavailable | Python False; page Available (flag unused) | Python False; page Unavailable on B-214 |
| AC4 | booking.py overlap `start < b and end > a`; clash test in availability.js | T1, T2, T10 | T1 Available, T2/T10 Unavailable | Python T1 False; page T10 Available | Python and page matched expected |
| AC5 | booking.py returns bool and does not write existing; final check does not push bookings | T11 | Available twice, list unchanged | Python False; page Unavailable and a second row 11:00-12:00 | Python True twice; page Available twice, still one booking |
| AC6 | web/final/styles.css `@media (max-width: 700px)` and result-detail text | T7, T12 | Readable reason; T1 still Available at ~375 px | v1 960 px column, "Not available for this slot" only | Stacked fields, Available on T12, reversed times named |

## 7. Issue log

| # | Issue | Reproduction | Priority | Prompt / change | Retest result |
| --- | --- | --- | --- | --- | --- |
| 1 | Check availability appends the window to bookings and localStorage, so the second identical check is refused | T11 / AC5: A-101, 11:00-12:00, Check, then Check again without reload | High | Choosing 11:00-12:00 and pressing Check twice gives Available, then Unavailable; AC5 says the data stays unchanged. Make the smallest change that fixes this: remove the Book button, remove localStorage, and do not push the tested window into the list. | Second check stayed Available; bookings list still only 10:00-11:00; checks-this-load counter went 1 then 2 |
| 2 | A-101 has only (600, 660), so T10 (720-780 against a second booking 700-760) cannot be set up, and v1 never asks for now | T10 / AC4 and T6 / AC1 | Medium | T10 needs existing (600, 660) and (700, 760) on the same room without saving anything. Add an in-memory sample-bookings selector (standard vs two bookings) and a current-time field that decideAvailability uses. Do not add storage or a Book action. | Two-booking fixture made 12:00-13:00 Unavailable; now 09:00 and start 09:00 answered Unavailable |

**Before / after:** evidence/before-1.png and evidence/after-1.png show issue 1, the T11 mutation when Check is pressed twice

## 8. Critique decisions

| # | AI claim or recommendation | How I verified it | Decision | Reason (AC or case) |
| --- | --- | --- | --- | --- |
| 1 | Python v1 rejects T1 because `start <= b and end >= a` treats a touch as overlap | Ran can_book(660, 720, 540, False, [(600, 660)]) on booking_v1.py; it returned False | accept | AC4 says touching at an endpoint is not overlap; T1 expected Available |
| 2 | Add a Book button and persist the accepted slot so the student can confirm | Read AC5 and the exclusions in section 1 of the brief; v1 already did this and T11 failed | reject | The page must only check availability; login, storage and confirm are excluded |
| 3 | The final page should refuse every request when the selected room is blocked | Chose B-214 on the final page, 11:00-12:00, now 09:00; headline Unavailable | accept | AC3; T3 expected Unavailable |
| 4 | Shorten the maximum duration from 120 minutes to 90 minutes to leave a cleaning gap | Compared with AC2; T4 is 720-840 and must stay Available | reject | AC2 permits exactly 120 minutes; a cleaning buffer would change the contract |

## 9. Coding-agent analysis

### 9.1 The loop

| Step | What happened in this assignment |
| --- | --- |
| User goal | Repair T11: the second Check on 11:00-12:00 must stay Available and must not add a booking |
| Model / plan | grok 4.6 proposed removing the push into `bookings`, deleting localStorage, and keeping one Check button |
| Tool call | Files under `web/final/` were edited (`index.html`, `src/app.js`, `src/data.js`) and the page was opened in Chrome |
| Observation | First Check: Available, still one list row. Second Check: Available, still one list row, checks-this-load = 2 |
| Next step | Added the sample-bookings selector so T10 could be run, then reran T1-T12 |
| Human review | Confirmed no fetch, localStorage, login or Book control remained in `web/final/` source |

### 9.2 Context, tools and permissions

| Tool | Context it used | Tools or permissions | Observed or assumed |
| --- | --- | --- | --- |
| Grok 4.6 | Week 05 v1, Week 06 original, AC1-AC6, T1-T12 | Read and write files in `sis-03/`; run `python -m unittest` | Observed |
| Local Python 3 | `code/booking.py` and `code/test_booking.py` | Process that imports can_book and prints Ran 32 tests OK | Observed |
| Bolt.new / Cline (week-06 v1) | The deck prompt with AC1-AC6 | Generated `index.html`, `app.js`, `styles.css` without a signed-in Bolt session | Assumed |
| Chrome at 375x812 | Final `index.html` after the T11 fix | Device metrics override to take `final-narrow.png` | Observed |

### 9.3 Checkpoint and dependability

**Safety checkpoint:** Before I accept a generated change I rerun the named case (here T11) on the real page, grep the final source for localStorage, fetch and login, and refuse any patch that creates a booking or talks to a network.

**Reliability, security, responsibility:** Reliability is the same True or False on a second call. Security here is the absence of storage, login and network calls in a checker that only uses fictional data. Those properties are not guaranteed by the model; I am responsible for the tests, the grep, and the decision to reject a Book button.

## 10. Reflection

AI-assisted coding on `can_book` was easier to pin down than vibe coding the page. One overlap line in v1 made T1 False; a unit test named the fault. The page hid several faults at once: no now field, unused blocked flag, a Book button and localStorage. Reliability risk: an inclusive overlap check that looks correct until T1. Usability risk: v1's 960 px column, which forced sideways scroll at 375 px. Security risk: v1 wrote bookings to localStorage, which is persistence the scope forbids. Code review, tool permissions and tests stay human work because the model will still invent a confirm step. I rejected the recommendation to add a Book button and a 90-minute cap; AC2 and AC5 already fix those rules. Next I would only tighten the T9 message that 24:01 cannot be typed, still inside one page.

## 11. Appendix A — AI exchanges

### B1

- **Tool:** Grok
- **Model:** grok 4.6
- **Date:** 2026-10-31
- **Stage:** Plan
- **Source:** this SIS

**Prompt:**

~~~~text
Plan the SIS 03 Path A work for can_book(start, end, now, blocked, existing) and the one-page availability checker. Reuse Week 05 Python v1 and Week 06 page v1 unchanged. List the AC1-AC4 checks, assumptions, T1-T12 boundary tests, and the two repairs I should make so the final page differs from v1 without adding login, backend or database. Do not invent a Book button or a cleaning buffer.
~~~~

**Response:**

~~~~text
Plan for SIS 03, Path A, reusing the Week 05 function v1 and the Week 06 page v1.

Checks, in this order:
1. If blocked is True, return False (AC3).
2. Require 0 <= start < end <= 1440 and start strictly greater than now (AC1).
3. Require end - start <= 120; exactly 120 is allowed (AC2).
4. Reject overlap with any pair (a, b) in existing using start < b and end > a so a touch at an endpoint is allowed (AC4).
5. Return True or False and never mutate existing (AC5).

Assumptions: times are integers; now is already in 0-1439; intervals include start and exclude end.

Boundary tests to keep: T1 touching 660-720; T2 overlap; T3 blocked; T4 720-840; T5 720-841; T6 start == now; T7 reversed; T8 1380-1440; T9 1380-1441; T10 second booking 700-760; T11 same call twice; T12 T1 at about 375 px.

Week 05 v1 will fail T1 because it uses start <= b and end >= a. Keep that file unedited. The final function should use strict inequalities.

Two repairs on the page, both in scope:
- Stop Check from pushing into bookings and localStorage (T11 / AC5).
- Add a current-time field and an in-memory sample-data switch so T6 and T10 can be run (AC1 / AC4). No login, backend, database, or Book control.
~~~~

### B2

- **Tool:** Copilot SDK in VS Code
- **Model:** GPT-5 (Copilot SDK)
- **Date:** 2026-10-08
- **Stage:** Generate
- **Source:** week-05

**Prompt:**

~~~~text
Implement can_book(start, end, now, blocked, existing) in Python using only the standard library. Return True only when AC1-AC4 all hold. AC1: 0 <= start < end <= 1440 and start strictly after now. AC2: duration at most 120 minutes, exactly 120 allowed. AC3: blocked rooms reject every request. AC4: overlap is rejected; touching at an endpoint is not overlap. Do not mutate existing. Save this first version unedited.
~~~~

**Response:**

~~~~text
Here is a first version of can_book. It rejects a blocked room, checks the day bounds and order, requires start after now, caps duration at 120 minutes, and treats any shared endpoint as overlap.

def can_book(start, end, now, blocked, existing):
    """Return whether the booking request is allowed."""
    if blocked:
        return False
    if not (0 <= start < end <= 1440):
        return False
    if start <= now:
        return False
    if end - start > 120:
        return False
    for a, b in existing:
        if start <= b and end >= a:
            return False
    return True

I assumed non-integer times are outside the contract. Suggested tests: touching at either endpoint, exact 120 minutes, 121 minutes, start equal to now, zero length, reversed times, day end 1440, each overlap shape, an empty list, and an unsorted list with more than one booking.
~~~~

### B3

- **Tool:** Grok
- **Model:** grok 4.6
- **Date:** 2026-10-31
- **Stage:** Critique
- **Source:** this SIS

**Prompt:**

~~~~text
Review the Python function in code/booking.py and code/original/booking_v1.py and the pages in web/original and web/final against AC1-AC6 only. Do not change the meaning of the criteria. For each claim, name the AC or the case. Suggest concrete repairs if a rule fails. Do not add login, payments, a backend or a Book confirm step unless you argue it from an AC, which I will then reject if it is out of scope.
~~~~

**Response:**

~~~~text
Python v1 fails AC4 on T1: the condition start <= b and end >= a rejects 660-720 against (600, 660). The final function uses start < b and end > a and T1 returns True. Duration, blocked, reversed times and 1440/1441 behave as AC1-AC3 require on the final function.

The original page fails several criteria at once. Check availability pushes the tested window into bookings and localStorage, so T11 becomes Unavailable (AC5). The blocked flag on B-214 is never read, so T3 shows Available (AC3). There is no current-time field, so T6 is not testable (AC1). Reversed 12:00-11:00 is answered Available (AC1). The layout is a 960 px column (AC6). The Book this slot button confirms a booking, which the story forbids.

I recommend adding a Book button and persisting the accepted slot so the student can confirm, and shortening the maximum from 120 minutes to 90 minutes to leave a cleaning gap. I also recommend refusing every request when the selected room is blocked, which the final page already does on B-214.

Those last two product ideas (Book, 90 minutes) are extra. AC2 allows 120 minutes. AC5 forbids mutating existing bookings. Keep the checker as a checker.
~~~~

### B4

- **Tool:** Grok
- **Model:** grok 4.6
- **Date:** 2026-10-31
- **Stage:** Repair
- **Source:** this SIS

**Prompt:**

~~~~text
Choosing 11:00-12:00 and pressing Check twice gives Available, then Unavailable; AC5 says the data stays unchanged. Make the smallest change that fixes this: remove the Book button, remove localStorage, and do not push the tested window into the list. Preserve AC1-AC4. Name the files you change.
~~~~

**Response:**

~~~~text
Changed web/final/index.html and web/final/src/app.js (and dropped the storage helpers that lived in the v1 app.js). Check availability now only calls decideAvailability and paints Available or Unavailable. It does not push into SAMPLE_BOOKINGS. There is no Book button and no localStorage key. A small checks-this-load counter is display-only. Retest T11: first Check Available, second Check Available, bookings list still 10:00-11:00. T1 remains Available because the clash test still uses start < end of the existing booking.
~~~~

### B5

- **Tool:** Grok
- **Model:** grok 4.6
- **Date:** 2026-10-31
- **Stage:** Repair
- **Source:** this SIS

**Prompt:**

~~~~text
T10 needs existing (600, 660) and (700, 760) on the same room without saving anything. Add an in-memory sample-bookings selector (standard vs two bookings) and a current-time field that decideAvailability uses. Do not add storage or a Book action. Keep AC1-AC6. Name the files you change.
~~~~

**Response:**

~~~~text
Changed web/final/index.html, web/final/src/data.js and web/final/src/app.js. SAMPLE_STANDARD keeps A-101 at 10:00-11:00. SAMPLE_TWO_ON_A101 adds 11:40-12:40 (700-760). The selector copies that array in memory only. The now field is required by decideAvailability. Retest: T6 with now 09:00 and start 09:00 is Unavailable. T10 with the two-booking fixture and 12:00-13:00 is Unavailable because it overlaps 11:40-12:40. T1 on the standard fixture is still Available.
~~~~

## 12. Appendix B — Test output

### 12.1 Your suite

~~~~text
test_after_day_end_is_rejected (test_booking.BookingTests.test_after_day_end_is_rejected) ... ok
test_blocked_room_is_rejected (test_booking.BookingTests.test_blocked_room_is_rejected) ... ok
test_blocked_room_with_no_bookings_is_rejected (test_booking.BookingTests.test_blocked_room_with_no_bookings_is_rejected) ... ok
test_containing_existing_booking_is_rejected (test_booking.BookingTests.test_containing_existing_booking_is_rejected) ... ok
test_day_end_is_allowed (test_booking.BookingTests.test_day_end_is_allowed) ... ok
test_empty_existing_allows_valid_request (test_booking.BookingTests.test_empty_existing_allows_valid_request) ... ok
test_exactly_two_hours_is_allowed (test_booking.BookingTests.test_exactly_two_hours_is_allowed) ... ok
test_existing_input_is_unchanged (test_booking.BookingTests.test_existing_input_is_unchanged) ... ok
test_fits_exactly_between_two_bookings (test_booking.BookingTests.test_fits_exactly_between_two_bookings) ... ok
test_free_slot_among_three_is_allowed (test_booking.BookingTests.test_free_slot_among_three_is_allowed) ... ok
test_identical_to_existing_booking_is_rejected (test_booking.BookingTests.test_identical_to_existing_booking_is_rejected) ... ok
test_inside_existing_booking_is_rejected (test_booking.BookingTests.test_inside_existing_booking_is_rejected) ... ok
test_negative_start_is_rejected (test_booking.BookingTests.test_negative_start_is_rejected) ... ok
test_now_zero_start_one_is_allowed (test_booking.BookingTests.test_now_zero_start_one_is_allowed) ... ok
test_now_zero_start_zero_is_rejected (test_booking.BookingTests.test_now_zero_start_zero_is_rejected) ... ok
test_one_minute_duration_is_allowed (test_booking.BookingTests.test_one_minute_duration_is_allowed) ... ok
test_over_two_hours_is_rejected (test_booking.BookingTests.test_over_two_hours_is_rejected) ... ok
test_partial_overlap_over_end_is_rejected (test_booking.BookingTests.test_partial_overlap_over_end_is_rejected) ... ok
test_partial_overlap_over_start_is_rejected (test_booking.BookingTests.test_partial_overlap_over_start_is_rejected) ... ok
test_rejected_request_leaves_existing_unchanged (test_booking.BookingTests.test_rejected_request_leaves_existing_unchanged) ... ok
test_result_is_real_boolean_false (test_booking.BookingTests.test_result_is_real_boolean_false) ... ok
test_result_is_real_boolean_true (test_booking.BookingTests.test_result_is_real_boolean_true) ... ok
test_reversed_interval_is_rejected (test_booking.BookingTests.test_reversed_interval_is_rejected) ... ok
test_same_check_twice_stays_allowed (test_booking.BookingTests.test_same_check_twice_stays_allowed) ... ok
test_second_booking_is_checked (test_booking.BookingTests.test_second_booking_is_checked) ... ok
test_starts_in_the_past_is_rejected (test_booking.BookingTests.test_starts_in_the_past_is_rejected) ... ok
test_starts_now_is_rejected (test_booking.BookingTests.test_starts_now_is_rejected) ... ok
test_starts_one_minute_after_now_is_allowed (test_booking.BookingTests.test_starts_one_minute_after_now_is_allowed) ... ok
test_touching_end_is_allowed (test_booking.BookingTests.test_touching_end_is_allowed) ... ok
test_touching_start_is_allowed (test_booking.BookingTests.test_touching_start_is_allowed) ... ok
test_unsorted_existing_is_checked (test_booking.BookingTests.test_unsorted_existing_is_checked) ... ok
test_zero_length_is_rejected (test_booking.BookingTests.test_zero_length_is_rejected) ... ok

----------------------------------------------------------------------
Ran 32 tests in 0.001s

OK
~~~~

### 12.2 Path B only — three faults you planted

| # | Line you broke | AC | Test that failed |
| --- | --- | --- | --- |
| 1 | | | |
| 2 | | | |
| 3 | | | |

## 13. Remaining limitations and known fails

| Check ID or limitation | Why it stays | What I would do next |
| --- | --- | --- |
| T9 on the page | `<input type="time">` stops at 23:59, so 1441 cannot be entered; C4 allows Not testable for T8/T9 | Keep the 24:00 checkbox for T8; do not invent a second-day field |
| Python v1 T1 and T11 | Inclusive overlap in booking_v1.py, kept unedited as required | Leave v1; the final function uses strict comparisons |
| Page v1 T3, T6, T7, T10, T11 | First export from Week 06, kept unedited | Leave original/; the final page is the repaired one |
