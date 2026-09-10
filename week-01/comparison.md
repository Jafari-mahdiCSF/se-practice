# Week 01 — Manual vs AI: Comparison

**Name:Mahdi Jafari**
**Group: mon 4pm**
**Date: 10 sep**

---

## live URL
https://markscalc-7ubj27.public.builtwithrocket.new


## 1. Facts

| | Manual (Part 1) | Rocket (Part 2) |
| --- | --- | --- |
| Language / stack used | Python 3, standard library only |
| Time to first version that ran | 60 min | 3 min |
| Time to all 4 test cases passing | 40 min | 8 min |
| Number of attempts / prompts needed | 6 test runs, 0 AI prompts | 4 prompts + 2 follow-ups |
| Lines of code you actually wrote | 65 | 0 |
| Did it handle invalid marks (case B)? | Yes — try/except ValueError in parse_mark | Yes — after a follow-up prompt; first try crashed on "abc" |
| Did it handle an empty list (case D)? | Yes — early return before dividing | Yes — but first version divided by zero |
| Did it use the ≥ 50 pass threshold? | Yes — if m >= 50 | Yes |
| Output format matches the spec? | Yes | Yes if the first promt be clear about what in specs requrements |
| Can you explain every line of it? | Yes | Mostly — some functions are advanced and some shurtcats are used i would need to check ai |

## 2. Test results

| Case | Input | Manual output | Rocket output | Spec says | Match? |
| --- | --- | --- | --- | --- | --- |
| A | `85, 23, 45, 90, 92` | | | avg 67.00 · high 92 · low 23 · pass 60.0% | |
| B | `88, 47, -5, 101, abc, 73, 50, , 100` | | | avg 71.60 · high 100 · low 47 · pass 80.0% | |
| C | `10, 20, 30` | | | avg 20.00 · high 30 · low 10 · pass 0.0% | |
| D | `abc, , xyz` | | | clear message, no crash | |

## 3. What the AI added that I never asked for

<!-- Tech stack, UI, extra features, a pass threshold it invented, styling, etc. -->

- Rocket.new added charts to the result page — I think it's very nice.
- The AI builder also added the pass threshold, and overall the app in UI mode looks many times better than a console-based app.

## 4. What the AI got wrong or silently skipped

<!-- Be concrete: input, expected, actual. -->

Honestly, the AI made it with no problem I can mention here. The AI builder made the app flawlessly, and it passes all 4 tests with not a single problem.

- It would be nice if I could have a history.
- For some numbers it would be better if they were in decimal.
- Overall, I think it's 95 percent correct.

## 5. The defect I asked Rocket to fix

**Prompt I used:**

> please add a remove button on top of scores so that i can erase all and input new records instead of one by one changing the records

**Result:** (fixed / partly fixed / broke something else)

Fixed and accurate.

**What this tells me:**

This tells me that AI will need some UI and overall guidance to make production-ready apps, and is not able to finish what is in my mind 100 percent.

## 6. Reflection (200–300 words)

Answer all four, in your own words:

1. Which parts of the work did the AI genuinely speed up?
2. Where did the AI cost you time, or give you something that looked right but was not?
3. Which of these two artefacts would you be willing to put your name on, and why?
4. What must a human engineer still be responsible for after this experiment?

<!-- Write your reflection below this line -->

1. **What AI sped up.** The rocket.new built the whole working app — UI, input, statistics, charts — in a few minutes. It also saved time on styling and layout, which I would have skipped entirely in a console app.

2. **Where AI cost me time.** The first attempt was refused, so I had to answer its questions before anything was built.

3. **Which artefact I'd put my name on.** The manual solution. I wrote every line, I can explain all of it. The Rocket app looks nicer, but I dont understan the code.

4. **What a human is still responsible for.** Defining the requirements (I rewrote the prompt for the AI), checking the output, and testing the app against edge cases. Also, the app should not contain security issues or inefficient use of system resources.