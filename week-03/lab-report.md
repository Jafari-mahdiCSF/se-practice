# Lab report — Practice #03, Requirements Engineering with AI

Name: Mahdi Jafari  
Student ID: 24B032230  
GitHub username: Jafari-mahdiCSF

---

## 1. Setup

| | |
| --- | --- |
| AI assistant (tool) | Copilot SDK in VS Code |
| Exact model name and version | GPT-6 Luna |
| Date of the session | 2026-09-25 |
| Diagram renderer used | PlantUML web renderer |

One tool and one model were used for all three prompts.

## 2. Original AI output — user stories (Part 1)

The following is the complete response generated for Prompt 1 before review:

```
US-01 As a Student, I want to see available study rooms and time slots, so that I can choose a room for individual or group study. Priority: High. Assumption: availability is based on current reservations.
US-02 As a Student, I want to reserve an available room, so that I can study at a planned time. Priority: High. Assumption: the selected time is in the future.
US-03 As a Student, I want to cancel my reservation, so that another student can use the room. Priority: Medium. Assumption: a student can cancel only their own reservation.
US-04 As an Administrator, I want to block or unblock rooms, so that rooms remain usable and their availability is accurate. Priority: High. Assumption: administrators can change room status.
US-05 As an Administrator, I want to review room usage, so that I can understand demand over time. Priority: Low. Assumption: usage is available for a selected period.
US-06 As a Student, I want confirmation after a booking change, so that I know the action succeeded. Priority: Medium. Assumption: confirmation follows a successful booking or cancellation.
US-07 As a Student, I want SMS reminders before my booking, so that I do not forget it. Priority: Low. Assumption: the campus provides a notification service.
```

## 3. Story review (Part 2)

| Story (as generated) | What I did | Why | Final ID |
| --- | --- | --- | --- |
| View available rooms and time slots | Kept and clarified the search result | It names a Student, one outcome, and a testable availability result | US-01 |
| Reserve an available room | Kept and added the future-slot constraint | It is a core function and must reflect R1–R3 | US-02 |
| Cancel my reservation | Kept and clarified ownership | It is a defined use case and is small enough to test | US-03 |
| Block or unblock rooms | Kept and changed the reason to room availability accuracy | It is an Administrator responsibility in the scenario | US-04 |
| Review room usage | Kept and clarified the reporting period | It maps directly to UC-05 without adding implementation detail | US-05 |
| Confirmation after a booking change | Kept and aligned it with UC-06 | It describes the student’s desired outcome without adding a delivery channel | US-06 |
| SMS reminders before a booking | Deleted | Notifications beyond confirmation are explicitly out of scope | none |

**Did the assistant invent anything outside the scenario?** Yes. The SMS reminder in the generated
US-07 was outside scope. I removed it rather than introducing a new actor or function. I also
checked that the final stories contain no payments, attendance, equipment, account, waiting-list,
or implementation concerns.

**How many stories did you end with, and why that number?** Six. They cover each of the six fixed
use cases once, remain within the two allowed roles, and avoid the generated out-of-scope reminder.

## 4. Original AI output — acceptance criteria (Part 3)

```
Assumptions:
- A booking ending when another begins does not overlap.
- Exactly two hours is allowed.

US-01:
AC-01 Given a future period, when a student searches, then available rooms are listed.
AC-02 Given an overlapping booking, when a student searches, then the room is unavailable.
AC-03 Given a past period, when a student searches, then the request is rejected.

US-02:
AC-04 Given an available room and future two-hour period, when the student books, then the booking is recorded.
AC-05 Given a period longer than two hours, when the student books, then the booking is rejected.
AC-06 Given an overlapping booking, when the student books, then the new booking is rejected.

US-04:
AC-07 Given an unblocked room, when an administrator blocks it, then it is unavailable.
AC-08 Given a blocked room, when a student books it, then the booking is rejected.
AC-09 Given a blocked room, when an administrator unblocks it, then it can be booked.
```

## 5. Criteria review (Part 3)

| Criterion (as generated) | Problem | What I changed it to | Final ID |
| --- | --- | --- | --- |
| Future availability is listed | The actor and observable result were abbreviated | Added explicit student action and room filtering | AC-01 |
| Overlapping room is unavailable | It did not say the booking must be for the same room | Specified the same room and requested period | AC-02 |
| Past period is rejected | The rule was correct but the reason was not observable | Added an explanation that the period must be future | AC-03 |
| Available two-hour room is booked | It did not state that the room is unblocked | Added unblocked status and exact boundary | AC-04 |
| Over-two-hour booking is rejected | It omitted the no-recording result | Added that no reservation is created | AC-05 |
| Overlap is rejected | It omitted preservation of the existing booking | Added the unchanged existing reservation result | AC-06 |
| Block and unblock behaviors | The generated criteria were usable but terse | Added administrator action and resulting eligibility | AC-07, AC-08, AC-09 |

**The two open questions.**

| Question | My decision | Why |
| --- | --- | --- |
| A booking ending exactly when another begins — overlap under R3? | allowed | The intervals share no occupied time, so adjacent bookings can coexist. |
| Is exactly two hours allowed under R2? | allowed | R2 says “at most two hours,” so the boundary is inclusive. |

**Which invalid or boundary case did the assistant leave out?** The raw response did not explicitly
state the exact adjacency boundary or that a blocked room remains unavailable after a rejected
attempt. I made both outcomes explicit in the assumptions and final criteria.

## 6. Original AI output — use-case diagram (Part 4)

```
@startuml
actor Student
actor Administrator
actor System
rectangle "Smart Campus study room booking" {
  usecase "View availability" as UC01
  usecase "Book room" as UC02
  usecase "Cancel booking" as UC03
  usecase "Block or unblock room" as UC04
  usecase "Review usage" as UC05
  usecase "Send confirmation" as UC06
}
Student --> UC01
Student --> UC02
Student --> UC03
Student --> UC05
Administrator --> UC04
Administrator --> UC05
Student --> UC06
System --> UC06
@enduml
```

Rendered diagram (image, or a link): [final PlantUML source](requirements/use-cases.puml)

## 7. Diagram review (Part 4)

| Element | Problem | What I changed |
| --- | --- | --- |
| `System` actor | It is an internal concept, not one of the two scenario actors | Removed it |
| Student → Review usage | Students do not perform the administrator usage-review function | Removed the association |
| Student → Send confirmation | A person does not trigger the system confirmation function | Removed the association |
| Administrator and six use cases | These were in scope | Kept them and retained only justified links |

**Associations.** The generated Student → Review usage and Student → Send confirmation links were
not person-triggered responsibilities. The System actor was also invalid. The final diagram connects
Student to availability, booking, and cancellation, and Administrator to room status and usage.

**Did any screen, database or internal component appear as a use case or an actor?** The raw output
included the invalid System actor but no screen or database. The final diagram contains neither.

## 8. Traceability (Part 5)

- Use cases with **no story** behind them: none.
- Stories with **no use case** they belong to: none.
- Criteria that test **no rule** from section 1: none; each criterion is attached to a selected story
  and tests an availability, booking, duration, overlap, future-start, or blocked-room behavior.

The largest gap is not story coverage but criteria coverage: UC-03, UC-05, and UC-06 have stories
but no acceptance-criteria set because the assignment limits the selected set to three stories.
That means the generated requirements still need tests for cancellation, usage review, and
confirmation before implementation is complete.

## 9. Checker runs

```
$ python tests/check_requirements.py
PASS   US-1  user-stories.md         no placeholders left
PASS   US-2  user-stories.md         6 stories, IDs US-01…US-06
PASS   US-3  user-stories.md         every story has the required sentence shape
PASS   US-4  user-stories.md         every story has a priority
PASS   US-5  user-stories.md         every story declares an assumption
PASS   US-6  user-stories.md         only Student and Administrator appear as roles
PASS   US-7  user-stories.md         nothing from the out-of-scope list appears
PASS   AC-1  acceptance-criteria.md  no placeholders left
PASS   AC-2  acceptance-criteria.md  three sections, all naming real stories: US-01, US-02, US-04
PASS   AC-3  acceptance-criteria.md  every section has 3 to 5 uniquely numbered criteria
PASS   AC-4  acceptance-criteria.md  all 9 criteria are complete Given/When/Then
PASS   AC-5  acceptance-criteria.md  every section covers an invalid or boundary case
PASS   AC-6  acceptance-criteria.md  3 assumptions listed before the criteria
PASS   AC-7  acceptance-criteria.md  both open questions are settled in the assumptions
PASS   PU-1  use-cases.puml          valid PlantUML block, no placeholders
PASS   PU-2  use-cases.puml          exactly two actors: Student, Administrator
PASS   PU-3  use-cases.puml          all six use cases present
PASS   PU-4  use-cases.puml          system boundary present
PASS   PU-5  use-cases.puml          no screens, databases or internal components
PASS   PU-6  use-cases.puml          no unjustified actor associations found
PASS   TR-1  traceability.md         all six use cases have a row
PASS   TR-2  traceability.md         every ID in the table resolves
PASS   TR-3  traceability.md         every story appears in the table
------------------------------------------------------------------------
23 PASS — 0 FAIL — 0 ERROR   (23 checks)
```

```
$ python tests/validate_submission.py
Shape is clean. This says nothing about whether the requirements are good.
```

| | PASS | FAIL | ERROR |
| --- | --- | --- | --- |
| `check_requirements.py` | 23 | 0 | 0 |

Commit these numbers were produced at (`git rev-parse --short HEAD`): `05b8795`.

Every FAIL, one line each: the first run found two leftover template TODO words in the instructional
text of `user-stories.md`; I removed that instructional line and reran the checker successfully.

**Did you run the checks by hand instead of with Python?** No.

## 10. Conclusion (150–200 words)

The most wrong generated requirement was the use-case diagram: it added a System actor and linked
Student to Review usage and Send confirmation. I would have caught this without a checker by walking
each association back to the two actor definitions and asking who actually initiates the function.
The assistant got the core six-function structure right, especially the booking rules and the
three useful invalid cases; producing a complete first draft of those criteria by hand would have
taken noticeably longer. The biggest remaining weakness is not a missing story but missing tests:
UC-03, UC-05, and UC-06 are represented in traceability, yet the selected criteria cover only
US-01, US-02, and US-04. If these requirements were handed to an implementer who would not be in
the room, I would rewrite US-06 first. “Confirm my booking or cancellation” is valuable but does
not define what information makes a confirmation observable or how cancellation confirmation should
be distinguished from booking confirmation. I would add explicit acceptance criteria for both
outcomes while preserving the rule that the system, rather than a person, sends the confirmation.
The review therefore matters more than the green structural checker: the checker verifies shape,
while traceability and actor review expose omissions that could otherwise survive into implementation.
