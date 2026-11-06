# Week 07 — Lab report

**Name:** Mahdi Jafari
**Group:** CSCI-2208
**Date:** 2026-11-06

Fill in every section. **Do not delete, rename or renumber the headings.** The checker and the
grader find your answers by them. You can add rows to any table, but never remove its header.

---

## 1. Setup

| | |
| --- | --- |
| Project I continue (`week-06` = my Week 06 Bolt project, `starter` = the provided starter) | week-06 |
| Bolt project link (or `not shared`, and why) | not shared — Week 06 used Cline instead of Bolt.new |
| Assistant that generated the tests (tool) | Grok |
| Exact model (with its version, or `not displayed`) | grok 4.6 |
| Where I ran the tests (Bolt terminal / my computer / Codespace) | my computer |
| Vitest version (the `RUN  v…` line of a run) | 5.1.0 |
| Test command | npx vitest run |

---

## 2. Task 1 — baseline and the booking function

**Before editing:** where did the booking decision live in the project you started from?

| | |
| --- | --- |
| File and function (or "inside the page component") | `src/availability.js`, function `decideAvailability` |
| Its inputs | A request with room, startText, endText, nowText, and the sample bookings list |
| What it returned | `{ available, headline, detail }` — Available or Unavailable plus a reason |
| How the page used it | `app.js` called `decideAvailability(readRequest())` and painted the result box |

**What I changed to extract `canBook`.** Say which file it now lives in, what you moved, and why
the behaviour did not change. Also say which file of the page now calls it. 40 words or more.

<!-- Write below this line -->

The Boolean decision now lives in `src/booking.js` as `export function canBook({ start, end, now, blocked, bookings })`. I copied the same rules that `decideAvailability` already used: blocked first, then `start < end` inside 0–1440, start after now, duration at most 120, then a strict overlap. Clock parsing and the headline/detail strings stay in `availability.js`. That file imports `canBook` and uses its return value for Available / Unavailable, so the page still goes through `decideAvailability` in `app.js` and the messages do not change.

---

## 3. Task 2 — the test plan

Default fixture: `now = 540`, `blocked = false`, `bookings = [{ start: 600, end: 660 }]`, fresh
for every test. **The Expected column comes from AC1–AC4, never from the code.** Write the
**reason** for each expected result **before** you send the generation prompt.

| ID | Candidate / changed input | Expected | AC | Reason (in your words) |
| --- | --- | --- | --- | --- |
| T01 | 660–720 (touching after) | true | AC4 | 660 is the existing end, so the intervals only meet at a point and do not share interior time. |
| T02 | 540–570 (starts now) | false | AC1 | Start must be strictly after now; 540 equals 540 so the window is not in the future. |
| T03 | 720–720 (zero duration) | false | AC1 | start < end is required; a zero-length interval is not a valid window. |
| T04 | 750–720 (reversed) | false | AC1 | End is before start, so the order 0 ≤ start < end ≤ 1440 fails. |
| T05 | 1380–1441 (past day end) | false | AC1 | 1441 is after midnight; end must be at most 1440. |
| T06 | 720–840 (120 minutes) | true | AC2 | Duration is exactly 120 minutes, which the limit still permits. |
| T07 | 720–841 (121 minutes) | false | AC2 | Duration is one minute over the 120-minute cap. |
| T08 | 570–600 (touching before) | true | AC4 | The request ends where the existing booking starts, so they only touch. |
| T09 | 630–690 (partial overlap) | false | AC4 | 630–690 sits across 660, so it shares interior minutes with 600–660. |
| T10 | 570–690 (contains booking) | false | AC4 | The request wraps the whole existing booking, which is still an overlap. |
| T11 | 615–645 (inside booking) | false | AC4 | The request sits entirely inside 600–660. |
| T12 | 600–660 (identical interval) | false | AC4 | The same interval as the existing booking is a full overlap. |
| T13 | 660–720, blocked = true | false | AC3 | A blocked room rejects every request, even one that would otherwise touch cleanly. |
| T14 | 630–690, bookings = [] | true | AC4 | With no existing bookings there is nothing to overlap, and the window is otherwise valid. |
| AC5 | an Available request — the bookings after the call equal the bookings before | true, data unchanged | AC5 | An allowed check must leave the bookings array equal to a copy taken before the call. |
| X1 | 541–571 (one minute after now) | true | AC1 | T02 rejects start equal to now; this checks the other side of that bound. |
| X2 | 720–780, bookings [{600,660},{700,760}] | false | AC4 | T01–T14 never give two existing bookings; this one overlaps the second. |

X1 and X2 are **your own two cases**: a boundary or a state that T01–T14 do not reach. Fill all
five columns.

---

## 4. Task 3 — the generation prompt and the first suite

**The prompt exactly as I sent it.** Use the deck's prompt with `[our test framework]` replaced by
`Vitest`, followed by the case table from section 3:

```text
Generate tests for the existing booking function using Vitest. Use AC1–AC6 and the reviewed case table below.

Import the real function used by the page. Keep its code unchanged. Use fixed time and fresh fixtures. Assert exact decisions and unchanged booking data.

Return the test file, run command, and AC mapping. Flag unclear requirements. We will run the tests ourselves.

Default fixture: now = 540, blocked = false, bookings = [{ start: 600, end: 660 }].

T01 660–720 touching after true AC4
T02 540–570 starts now false AC1
T03 720–720 zero duration false AC1
T04 750–720 reversed false AC1
T05 1380–1441 past day end false AC1
T06 720–840 (120 min) true AC2
T07 720–841 (121 min) false AC2
T08 570–600 touching before true AC4
T09 630–690 partial overlap false AC4
T10 570–690 contains booking false AC4
T11 615–645 inside booking false AC4
T12 600–660 identical false AC4
T13 660–720, blocked = true false AC3
T14 630–690, bookings = [] true AC4
```

**The assistant's answer: run command, AC mapping and any unclear requirements it flagged,
pasted unedited.** Its test file goes to `suites/first/` and is not pasted here:

```text
Run command: npx vitest run

AC mapping:
T01, T08, T09, T10, T11, T12, T14 -> AC4 overlap / touching
T02, T03, T04, T05 -> AC1 interval and now
T06, T07 -> AC2 duration
T13 -> AC3 blocked room

Unclear: AC2 says "longer than 120 minutes". I treated exactly 120 minutes as over the cap and set T06 to false. AC5 data preservation and extra cases were not in the fourteen-row table, so they are not in this file.

The test file is returned separately.
```

The first suite was saved to `suites/first/` **before** I changed anything in it: yes

---

## 5. Task 4 — review of the first suite

Review it **before** you run it. Look at the imports, the expected values, isolation, duplicates
and skipped tests. Make one row per decision. At least **two** rows, and each one names the kind of
weakness (the deck's table: *no exception occurred* · *expected = current output* · *only valid
requests* · *mocked booking function*, or your own) and the AC that decides it.

| # | Test or part of the suite | What is weak or wrong | Decision: accept / revise / reject | AC or reason |
| --- | --- | --- | --- | --- |
| 1 | T06 AC2: two hours, `.toBe(false)` | expected = current output: the assistant read AC2 as rejecting exactly 120 minutes | reject | AC2 rejects only duration longer than 120; 720–840 must be true |
| 2 | whole first suite | no AC5 comparison of bookings before and after an Available call | revise | AC5: copy the list, call an allowed request, then compare |
| 3 | whole first suite | only the fourteen planned rows; X1 and X2 are missing | revise | own boundaries: start = now + 1 (AC1) and two existing bookings (AC4) |

---

## 6. Task 5 — running, diagnosing, improving

### 6.1 The first run

The **real** terminal output of the first run of the first suite, pasted unedited. Include the
`RUN  v…` line and the `Tests` summary line. A build message or the assistant saying "tests pass"
is not a run.

```text
npm warn Unknown env config "devdir". This will stop working in the next major version of npm. See `npm help npmrc` for supported config options.

 RUN  v5.1.0 C:/Users/mahdi/OneDrive/Desktop/se-practice-remote-check/week-07/app

 ❯ src/booking.test.js (14 tests | 1 failed) 10ms
   ❯ canBook (14)
     × T06 AC2: two hours 5ms

⎯⎯⎯⎯⎯⎯⎯ Failed Tests 1 ⎯⎯⎯⎯⎯⎯⎯

 FAIL  src/booking.test.js > canBook > T06 AC2: two hours
AssertionError: expected true to be false // Object.is equality

- Expected
+ Received

- false
+ true

 ❯ src/booking.test.js:41:71
     39|   test("T06 AC2: two hours", () => {
     40|     const { now, blocked, bookings } = fixture();
     41|     expect(canBook({ start: 720, end: 840, now, blocked, bookings })).…
       |                                                                       ^
     42|   });
     43|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/1]⎯


 Test Files  1 failed (1)
      Tests  1 failed | 13 passed (14)
   Start at  20:28:02
   Duration  201ms (transform 50%, import 25%, tests 17%, worker 8%)
```

**Each failure, diagnosed** (the deck's table: import/runner error · assertion mismatch · result
changing per run · no tests discovered). Write `none` in the first row if nothing failed.

| Failing test | Observed failure | First check | Test repair or implementation fix? | Action taken |
| --- | --- | --- | --- | --- |
| T06 AC2: two hours | assertion mismatch: expected false, received true | compared 720–840 with AC2 | Test repair | kept canBook; changed the test to `.toBe(true)` |

### 6.2 The improvement prompt

The deck's improvement prompt exactly as sent, followed by the actual output from 6.1. Then
paste the assistant's answer, unedited:

```text
Review this test suite against AC1–AC6 and our case table. Identify incorrect expectations, weak assertions, duplicated cases, and missing boundaries.

For each proposed change, explain the requirement and the defect it could detect. Improve the tests without changing correct expectations to match buggy behavior.

Use the actual failure output below. Separate test repairs from implementation fixes.

 RUN  v5.1.0 C:/Users/mahdi/OneDrive/Desktop/se-practice-remote-check/week-07/app

 ❯ src/booking.test.js (14 tests | 1 failed) 10ms
   ❯ canBook (14)
     × T06 AC2: two hours 5ms

 Test Files  1 failed (1)
      Tests  1 failed | 13 passed (14)
```

```text
T06 is a test repair, not an implementation fix. AC2 rejects duration longer than 120 minutes, so 720–840 must stay true. Changing canBook to `>= 120` would hide M1.

Missing AC5: call an Available request (660–720) and compare bookings with JSON.stringify of a copy taken before. That would detect a check that pushed onto the list.

Missing X1: start 541 with now 540 should be true (AC1 other side of T02).
Missing X2: 720–780 against [{600,660},{700,760}] should be false (AC4, second booking).

Keep every other T01–T14 expectation. Do not mock canBook. Do not use Date.now.
```

### 6.3 The final run

The **real** output of the final suite (`booking.test.*` beside your module), after every
change and after restoring the correct code from section 7. Every test must pass. If a real defect
is still open, leave its test failing and explain it in 9.1.

```text
npm warn Unknown env config "devdir". This will stop working in the next major version of npm. See `npm help npmrc` for supported config options.

 RUN  v5.1.0 C:/Users/mahdi/OneDrive/Desktop/se-practice-remote-check/week-07/app


 Test Files  1 passed (1)
      Tests  17 passed (17)
   Start at  20:29:42
   Duration  164ms (import 41%, transform 28%, tests 16%, worker 13%, environment 1%)
```

---

## 7. Task 6 — deliberate defects

You need a reviewed, passing suite first. Then introduce **one** defect at a time in your booking
module, leave the tests unchanged, run, record, and **restore** the code. A syntax or import
error does not count as detection.

| Trial | Intentional change | Detected / Survived | Failing test ID(s) | If it survived: why, and what you added |
| --- | --- | --- | --- | --- |
| M1 | Reject duration >= 120 instead of > 120 | Detected | T06 | |
| M2 | Treat touching endpoints as an overlap | Detected | T01, T08, AC5 | |
| M3 | Remove the blocked-room rejection | Detected | T13 | |

**The run of each mutant, pasted unedited.** Paste the `Tests` summary line and the failing test
names at least:

```text
M1 — duration >= 120:

 RUN  v5.1.0 C:/Users/mahdi/OneDrive/Desktop/se-practice-remote-check/week-07/app

 ❯ src/booking.test.js (17 tests | 1 failed) 11ms
   ❯ canBook (17)
     × T06 AC2: exactly 120 minutes is allowed 6ms

 Test Files  1 failed (1)
      Tests  1 failed | 16 passed (17)
   Start at  20:28:57
   Duration  191ms (transform 40%, import 28%, tests 22%, worker 9%, environment 1%)

M2 — touching as overlap:

 RUN  v5.1.0 C:/Users/mahdi/OneDrive/Desktop/se-practice-remote-check/week-07/app

 ❯ src/booking.test.js (17 tests | 3 failed) 13ms
   ❯ canBook (17)
     × T01 AC4: touching after the existing booking 8ms
     × T08 AC4: touching before the existing booking 1ms
     × AC5: an available request leaves bookings unchanged 1ms

 Test Files  1 failed (1)
      Tests  3 failed | 14 passed (17)
   Start at  20:29:12
   Duration  200ms (transform 39%, import 28%, tests 24%, worker 8%)

M3 — no blocked check:

 RUN  v5.1.0 C:/Users/mahdi/OneDrive/Desktop/se-practice-remote-check/week-07/app

 ❯ src/booking.test.js (17 tests | 1 failed) 13ms
   ❯ canBook (17)
     × T13 AC3: blocked room 6ms

 Test Files  1 failed (1)
      Tests  1 failed | 16 passed (17)
   Start at  20:29:28
   Duration  193ms (transform 42%, import 27%, tests 23%, worker 8%)
```

All three changes reverted, and the full suite run again (section 6.3): yes

---

## 8. Task 7 — manual UI checks

Use `now = 09:00` and an existing `10:00–11:00` booking. Do them in the page in a browser. Save a
screenshot of each as `evidence/ui-1.png` … `evidence/ui-5.png`. Take **ui-4 at phone width**
(about 375 px, portrait).

| # | Action | Expected observation | AC | What I observed | Pass / Fail / Not testable |
| --- | --- | --- | --- | --- | --- |
| U1 | Check 11:00–12:00, unblocked | Available, with the fixed sample booking | AC5 | A-101, now 09:00, 11:00–12:00: green Available; list still 10:00–11:00 | Pass |
| U2 | Enable blocked, then check again | Unavailable replaces the earlier result | AC3, AC5 | Switched to B-214 (blocked); Unavailable, room is blocked; list still 14:00–16:00 | Pass |
| U3 | Clear a required input and submit | Understandable validation feedback | AC6 | Cleared Current time; message “Enter the current time as HH:MM so the check can compare with it.” | Pass |
| U4 | Use a narrow (phone) width | Controls and result remain usable | AC6 | 375×812 portrait: fields stack, Check and Available still on screen without horizontal cut-off | Pass |
| U5 | Repeat the checks on the same data | Existing bookings remain unchanged | AC5 | Second Check on A-101 11:00–12:00 still Available; list still one row 10:00–11:00; checks-this-load 5 | Pass |

---

## 9. Comparison and what still fails

### 9.1 Checks I am keeping as FAIL or ERROR

Use the same IDs as `known_fails` in `submission.yml`. Write `none` if the run is clean.

| Check | Why it stays |
| --- | --- |
| none | last checker run had no FAIL or ERROR |

### 9.2 Original and improved suites

| Measure | First suite | Improved suite |
| --- | --- | --- |
| Executed / passed / failed | 14 executed, 13 passed, 1 failed | 17 executed, 17 passed, 0 failed |
| Requirements with meaningful tests (AC IDs and gaps) | AC1–AC4 on T01–T14; no AC5; no X1/X2 | AC1–AC5; X1 (now+1) and X2 (two bookings); AC6 still only UI |
| Selected mutants detected | would miss nothing of M1 because T06 expected the mutant | M1 T06, M2 T01 T08 AC5, M3 T13, all detected |
| Accepted / revised / rejected tests | T01–T05 and T07–T14 accepted; T06 rejected; AC5/X1/X2 missing | T06 repaired to true; AC5, X1, X2 added |
| Remaining limitations | T06 would green-light M1 | invalid existing booking still unspecified; AC6 not in Vitest |

### 9.3 What no AC decides

Call your function with `bookings = [{ start: 700, end: 650 }]` (a reversed existing booking)
and a request of 660–720. What does it return? Does any AC say what it should return? (This is
the value you declare in `submission.yml` under `assumptions.invalid_existing_booking`.)

It returns true. AC4 talks about overlapping existing bookings, but it never says an existing row must itself be a valid interval. The overlap loop uses `start < booking.end && end > booking.start`. For 660–720 against 700–650 that is `660 < 650 && 720 > 700`, which is false, so the request is treated as free. I am declaring `returns-true` because that is what this `canBook` actually did when I called it, not because an AC requires it.

---

## 10. Conclusion (120–180 words)

The first suite expected T06 to fail: 720 to 840, exactly 120 minutes, was asserted false. AC2 only rejects a booking longer than 120 minutes, so that expected value was already wrong before any run. I saw it while matching each title to the plan, and the first Vitest output repeated it (expected false, received true). If I had edited canBook to reject duration greater than or equal to 120, the suite would have gone green and M1 would have been the shipped rule.

The later run of 17 passing tests shows that this canBook matches T01 to T14, the AC5 copy check, X1 and X2 on the planned numbers. It does not show that the page is safe. U5 still needed two clicks in the browser to confirm the sample 10:00–11:00 row did not grow, and M3 failed only T13. Drop T13 and a missing blocked check would walk through.

One limit stays open: a reversed existing booking `{start:700,end:650}` with request 660–720 returns true, and no AC names that result.
