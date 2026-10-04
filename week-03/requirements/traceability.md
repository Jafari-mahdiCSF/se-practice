# Traceability — use cases → stories → criteria

One row per use case. Every story is mapped to a use case; the criteria column shows which of the
three selected stories received acceptance criteria.

| Use case | Stories (US-nn) | Criteria (AC-nn) | Gap? |
| --- | --- | --- | --- |
| UC-01 View availability | US-01 | AC-01, AC-02, AC-03 | none |
| UC-02 Book room | US-02 | AC-04, AC-05, AC-06 | none |
| UC-03 Cancel booking | US-03 | none | Criteria for cancellation are not in the selected three sets |
| UC-04 Block or unblock room | US-04 | AC-07, AC-08, AC-09 | none |
| UC-05 Review usage | US-05 | none | Criteria for usage review are not in the selected three sets |
| UC-06 Send confirmation | US-06 | none | Criteria for confirmation are not in the selected three sets |

**Stories that belong to no use case:** none

**What the gaps tell you:** Every story maps to a use case, but the nine criteria cover only the
three selected stories, leaving cancellation, usage review, and confirmation without direct tests.
