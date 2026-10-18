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
| T1 | Touching | 11:00–12:00 | Available | AC4 | Available | Available | final-T1.png |
| T2 | Overlap | 10:30–11:30 | Unavailable | AC4 | Unavailable | Unavailable | final-T2.png |
| T3 | Blocked | 11:00–12:00, room B-214 blocked | Unavailable | AC3 | Available | Unavailable | final-T3.png |
| T4 | Exactly 2 hours | 12:00–14:00 | Available | AC2 | Available | Available | final-T4.png |
| T5 | Over 2 hours | 12:00–14:01 | Unavailable | AC2 | Unavailable | Unavailable | final-T5.png |
| T6 | Starts now | 09:00–09:30 (current time 09:00) | Unavailable | AC1 | Not testable | Unavailable | final-T6.png |
| T7 | Reversed times | 12:00–11:00, and the page says why | Unavailable | AC1, AC6 | Available | Unavailable | final-T7.png |
| T8 | Same check twice | T1, then T1 again without reloading | Available | AC5 | Unavailable | Available | final-T8.png |
| T9 | Narrow screen | T1 at about 375 px wide | Available | AC6 | Available | Available | final-T9.png |

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

**Functional fix prompt, as sent, and the builder's answer:**

```text
In the current prototype, entering 12:00 as the start and 11:00 as the end produces "Available - 12:00
to 11:00", and the page has no field for the supplied current time, but AC1 requires every interval to
satisfy 0 <= start < end <= 1440 and to start after the supplied current time. Make the smallest change
that fixes this behavior. Preserve the other acceptance criteria. Explain which file/component you
changed and why.
```

```text
Changed index.html and app.js.

index.html: added a "Current time" field (<input id="now" type="time">) next to Start and End, so the
current time is supplied by the user instead of being assumed.

app.js: checkAvailability() now reads that field and validates the window before any booking logic:
- a missing or unparsable start/end is rejected with an explicit message;
- start >= end is rejected, which covers 12:00-11:00 and a zero-length window;
- end - start > 120 is still rejected (AC2 kept);
- start <= now is rejected, and the message names both times (AC1 says the start must be *after* the
  supplied current time, so 09:00 with now 09:00 is rejected);
- the overlap test start < booking.end && end > booking.start is unchanged, so touching endpoints stay
  allowed (AC4).
On load the field defaults to the machine clock; it stays editable. I left the rest of v1 alone for
now. If you plan to book ahead I can also add a date picker and a "repeat weekly" option here.
```

**Second functional fix prompt, as sent, and the builder's answer:**

```text
In the current prototype, choosing B-214 - Study Room, which is marked blocked in the room data, and
checking 11:00-12:00 produces "Available", but AC3 requires the request to be rejected when the selected
room is blocked. Make the smallest change that fixes this behavior. Preserve the other acceptance
criteria. Explain which file/component you changed and why.
```

```text
Changed app.js and index.html.

app.js: ROOMS entries now carry a note as well as blocked, renderRooms() appends "(blocked)" to the room
name in the list, and a new updateRoomStatus() writes a line under the room select for the selected room
(red for a blocked room). checkAvailability() checks room.blocked straight after the time parsing and
returns "Unavailable" with the room name and the reason. index.html only gained the <p id="room-status">
element that line is written into.

I can also add an "unblock this room" toggle for a technician if you want it.
```

**Cleanup prompt, as sent, and the builder's answer:**

```text
Review only the result panel and the page layout for unnecessary duplication, confusing naming, or UI
feedback problems. Suggest one small cleanup. Do not add features or redesign the whole application.
Implement it only if it preserves AC1-AC6.
```

```text
Changed app.js, index.html, styles.css and added src/availability.js and src/data.js.

Problem found: the decision was seven if-blocks inside checkAvailability(), each composing its own
sentence, and the layout was a fixed 960 px column.

Cleanup: the rules now live in one ordered function, decideAvailability(request), in src/availability.js.
It returns { available, headline, detail } and stops at the first rule that rejects the request, in this
order: unparsable times, 24:00 used as a start, blocked room, start not before end, longer than 120
minutes, start not after the supplied now, overlap. app.js keeps only the wiring and prints the headline
and the detail. The sample rooms and bookings moved to src/data.js. The result panel is now a headline
plus one sentence, and under 700 px the three time fields stack and the button goes full width, so the
decision is still on screen at 375 px. I also added an "ends at 24:00" checkbox next to End, because a
native time field cannot hold 24:00 and AC1 allows end = 1440.

If you want, I can add a confirmation dialog and a "Book" flow on top of the decision.
```

**Every change or suggestion the builder made, judged.** Accepting is a decision; so is rejecting. Cite
the AC (or the scope) that justifies it.

| # | What the builder changed or suggested | accept / reject | Reason — cite the AC or the scope | Retest: which cases, result |
| --- | --- | --- | --- | --- |
| 1 | Add a "Current time" field and reject unparsable times, start >= end and start <= now | accept | AC1: the interval must satisfy 0 ≤ start < end ≤ 1440 *and* start after the supplied current time; without the field T6 cannot be set up at all | T6 Unavailable (was Not testable), T7 Unavailable (was Available); all nine re-run: 7 of 9 |
| 2 | "Add a date picker and a repeat-weekly option" | reject | Scope: one page, one selected room, no extra features; a repeat rule would need stored state and would change what AC4 compares | not applied; the nine cases unchanged |
| 3 | Read the `blocked` flag, label the room "(blocked)", print a status line and reject every request on it | accept | AC3: reject the request when the selected room is blocked; the flag existed in v1's data and no code read it | T3 Unavailable (was Available); all nine: 8 of 9 |
| 4 | "Add an unblock-this-room toggle for a technician" | reject | Scope: the page checks availability, it does not manage rooms; changing room state is also the kind of write AC5 keeps out of the check | not applied |
| 5 | Remove the "hold" the Check button wrote into the bookings, remove the Book button and the localStorage copy | accept | AC5: showing the decision must not change the existing booking data; the scope says the prototype does not save or confirm a booking | T8 Available twice (was Unavailable); all nine: 9 of 9 |
| 6 | "Keep localStorage so the bookings persist between visits" | reject | Scope forbids saving, AC5 forbids changing the booking data, and P3 flags browser storage | not applied; P3 clean |
| 7 | Move the rules into one ordered `decideAvailability()` in `src/availability.js` that returns a reason | accept | AC6: the feedback must be understandable, and one ordered list removes seven duplications and makes the rule that fired visible | all nine re-run: 9 of 9, same answers, every message now names its rule |
| 8 | "Add a confirmation dialog and a Book flow" | reject | Scope: confirming a booking is exactly what the prototype must not do; AC5 keeps the check read-only | not applied |
| 9 | Stack the time fields under 700 px, full-width button, keep the decision in view; add the "ends at 24:00" checkbox | accept | AC6: usable at narrow width — the document measured 960 px at a 375 px viewport before the change; the checkbox is the AC1 `end = 1440` case, declared as `assumptions.end_of_day: end-of-day-option` | T9 at 375×812, full page 375×1048: Available |

---

## 7. Change log — v1 to final

Two to four concrete changes, each one retested.

| # | Issue | Decision | Change (file or component) | Result after retest |
| --- | --- | --- | --- | --- |
| 1 | AC1 not implemented: no supplied current time, reversed window accepted | Fix | `index.html` gained the "Current time" field; `app.js` got the ordered time validation (unparsable, start >= end, start <= now) | T6 Unavailable and T7 Unavailable; all nine re-run: 7 of 9 |
| 2 | AC3 not implemented: the blocked room answered Available | Fix | `app.js`: read `room.blocked`, label the option "(blocked)", status line, reject with the room name; `index.html` gained the status element | T3 Unavailable; all nine: 8 of 9 |
| 3 | AC5 violated and scope creep: the check wrote a hold into the bookings and localStorage kept it | Fix | `index.html` and `app.js`: hold, Book button and storage removed; read-only "booking data unchanged / checks on this page load" line added | T8 Available twice; all nine: 9 of 9 |
| 4 | AC6: no reason with the answer, fixed 960 px layout on a phone | Fix | New `src/availability.js` (one ordered rule list returning headline + reason), `src/data.js`, `src/app.js` wiring only, responsive `styles.css`, "ends at 24:00" option | all nine still 9 of 9 on the rebuilt page; T9 at 375×812 and full-page 375×1048: Available |

---

## 8. One generated component, in my own words

Pick one file or component Bolt generated that matters for AC1–AC5 — the one that decides
availability is the best choice. Name its path in backticks, then explain in your own words, without
the assistant, what it does and how it decides. 60 words or more.

**File:** `src/availability.js`

<!-- Write your explanation below this line -->
This file holds the only function that decides anything, `decideAvailability`. It is handed one request
object: the chosen room, the start and end text from the form, the current-time text, and the sample
booking list. It first turns both clock strings into minutes after midnight; `24:00` becomes 1440 and is
refused as a start, and anything that is not a real time becomes `null`. Then it walks a fixed list of
rules and stops at the first one that bites: an unreadable time, a blocked room, a start that is not
before the end, a window longer than 120 minutes, a start that is not after the supplied current time,
and finally an overlap test, `start < booking.end && end > booking.start`, which lets a window that only
touches another booking through. It reads the booking list and never adds to it; it returns a headline
and the sentence the panel shows.

---

## 9. What still fails, and what the criteria do not say

### 9.1 Checks I am keeping as FAIL or ERROR

The same IDs as `known_fails` in `submission.yml`. Write `none` if the run is clean.

| Check | Why it stays |
| --- | --- |
| none | The last run of `tests/check_prototype.py` on this folder was 27 PASS, 0 FAIL, 0 ERROR, so `known_fails` is `[]`. The one thing the checker cannot see is honesty: the screenshots are unedited Chrome captures of the runs written down in §4. |

### 9.2 The end of the day

- Yes, and the page asks for it with a checkbox rather than by typing. Next to End there is
  "ends at 24:00": ticking it disables the End field and sends end = 1440, which is exactly what AC1
  allows. Unticked, the native time field can only hold 00:00–23:59, so 24:00 would simply be
  unreachable — the checkbox is the whole answer to the open question.
- Verified in the final page: room A-101, current time 09:00, start 23:00, box ticked → end field
  greyed out, result "Available 23:00-24:00 (60 min)". A start of 24:00 is refused with
  "24:00 can only be the end of a slot, never the start."
- It is declared in `submission.yml` as `assumptions.end_of_day: end-of-day-option`. I chose it over a
  free-text time field because typing `24:00` invites typos in a field that otherwise has a picker;
  one extra control is cheaper than re-teaching the user the format.

### 9.3 Which "now"?

- v1 had no "now" at all. Nothing in `app.js` read `new Date()`, and there was no field for it, so AC1's
  "after the supplied current time" was simply not implemented — not wrong, absent.
- For T6 that meant **Not testable**: the case needs current time 09:00 while the request starts at
  09:00, and the page gave no way to supply 09:00. The check it did perform (09:00–09:30 against the
  10:00–11:00 booking) answered "Available", which would have been the wrong answer even at a real 09:00.
- The final page supplies the current time explicitly: the field starts at the machine clock and stays
  editable, and `decideAvailability` rejects `start <= now`. With 09:00 in the field, T6 now answers
  "Unavailable - Start 09:00 is not after the current time 09:00." (`evidence/final-T6.png`).

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
Both predictions came true, and the first one hid a bigger gap. v1 had no current-time field at all, so
AC1's "after the supplied current time" was absent rather than wrong, and T6 could only be recorded as
Not testable. Its Check button then wrote the tested window into the booking list, so T8 answered
Unavailable the second time, exactly as I predicted. What I did not predict was T3: the room data
carried blocked: true, no code read it, and the blocked room answered Available.

I rejected keeping the bookings in browser storage. AC5 says the check must not change the booking data
and the scope says the prototype does not save a booking, so persistence would have preserved the T8
defect and disguised it as a feature.

"Looks finished" is a green box on a page. "Meets AC1-AC6" is T7: v1 answered "Available - 12:00 to
11:00", while the final page answers Unavailable and says that the window is reversed. Same screen,
different amount of truth.
