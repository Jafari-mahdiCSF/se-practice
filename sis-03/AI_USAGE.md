# AI Usage Disclosure — SIS #03

Required by the course academic policy (Generative AI use level **D — AI-integrated**).
You are responsible for the accuracy, testing and integrity of everything you submit,
including anything an AI tool produced.

| Tool | Exact model / plan | Used for | Which files it touched | Reused from |
| --- | --- | --- | --- | --- |
| Grok | grok 4.6 | the plan (stage A) | `report.md` section 11 B1 | this SIS |
| Copilot SDK in VS Code | GPT-5 (Copilot SDK) | Python v1 (stage B) | `code/original/booking_v1.py` | week-05 |
| Cline (instead of Bolt.new) | not displayed | web prototype v1 (stage B) | `web/original/` | week-06 |
| Grok | grok 4.6 | critique (stage C) | `report.md` section 8 and 11 B3 | this SIS |
| Grok | grok 4.6 | repair (stage D) | `web/final/`, `code/booking.py`, `code/test_booking.py` | this SIS |

**The assistant wrote, or helped write, my tests in `code/`:** yes
The suite was expanded from the Week 05 tests. Expected values were taken from AC1-AC5 and from T1-T11, not from whatever v1 happened to return. T1 on v1 is recorded as False because that is what the file returns.

**`code/original/` and `web/original/` hold the AI's first versions exactly as returned:** yes

**Every result in report.md section 5 was actually run or seen, not assumed:** yes

**Everything I submitted, I can explain and defend in class — including the overlap condition
and what the agent did in section 9:** yes

**Anything I accepted from the AI without fully understanding it:**
none for the booking rule. I used Chrome device metrics to take `final-narrow.png` at 375 px; I understand it changes the layout width, not the internals of the protocol.

Signed: Mahdi Jafari
Date: 2026-10-31
