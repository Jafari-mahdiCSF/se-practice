# AI Usage Disclosure — Week 07

Required by the course academic policy (Generative AI use level **D — AI-integrated**).
You are responsible for the accuracy, testing and integrity of everything you submit,
including anything an AI tool produced.

| Tool | Exact model / plan | Used for | Which files it touched |
| --- | --- | --- | --- |
| Grok | grok 4.6 | the first test suite (Task 3) | `suites/first/booking.test.js`, then copied to `app/src/booking.test.js` |
| Grok | grok 4.6 | the improvement prompt (Task 5) | `app/src/booking.test.js` (T06, AC5, X1, X2) |
| Grok | grok 4.6 | extract `canBook`, fill worksheet drafts, UI capture help | `app/src/booking.js`, `app/src/availability.js`, `lab-report.md` |

**I used an assistant to extract `canBook` (Task 1), or to fix a defect in it:** yes
The Boolean rules moved from `decideAvailability` in `src/availability.js` into `src/booking.js`. I checked by keeping the same blocked / range / now / duration / overlap order and by running the page on A-101 11:00–12:00 (Available) and B-214 (Unavailable). I did not change `canBook` to make T06 pass.

**I used another assistant as well (to explain a failure, to draft text in lab-report.md, …):** no

**`suites/first/` holds the assistant's first test file exactly as it generated it:** yes

**Every terminal output in lab-report.md was pasted from a real run, unedited:** yes

**I can explain every test in my final suite — its input, its expected result and the AC behind
it — without the assistant:** yes

**Anything I accepted from the AI without fully understanding it:**
Nothing in the final suite. I rejected the generated T06 expectation because it contradicted AC2.

Signed: Mahdi Jafari
Date: 2026-11-06
