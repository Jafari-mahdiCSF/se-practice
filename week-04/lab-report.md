# Week 04 — Lab report: Modeling the System with UML

## 1. Setup

| Field | Value |
| --- | --- |
| Name | Mahdi Jafari |
| Group | Individual |
| AI assistant | Copilot SDK in VS Code |
| Exact model | GPT-5 (Copilot SDK) |
| Renderer | PlantUML web server |
| Behaviour diagram | sequence |
| Stories used | the reference set from README §3 |

## 2. Prompts as sent

### 2.1 Task 1 — use-case prompt

```text
Using the supplied scenario and approved stories, generate PlantUML for a use-case diagram. Include Student and Administrator outside a named system boundary. Model their goals, show justified associations, and list assumptions. Use include or extend only with a clear reason.
```

### 2.2 Task 2 — class prompt

```text
Create a UML domain class diagram in PlantUML for Smart Campus. Start with Student, Room, and Booking. Add attributes, appropriate operations, and association multiplicities. Add other classes only when requirements justify them. Explain each relationship and list assumptions. Avoid unjustified inheritance or composition.
```

### 2.3 Task 3 — behaviour prompt (3A sequence)

```text
Generate PlantUML for Book room. Use Student, BookingService, and BookingRepository lifelines. Validate the supplied rules, then attempt the reservation. Show a successful confirmation and an unavailable-room alternative using alt. Label messages and replies. Explain new design components and all assumptions.
```

### 2.4 Focused correction prompts

```text
none
```

### 2.5 Critique prompt

```text
Compare my diagrams with the requirements. Identify missing rules, inconsistent names, and unjustified elements. Cite each issue and propose a specific correction.
```

## 3. Task 1 — use-case review

**Assumptions the AI listed:** The original draft listed no assumptions; I treated that as a finding and documented explicit assumptions in the class review.

| # | Element | Problem | Rule or story | Fix |
| --- | --- | --- | --- | --- |
| 1 | `Student --> Send confirmation` | Confirmation is an outcome, not a student goal. | R4 says a successful booking produces a confirmation. | Removed the actor association and retained confirmation as an included outcome of booking. |
| 2 | `Book room ..> Send confirmation` | The relationship had no explanation of why inclusion was appropriate. | R4 and US-01 make confirmation part of successful booking. | Added the directly preceding `why` comment explaining the inclusion. |
| 3 | `Administrator --> Review usage` | The original did not clearly distinguish administrator-only responsibilities from student goals. | US-06 assigns usage review to administrators. | Kept only the Administrator association for `Review usage` and documented the responsibility. |

## 4. Task 2 — class diagram review

### 4.1 Relationships, read both ways

| Association | Read left → right | Read right → left | Multiplicities |
| --- | --- | --- | --- |
| `Student — Booking` | One student makes zero or more bookings. | Each booking belongs to exactly one student. | `1 / 0..*` |
| `Room — Booking` | One room hosts zero or more bookings. | Each booking is for exactly one room. | `1 / 0..*` |

### 4.2 Constraints the multiplicities cannot show

- R2: A note on `Booking` states that active bookings for the same room must not overlap; multiplicity cannot express this temporal constraint.
- R1: `Booking.start` and `Booking.end` represent a future interval whose duration is greater than zero and at most two hours; the exact validation is shown in the sequence diagram.
- R3: `Room.blocked` records whether a room can accept new bookings; the decision is shown in the sequence diagram.

### 4.3 Assumptions

- A1: Touching bookings, where one ends at 14:00 and another starts at 14:00, are allowed because they do not overlap.
- A2: When a booked room is blocked, existing bookings are kept; blocking prevents new bookings and does not retroactively cancel reservations.

### 4.4 Findings

| # | Element | Problem | Rule or story | Fix |
| --- | --- | --- | --- | --- |
| 1 | `Student "1" -- "1..*" Booking` and `Room "1" -- "1..*" Booking` | `1..*` incorrectly requires every student and room to have a booking. | The scenario permits students and rooms with no bookings; the required relationship is one-to-zero-or-many. | Changed both booking ends to `0..*` and retained `1` at the Student and Room ends. |
| 2 | Missing Booking constraint note | Multiplicities cannot express temporal overlap. | R2 prohibits overlapping active bookings for the same room. | Added an explicit R2 note beside `Booking`. |

## 5. Task 3 — behaviour diagram review

**Option chosen and why:** 3A sequence, because it makes validation order, failure branches, persistence, and confirmation explicit.

**Design components added beyond the domain model:** `BookingService` validates R1–R3 and coordinates the booking; `BookingRepository` retrieves room and booking data and persists only a successful booking.

| # | Element | Problem | Rule or story | Fix |
| --- | --- | --- | --- | --- |
| 1 | `BookingService -> BookingRepository : save(booking)` before validation | The original saved immediately and had no failure branch, so an invalid or blocked request could be persisted. | R1 and R3 must be checked before reservation; R2 also prevents conflicts. | Added validation before creation, guarded `alt` branches, overlap checking, and no save in failure branches. |
| 2 | Missing R1 and R3 checks | The original did not show time validity or blocked-room handling. | R1 limits the future duration and R3 rejects blocked rooms. | Added `validateTimeRange(R1)` and `checkBlocked(R3)` with an explanatory note. |

## 6. AI critique

| # | Issue the AI raised | Element it cited | Verdict | Why |
| --- | --- | --- | --- | --- |
| 1 | R2 should be visible in the domain model rather than only in the sequence. | `Booking` note | accept | The note explicitly states the no-overlap constraint, while `checkOverlap(R2)` operationalizes it. |
| 2 | Confirmation should be associated directly with Student to show that the student receives it. | `Send confirmation` | reject | R4 defines confirmation as an outcome, not a user goal; the revised use-case diagram correctly uses an include from `Book room` without an actor association. |
| 3 | The sequence should save before checking availability so the request is not lost. | `save(booking)` | reject | Saving before R1–R3 checks violates the scenario and could create invalid or conflicting bookings. |
| 4 | `BookingService` and `BookingRepository` do not belong in the domain class diagram. | sequence lifelines | accept | They are design components used only in the behaviour diagram and are explained in §5, while the class diagram contains domain concepts only. |

## 7. Consistency table

| Requirement / story | Use case | Classes | Behaviour element |
| --- | --- | --- | --- |
| R1 | `Book room` | `Booking.start`, `Booking.end` | `validateTimeRange(R1)` and the R1 note |
| R2 | `Book room` | `Booking`, R2 note | `checkOverlap(R2)` and `alt overlap conflict` / `available slot` |
| R3 | `Book room` | `Room.blocked` | `checkBlocked(R3)` and blocked-room branch |
| R4 | `Book room` | `Booking` | confirmation reply after save |
| US-01 | `Book room` | `Student`, `Booking`, `Room` | `bookRoom(studentId, roomId, start, end)` |
| US-02 | `View availability` | `Room`, `Booking` | availability is represented by room and active-booking data |
| US-03 | `Cancel booking` | `Booking`, `Student` | cancellation is a status change outside the Book room interaction |
| US-04 | `Block / unblock room` | `Room.blocked` | administrator changes blocked status |
| US-05 | `Block / unblock room` | `Room.blocked` | administrator reverses blocked status |
| US-06 | `Review usage` | `Room`, `Booking` | administrator reviews booking records |
| US-01 | `Send confirmation` | `Booking` | included confirmation outcome of `Book room` |

## 8. Change log

| # | Diagram | Before (AI's original) | After (your revision) | Reason |
| --- | --- | --- | --- | --- |
| 1 | use case | Student was linked to `Send confirmation`; the include had no rationale. | Student is linked only to student goals, and `Book room` includes confirmation with a `why` comment. | R4 treats confirmation as a booking outcome, not a separate user goal. |
| 2 | class | Booking multiplicities were `1..*`, with no attributes or R2 note. | Student/Room to Booking are `1` to `0..*`, required attributes are present, and Booking has the R2 note. | Corrects relationship semantics and makes required constraints visible. |
| 3 | sequence | The original saved a booking without validation or alternatives. | R1, R3, and R2 are checked before save, with guarded success and rejection branches. | Prevents invalid, blocked, or overlapping bookings and shows R4 confirmation. |

## 9. Checker output

```text
Week 04 structural check - shape only, never quality

UC1  PASS  Student and Administrator declared
UC2  PASS  named system boundary: "Smart Campus booking system"
UC3  PASS  all actors declared outside the boundary
UC4  PASS  all scenario goals present (6 use cases)
UC5  PASS  no actor is associated with a confirmation use case
UC6  PASS  actor responsibilities match the scenario
UC7  PASS  use cases are goals, not screens or components
UC8  PASS  every include / extend / generalization carries a ' why: comment (or there are none)
UC9  PASS  revised diagram differs from the AI's original
CL1  PASS  Student, Room and Booking present
CL2  PASS  Booking is associated with Student and with Room
CL3  PASS  every association has multiplicities at both ends
CL4  PASS  1 student / 1 room per booking, 0..* bookings per student and per room
CL5  PASS  every inheritance / composition / aggregation carries a ' why: comment (or there are none)
CL6  PASS  only domain concepts in the class diagram
CL7  PASS  attributes needed by R1-R3 are present
CL8  PASS  a note states R2 (no overlapping active bookings)
SQ1  PASS  Student, BookingService and BookingRepository lifelines present
SQ2  PASS  alt block with a guard on every branch (4 branches)
SQ3  PASS  validation happens before creation
SQ4  PASS  nothing is saved on a failure branch
SQ5  PASS  every message is labelled
SQ6  PASS  R1 (time range) is visible - checked or stated as a precondition
SQ7  PASS  R3 (blocked room) is visible
FI1  PASS  the AI's original output is kept for every diagram
FI2  PASS  a rendered image for every diagram
LR1  PASS  §1 setup filled (tool and model recorded)
LR2  PASS  5 prompts pasted in §2
LR3  PASS  3 use-case findings in §3
LR4  PASS  §4 relationships read both ways, 2 assumption(s) declared
LR5  PASS  2 behaviour-diagram findings in §5
LR6  PASS  4 critique issues with a verdict
LR7  PASS  3 change-log rows covering all three diagrams
CS1  PASS  6 approved stories
CS2  PASS  §7 traces R1-R4 into the diagrams
CS3  PASS  every use case traces to an approved story
CS4  PASS  every lifeline is a domain class or an explained design component

SUMMARY pass=37 fail=0 error=0
A FAIL you report and explain in lab-report.md §9 costs you nothing. One you hide costs the criterion.
```

**FAILs I am keeping, and why:** none

## 10. Conclusion (120–180 words)

The AI got the first use-case draft most wrong because it treated “Send confirmation” as an actor goal and linked Student directly to it. That would have encouraged a separate confirmation interaction instead of modeling confirmation as the outcome of a successful booking under R4. The first class draft also used `1..*` at the Booking ends, which says every student and every room must already have at least one booking; that is inconsistent with availability and empty schedules. The sequence draft was the most dangerous implementation-wise: it saved a booking before validating time, blocked-room status, or overlap, and it had no rejection path. The revised sequence makes the order explicit and saves only after all checks pass. The critique correctly reinforced the need for an R2 note and for keeping design components out of the domain model. It incorrectly suggested directly associating confirmation with Student; I rejected that claim because confirmation is an outcome of booking, not an independent goal. The final diagrams now trace every rule and approved story.
