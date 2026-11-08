# Week 08 — Lab report

**Name:** Mahdi Jafari
**Group:** CSCI-2208
**Date:** 2026-11-08

Fill in every section. **Do not delete, rename or renumber the headings.** The checker and the
grader find your answers by them. You can add rows to any table, but never remove its header.

---

## 1. Setup

| | |
| --- | --- |
| Assistant I debugged with (tool) | Cursor |
| Exact model (with its version, or `not displayed`) | Grok 4.7 |
| Where the skill was installed (ChatGPT / Claude web / Claude Code / prompt-only simulation) | prompt-only simulation |
| Where I ran the tests (Bolt terminal / my computer / Codespace) | my computer |
| Vitest version (the `RUN  v…` line of a run) | 5.1.0 |
| Language of my booking module (`ts` or `js`) — the file I copied from `buggy/` | js |

---

## 2. Task 1 — baseline, buggy code, failing tests

### 2.1 My Week 07 suite on my own code

The **real** output of your Week 07 suite, run in `week-08/app/` **before** you replace
anything. It should be green. If it is not, say why under the block.

```text
npm warn Unknown env config "devdir". This will stop working in the next major version of npm. See `npm help npmrc` for supported config options.

 RUN  v5.1.0 C:/Users/mahdi/OneDrive/Desktop/se-practice-remote-check/week-08/app


 Test Files  1 passed (1)
      Tests  17 passed (17)
   Start at  23:08:44
   Duration  211ms (transform 53%, import 24%, worker 13%, tests 10%)
```

### 2.2 The same suite on the provided canBook

You copied the whole `canBook` function from `buggy/booking.ts` (or `.js`) over yours and changed
nothing else. This is the real output:

```text
npm warn Unknown env config "devdir". This will stop working in the next major version of npm. See `npm help npmrc` for supported config options.

 RUN  v5.1.0 C:/Users/mahdi/OneDrive/Desktop/se-practice-remote-check/week-08/app

 ❯ src/booking.test.js (17 tests | 3 failed) 11ms
   ❯ canBook (17)
     × T01 AC4: touching after the existing booking 7ms
     × T08 AC4: touching before the existing booking 1ms
     × AC5: an available request leaves bookings unchanged 0ms

⎯⎯⎯⎯⎯⎯⎯ Failed Tests 3 ⎯⎯⎯⎯⎯⎯⎯

 FAIL  src/booking.test.js > canBook > T01 AC4: touching after the existing booking
AssertionError: expected false to be true // Object.is equality

- Expected
+ Received

- true
+ false

 ❯ src/booking.test.js:16:71
     14|   test("T01 AC4: touching after the existing booking", () => {
     15|     const { now, blocked, bookings } = fixture();
     16|     expect(canBook({ start: 660, end: 720, now, blocked, bookings })).…
       |                                                                       ^
     17|   });
     18|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/3]⎯

 FAIL  src/booking.test.js > canBook > T08 AC4: touching before the existing booking
AssertionError: expected false to be true // Object.is equality

- Expected
+ Received

- true
+ false

 ❯ src/booking.test.js:51:71
     49|   test("T08 AC4: touching before the existing booking", () => {
     50|     const { now, blocked, bookings } = fixture();
     51|     expect(canBook({ start: 570, end: 600, now, blocked, bookings })).…
       |                                                                       ^
     52|   });
     53|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[2/3]⎯

 FAIL  src/booking.test.js > canBook > AC5: an available request leaves bookings unchanged
AssertionError: expected false to be true // Object.is equality

- Expected
+ Received

- true
+ false

 ❯ src/booking.test.js:87:83
     85|     const bookings = [{ start: 600, end: 660 }];
     86|     const before = JSON.stringify(bookings);
     87|     expect(canBook({ start: 660, end: 720, now: 540, blocked: false, b…
       |                                                                                   ^
     88|     expect(JSON.stringify(bookings)).toEqual(before);
     89|   });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[3/3]⎯


 Test Files  1 failed (1)
      Tests  3 failed | 14 passed (17)
   Start at  23:12:06
   Duration  242ms (transform 41%, import 25%, tests 21%, worker 12%, environment 1%)
```

### 2.3 One failing test per bug

Add the two regression tests from README Part 1, step 5: one named `BUG-A` and one named `BUG-B`.
Run them **on the buggy code**. Both must fail here. That is the evidence that each test can see
its bug.

```text
npm warn Unknown env config "devdir". This will stop working in the next major version of npm. See `npm help npmrc` for supported config options.

 RUN  v5.1.0 C:/Users/mahdi/OneDrive/Desktop/se-practice-remote-check/week-08/app

 ❯ src/booking.test.js (19 tests | 5 failed) 15ms
   ❯ canBook (19)
     × T01 AC4: touching after the existing booking 8ms
     × T08 AC4: touching before the existing booking 1ms
     × AC5: an available request leaves bookings unchanged 0ms
     × BUG-A AC4: a request that touches bookings on both sides 0ms
     × BUG-B AC5: available 720-780 that touches nothing leaves bookings unchanged 2ms

⎯⎯⎯⎯⎯⎯⎯ Failed Tests 5 ⎯⎯⎯⎯⎯⎯⎯

 FAIL  src/booking.test.js > canBook > T01 AC4: touching after the existing booking
AssertionError: expected false to be true // Object.is equality

- Expected
+ Received

- true
+ false

 ❯ src/booking.test.js:16:71
     14|   test("T01 AC4: touching after the existing booking", () => {
     15|     const { now, blocked, bookings } = fixture();
     16|     expect(canBook({ start: 660, end: 720, now, blocked, bookings })).…
       |                                                                       ^
     17|   });
     18|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/5]⎯

 FAIL  src/booking.test.js > canBook > T08 AC4: touching before the existing booking
AssertionError: expected false to be true // Object.is equality

- Expected
+ Received

- true
+ false

 ❯ src/booking.test.js:51:71
     49|   test("T08 AC4: touching before the existing booking", () => {
     50|     const { now, blocked, bookings } = fixture();
     51|     expect(canBook({ start: 570, end: 600, now, blocked, bookings })).…
       |                                                                       ^
     52|   });
     53|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[2/5]⎯

 FAIL  src/booking.test.js > canBook > AC5: an available request leaves bookings unchanged
AssertionError: expected false to be true // Object.is equality

- Expected
+ Received

- true
+ false

 ❯ src/booking.test.js:87:83
     85|     const bookings = [{ start: 600, end: 660 }];
     86|     const before = JSON.stringify(bookings);
     87|     expect(canBook({ start: 660, end: 720, now: 540, blocked: false, b…
       |                                                                                   ^
     88|     expect(JSON.stringify(bookings)).toEqual(before);
     89|   });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[3/5]⎯

 FAIL  src/booking.test.js > canBook > BUG-A AC4: a request that touches bookings on both sides
AssertionError: expected false to be true // Object.is equality

- Expected
+ Received

- true
+ false

 ❯ src/booking.test.js:103:83
    101|   test("BUG-A AC4: a request that touches bookings on both sides", () …
    102|     const bookings = [{ start: 600, end: 660 }, { start: 780, end: 840…
    103|     expect(canBook({ start: 660, end: 780, now: 540, blocked: false, b…
       |                                                                                   ^
    104|   });
    105|

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[4/5]⎯

 FAIL  src/booking.test.js > canBook > BUG-B AC5: available 720-780 that touches nothing leaves bookings unchanged
AssertionError: expected '[{"start":600,"end":660},{"start":720…' to deeply equal '[{"start":600,"end":660}]'

Expected: "[{"start":600,"end":660}]"
Received: "[{"start":600,"end":660},{"start":720,"end":780}]"

 ❯ src/booking.test.js:110:38
    108|     const before = JSON.stringify(bookings);
    109|     expect(canBook({ start: 720, end: 780, now: 540, blocked: false, b…
    110|     expect(JSON.stringify(bookings)).toEqual(before);
       |                                      ^
    111|   });
    112| });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[5/5]⎯


 Test Files  1 failed (1)
      Tests  5 failed | 14 passed (19)
   Start at  23:12:41
   Duration  253ms (transform 44%, tests 25%, import 22%, worker 9%)
```

---

## 3. Defect log

One row per defect. At least **BUG-A and BUG-B**. "Suspected cause" is your hypothesis
**before** you ask any assistant: the line and why.

| Defect | Test ID | Input | Expected | Actual | Suspected cause (line and why) |
| --- | --- | --- | --- | --- | --- |
| BUG-A | T01, T08, BUG-A | 660-720 against 600-660; also 660-780 touching 600-660 and 780-840 | true, the intervals only meet at an endpoint | false | `start <= b.end && end >= b.start` counts a shared endpoint as an overlap. 660 <= 660 is true, so AC4's touching case is rejected. |
| BUG-B | BUG-B | 720-780, now 540, bookings [{start:600,end:660}], which shares no endpoint | true, and the array still equal to the copy taken before the call | the call returns true, then the array also holds {start:720,end:780} | `bookings.push({ start, end })` writes the free slot into the caller's list. The Week 07 AC5 test never reached this line: 660-720 was already false because of BUG-A. |

---

## 4. Tasks 2–3 — the skill

**The checks from the deck, before you zip it.** Answer each one yes / no:

| Check | yes / no |
| --- | --- |
| The file is plain UTF-8 text, named exactly `SKILL.md` (not `SKILL.md.txt`) | yes |
| The first and the closing YAML delimiter are exactly three hyphens: `---` | yes |
| `name` is lowercase with hyphens, and `description` says WHEN to use it | yes |
| I read the whole file once: no passwords, API keys or private student data | yes |

**The contents of `skills/bug-detector.zip`.** Paste the listing (Windows: open the ZIP and copy
the paths; macOS/Linux: `unzip -l skills/bug-detector.zip`):

```text
Archive:  skills/bug-detector.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
      571  2026-11-08 23:15   bug-detector/SKILL.md
---------                     -------
      571                     1 file
```

**Installation.** Where you uploaded it, what the upload said, and whether a new chat showed the
skill as enabled. If upload was not available, write `prompt-only simulation` and say why.
Screenshot of the result: `evidence/install.png`.

<!-- Write below this line -->

prompt-only simulation. This session is Cursor, and ChatGPT and Claude skill upload were not available here, so nothing was installed and no new chat showed a skill badge. I pasted the text of skills/bug-detector/SKILL.md as the first message and stated that it was a simulation, not an installed skill. The screenshot of that message is evidence/install.png.

---

## 5. Task 4 — without the skill

A **fresh chat, with no skill enabled**. Paste exactly what you sent: the deck's question, then
the same input you will use in section 6 (AC1–AC6, the failing test output, the code of
`canBook`):

```text
Find the root cause of the failed room-booking test. Propose minimal patch and regression test. Do not edit code.

AC1 Reject start >= end and requests in the past.
AC2 Enforce the maximum allowed duration (120 minutes).
AC3 Reject a blocked room.
AC4 Reject overlaps; allow bookings that only touch at endpoints.
AC5 Return Available / Unavailable without changing booking data.
AC6 Preserve clear UI feedback on desktop and mobile.

Failing test from the suite on the provided canBook, before any fix:

 FAIL  src/booking.test.js > canBook > T01 AC4: touching after the existing booking
AssertionError: expected false to be true // Object.is equality

- Expected
+ Received

- true
+ false

The test and fixture:

test("T01 AC4: touching after the existing booking", () => {
  const { now, blocked, bookings } = fixture();
  expect(canBook({ start: 660, end: 720, now, blocked, bookings })).toBe(true);
});

fixture: now = 540, blocked = false, bookings = [{ start: 600, end: 660 }]

The provided canBook, unchanged:

export function canBook({ start, end, now, blocked, bookings }) {
  if (!(0 <= start && start < end && end <= 1440)) return false;
  if (!(start > now)) return false;
  if (end - start > 120) return false;
  if (blocked) return false;
  for (const b of bookings) {
    if (start <= b.end && end >= b.start) return false;
  }
  // keep the room's list current with the slot that was just found free
  bookings.push({ start, end });
  return true;
}
```

**The assistant's answer, pasted unedited:**

```text
T01 calls canBook with start 660, end 720, now 540, blocked false, and bookings [{start: 600, end: 660}]. AC4 says a request that only touches an existing booking is allowed, so expected true is the right result. The function returns false from the loop. The condition is start <= b.end && end >= b.start. On this input 660 <= 660 and 720 >= 600, so a shared endpoint is treated as an overlap. That is the root cause of this failure. The other guards do not reject it: the window is inside the day, start is after now, the duration is 60 minutes, and the room is not blocked.

Minimal patch: change that comparison to start < b.end && end > b.start, and delete bookings.push({ start, end }). The push is the second defect. After the loop the function writes the slot into the caller's array, which is why this Available check fails AC5 as well.

Regression test: the same 660-720 fixture, expect true, then JSON.stringify(bookings) equal to a copy taken before the call. I did not edit the code.
```

---

## 6. Task 5 — with the skill

**Another fresh chat, with `bug-detector` enabled.** Send exactly the same input as in section 5.
Only the question changes, to the deck's:

```text
Use the bug-detector skill to diagnose the failed room-booking test.

AC1 Reject start >= end and requests in the past.
AC2 Enforce the maximum allowed duration (120 minutes).
AC3 Reject a blocked room.
AC4 Reject overlaps; allow bookings that only touch at endpoints.
AC5 Return Available / Unavailable without changing booking data.
AC6 Preserve clear UI feedback on desktop and mobile.

Failing test from the suite on the provided canBook, before any fix:

 FAIL  src/booking.test.js > canBook > T01 AC4: touching after the existing booking
AssertionError: expected false to be true // Object.is equality

- Expected
+ Received

- true
+ false

The test and fixture:

test("T01 AC4: touching after the existing booking", () => {
  const { now, blocked, bookings } = fixture();
  expect(canBook({ start: 660, end: 720, now, blocked, bookings })).toBe(true);
});

fixture: now = 540, blocked = false, bookings = [{ start: 600, end: 660 }]

The provided canBook, unchanged:

export function canBook({ start, end, now, blocked, bookings }) {
  if (!(0 <= start && start < end && end <= 1440)) return false;
  if (!(start > now)) return false;
  if (end - start > 120) return false;
  if (blocked) return false;
  for (const b of bookings) {
    if (start <= b.end && end >= b.start) return false;
  }
  // keep the room's list current with the slot that was just found free
  bookings.push({ start, end });
  return true;
}
```

**The assistant's answer, pasted unedited:**

```text
defect: touching endpoints are rejected. AC4 allows a booking that only meets another at an endpoint, and T01 expected true.

evidence: smallest input is start 660, end 720, now 540, blocked false, bookings [{start: 600, end: 660}]. Received false. 660 <= 660 is true and 720 >= 600 is true, so the loop returns false. Duration is 60, start is after now, the room is not blocked, and start < end holds, so those guards are not the failure.

root cause: confirmed. The line if (start <= b.end && end >= b.start) uses inclusive comparisons. A shared endpoint satisfies them.

hypothesis, not confirmed by this failure: bookings.push({ start, end }) would mutate the caller's array when the function returns true. T01 never reaches that line, because it returns false on the overlap. Do not call the push the cause of this test.

fix: do not edit yet. One line for the observed failure: start < b.end && end > b.start. Leave the push for a separate change once a test shows it.

test: 660-720 on booking 600-660 must be true. A second test that this output does not show: 720-780, which touches nothing, must be true, and bookings must still equal a copy taken before the call. Only that second test can fail because of the push.
```

Did the environment show that the skill was invoked? not shown

---

## 7. Comparison — judged against the actual code

Do not assume the skill did better. Judge both answers against the code and against what your
tests showed. Write a short verdict in each cell, and give a reason where they differ.

| Criterion | No skill | With skill |
| --- | --- | --- |
| Correct root cause | The `<=` line is the cause of T01. Naming `bookings.push` as a cause of this same failure does not match the code: T01 returns on the overlap line. | The `<=` line is confirmed for T01. The push is kept as a hypothesis because this test returns before it runs. |
| Reproducible test | 660-720 with `.toBe(true)` would catch BUG-A. Pairing it with a JSON compare cannot show the push, because the buggy function returns false first. | 660-720 for the observed failure, and a separate 720-780 compare against a copy. That second input is the one BUG-B actually failed on. |
| Minimal proposed patch | Changing `<=` / `>=` to `<` / `>` is the one-line repair. Deleting the push in the same patch is a second change, and this test did not prove it. | One line for T01, the strict overlap. The push is named as a later, separate edit. |
| Unsupported claims | Says the push is why this Available check fails AC5. The T01 assertion fails on false versus true, and the Week 07 AC5 test fails the same way, before the array is compared. | Does not claim the push caused T01. It says the mutation is unproven until a non-touching Available request is compared with a copy. |
| Clarity of explanation | One paragraph with the numbers 660 <= 660 and the AC4 rule, then a combined repair. | Split into defect, evidence, root cause, fix, and test, with confirmed and hypothesis kept apart. |

**Which bugs did each answer find?** (BUG-A, BUG-B, both, neither)

Both answers found BUG-A from T01. The plain answer also named BUG-B, but it attached the push to the T01 failure. The skill answer named BUG-B only as a hypothesis. The BUG-B run is what proved the push: after the call the array was `[{start:600,end:660},{start:720,end:780}]`.

---

## 8. Task 6 — repair and regression

Review the proposed patch yourself, then make **one minimal change per bug**, one commit each.
Rerun the test that was failing, then the full suite.

### 8.1 The BUG-A patch

The change as a diff (`git diff`, or the old and the new line), then the real run:

```text
diff --git a/week-08/app/src/booking.js b/week-08/app/src/booking.js
--- a/week-08/app/src/booking.js
+++ b/week-08/app/src/booking.js
@@ -4,7 +4,7 @@ export function canBook({ start, end, now, blocked, bookings }) {
   if (end - start > 120) return false;
   if (blocked) return false;
   for (const b of bookings) {
-    if (start <= b.end && end >= b.start) return false;
+    if (start < b.end && end > b.start) return false;
   }
   // keep the room's list current with the slot that was just found free
   bookings.push({ start, end });
```

```text
npm warn Unknown env config "devdir". This will stop working in the next major version of npm. See `npm help npmrc` for supported config options.

 RUN  v5.1.0 C:/Users/mahdi/OneDrive/Desktop/se-practice-remote-check/week-08/app


 Test Files  1 passed (1)
      Tests  1 passed | 18 skipped (19)
   Start at  23:15:52
   Duration  217ms (transform 45%, import 33%, worker 13%, tests 8%)
```

### 8.2 The BUG-B patch and the final run

The change as a diff, then the real output of the **full** suite. Every test must pass.

```text
diff --git a/week-08/app/src/booking.js b/week-08/app/src/booking.js
--- a/week-08/app/src/booking.js
+++ b/week-08/app/src/booking.js
@@ -6,7 +6,5 @@ export function canBook({ start, end, now, blocked, bookings }) {
   for (const b of bookings) {
     if (start < b.end && end > b.start) return false;
   }
-  // keep the room's list current with the slot that was just found free
-  bookings.push({ start, end });
   return true;
 }
```

```text
npm warn Unknown env config "devdir". This will stop working in the next major version of npm. See `npm help npmrc` for supported config options.

 RUN  v5.1.0 C:/Users/mahdi/OneDrive/Desktop/se-practice-remote-check/week-08/app


 Test Files  1 passed (1)
      Tests  19 passed (19)
   Start at  23:16:35
   Duration  197ms (transform 45%, import 30%, tests 13%, worker 12%)
```

---

## 9. What still fails, and what AI-assisted debugging cannot do

### 9.1 Checks I am keeping as FAIL or ERROR

Use the same IDs as `known_fails` in `submission.yml`. Write `none` if the run is clean.

| Check | Why it stays |
| --- | --- |
| none | the last checker run had no FAIL or ERROR |

### 9.2 One limitation of AI-assisted debugging

<!-- Use something that actually happened in sections 5-8. 20 words or more. -->

The plain answer treated bookings.push as a cause of the T01 failure. T01 returns false on the overlap line, so the push never runs. A diagnosis that sees only one failing test can hang a second defect on the wrong assertion. BUG-B stayed invisible until 720-780 was allowed and the array was compared with a copy taken before the call.

---

## 10. Conclusion (80–150 words)

<!-- Answer both, in your own words, without the assistant (3-5 sentences, as the deck asks):
     (a) Did the skill help? Show it with one row of section 7.
     (b) What did your tests actually prove - and what did they not?
     Worthless: "The skill made the AI much better at debugging."
     Worth everything: "Both answers found BUG-A from the T01 failure. Only the skill answer
     separated BUG-B as a hypothesis instead of a fact, because step 4 told it to. BUG-B was only
     visible after the BUG-A patch: the AC5 test had been failing for the wrong reason." -->

<!-- Write your conclusion below this line -->

The skill did help. The row that shows it is Minimal proposed patch in section 7. Both answers found BUG-A from the T01 failure: 660 to 720 against a booking that ends at 660 is rejected because the comparison is start <= b.end. The plain answer also said to delete bookings.push in that same repair, and it said the push is why T01 failed. T01 returns false on the overlap line, so the push never runs. The skill answer called the push a separate hypothesis and gave it another test, 720 to 780 compared with a copy. After only the comparison change, T01, T08 and BUG-A passed, and BUG-B still failed because the array gained a 720 to 780 object. The suite proves those two defects and the two repairs. It does not prove the page, and no acceptance criterion names a reversed existing booking.
