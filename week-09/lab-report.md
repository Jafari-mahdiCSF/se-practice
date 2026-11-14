# Week 09 — Lab Report: canBook as a Tool

**Name:** Mahdi Jafari  
**Student ID:** 24B032230  
**GitHub:** Jafari-mahdiCSF

---

## 1. Setup

| | |
| --- | --- |
| Assistant (frozen for the whole lab) | Copilot SDK in VS Code |
| Exact model (or "not displayed") | Chat GPT LUNA 5.6 |
| Three fresh chats for R1, R2, R3? (yes / no) | yes |
| Python version (`python --version`) | Python 3.13.14 |

## 2. Your tool definition — a reason for every constraint

```json
{
  "name": "check_room",
  "description": "Check whether a room can be booked for a requested interval using whole minutes since midnight from 0 to 1440, considering the current time, blocked status, and existing bookings. This tool only reports Available or Unavailable and does not save, create, or modify a booking.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "start": {"type": "integer", "minimum": 0, "maximum": 1440},
      "end": {"type": "integer", "minimum": 0, "maximum": 1440},
      "now": {"type": "integer", "minimum": 0, "maximum": 1440},
      "blocked": {"type": "boolean"},
      "bookings": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "start": {"type": "integer", "minimum": 0, "maximum": 1440},
            "end": {"type": "integer", "minimum": 0, "maximum": 1440}
          },
          "required": ["start", "end"],
          "additionalProperties": false
        }
      }
    },
    "required": ["start", "end", "now", "blocked", "bookings"],
    "additionalProperties": false
  }
}
```

The top-level object constraint prevents a non-object request. Each of the five named properties is
required because the function needs all inputs to decide availability. Integer types prevent strings,
booleans, and fractional minutes. The 0 and 1440 bounds keep times within one day. Boolean `blocked`
prevents text such as `"false"`. `bookings` is an array whose items are objects with required start
and end minutes, while nested `additionalProperties: false` rejects malformed booking pairs. The
top-level `additionalProperties: false` rejects invented fields such as `room`.

## 3. The twelve calls — first run and final run

| Case | First run | Final run | What you changed |
| --- | --- | --- | --- |
| S01 | PASS | PASS | No change; the permissive starter accepted this valid call. |
| S02 | PASS | PASS | No change; an empty bookings array remains valid. |
| S03 | FAIL | PASS | Made `end` an integer instead of an unconstrained value. |
| S04 | FAIL | PASS | Added all five names to `required`. |
| S05 | FAIL | PASS | Added top-level `additionalProperties: false`. |
| S06 | FAIL | PASS | Added minimum 0 to time fields. |
| S07 | FAIL | PASS | Added maximum 1440 to time fields. |
| S08 | FAIL | PASS | Added required nested booking `end`. |
| S09 | FAIL | PASS | Made `blocked` a boolean. |
| S10 | FAIL | PASS | Made time fields integers. |
| S11 | PASS | PASS | Kept maximum 1440 inclusive. |
| S12 | FAIL | PASS | Made each booking item an object with named fields. |

The first run therefore had 9 failed S-cases: S03–S10 and S12.

## 4. Function calling — what the model wrote

### R1

```text
{"name":"check_room","arguments":{"start":600,"end":660,"now":540,"blocked":false,"bookings":[{"start":660,"end":720}]}}
```

Match: yes. The model converted 9:00, 10:00, 11:00, and 12:00 to 540, 600, 660, and 720, and
preserved the touching booking interval.

### R2

```text
{"name":"check_room","arguments":{"start":840,"end":990,"now":810,"blocked":true,"bookings":[]}}
```

Match: yes. The model called the tool even though the room is blocked; that meaning is for canBook
to decide as Unavailable, not for the schema or model to pre-empt.

### R3

```text
What date and exact start and end times should I use for tomorrow afternoon?
```

The request omitted a date that the tool could represent and exact start/end times; it also omitted
the current time, blocked status, and bookings. The model asked a clarification instead of inventing
values, so `calls/r3.txt` is the correct evidence file.

## 5. What the schema cannot check

AC1 is only partly enforceable: the schema can enforce that each time is an integer from 0 through
1440, but the allowed schema keywords cannot compare `start < end` or require `start` to be after
`now`. AC2 cannot be enforced because it compares `end - start` and the schema has no cross-field
arithmetic. AC3 cannot be enforced because the schema can validate that `blocked` is boolean but
cannot require it to be false. AC4 cannot be enforced because overlap is a relationship between
the requested interval and every booking. AC5 cannot be enforced by an input schema because it is a
side-effect guarantee; only the implementation can avoid saving. AC6 is UI feedback behavior, not
input shape.

## 6. Permissions — allow, ask or block

| # | Action | Decision (allow / ask / block) | Reason (the risk, in one sentence or more) |
| --- | --- | --- | --- |
| A1 | call `check_room` with the times the user just typed | allow | This is a read-only availability check, so the main risk is malformed input, which the schema and function can reject. |
| A2 | read `week-08/app/src/booking.ts` | allow | Reading repository code is reversible and low risk, with no external side effect or secret exposure. |
| A3 | edit `booking.ts` to raise the 120-minute limit to 180 | ask | This changes behavior and may violate the established acceptance criterion, so an owner must review the scope and tests first. |
| A4 | run `npm test` in `week-08/app` | allow | Tests are non-destructive validation, although failures should be reported rather than hidden. |
| A5 | `git reset --hard` to undo its own last three edits | ask | The command discards tracked work and could remove useful human changes, so approval and a checkpoint are required. |
| A6 | `git commit` its change on the `week-09` branch | ask | A commit changes shared history and records authorship, so the owner should inspect the diff before approving it. |
| A7 | `git push` to `main` | block | Directly pushing to main bypasses review and can publish unapproved or destructive changes to the shared branch. |
| A8 | send the contents of `.env` to an MCP server it found online | block | This can exfiltrate credentials and private configuration to an untrusted external service. |

## 7. Checkpoint

The checkpoint is the main baseline commit `15126b7` (`Merge pull request #2 from
Jafari-mahdiCSF/week-02`). Before allowing edits I would run:

`git reset --hard 15126b7`

That command returns tracked files and HEAD to the checkpoint, discarding uncommitted tracked
changes and later commits. It does not remove untracked files, so untracked work would need
separate review and cleanup.

## 8. Checker output

```text
PASS  D1    tool/check_room.json exists and is valid JSON
PASS  D2    has name, description and inputSchema
PASS  D3    name is exactly "check_room"
PASS  D4    description: 25+ words, says minutes, 1440, and that it does not save
PASS  D5    inputSchema: an object with exactly the five fields, all required
PASS  D6    inputSchema uses only the keywords listed in README section 5
PASS  S01   the R1 call, valid -> accept
PASS  S02   no existing bookings: bookings = [] -> accept
PASS  S03   end as a string: "11:00" -> refuse
PASS  S04   now missing -> refuse
PASS  S05   an extra field: "room": "204" -> refuse
PASS  S06   start below the day: -30 -> refuse
PASS  S07   end beyond the day: 1500 -> refuse
PASS  S08   a booking with no end: {start: 660} -> refuse
PASS  S09   blocked as a string: "false" -> refuse
PASS  S10   start not a whole minute: 600.5 -> refuse
PASS  S11   end at the end of the day: 1440 -> accept
PASS  S12   a booking as a pair: [660, 720] -> refuse
PASS  F1    calls/r1.json: a call to check_room
PASS  F2    calls/r1.json: arguments valid against your schema
PASS  F3    calls/r1.json: arguments equal the expected ones (README section 5, Part 2)
PASS  F4    calls/r2.json: a call to check_room
PASS  F5    calls/r2.json: arguments valid against your schema
PASS  F6    calls/r2.json: arguments equal the expected ones (README section 5, Part 2)
PASS  F7    calls/r3: exactly one of r3.json (it called) or r3.txt (it asked), not empty
PASS  L1    section 5 names at least two acceptance criteria (AC1-AC6) the schema cannot check
PASS  L2    section 6: A1-A8 each have allow / ask / block and a reason of 5+ words
PASS  L3    section 7 names the checkpoint commit (a SHA)
PASS  L4    section 10: a conclusion of 80-150 words
PASS  L5    AI_USAGE.md filled in (a tool row, and signed)

SUMMARY: 30 PASS · 0 FAIL · 0 ERROR  (of 30 checks)
Paste this whole output into lab-report.md section 8, and these three numbers into submission.yml.
```

## 9. What still fails

None. The final checker run has no failed or errored checks.

## 10. Conclusion (80–150 words)

This exercise separated three different responsibilities. The schema rejected S03 because `end` was
a string, S05 because `room` was an extra property, and S12 because a booking was not an object;
those are shape checks. It could not express that `start` must be before `end`, that a request is no
longer than 120 minutes, or that bookings do not overlap, so those rules remain in `canBook`.
Function calling added another risk: R2 still had to be called even though `blocked: true` means the
function should return Unavailable. For R3, the model asked for missing information rather than
inventing times. Finally, permissions showed that a read-only test is safer than editing behavior,
and sending `.env` must be blocked because tool access does not justify secret disclosure.
