# AI Usage Disclosure — Week 09

Required by the course academic policy (Generative AI use level **D — AI-integrated**).
You are responsible for the accuracy, testing and integrity of everything you submit,
including anything an AI tool produced.

| Tool | Exact model / plan | Used for | Which files it touched |
| --- | --- | --- | --- |
| Copilot SDK in VS Code | not displayed | Part 2 — drafted the R1, R2, and R3 replies and reviewed the fixed cases and requirements | calls/ |

**I wrote `tool/check_room.json` myself:** no
The assistant drafted the schema. I checked its five exact properties, required fields, supported keywords, numeric bounds, nested booking shape, and the twelve checker cases.

**I used an AI to explain a JSON Schema keyword or a check:** yes
The assistant explained why `additionalProperties: false`, nested `items`, and integer minimum/maximum constraints are needed; I verified those points against `tests/check_tool.py`.

**Every reply in `calls/` and in lab-report.md section 4 is exactly what the model returned:** yes

**Every terminal output in lab-report.md was pasted from a real run, unedited:** yes

**Anything I accepted from the AI without fully understanding it:**
Nothing. I reviewed the schema constraints, the expected R1/R2 minute conversions, the R3 clarification, and the checker output.

Signed: Mahdi Jafari
Date: 2026-11-14
