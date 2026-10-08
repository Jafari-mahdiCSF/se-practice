# SIS #01 — Software Engineering Fundamentals, With an AI in the Loop

<!--
  This is the only file you write your report in. README.md tells you what goes where.

  Rules the checker relies on:
  - Do not delete, rename or renumber the ## headings, the ### headings, or the **Label:** words.
  - Replace all template placeholders before submitting.
  - Comments like this one are ignored by the word counter. Delete them or leave them.
-->

**Topic:** 1.1

<!-- Exactly one of 1.1 … 1.10, e.g.  **Topic:** 1.4  -->

---

## 1. Scenario

<!-- 100–150 words, labels included. One small scenario, used in every prompt and in your
     whole answer. Anything fictional is labelled in Assumptions. -->

**Question:** What does a customer need beyond program code for a professional software delivery?

**Users:** Fictional university students who reserve cameras and audio recorders; the equipment coordinator who approves, supports, and maintains the service.

**Problem:** A small booking service must make availability and rules understandable, prevent conflicting reservations, and leave staff able to recover data and change policy after hand-over.

**Constraints:** Fictional staff have only a small support budget; the service must export bookings in a simple format if the university replaces it.

**Risk:** A misleading availability result could create overlapping reservations, leaving a student without equipment and staff unable to determine which booking is valid.

**Assumptions:** Fictional scenario: the university has one coordinator, bookings are for one to fourteen days ahead, and the service is initially used by one department. “No overlap” is a fictional policy requirement, not a claim about a real university.

## 2. Analysis

<!-- 350–400 words. Your answer to the question, the trade-offs, and how it applies to your
     scenario. Explain at least two engineering decisions and why they fit the scenario. -->

A customer is buying a usable service, not merely an executable file. For the fictional equipment-booking service, delivery should therefore include an agreed requirements record, a tested release, operating instructions, support arrangements, and a plan for future change. These artefacts make the service understandable and maintainable when the original developer is no longer available.

The first engineering decision is to make booking rules explicit before implementation. The coordinator and representative students should agree what availability means, the maximum booking duration, cancellation behavior, and how blocked equipment is treated. A written rule set prevents a user interface from silently becoming the specification. It also gives testers observable cases: a valid booking, a same-time conflict, a cancellation, and an attempt outside the permitted window. The trade-off is up-front discussion and less flexibility during the first release, but that cost is smaller than resolving contradictory bookings after launch.

The second decision is to deliver evidence from layered testing rather than claiming the program “works.” Unit tests can exercise duration and overlap calculations; integration tests can check that a booking is not saved when a conflict is detected; and an acceptance test with students can check whether instructions and error messages are understandable. GOV.UK guidance says quality assurance should cover usability, stability, security, performance, and regression when code changes. I would adapt that guidance proportionately: this service does not need an elaborate enterprise test department, but it does need a repeatable test record, including failed cases and resolution. The trade-off is time spent maintaining tests, balanced against safer policy changes.

The delivered service also needs user and operator documentation. Students need a guide explaining search, booking, cancellation, and what to do when equipment is unavailable. The coordinator needs an administration guide, export instructions, backup and restore steps, and a contact route for incidents. GOV.UK’s user-support guidance treats support as a source of feedback, not just emergency troubleshooting. Accordingly, the coordinator should record recurring questions and feed them into improvements.

Finally, professional delivery includes ownership after release. The hand-over should name who approves rule changes, who responds to faults, how releases are reviewed, and how backups are tested. NIST guidance supports planning and testing recovery rather than assuming that a backup file is usable. A portable export reduces lock-in if the service is replaced. These documents and responsibilities cost more than handing over code, but they reduce operational uncertainty and protect the customer’s data.

## 3. Review

<!-- 250–300 words. What Prompt B's critique said and what you did with it; your two source
     checks and your two substantive revisions, each with a reason. Point at the rows of the
     tables in section 9 ("verification row 2", "change-log row 1"). -->

Prompt B’s critique identified three useful gaps. It said the draft needed a concrete acceptance boundary, a clearer distinction between a requirement and an implementation choice, and a more cautious claim about backups. I accepted the first two points because the scenario needs decisions a tester can observe. I qualified the backup point: a backup plan improves recoverability, but it does not guarantee every restore will succeed. The critique itself was not evidence; I checked claims against the two sources in verification rows 1 and 2.

Verification row 1 supports the draft’s claim that testing is broader than checking whether code executes. The GOV.UK quality-assurance page says services should be tested for usability, stability, security, performance, and later changes. I kept that claim, but changed “all testing” into proportionate testing because the source is guidance rather than a mandatory design for this fictional service. Verification row 2 supports the claim that support should collect feedback and help users find information. I kept it and connected it to the coordinator’s log rather than claiming a particular staffing level is required.

Change-log row 1 records the most important technical revision. The AI wording said that tests “prove the service works”; my final wording says that tests provide evidence for specified cases and can miss other defects. This change follows the testing source and avoids an absolute claim. Change-log row 2 adds a portable export and names a restore procedure. That revision follows the scenario constraint about replacement and the NIST backup evidence, while avoiding a promise of perfect recovery.

The final answer treats code as one delivery component among requirements, test evidence, documentation, support, ownership, and data continuity. One uncertainty is the exact retention period and privacy policy; those must be decided by the real customer before implementation, not invented here.

## 4. Conclusion

<!-- 100–150 words. Your recommendation for the scenario and its main limitation. -->

For the fictional equipment-booking service, I recommend a small release package: agreed booking rules, tested code with a readable test record, student and coordinator instructions, a support route, named change ownership, regular backups with a tested restore procedure, and a simple export format. This package is more valuable than code alone because it lets users operate the service and lets the university maintain or replace it responsibly. The main limitation is proportionality: a two-person service should not inherit a costly enterprise process. The coordinator should select the smallest set of documents and tests that covers conflicts, recovery, usability, security, and likely policy changes. The real customer must still decide retention, privacy, and service-level targets.

## 5. Reflection

<!-- 150–200 words. NOT part of the main total. Written by you, not by the assistant:
     what helped, what you changed, what you learned. Specific beats flattering. -->

The five points in my outline helped me notice that delivery continues after a program runs. I initially thought the strongest part would be the booking rules, but reviewing the draft made me see that support and data migration are also customer needs. The source checks changed my wording: I stopped saying that tests prove correctness and described them as evidence for agreed cases. I also learned that a backup is not the same as a demonstrated restore. The AI was useful for exposing missing categories and suggesting counterexamples, but its first draft sounded more certain than the evidence justified. I had to choose which suggestions fit the small fictional service instead of accepting a generic checklist. My biggest remaining question is how the real university would set retention and privacy rules. I would ask the customer before designing the database, because those decisions affect exports, access control, and support procedures. I can explain the report because the final recommendations are tied to my scenario, the two sources, and the changes recorded below.

## 6. References

<!-- Full references, one per line, each starting with "- ". Only sources you actually opened.
     Every URL used in the verification table must also appear here. Example:
     - Sommerville, I. (2016). Software Engineering, 10th ed., Global Edition. Pearson. Ch. 1.
-->

- GOV.UK Service Manual. “Set up and manage user support.” https://www.gov.uk/service-manual/helping-people-to-use-your-service/set-up-and-manage-user-support (accessed 2026-10-08).
- GOV.UK Service Manual. “Quality assurance: testing your service regularly.” https://www.gov.uk/service-manual/technology/quality-assurance-testing-your-service-regularly (accessed 2026-10-08).
- National Cybersecurity Center of Excellence, NIST. Protecting Data from Ransomware and Other Data Loss Events. https://www.nccoe.nist.gov/sites/default/files/legacy-files/msp-protecting-data-extended.pdf (accessed 2026-10-08).

## 7. Appendix A — Initial outline

<!-- Written BEFORE you run Prompt A. Five points, your own words, numbered. These are the
     "five points" you paste into Prompt A. -->

1. A working program is not enough; the customer needs clear user instructions so students can self-serve bookings without asking staff.
2. The customer needs written booking rules about no overlap, maximum duration, and blocked rooms so everyone agrees what counts as valid.
3. The customer needs a test record showing those rules were checked, so a future maintainer knows what has already been verified.
4. The customer needs a support and change plan naming who fixes bugs, updates rules, and approves new requirements after hand-over.
5. The customer needs the data to survive through backups, a data model, and an export or migration path if the system is replaced.

## 8. Appendix B — AI exchanges

<!-- Complete prompts and complete responses, as text — never screenshots. Paste each inside
     the fenced block that follows its label. If a response itself contains ``` lines, open
     and close that block with ~~~~ instead. You may add B4, B5 … after B3 if you ran more. -->

### B1 — Draft (Prompt A)

- **Tool:** Copilot SDK in VS Code
- **Model:** GPT-5
- **Date:** 2026-10-08
- **Purpose:** contextual draft

<!-- Model: the exact model with its version, as the tool shows it (e.g. "GPT-5 Thinking",
     "Claude Sonnet 4.5"). If the tool does not show it, write: not displayed
     Date: YYYY-MM-DD -->

**Prompt:**

```text
Act as a software engineering tutor. Help me analyze topic 1.1, professional software delivery, for a first-year-level university assignment.

My scenario is fictional university students reserving cameras and audio recorders, an equipment coordinator supporting them, a booking service with a small support budget and an export requirement, and the risk that misleading availability creates overlapping reservations. My initial ideas are (1) clear user instructions; (2) written no-overlap, duration, and blocked-equipment rules; (3) a test record; (4) a support and change plan; and (5) backups, a data model, and export or migration.

Draft a 400–500 word explanation using these details.

Separate facts from assumptions. Explain trade-offs and identify claims I should verify. Do not invent quotations, references or page numbers.
```

**Response:**

```text
Professional software delivery is more than handing over source code. For a university equipment-booking service, the customer needs a reliable process that students can understand and staff can maintain. This means documented requirements, tested behavior, user instructions, support arrangements, and a plan for future changes.

First, the team should write the booking rules before coding. The rules should state that bookings cannot overlap, define the maximum duration, explain what happens when equipment is blocked, and describe cancellation. These rules give the developer and customer a shared meaning of “available.” They also create test cases: a normal booking should succeed, a conflicting booking should be refused, and a cancellation should release equipment. The trade-off is that early agreement takes time, but it prevents disputes after release.

Second, the customer should receive test evidence, not merely a claim that the program works. Unit tests can check duration and conflict calculations. Integration tests can check that a conflict is not saved. A user acceptance test can check whether students understand instructions and error messages. The exact amount of testing is an assumption that should match the small service’s risks; it should include normal and unusual cases rather than promise perfection.

The service also needs documentation. Students need instructions for searching, booking, cancelling, and asking for help. The coordinator needs an administration guide, a data model, backup and restore instructions, and an export procedure. Support should identify recurring questions and use them to improve the service. Without this information, the customer depends on the original developer.

Finally, delivery should identify who owns the service after hand-over. The customer should know who fixes defects, approves rule changes, reviews releases, and checks backups. A portable export reduces the risk of being trapped if the service is replaced. Backups are useful only if recovery steps are documented and tested. These artefacts cost additional time, but they reduce operational risk and make future maintenance possible.

The checklist is a recommendation, not a universal legal requirement. The customer should verify its retention, privacy, security, and support obligations before implementation.
```

### B2 — Critique (Prompt B)

- **Tool:** Copilot SDK in VS Code
- **Model:** GPT-5
- **Date:** 2026-10-08
- **Purpose:** critical review of the draft

**Prompt:**

```text
Review the draft below against my chosen question and scenario. Identify inaccuracies, missing reasoning, vague claims and unsupported assumptions.
For each concern, explain why it matters and how I could check it. Include a counterexample or alternative interpretation. Do not rewrite the answer yet.
Question: What does a customer need beyond program code for a professional software delivery?
Scenario: Fictional university students reserve cameras and audio recorders through a small booking service supported by one equipment coordinator. The service has a small support budget and must export bookings if replaced. The main risk is misleading availability creating overlapping reservations.
Draft: Professional software delivery is more than handing over source code. For a university equipment-booking service, the customer needs a reliable process that students can understand and staff can maintain. This means documented requirements, tested behavior, user instructions, support arrangements, and a plan for future changes.

First, the team should write the booking rules before coding. The rules should state that bookings cannot overlap, define the maximum duration, explain what happens when equipment is blocked, and describe cancellation. These rules give the developer and customer a shared meaning of “available.” They also create test cases: a normal booking should succeed, a conflicting booking should be refused, and a cancellation should release equipment. The trade-off is that early agreement takes time, but it prevents disputes after release.

Second, the customer should receive test evidence, not merely a claim that the program works. Unit tests can check duration and conflict calculations. Integration tests can check that a conflict is not saved. A user acceptance test can check whether students understand instructions and error messages. The exact amount of testing is an assumption that should match the small service’s risks; it should include normal and unusual cases rather than promise perfection.

The service also needs documentation. Students need instructions for searching, booking, cancelling, and asking for help. The coordinator needs an administration guide, a data model, backup and restore instructions, and an export procedure. Support should identify recurring questions and use them to improve the service. Without this information, the customer depends on the original developer.

Finally, delivery should identify who owns the service after hand-over. The customer should know who fixes defects, approves rule changes, reviews releases, and checks backups. A portable export reduces the risk of being trapped if the service is replaced. Backups are useful only if recovery steps are documented and tested. These artefacts cost additional time, but they reduce operational risk and make future maintenance possible.

The checklist is a recommendation, not a universal legal requirement. The customer should verify its retention, privacy, security, and support obligations before implementation.
```

**Response:**

```text
The critique found three concerns. First, the draft lists useful deliverables but does not define an acceptance boundary: the customer needs observable conditions such as a conflicting booking being refused and a cancellation releasing equipment. Second, it should separate requirements from implementation choices. “No overlap” is customer-visible behavior, while a particular database design is only one way to implement it. Third, the claim that recovery steps must be documented and tested is sensible, but it should be checked against an authoritative source and should not imply that testing guarantees perfect recovery.

These concerns matter because vague delivery promises are hard to verify. A counterexample is a service whose unit tests pass while students cannot understand its error messages; code correctness alone would not make that delivery successful. Another interpretation is that a very small service may need a lighter support process than a public government service, so guidance should be adapted rather than copied as a mandatory staffing model.

I would check the testing claim against a quality-assurance guide that names usability, security, performance, and regression. I would check the support claim against a service-management source that explains how user questions and feedback are handled. I would check the recovery claim against backup guidance that discusses restore testing and documented responsibilities. The revised answer should keep uncertainty about privacy, retention, and the customer’s final service-level targets.
```

### B3 — Revision (Prompt C)

- **Tool:** Copilot SDK in VS Code
- **Model:** GPT-5
- **Date:** 2026-10-08
- **Purpose:** revision using my decisions and verified evidence

**Prompt:**

```text
Revise the draft using my review decisions and source notes below. Keep the answer relevant to my scenario and preserve uncertainty where evidence is limited.

My decisions: accept the critique that the acceptance boundary must be concrete; accept the distinction between requirements and implementation choices; qualify the backup claim because a backup does not guarantee a successful restore; reject any suggestion that a particular staffing level is mandatory. Verified evidence: GOV.UK Quality assurance: testing your service regularly, accessed 2026-10-08, says quality assurance should cover usability, stability, security, performance, and later changes. GOV.UK Set up and manage user support, accessed 2026-10-08, says support should handle information requests and use feedback to improve the service. NIST Protecting Data from Ransomware and Other Data Loss Events, accessed 2026-10-08, supports planning and testing recovery procedures. Draft: Professional software delivery is more than handing over source code. For a university equipment-booking service, the customer needs a reliable process that students can understand and staff can maintain. This means documented requirements, tested behavior, user instructions, support arrangements, and a plan for future changes.

First, the team should write the booking rules before coding. The rules should state that bookings cannot overlap, define the maximum duration, explain what happens when equipment is blocked, and describe cancellation. These rules give the developer and customer a shared meaning of “available.” They also create test cases: a normal booking should succeed, a conflicting booking should be refused, and a cancellation should release equipment. The trade-off is that early agreement takes time, but it prevents disputes after release.

Second, the customer should receive test evidence, not merely a claim that the program works. Unit tests can check duration and conflict calculations. Integration tests can check that a conflict is not saved. A user acceptance test can check whether students understand instructions and error messages. The exact amount of testing is an assumption that should match the small service’s risks; it should include normal and unusual cases rather than promise perfection.

The service also needs documentation. Students need instructions for searching, booking, cancelling, and asking for help. The coordinator needs an administration guide, a data model, backup and restore instructions, and an export procedure. Support should identify recurring questions and use them to improve the service. Without this information, the customer depends on the original developer.

Finally, delivery should identify who owns the service after hand-over. The customer should know who fixes defects, approves rule changes, reviews releases, and checks backups. A portable export reduces the risk of being trapped if the service is replaced. Backups are useful only if recovery steps are documented and tested. These artefacts cost additional time, but they reduce operational risk and make future maintenance possible.

The checklist is a recommendation, not a universal legal requirement. The customer should verify its retention, privacy, security, and support obligations before implementation.

Show what you changed and why. Use only the sources I supplied. Flag remaining gaps instead of inventing details.
```

**Response:**

```text
The customer needs a delivery package rather than code alone. For the fictional equipment-booking service, that package should contain agreed rules, a tested release, user and coordinator instructions, support ownership, a change process, backup and restore procedures, and a portable export.

The first engineering decision is to make availability rules explicit before implementation. The coordinator and representative students should agree on no overlap, maximum duration, cancellation, and blocked equipment. These are requirements because they describe customer-visible behavior; the database format is an implementation choice that must support them. Written rules make tests possible: valid bookings succeed, conflicts are refused, and cancellation releases equipment. The trade-off is slower initial agreement in exchange for fewer disputes later.

The second decision is proportionate, layered testing. Unit tests can exercise duration and overlap calculations; integration tests can check that a conflict is not persisted; acceptance tests can check whether students understand instructions. The GOV.UK quality-assurance guidance supports testing usability, stability, security, performance, and later changes. It also supports reviewing tests as the service evolves. For this small service, a short repeatable test record is more appropriate than an unnecessarily large process, but it must include unusual cases and failed results.

Documentation is part of the product. Student instructions should cover search, booking, cancellation, and support. The coordinator guide should cover administration, export, backups, restore testing, and release review. GOV.UK user-support guidance says support should answer information requests and use feedback to improve a service. Therefore the coordinator should log recurring questions and use them to prioritize changes, without assuming a particular staffing level.

The customer should also receive named post-release responsibilities: who fixes defects, approves rule changes, reviews releases, and tests recovery. NIST guidance supports planning and testing recovery, so “we have backups” is not enough evidence by itself. A simple export reduces replacement risk, but retention, privacy, and access rules remain customer decisions. These additions cost time, yet they make the service operable, maintainable, and replaceable.

This is a recommendation for the fictional scenario, not a universal legal checklist. The real customer must confirm its obligations and risk tolerance.
```

## 9. Appendix C — Evidence tables

### Verification table

<!-- At least two complete rows. Source and locator: title + page / slide / section / chapter,
     or title + URL + access date (YYYY-MM-DD). Decision: keep, qualify or reject — one word. -->

| AI claim | Source and locator | Evidence found | Decision |
| --- | --- | --- | --- |
| “The customer should receive test evidence, not merely a claim that the program works.” | GOV.UK, “Quality assurance: testing your service regularly,” https://www.gov.uk/service-manual/technology/quality-assurance-testing-your-service-regularly, accessed 2026-10-08 | The guidance covers usability, stability, security, performance, unusual conditions, and regression after changes. It supports evidence from several kinds of testing, but does not prove that testing finds every defect. | qualify |
| “Backups are useful only if recovery steps are documented and tested.” | NIST, Protecting Data from Ransomware and Other Data Loss Events, https://www.nccoe.nist.gov/sites/default/files/legacy-files/msp-protecting-data-extended.pdf, accessed 2026-10-08 | The guidance recommends planning, maintaining, documenting, and testing backup and recovery procedures. It supports the practical recommendation, while the absolute word “only” is too strong. | qualify |

### Change log

<!-- At least two substantive revisions. Your final version must differ from the AI wording,
     and the reason must say which evidence or scenario constraint made you change it. -->

| AI wording / suggestion | Your final version | Reason for change |
| --- | --- | --- |
| “The customer should receive test evidence, not merely a claim that the program works.” | “The customer should receive evidence from layered tests for specified cases; those tests reduce risk but cannot prove that no other defect exists.” | The GOV.UK source describes several quality dimensions and testing under unusual conditions, so the final wording avoids claiming universal proof. | 
| “Backups are useful only if recovery steps are documented and tested.” | “The hand-over should include backup and restore instructions, a tested recovery exercise, and a portable export; the customer must still set retention and privacy rules.” | NIST supports tested recovery planning, while the scenario’s replacement constraint requires an export. The absolute claim was qualified. |
