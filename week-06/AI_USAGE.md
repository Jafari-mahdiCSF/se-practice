# AI Usage Disclosure — Week 06

Required by the course academic policy (Generative AI use level **D — AI-integrated**).
You are responsible for the accuracy, testing and integrity of everything you submit,
including anything an AI tool produced.

| Tool | Exact model / plan | Used for | Which files it touched |
| --- | --- | --- | --- |
| Cline — AI coding agent inside VS Code (used instead of Bolt.new, which this machine could not reach: no signed-in browser session) | not displayed — the session shows no model name, so none is claimed | prototype v1, generated in one pass from the deck's initial prompt (Task 2) | `original/index.html`, `original/styles.css`, `original/app.js` |
| Cline — same session | not displayed | the three cleanup prompts of Task 4, one issue per prompt | `prototype/index.html`, `prototype/styles.css`, `prototype/src/app.js`, `prototype/src/availability.js`, `prototype/src/data.js` |
| Cline — same session | not displayed | the Selenium script that drove Chrome for T1–T9, filled the page's own fields, clicked its buttons and saved the screenshots; and the first draft of the prose in `lab-report.md`, which I then corrected against the real runs | `evidence/*.png`; the driving script was kept outside the repository (temp folder), not committed |

**I used another assistant as well (to explain code, to draft text in lab-report.md, …):** no — Cline is the only assistant in this lab, and the rows above list everything it touched, including the screenshots and the first draft of the report.

**`original/` holds Bolt's first version exactly as downloaded, and `evidence/v1.png` shows it:** yes, with one honest substitution — the builder was Cline, not Bolt (see §1 of `lab-report.md`). `original/` is its first output, unedited, committed at `1ca0d7a` before any cleanup prompt existed; `evidence/v1.png` is the screenshot of that version.

**Every screenshot in `evidence/` is an unedited capture of the page as it behaved:** yes — Chrome 155 screenshots taken by the script at the moment the decision appeared; 1280×900 for the desktop cases, 375×812 (full page 375×1048) for T9. No image was cropped, retouched or composited.

**I can explain the component I chose in lab-report.md section 8 — and how the page decides
availability — without the assistant:** yes — `src/availability.js` is described in §8 in my own words, and the rule order is written out there.

**Anything I accepted from the AI without fully understanding it:**
The `Emulation.setDeviceMetricsOverride` call in my screenshot script: I took it from the Chrome DevTools
protocol notes to get a real 375 px viewport, because a normal Chrome window refuses to go below 500 px
wide. I understand what it does (it tells Chrome to lay the page out at 375×812) but not the protocol
internals behind it. It is part of the measuring tool, not of the prototype, and it is not committed.

Signed: Mahdi Jafari
Date: 18 October 2026
