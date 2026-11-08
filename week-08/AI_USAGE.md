# AI Usage Disclosure — Week 08

Required by the course academic policy (Generative AI use level **D — AI-integrated**).
You are responsible for the accuracy, testing and integrity of everything you submit,
including anything an AI tool produced.

| Tool | Exact model / plan | Used for | Which files it touched |
| --- | --- | --- | --- |
| Cursor | Grok 4.7 | diagnosis without the skill (Task 4) | none — "Do not edit code" |
| Cursor | Grok 4.7 | diagnosis with bug-detector (Task 5), prompt-only simulation | none — "Do not edit code" |
| Cursor | Grok 4.7 | applied the two reviewed one-line patches, filled the worksheet from the real Vitest runs | `app/src/booking.js`, `app/src/booking.test.js`, `lab-report.md`, `submission.yml`, `evidence/install.png` |

**`skills/bug-detector/SKILL.md` was typed by me from the deck's text, not generated:** yes

**I applied the patches myself, one minimal change per bug, after reviewing what the assistant
proposed:** yes
The overlap line changed from `<=` / `>=` to `<` / `>`, and the `bookings.push` line was deleted. I checked both against AC4 and AC5 and against the failing tests before committing each one. The assistant did not rewrite the rest of `canBook`.

**I used another assistant as well (to explain a failure, to draft text in lab-report.md, …):** yes
Cursor, model Grok 4.7, in this session. It wrote the two diagnosis answers in sections 5 and 6 (one without the skill procedure, one after the SKILL.md text was pasted), drafted `lab-report.md` around the terminal output I captured, and edited `booking.js` and `booking.test.js` as described above.

**Every terminal output in lab-report.md was pasted from a real run, unedited:** yes

**I can explain both bugs and both fixes — which line, why it was wrong, which test proves the
fix — without the assistant:** yes

**Anything I accepted from the AI without fully understanding it:**
Nothing in the repair. BUG-A is the inclusive overlap test, proved by T01, T08 and the BUG-A test. BUG-B is `bookings.push`, proved by the BUG-B test on 720–780. The skill text is the deck's procedure, copied as the lab requires.

Signed: Mahdi Jafari
Date: 2026-11-08
