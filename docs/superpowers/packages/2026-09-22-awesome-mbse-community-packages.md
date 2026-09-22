---
date: 2026-09-22
project: awesome-mbse-community
mode: full
rounds: 1
input_digest: d7271e62c2afed40ffa51ede1f753d1f0303cd23538a17db205e6503afdf30ec
open_objections: []
---

# Packages: awesome-mbse-community, 2026-09-22

Full-mode cut from the 2026-09-22 repo-review findings (7 issues, 15
advisories). Three lenses proposed, one round to convergence: every package
passed triage with no critical defects. Dependency order: P1, P4, P2, P3,
P5, P6.

## P1. issue-intake-surface

- **id:** P1
- **name:** issue-intake-surface
- **size:** M
- **status:** done
- **deps:** none
- **corroboration:** 3 (value, risk, cohesion)
- **promoted_ids:** b-14

All three issue forms omit the schema-required top-level `name` and
`description` keys while `config.yml` disables blank issues and both contact
links leave the repo, so the chooser can hide every form. CONTRIBUTING still
claims templates arrive later though they ship, and README documents a
phantom improvement form (RR-B-32) that is not in the tree. Intake, opt-out,
and bug-report paths are dead or contradictory as one subsystem.

**Evidence:**

- `.github/ISSUE_TEMPLATE/bug_report.yml:L1-3`: `title: "[Bug] "` / `labels: [bug]` / `body:`
- `.github/ISSUE_TEMPLATE/config.yml:L1-2`: `blank_issues_enabled: false`
- `CONTRIBUTING.md:L16-18`: "(Structured issue and PR templates arrive with a later effort.)"
- `README.md:L110-116`: Support bullets plus the RR-B-32 improvement-form note

**in_scope:**

- Add required `name` and `description` to bug_report.yml, suggest-entry.yml, opt-out.yml
- Sanity-check config.yml routing without re-enabling blank issues
- Rewrite CONTRIBUTING section 1 so issue/PR templates are described as present
- Remove or replace the README Support phantom improvement-form note
- Keep Support bullets aligned with the three real forms and the SECURITY advisory route
- Verify forms appear in the chooser

**out_scope:** New issue form types; landing or release-gate changes; entry
tag/alpha CI enforcement; markdownlint pin or local lint runbook; weekly
sweep behavior; hub issue routing changes.

**why_now:** Unbroken forms and matching docs must exist before the
contributor-facing CI, runbook, and gate packages assume those links work.

**first_prompt:** `/superpowers-process full restore issue-form intake surface for awesome-mbse-community`

## P4. release-gate-truth

- **id:** P4
- **name:** release-gate-truth
- **size:** M
- **status:** in-flight
- **deps:** none
- **corroboration:** 3 (risk, cohesion)
- **promoted_ids:** b-01, b-03

`scripts/check_release.py` is the single truth hub but incomplete and
underexplained: version is compared only to the landing `version` chip while
CITATION.cff version and the RELEASE-INFO Tag line are never cross-checked;
the landing-chip duty is undocumented for contributors; the module docstring
still names awesome-stpa. validate.yml blocks every PR on this script, so the
hub must be coherent before a local runbook tells contributors how to satisfy
it, and the next version bump silently desyncs citation and tag metadata.

**Evidence:**

- `scripts/check_release.py:L79-90`: version check compares only to `landing_chip(html, "version")`
- `scripts/check_release.py:L146-151`: `chip_entries = landing_chip(html, "entries")`
- `scripts/check_release.py:L6-7`: "Adapted for awesome-stpa (RR-B Base, standalone model)"
- `CITATION.cff:L4-5`: `version: 0.1.0`
- `RELEASE-INFO.txt:L2-4`: `Version: 0.1.0` / `Tag: v0.1.0`
- `.github/PULL_REQUEST_TEMPLATE.md:L4`: "Version files (CHANGELOG, RELEASE-INFO, CITATION) updated together"
- `.github/workflows/validate.yml:L23-24`: runs the gate on every PR to main

**in_scope:**

- Cross-check CITATION.cff version and RELEASE-INFO Tag (optionally CHANGELOG section) against RELEASE-INFO Version; fail validate.yml on drift
- Document docs/index.html chip sync in CONTRIBUTING and/or PR template; clarify source-of-truth vs derived chips
- Fix the stale awesome-stpa module docstring

**out_scope:** Removing the landing truth gate; auto-generating
docs/index.html; performing a version bump or release; CITATION schema
rewrite; issue forms (P1); markdownlint pin (P5); full unit-test harness;
weekly sweep UX; FORBIDDEN_CONTENT glob changes.

**why_now:** The gate already blocks PRs; the hub must be coherent before P6
documents how to run it locally, and P2 builds contributor docs on top.

**first_prompt:** `/superpowers-process full release-gate version and landing-chip truth cross-checks`

## P2. align-contribution-path-docs

- **id:** P2
- **name:** align-contribution-path-docs
- **size:** M
- **status:** proposed
- **deps:** [P1, P4]
- **corroboration:** 1 (value)
- **promoted_ids:** []

CONTRIBUTING's how-to-suggest path and the PR checklist omit the
landing-chip and check_release gate duties that validate.yml enforces on
every PR. First-time entry PRs bounce on requirements documented only inside
the gate script.

**Evidence:**

- `CONTRIBUTING.md:L16-18`: "edit `README.md` ... (Structured issue and PR templates arrive with a later effort.)"
- `.github/PULL_REQUEST_TEMPLATE.md:L4`: version-files checklist line, no landing mention
- `scripts/check_release.py:L146-151`: entries-chip comparison
- `docs/index.html:L33-35`: `<dt>version</dt><dd>0.1.0</dd>`

**in_scope:**

- Rewrite CONTRIBUTING how-to-suggest to point at the shipped issue forms and PR template
- Document that entry-count or version/sweep changes must keep docs/index.html chips in sync
- Extend the PR template checklist for landing chips
- Optional: short local commands for awesome-lint@2.3.0, markdownlint, privacy grep, and `python scripts/check_release.py` beside the Docker lychee recipe

**out_scope:** Changing check_release.py assertion logic; auto-generating
chips; issue-form YAML (P1); adding the missing improvement form; pinning
markdownlint (P5).

**why_now:** After P1 makes forms chooser-valid and P4 settles the gate's
source-of-truth semantics, docs must stop contradicting intake and surface
the landing-chip gate.

**first_prompt:** `/superpowers-process full align CONTRIBUTING and PR template with the release gate`

## P3. entry-policy-gates

- **id:** P3
- **name:** entry-policy-gates
- **size:** M
- **status:** proposed
- **deps:** [P2]
- **corroboration:** 2 (value, risk)
- **promoted_ids:** []

CONTRIBUTING claims CI enforces most format rules, but the only structural
entry check in check_release.py is a loose bullet-grammar regex. Tag
vocabulary and order, who-tag vs section pairing, per-section alphabetical
order, and single-link/description-length rules are ungated, so
policy-breaking or ranking-shaped entries merge green and erode editorial
neutrality.

**Evidence:**

- `scripts/check_release.py:L109`: `ENTRY_RX = re.compile(r"^- \[[^\]]+\]\(https?://[^)\s]+\)\s+-\s+.+\(\d{4}\)\.$")`
- `CONTRIBUTING.md:L231-232`: "**Sections are alphabetical** by entry name, case-insensitive"
- `CONTRIBUTING.md:L249-252`: "The `who` value must match the entry's section"
- `CONTRIBUTING.md:L74-76`: "Tags appear in this fixed order, drawn **only** from this vocabulary"

**in_scope:**

- Extend the check_release.py curated walk to enforce tag vocabulary/order, who-vs-section, per-section alphabetical order, and the documented single-link/description-length rules
- Keep validate.yml as the runner; add minimal fixture/assert output proving the new checks fail closed
- Actionable failures with line/section context

**out_scope:** Re-curating existing entries except fixes required to pass
the new gates; year-rule live verification; URL dedupe; CITATION/Tag
cross-checks (P4); contributor doc rewrites (P2); changing the tag
vocabulary; sweep automation.

**why_now:** Launch and intake fixes only pay off if green CI preserves the
neutrality and format bar as external PRs land.

**first_prompt:** `/superpowers-process full enforce entry policy invariants in the release gate`

## P5. pin-markdownlint-runbook

- **id:** P5
- **name:** pin-markdownlint-runbook
- **size:** S
- **status:** proposed
- **deps:** none
- **corroboration:** 1 (risk)
- **promoted_ids:** []

markdownlint-cli2 installs via unpinned `npx -y` on the public PR CI path
while action SHAs and awesome-lint@2.3.0 are pinned in the same file. A
compromised publish runs inside the job with the workflow token and full
PR-head checkout.

**Evidence:**

- `.github/workflows/link-check-pr.yml:L64`: `run: npx -y markdownlint-cli2 "README.md" "CONTRIBUTING.md"`
- `.github/workflows/link-check-pr.yml:L54`: `run: npx awesome-lint@2.3.0 README.md`
- `.github/workflows/link-check-pr.yml:L20-21`: `permissions: contents: read`

**in_scope:** Pin markdownlint-cli2 to an explicit version in
link-check-pr.yml.

**out_scope:** lychee accept codes or schedule workflow; new lint tools;
branch-protection policy.

**why_now:** Active supply-chain exposure on the public PR path today.

**first_prompt:** `/superpowers-process full pin markdownlint-cli2 in PR CI`

## P6. pr-lint-local-runbook

- **id:** P6
- **name:** pr-lint-local-runbook
- **size:** S
- **status:** proposed
- **deps:** [P4]
- **corroboration:** 1 (cohesion)
- **promoted_ids:** b-07, b-15

CONTRIBUTING marks lint mandatory but documents only a Docker lychee
one-liner that omits CI flags and token; no local recipes exist for
awesome-lint@2.3.0, markdownlint-cli2, the privacy grep, or
`python scripts/check_release.py`. PR authors without Docker iterate through
CI failures for checks they were told are mandatory.

**Evidence:**

- `CONTRIBUTING.md:L3`: "**Lint is mandatory.**"
- `CONTRIBUTING.md:L177-182`: "## Local link-check" with the lychee one-liner only
- `.github/workflows/link-check-pr.yml:L54, L64`: the CI commands with no local counterpart

**in_scope:**

- Expand the CONTRIBUTING local-check section with recipes matching CI: awesome-lint@2.3.0, markdownlint-cli2, privacy grep, check_release.py
- Align the Docker lychee example with CI args where practical

**out_scope:** New gate logic (P3/P4); issue forms (P1); schedule workflow
changes; lychee 429 policy; privacy grep scope.

**why_now:** Depends on P4 so the documented local gate steps match what the
gate actually checks.

**first_prompt:** `/superpowers-process full document local preflight recipes in CONTRIBUTING`
