# Week 06 — Lab report

**Name:** Mahdi Jafari
**Group:** CSCI-2208
**Date:** 18 October 2026

Fill in every section. **Do not delete, rename or renumber the headings** — the checker and the
grader find your answers by them. Add rows to any table; never remove its header.

---

## 1. Setup

| | |
| --- | --- |
| Tool | Cline (AI coding agent inside VS Code) — used instead of Bolt.new, see the last row |
| Exact model (as Bolt shows it, or `not displayed`) | not displayed — the Cline session shows no model name, so I did not invent one |
| Bolt project link (or `not shared`, and why) | not shared — no Bolt project exists: I could not reach Bolt.new from this machine (no signed-in browser session), so nothing was generated there |
| Browser and version | Google Chrome 155.0.8059.80, driven headless at 1280×900 (desktop) and 375×812 (T9) |
| If you could not use Bolt.new: the tool you used instead, and why | Cline, an AI coding agent in VS Code. Bolt.new needs an interactive signed-in browser account, which this environment cannot open; Cline accepted the same three deck prompts unchanged and its first output was saved unedited in `original/`. `submission.yml` → `assistant.fallback_reason` says the same. |

---

## 2. Task 1 — define before generating

**Two predictions, written BEFORE you send the first prompt.** Where do you expect v1 to go wrong?
Fill the first three columns now; fill the last one after Task 3.

| # | What I expect to go wrong | AC it concerns | Was I right? (after Task 3) |
| --- | --- | --- | --- |
| 1 | The page will read the machine clock and give me no field to supply "now", so a slot that starts exactly at the supplied current time (T6) can be neither set up nor rejected. | AC1 | |
| 2 | An app builder usually adds a confirm/book step, so the check itself will add the requested interval to the booking list; the second identical check in T8 will then see a clash and answer Unavailable. | AC5 | |

**The initial prompt exactly as I sent it** — the deck's prompt with AC1–AC6 pasted in place of
`[paste AC1–AC6]`, nothing else changed:

```text
Build a small responsive Smart Campus Room Availability Checker. Requirements:
AC1: Accept a candidate interval only when 0 <= start < end <= 1440 and start is after the supplied current time.
AC2: Reject a booking longer than 120 minutes.
AC3: Reject the request when the selected room is blocked.
AC4: Reject any interval that overlaps an existing booking; touching endpoints are allowed.
AC5: Show a clear Available / Unavailable decision without changing the existing booking data.
AC6: The page remains usable at desktop and narrow/mobile width and gives understandable validation feedback.
Use fictional sample data only. Keep the implementation simple and within one-page scope. Do not add authentication, backend services, analytics, or unrelated features. After building, briefly list the main files/components you created.
```

---

## 3. Task 2 — prototype v1

v1 export saved in `original/` and screenshot saved as `evidence/v1.png` **before** any cleanup
prompt: yes

**The builder's list of the files/components it created, pasted unedited:**

```text
Created 3 files, no build step and no dependencies:
- index.html  - page shell: room <select>, start and end <input type="time">, "Check availability"
                and "Book this slot" buttons, a result box and a bookings list
- styles.css  - one white panel layout in a fixed 960 px container
- app.js      - ROOMS (3 fictional rooms, B-214 flagged blocked: true) and SAMPLE_BOOKINGS
                (A-101 10:00-11:00, C-305 13:00-14:00); toMinutes(), toClock(), bookingsFor(),
                checkAvailability(), bookSlot(), renderRooms(), renderBookings();
                bookings are read from and written to localStorage key "smart-campus-bookings"
```

**What v1 does — one line per thing that works, or visibly does not:**

- Works: 11:00–12:00 against the only booking 10:00–11:00 answers "Available - 11:00 to 12:00" — touching endpoints are allowed (T1).
- Works: 10:30–11:30 answers "Not available for this slot." (T2, AC4).
- Works: 12:00–14:00 is accepted and 12:00–14:01 is refused, so the 120-minute rule is there (T4, T5, AC2).
- Does not work: the room list never shows or uses the `blocked` flag, so the blocked room B-214 answers "Available" (T3, AC3).
- Does not work: 12:00–11:00 answers "Available - 12:00 to 11:00" — the interval is never checked for order (T7, AC1).
- Does not work: there is no field for the current time and no comparison with "now" anywhere in `app.js` (T6, AC1 — not testable).
- Does not work: the Check button appends the interval to the booking list and writes localStorage, so the second identical check answers "Not available for this slot." (T8, AC5).
- Does not work: the layout is a fixed 960 px column, so at 375 px the title, the end-time field and the bookings are cut off and the page scrolls sideways (T9, AC6).
- Out of scope: the "Book this slot" button and the localStorage persistence both save/confirm a booking, which the scope forbids; the checker reports "browser storage" under `original/`.

**Repair prompt** (only if the first build did not run — the deck allows one, then the result is
v1). Leave empty if you did not need it:

```text
```

---

## 4. Task 3 — the nine cases

Base for every case unless the row says otherwise: **current time 09:00**, room **not blocked**,
the room's **only booking 10:00–11:00**. The Expected column comes from AC1–AC6 — do not change it.
Write each result exactly as **Available**, **Unavailable** or **Not testable** (the page gives you
no way to set up the case). Save each final run as `evidence/final-T<n>.png`.

| # | Case | What you set up and request | Expected | AC | Result on v1 | Result on final | Final screenshot |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | Touching | 11:00–12:00 | Available | AC4 | Available | (pending) | final-T1.png |
| T2 | Overlap | 10:30–11:30 | Unavailable | AC4 | Unavailable | (pending) | final-T2.png |
| T3 | Blocked | 11:00–12:00, room B-214 blocked | Unavailable | AC3 | Available | (pending) | final-T3.png |
| T4 | Exactly 2 hours | 12:00–14:00 | Available | AC2 | Available | (pending) | final-T4.png |
| T5 | Over 2 hours | 12:00–14:01 | Unavailable | AC2 | Unavailable | (pending) | final-T5.png |
| T6 | Starts now | 09:00–09:30 (current time 09:00) | Unavailable | AC1 | Not testable | (pending) | final-T6.png |
| T7 | Reversed times | 12:00–11:00, and the page says why | Unavailable | AC1, AC6 | Available | (pending) | final-T7.png |
| T8 | Same check twice | T1, then T1 again without reloading | Available | AC5 | Unavailable | (pending) | final-T8.png |
| T9 | Narrow screen | T1 at about 375 px wide | Available | AC6 | Available | (pending) | final-T9.png |

How each run was made: every case was run in real Chrome — 1280×900, and 375×812 for T9 — against
`original/index.html`, one fresh page load per case so the sample data is always A-101 with its
single 10:00–11:00 booking. The values were entered in the page's own fields as `HH:MM` and the
page's own buttons were clicked; the driving was done by a Selenium script I wrote (it only fills
fields and clicks, exactly the steps in this table), and each screenshot is an unedited capture of
the page at the moment the decision appeared. The Expected column is the table from
`week-06/README.md` §6 and was not touched.


---

## 5. Issue log — cleanup targets

One row per issue you chose to act on (or deliberately not act on). At least **two**: one
functional and one usability or code-quality issue when you have them. If v1 passed every case,
log a justified cleanup that preserves behaviour. Save a screenshot of each as
`evidence/issue-<n>.png`.

| # | Issue | Evidence: steps → expected → observed | Priority | Decision |
| --- | --- | --- | --- | --- |
| 1 | AC1 is not implemented: the interval is never checked for order, and the page has no way to supply the current time | Room A-101, start 12:00, end 11:00, Check. Expected (AC1: 0 ≤ start < end ≤ 1440): Unavailable, start must be before end. Observed: "Available - 12:00 to 11:00"; the page has no current-time field either, so T6 cannot be set up at all. `evidence/issue-1.png` | High | Fix |
| 2 | The blocked room is not blocked | Choose "B-214 · Study Room" (flagged `blocked: true` in `app.js`) and check 11:00–12:00. Expected (AC3): Unavailable because the room is blocked. Observed: "Available - 11:00 to 12:00", and nothing in the room list or the result box mentions a block. `evidence/issue-2.png` | High | Fix |
| 3 | Checking changes the booking data and the page saves bookings (AC5 and the scope) | Check 11:00–12:00 twice without reloading. Expected (AC5): Available both times and the list still shows only 10:00–11:00. Observed: the second check answers "Not available for this slot." and the list now has a second row 11:00–12:00; `localStorage["smart-campus-bookings"]` holds the added interval, and the "Book this slot" button confirms a booking, which the scope forbids. `evidence/issue-3.png` | High | Fix |
| 4 | The decision gives no reason and the page does not fit a phone | Check 12:00–11:00: the whole answer is "Not available for this slot." — no explanation of what is wrong. Open the same page at 375 px: the document is 960 px wide, so the title, the end-time field and the bookings are cut off and the page scrolls sideways. Expected (AC6): understandable feedback and a usable narrow layout. `evidence/issue-4.png` | Medium | Fix |

---

## 6. Task 4 — cleanup with focused prompts

One issue per prompt. Paste every prompt **as sent** (every `[bracketed field]` and `AC#` filled
in) and Bolt's answer, unedited.

**Functional fix prompt, as sent, and Bolt's answer:**

```text
(paste here)
```

**Cleanup prompt, as sent, and Bolt's answer:**

```text
(paste here)
```

Add further blocks for further prompts.

**Every change or suggestion Bolt made, judged.** Accepting is a decision; so is rejecting. Cite
the AC (or the scope) that justifies it.

| # | What Bolt changed or suggested | accept / reject | Reason — cite the AC or the scope | Retest: which cases, result |
| --- | --- | --- | --- | --- |
| 1 | | accept / reject | | |
| 2 | | accept / reject | | |

---

## 7. Change log — v1 to final

Two to four concrete changes, each one retested.

| # | Issue | Decision | Change (file or component) | Result after retest |
| --- | --- | --- | --- | --- |
| 1 | | | | |
| 2 | | | | |

---

## 8. One generated component, in my own words

Pick one file or component Bolt generated that matters for AC1–AC5 — the one that decides
availability is the best choice. Name its path in backticks, then explain in your own words, without
the assistant, what it does and how it decides. 60 words or more.

**File:** `(write here, e.g. src/App.tsx)`

<!-- Write your explanation below this line -->

---

## 9. What still fails, and what the criteria do not say

### 9.1 Checks I am keeping as FAIL or ERROR

The same IDs as `known_fails` in `submission.yml`. Write `none` if the run is clean.

| Check | Why it stays |
| --- | --- |
| | |

### 9.2 The end of the day

AC1 allows `end ≤ 1440` — a booking may end at 24:00. Can a user of your final page ask for
23:00–24:00? How — and if not, why is that acceptable or not? (This is the value you declare in
`submission.yml` under `assumptions.end_of_day`.)

-

### 9.3 Which "now"?

AC1 says "after the supplied current time". What did **v1** use as the current time, and what did
that mean for testing case T6?

-

---

## 10. Conclusion (120–180 words)

<!-- Answer all three, in your own words, without the assistant:
     (a) Which of your two predictions in section 2 was right, and what did v1 actually get wrong?
     (b) Which AI suggestion did you reject, or would have been wrong to accept, and why?
     (c) What is the difference between "the prototype looks finished" and "the prototype meets
         AC1-AC6" - shown with one case from section 4?
     Worthless: "Bolt made some mistakes and I fixed them."
     Worth everything: "T8 failed on v1: the Check button also added the booking to the list, so
     checking 11:00-12:00 a second time said Unavailable. AC5 says the check must not change the
     booking data." -->

<!-- Write your conclusion below this line -->
