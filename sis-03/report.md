# SIS #03 — Report: Smart Campus Room Availability Checker

<!-- The ONLY file you write prose in. Keep every numbered heading (## 1. … ## 13.) and every
     ### sub-heading, and the **Label:** words — the checker finds your answers by them.
     Replace every "(write here)" and "(paste here)". Delete these <!-- --> comments if you like. -->

## 1. Setup and reuse

<!-- Model: the exact model with its version, as the tool shows it ("ChatGPT" is a tool, not a
     model). If the tool does not show it, write: not displayed
     Reuse: week-05 if code/original/booking_v1.py is your Week 05 v1, copied unedited;
     week-06 if web/original/ is your Week 06 v1 export; fresh if you generated it for this SIS. -->

| Item | Value |
| --- | --- |
| Coding assistant (tool) | (write here) |
| Coding assistant model | (write here) |
| Bolt.new model | (write here) |
| Bolt project link | (write here) |
| Language | (write here) |
| Path | (write here) |
| Python v1 from | (write here) |
| Web v1 from | (write here) |

## 2. Baseline — before any new AI exchange

<!-- Written by you, without AI, before the first exchange of this SIS. Commit and push it
     first (README §2). Reusing Week 05/06 work does not exempt you: this section is new. -->

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

<!-- One row per conditional branch in code/original/booking_v1.py (your language's v1 on
     Path B). Quote the condition exactly. AC1-AC4 must all appear in the AC column. -->

| Branch in v1 (quoted) | AC | Satisfies it? | Why |
| --- | --- | --- | --- |
| (write here) | (write here) | (write here) | (write here) |
| (write here) | (write here) | (write here) | (write here) |
| (write here) | (write here) | (write here) | (write here) |
| (write here) | (write here) | (write here) | (write here) |

## 4. Prototype v1 in Bolt.new

**Prompt as sent:**

~~~~text
(paste here)
~~~~

<!-- Main generated files or components, with their path inside web/original/
     (for example src/App.tsx). At least two. -->

| Generated file or component | Path | Its role |
| --- | --- | --- |
| (write here) | (write here) | (write here) |
| (write here) | (write here) | (write here) |

**What v1 does:**

- (write here)

## 5. Test cases — executed on both artifacts

<!-- Base for every case unless the row says otherwise: now = 540, blocked = False,
     existing = [(600, 660)]. Do not change the first four columns.
     Python columns: True, False or Error (it raised) — what the call actually returned.
       T11: the result of the SECOND call. T12: n/a.
       Path A: the checker runs both of your files on T1-T11 and compares (C2, C3).
     Page columns: Available, Unavailable or Not testable — what the page actually showed.
     Never write a result you did not observe. -->

| Case | Name | Input | Expected | Python v1 | Python final | Page v1 | Page final |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | Touching | 660–720 | Available | | | | |
| T2 | Overlap | 630–690 | Unavailable | | | | |
| T3 | Blocked | 660–720, blocked | Unavailable | | | | |
| T4 | Exactly 120 min | 720–840 | Available | | | | |
| T5 | 121 min | 720–841 | Unavailable | | | | |
| T6 | Starts now | 540–570 | Unavailable | | | | |
| T7 | Reversed | 720–660 | Unavailable | | | | |
| T8 | Ends at midnight | 1380–1440 | Available | | | | |
| T9 | Past midnight | 1380–1441 | Unavailable | | | | |
| T10 | Second booking | 720–780, existing (600–660), (700–760) | Unavailable | | | | |
| T11 | Same check twice | 660–720, twice | Available | | | | |
| T12 | Narrow screen | T1 at ~375 px wide | Available | n/a | n/a | | |

## 6. Traceability

<!-- His table. Implementation / file: where the rule lives (booking.py line, a component).
     Test input: the case IDs from section 5. v1 / final actual: what those cases gave. -->

| AC | Implementation / file | Test input | Expected | v1 actual | Final actual |
| --- | --- | --- | --- | --- | --- |
| AC1 | (write here) | (write here) | (write here) | (write here) | (write here) |
| AC2 | (write here) | (write here) | (write here) | (write here) | (write here) |
| AC3 | (write here) | (write here) | (write here) | (write here) | (write here) |
| AC4 | (write here) | (write here) | (write here) | (write here) | (write here) |
| AC5 | (write here) | (write here) | (write here) | (write here) | (write here) |
| AC6 | (write here) | (write here) | (write here) | (write here) | (write here) |

## 7. Issue log

<!-- At least two, from v1 — a functional defect and a usability or code-quality issue where you
     have them. If every case passed on v1, log the preventive cleanup and say why.
     Reproduction names a case (T1-T12) or an AC. Priority: High, Medium or Low.
     Prompt / change: the focused prompt you sent, and what changed. Never "make it better". -->

| # | Issue | Reproduction | Priority | Prompt / change | Retest result |
| --- | --- | --- | --- | --- | --- |
| 1 | (write here) | (write here) | (write here) | (write here) | (write here) |
| 2 | (write here) | (write here) | (write here) | (write here) | (write here) |

**Before / after:** `evidence/before-1.png` → `evidence/after-1.png` show issue (write here)

## 8. Critique decisions

<!-- The AI's review against AC1-AC6 (stage C), claim by claim. At least three rows.
     How I verified it: the case, test or run that confirmed or refuted the claim.
     Decision: accept, reject or modify. At least one reject or modify — the reflection asks for it. -->

| # | AI claim or recommendation | How I verified it | Decision | Reason (AC or case) |
| --- | --- | --- | --- | --- |
| 1 | (write here) | (write here) | (write here) | (write here) |
| 2 | (write here) | (write here) | (write here) | (write here) |
| 3 | (write here) | (write here) | (write here) | (write here) |

## 9. Coding-agent analysis

### 9.1 The loop

<!-- One real pass through the loop from this assignment — with your assistant or with Bolt. -->

| Step | What happened in this assignment |
| --- | --- |
| User goal | (write here) |
| Model / plan | (write here) |
| Tool call | (write here) |
| Observation | (write here) |
| Next step | (write here) |
| Human review | (write here) |

### 9.2 Context, tools and permissions

<!-- At least three rows. Last column: Observed (you saw it happen) or Assumed (you infer it
     about the internals). Use both at least once. -->

| Tool | Context it used | Tools or permissions | Observed or assumed |
| --- | --- | --- | --- |
| (write here) | (write here) | (write here) | (write here) |
| (write here) | (write here) | (write here) | (write here) |
| (write here) | (write here) | (write here) | (write here) |

### 9.3 Checkpoint and dependability

**Safety checkpoint:** (write here)

**Reliability, security, responsibility:** (write here)

## 10. Reflection

<!-- 100-200 words, in your own words, no AI. Compare AI-assisted coding (the Python part) with
     vibe coding (the Bolt part); one example each of a reliability, an availability/usability and
     a security risk; why review, tool permissions and tests stay human responsibilities; one AI
     recommendation you rejected or modified, and why; what you would improve next without
     expanding the scope. -->

(write here)

## 11. Appendix A — AI exchanges

<!-- At least four. Complete prompts and complete responses, as text — never screenshots. Paste
     each inside the ~~~~ block that follows its label.
     Stage: Plan, Generate, Critique or Repair (the brief's A-D) — at least one of each.
     Source: this SIS, week-05 or week-06. Reused exchanges keep their original date.
     The Generate exchange for Python must contain your v1 exactly as it is in code/original/.
     Add B5, B6 … if you ran more. -->

### B1

- **Tool:** (write here)
- **Model:** (write here)
- **Date:** (write here)
- **Stage:** (write here)
- **Source:** (write here)

**Prompt:**

~~~~text
(paste here)
~~~~

**Response:**

~~~~text
(paste here)
~~~~

### B2

- **Tool:** (write here)
- **Model:** (write here)
- **Date:** (write here)
- **Stage:** (write here)
- **Source:** (write here)

**Prompt:**

~~~~text
(paste here)
~~~~

**Response:**

~~~~text
(paste here)
~~~~

### B3

- **Tool:** (write here)
- **Model:** (write here)
- **Date:** (write here)
- **Stage:** (write here)
- **Source:** (write here)

**Prompt:**

~~~~text
(paste here)
~~~~

**Response:**

~~~~text
(paste here)
~~~~

### B4

- **Tool:** (write here)
- **Model:** (write here)
- **Date:** (write here)
- **Stage:** (write here)
- **Source:** (write here)

**Prompt:**

~~~~text
(paste here)
~~~~

**Response:**

~~~~text
(paste here)
~~~~

## 12. Appendix B — Test output

### 12.1 Your suite

<!-- The complete terminal output of your final suite. Path A: python -m unittest -v, run inside
     code/ — the part ending in "Ran N tests" and OK or FAILED. -->

~~~~text
(paste here)
~~~~

### 12.2 Path B only — three faults you planted

<!-- Path A: leave this table as it is. Path B: three rows — the line you broke, the AC it
     breaks, the test that failed. -->

| # | Line you broke | AC | Test that failed |
| --- | --- | --- | --- |
| 1 | | | |
| 2 | | | |
| 3 | | | |

## 13. Remaining limitations and known fails

<!-- One row per check ID in submission.yml known_fails, and any limitation you know of.
     If the checker is clean and you know of none, one row that says so. -->

| Check ID or limitation | Why it stays | What I would do next |
| --- | --- | --- |
| (write here) | (write here) | (write here) |
