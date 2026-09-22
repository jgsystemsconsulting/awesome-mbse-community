---
date: 2026-09-22
project: awesome-mbse-community
mode: light
rounds: 1
slice: []
input_digest: aac67274edff39ed5637383278ddc6699a5e64f6ef1cffbd95571820435560f5
open_objections: []
---

# Findings: awesome-mbse-community, 2026-09-22

Four-lens review (rot, defect, guard, operate), one round, whole repo. Triage
verified every citation against the repo; all seven findings passed grading.
Two are HIGH. Advisory items close the document.

## I3. Issue forms missing required `name`/`description` metadata

- **id:** I3
- **name:** issue-forms-missing-required-metadata
- **severity:** HIGH
- **corroboration:** 1 (defect)
- **lenses:** defect
- **deps:** []

All three GitHub issue forms open with `title:`/`labels:`/`body:` and omit the
schema-required top-level `name` and `description` keys. GitHub issue forms
need both for the template chooser; without them a form is invalid or hidden.
Because `config.yml` sets `blank_issues_enabled: false` and both contact links
route elsewhere (security advisories URL, a different repo), contributors can
be left with no usable template at all. The documented bug-report,
suggest-entry, and opt-out paths fail even though the YAML files exist and
README Support points at them. Triage verified the files against the repo.

**Evidence:**

- `.github/ISSUE_TEMPLATE/bug_report.yml:L1-3`: `title: "[Bug] "` / `labels: [bug]` / `body:`
- `.github/ISSUE_TEMPLATE/suggest-entry.yml:L1-3`: `title: "[Suggest] "` / `labels: [entry]` / `body:`
- `.github/ISSUE_TEMPLATE/opt-out.yml:L1-3`: `title: "[Opt-out] "` / `labels: [opt-out]` / `body:`
- `.github/ISSUE_TEMPLATE/config.yml:L1-2`: `blank_issues_enabled: false` / `contact_links:`
- `README.md:L149-151`: "Suggest a person or organization: the suggest-an-entry issue form"

**blast_radius:** Opt-out, entry suggestions, and bug reports never appear in
the issue UI. People-policy removal intake claimed as live is unreachable.

## I7. Landing-chip gate requirement undocumented for contributors

- **id:** I7
- **name:** landing-chip-undocumented
- **severity:** HIGH
- **corroboration:** 1 (operate)
- **lenses:** operate
- **deps:** []

`validate.yml` runs `scripts/check_release.py` on every PR to main, and the
gate requires `docs/index.html` chips (entries, version, and related) to match
README and RELEASE-INFO. CONTRIBUTING tells contributors to edit `README.md`
only, and the PR template asks for CHANGELOG/RELEASE-INFO/CITATION together
but never mentions `docs/index.html`. A first-time entry PR therefore fails
the release gate for a requirement documented only inside the gate script.
Triage confirmed the gate compares the entries chip (check_release.py
L146-151) and that no contributor-facing doc mentions the landing page.

**Evidence:**

- `CONTRIBUTING.md:L16-19`: "- **PR:** edit `README.md`, follow the entry format below"
- `.github/PULL_REQUEST_TEMPLATE.md:L4`: "Version files (CHANGELOG, RELEASE-INFO, CITATION) updated together"
- `scripts/check_release.py:L52-56`: "# --- landing truth gate ---"
- `scripts/check_release.py:L619-624`: `chip_entries = landing_chip(html, "entries")`
- `docs/index.html:L33-35`: `<dt>version</dt><dd>0.1.0</dd>`
- `.github/workflows/validate.yml:L23-24`: `- name: Run release gate` / `run: python scripts/check_release.py`

**blast_radius:** Entry PRs fail CI until a maintainer knows to hand-edit the
chips; external contributors bounce and review cycles burn.

## I5. Entry policy invariants ungated by CI

- **id:** I5
- **name:** entry-policy-invariants-ungated
- **severity:** MEDIUM
- **corroboration:** 1 (defect)
- **lenses:** defect
- **deps:** []

CONTRIBUTING says CI enforces most inclusion and format rules, but the only
structural entry check in `check_release.py` is a loose bullet-grammar regex
(link, hyphen separator, trailing year). Tag vocabulary and order, who-tag vs
section pairing, single-link and description length, and case-insensitive
alphabetical order inside curated sections are all ungated. awesome-lint and
markdownlint cover manifest and markdown style; the privacy grep covers email
only. Policy-breaking or ranking-shaped entries can merge on green CI.

**Evidence:**

- `scripts/check_release.py:L109-137`: `ENTRY_RX = re.compile(r"^- \[[^\]]+\]\(https?://[^)\s]+\)\s+-\s+.+\(\d{4}\)\.$")`
- `CONTRIBUTING.md:L236-247`: "Tags appear in this fixed order, drawn **only** from this vocabulary"
- `CONTRIBUTING.md:L249-252`: "The `who` value must match the entry's section"
- `CONTRIBUTING.md:L231-232`: "**Sections are alphabetical** by entry name, case-insensitive"
- `CONTRIBUTING.md:L3-4`: "**Lint is mandatory.**"

**blast_radius:** Editorial-neutrality and tag-vocabulary guarantees regress
without a failing check to catch them.

## I4. CITATION.cff and Tag drift ungated

- **id:** I4
- **name:** citation-release-version-drift-ungated
- **severity:** MEDIUM
- **corroboration:** 1 (defect)
- **lenses:** defect
- **deps:** []

The release gate treats the RELEASE-INFO `Version` field as source of truth
and compares it only to the landing `version` chip. `CITATION.cff` `version`
and the RELEASE-INFO `Tag` line are never cross-checked, and CHANGELOG section
headers are not tied to the same value. The PR template tells contributors to
update CHANGELOG, RELEASE-INFO, and CITATION together, but nothing fails when
one lags, so published citation metadata can diverge while CI prints PASS.

**Evidence:**

- `scripts/check_release.py:L79-90`: version check compares only to `landing_chip(html, "version")`
- `CITATION.cff:L4-5`: `version: 0.1.0` / `date-released: "2026-09-22"`
- `RELEASE-INFO.txt:L2-4`: `Version: 0.1.0` / `Tag: v0.1.0`
- `.github/PULL_REQUEST_TEMPLATE.md:L4`: "Version files (CHANGELOG, RELEASE-INFO, CITATION) updated together"

**blast_radius:** Downstream citers and release auditors trust stale
CITATION.cff after a version bump.

## I6. PR CI gate gaps: unpinned markdownlint and no local runbook

- **id:** I6
- **name:** ci-pr-gate-gaps
- **severity:** MEDIUM
- **corroboration:** 2 (guard, operate)
- **lenses:** guard, operate
- **deps:** [I7]

Two readings of the same PR gate. Guard: the markdownlint job installs
markdownlint-cli2 via unpinned `npx -y`, so every matching PR executes
whatever version npm serves that day, while action SHAs and
awesome-lint@2.3.0 are pinned in the same file; a compromised publish runs
inside the job with the workflow token and full PR-head checkout. Operate:
CONTRIBUTING calls awesome-lint mandatory and lists the other CI checks, but
the only local recipe is a Docker lychee one-liner; there is no documented
local command for awesome-lint@2.3.0, markdownlint-cli2, the privacy grep, or
`python scripts/check_release.py`.

**Evidence:**

- `.github/workflows/link-check-pr.yml:L64`: `run: npx -y markdownlint-cli2 "README.md" "CONTRIBUTING.md"`
- `.github/workflows/link-check-pr.yml:L54`: `run: npx awesome-lint@2.3.0 README.md`
- `.github/workflows/link-check-pr.yml:L20-21`: `permissions:` / `contents: read`
- `CONTRIBUTING.md:L3`: "**Lint is mandatory.**"
- `CONTRIBUTING.md:L177-185`: "## Local link-check"

**blast_radius:** Supply-chain exposure on the public PR path; separately,
PR authors without Docker iterate through CI failures for checks they were
told are mandatory.

## I1. CONTRIBUTING claims templates arrive later; they already exist

- **id:** I1
- **name:** contributing-templates-stale
- **severity:** MEDIUM
- **corroboration:** 2 (rot, operate)
- **lenses:** rot, operate
- **deps:** [I2]

CONTRIBUTING still says "(Structured issue and PR templates arrive with a
later effort.)" while the repo ships bug_report, suggest-entry, opt-out issue
forms and a PR template, CHANGELOG 0.1.0 records them as shipped packaging,
and README Support points contributors at the forms. Onboarding docs
contradict the product surface and steer people to free-form issues.

**Evidence:**

- `CONTRIBUTING.md:L178-181`: "(Structured issue and PR templates arrive with a later effort.)"
- `CHANGELOG.md` (0.1.0 packaging note): "issue forms (bug report, suggest-entry, opt-out), PR template"
- `.github/PULL_REQUEST_TEMPLATE.md:L1-4`: PR checklist exists
- `README.md:L149-151`: Support section names the issue forms

**blast_radius:** Contributors skip the structured forms; triage load grows;
README, CHANGELOG, and CONTRIBUTING disagree on the intake path.

## I2. README documents an improvement form that is not in the tree

- **id:** I2
- **name:** phantom-improvement-form
- **severity:** MEDIUM
- **corroboration:** 1 (rot)
- **lenses:** rot
- **deps:** [I1]

README Support documents an intentional "improvement form" filename WARN
(RR-B-32), but the issue-template tree contains only bug_report, config,
opt-out, and suggest-entry. The note is dead documentation for an artifact
this spoke never added.

**Evidence:**

- `README.md:L154-155`: "The improvement form's filename intentionally carries a known auditor WARN (RR-B-32); it is accepted, not renamed."
- `.github/ISSUE_TEMPLATE/` tree: bug_report.yml, config.yml, opt-out.yml, suggest-entry.yml only

**blast_radius:** Maintainers and auditors chase a template that does not
exist; copy-paste may propagate the ghost claim to sibling spokes.

## Advisories

Below-the-findings-bar material, left for a later packaging run to judge.

| id | title | evidence |
|----|-------|----------|
| a-01 | check_release.py module docstring still names awesome-stpa | scripts/check_release.py:L6 |
| a-02 | CHANGELOG sparx-ea deferred line has an extra closing paren | CHANGELOG.md:L39-40 |
| a-03 | Landing chips dual-maintained but gate asserts sync | scripts/check_release.py:L525-530 |
| a-04 | No unit tests for check_release edge paths | scripts/check_release.py:L1-193 |
| a-05 | Lint jobs PR path-filtered only; main push relies on branch protection | .github/workflows/link-check-pr.yml:L8-14 |
| a-06 | Weekly sweep always opens a new issue even when clean | .github/workflows/link-check-schedule.yml:L55-60 |
| a-07 | Local Docker lychee snippet omits CI flags | CONTRIBUTING.md:L344 |
| a-08 | FORBIDDEN_CONTENT scan limited to scripts/*.py | scripts/check_release.py:L36-44 |
| a-09 | lychee --accept 429 treats rate-limited dead hosts as success | .github/workflows/link-check-pr.yml:L38 |
| a-10 | Privacy email grep covers README only | .github/workflows/link-check-pr.yml:L70-74 |
| a-11 | No tracked secrets (clean result, recorded) | SECURITY.md:L1-20 |
| a-12 | Weekly sweep uses issues:write for rendered report text | .github/workflows/link-check-schedule.yml:L55-60 |
| a-13 | Static docs/index.html has no scripts or sinks (clean result) | docs/index.html:L1-49 |
| a-14 | README Support exposes internal RR-B-32 jargon to end users | README.md:L115-116 |
| a-15 | Local Docker lychee recipe omits token | CONTRIBUTING.md:L182 |
