# Backlog: awesome-mbse-community

Created 2026-09-22 from package-loop round-1 triage routing (repo-review
advisories). Rows are never deleted; every transition is a status change.

| id | title | source | status | evidence |
|----|-------|--------|--------|----------|
| b-01 | Fix stale awesome-stpa docstring in check_release.py | advisory round 1 | merged-into | P4 (scripts/check_release.py:L6-7) |
| b-02 | Fix unclosed parenthesis in CHANGELOG.md entry | advisory round 1 | open | CHANGELOG.md:L39-40 |
| b-03 | Resolve dual-maintained landing chips (source-of-truth vs derived) | advisory round 1 | merged-into | P4 (docs/index.html:L33-35) |
| b-04 | Add unit tests for check_release edge paths (module and harness undefined) | advisory round 1 | needs-info | scripts/check_release.py |
| b-05 | Decide whether lint job path filters should widen | advisory round 1 | needs-info | .github/workflows/link-check-pr.yml:L20-21 |
| b-06 | Decide desired weekly-sweep issue behavior (always opens new issue) | advisory round 1 | needs-info | .github/workflows/link-check-schedule.yml:L55-60 |
| b-07 | Align lychee snippet flags in CONTRIBUTING with CI args | advisory round 1 | merged-into | P6 (CONTRIBUTING.md:L182) |
| b-08 | Review/tighten FORBIDDEN_CONTENT globs (desired set undefined) | advisory round 1 | needs-info | scripts/check_release.py:L36-44 |
| b-09 | Define lychee 429 rate-limit policy (retry/accept/token) | advisory round 1 | needs-info | .github/workflows/link-check-pr.yml:L38 |
| b-10 | Extend privacy grep beyond README to tracked markdown | advisory round 1 | open | .github/workflows/link-check-pr.yml:L70-74 |
| b-11 | No-secrets scan came back clean (observation, no task) | advisory round 1 | needs-info | SECURITY.md:L1-20 |
| b-12 | Review sweep issues:write token scope (confirm least privilege) | advisory round 1 | needs-info | .github/workflows/link-check-schedule.yml:L14 |
| b-13 | Static HTML scan clean (observation, no task) | advisory round 1 | needs-info | docs/index.html:L1-49 |
| b-14 | Rewrite RR-B-32 jargon in README improvement-form note | advisory round 1 | merged-into | P1 (README.md:L110-116) |
| b-15 | Align CONTRIBUTING lychee token guidance with CI | advisory round 1 | merged-into | P6 (CONTRIBUTING.md:L177-182) |
