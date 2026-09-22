# Issue intake surface (P1) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the three GitHub issue forms chooser-valid and align CONTRIBUTING/README prose with the intake paths that actually ship.

**Architecture:** Patch-only edits to the three form YAML files (add schema-required `name`/`description`, one sentence added to the opt-out body), prose replacement in CONTRIBUTING.md section 1 and README.md Usage/Support, one CHANGELOG Unreleased line, and two repo-settings actions run via `gh` (create labels, enable private vulnerability reporting). No gate, landing, or workflow changes.

**Tech Stack:** GitHub issue forms (YAML), markdown, `gh` CLI, PyYAML for the one-off schema check, npx awesome-lint 2.3.0 / markdownlint-cli2.

**Spec:** docs/superpowers/specs/2026-09-22-issue-intake-surface.md

## Research

GitHub issue-form schema: "All issue form configuration files must begin with `name`, `description`, and `body` key-value pairs"; `title` and `labels` are optional; a label not present in the repo is not added to the issue. https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms
Chooser configuration: `name` must be longer than 3 characters; templates list alphanumerically, YAML before Markdown. https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository
Private vulnerability reporting: `PUT /repos/{owner}/{repo}/private-vulnerability-reporting` enables it, returns 204, needs admin. https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28

## Global Constraints

- Published prose contains no em dashes (PR template checklist; check with `grep -n -P "\x{2014}"`).
- `npx -y awesome-lint@2.3.0 README.md` must exit 0 and `npx -y markdownlint-cli2 README.md CONTRIBUTING.md` must report 0 issues after every prose task.
- Support-section bullets keep starting with plain text (awesome-lint list-item rule validates link-first items).
- Issue-form names are unique, longer than 3 characters, and match the wording used in README and CONTRIBUTING.
- `config.yml` is not edited; blank issues stay disabled.
- Labels: `entry` and `opt-out` do not exist in the repo yet (verified 2026-09-22 via `gh label list`).
- Nothing new is committed except the tracked file edits below; the schema-check script is a one-off, not committed.

---

### Task 1: Patch the three issue forms

**Files:**
- Modify: `.github/ISSUE_TEMPLATE/bug_report.yml:1-3`
- Modify: `.github/ISSUE_TEMPLATE/suggest-entry.yml:1-3`
- Modify: `.github/ISSUE_TEMPLATE/opt-out.yml:1-12`

**Interfaces:**
- Consumes: nothing.
- Produces: chooser-valid forms named "Bug report", "Suggest an entry", "Opt-out"; the `opt-out.yml` body gains one sentence pointing at the private advisory route. Later tasks' prose quotes these names verbatim.

**Model:** flash

Patch only: insert the two keys at the top; do not touch `title`, `labels`, or `body` except the stated sentence.

- [ ] **Step 1: Insert `name` and `description` at the head of bug_report.yml**

```yaml
name: Bug report
description: Report a broken or hijacked link, or a CI failure.
title: "[Bug] "
labels: [bug]
body:
```

(The existing `body:` and everything under it stays byte-identical.)

- [ ] **Step 2: Insert `name` and `description` at the head of suggest-entry.yml**

```yaml
name: Suggest an entry
description: Propose a person or organization, with one checkable contribution as evidence.
title: "[Suggest] "
labels: [entry]
body:
```

(Body unchanged.)

- [ ] **Step 3: Rewrite opt-out.yml to the spec's full target**

```yaml
name: Opt-out
description: Ask for removal of a person or organization entry. No reason needed.
title: "[Opt-out] "
labels: [opt-out]
body:
  - type: markdown
    attributes:
      value: >
        Request removal of a person or organization entry. No reason is
        needed. Removal is unconditional. For a request that should not be
        public, use the Security advisory link in the issue chooser instead
        (see SECURITY.md).
  - type: input
    id: entry
    attributes:
      label: Entry name as written in README (optional)
```

- [ ] **Step 4: Run the one-off schema check**

Run (from repo root, Python with PyYAML):

```python
import glob, sys, yaml
names, bad = {}, 0
for p in sorted(glob.glob(".github/ISSUE_TEMPLATE/*.yml")):
    if p.endswith("config.yml"):
        continue
    d = yaml.safe_load(open(p, encoding="utf-8"))
    probs = [f"missing {k}" for k in ("name", "description", "body") if k not in d]
    n = d.get("name")
    if isinstance(n, str):
        if len(n) <= 3:
            probs.append("name too short")
        if n in names:
            probs.append(f"name duplicates {names[n]}")
        names[n] = p
    if not isinstance(d.get("body"), list) or not d["body"]:
        probs.append("body empty")
    print(p, "OK" if not probs else "; ".join(probs))
    bad += bool(probs)
sys.exit(1 if bad else 0)
```

Expected: three `OK` lines, exit 0.

- [ ] **Step 5: Commit**

```bash
git add .github/ISSUE_TEMPLATE/bug_report.yml .github/ISSUE_TEMPLATE/suggest-entry.yml .github/ISSUE_TEMPLATE/opt-out.yml
git commit -m "fix: add schema-required name and description to issue forms"
```

### Task 2: Align CONTRIBUTING section 1

**Files:**
- Modify: `CONTRIBUTING.md:9-19`

**Interfaces:**
- Consumes: form names from Task 1 ("Suggest an entry", "Bug report", "Opt-out").
- Produces: none downstream.

**Model:** flash

- [ ] **Step 1: Replace the intro sentence**

Replace:

```markdown
The fastest path: open an issue naming the person or org and the evidence,
or open a pull request that edits `README.md` directly.
```

with:

```markdown
The fastest path: open the "Suggest an entry" issue form with the evidence,
or open a pull request that edits `README.md` directly.
```

- [ ] **Step 2: Replace section 1**

Replace the whole `## 1. How to suggest a person or org` section (through the line before `## 2. Inclusion bar`) with:

```markdown
## 1. How to suggest a person or org

- **Issue:** open a [new issue](https://github.com/jgsystemsconsulting/awesome-mbse-community/issues/new/choose)
  and pick the "Suggest an entry" form. It asks for the display name, the
  public profile URL, the target section, one contribution evidence URL, why
  the entry meets the five-point bar (section 2), and the required
  confirmation that the evidence shows only public professional info.
- **PR:** edit `README.md`, follow the entry format below, describe the
  evidence in the PR body, and tick the PR template checklist. CI link-checks
  the entry, lints the list, and runs the privacy grep.

The same chooser holds the "Bug report" form (broken or hijacked link, CI
failure) and the "Opt-out" form (removal of a person or organization entry,
People policy clause 4). Security reports go through the private advisory
route in SECURITY.md.
```

- [ ] **Step 3: Lint and grep**

```bash
npx -y awesome-lint@2.3.0 README.md
npx -y markdownlint-cli2 README.md CONTRIBUTING.md
grep -n "later effort" CONTRIBUTING.md
```

Expected: lint exit 0 / 0 issues; grep prints nothing.

- [ ] **Step 4: Commit**

```bash
git add CONTRIBUTING.md
git commit -m "docs: CONTRIBUTING section 1 describes the shipped issue forms"
```

### Task 3: Rewrite README Usage and Support

**Files:**
- Modify: `README.md:101-116`

**Interfaces:**
- Consumes: form names from Task 1.
- Produces: none downstream. `## Support` is not a curated section, so `scripts/check_release.py` ignores it.

**Model:** flash

- [ ] **Step 1: Replace the Usage paragraph**

Replace:

```markdown
Browse by section, or search the Contents. Open a profile link to see the
person or organization behind a contribution. To suggest a person or
organization, use the suggest-an-entry issue form with the contribution
evidence. To request removal, use the opt-out form; no reason is needed.
```

with:

```markdown
Browse by section, or search the Contents. Open a profile link to see the
person or organization behind a contribution. To suggest a person or
organization, use the "Suggest an entry" issue form with the contribution
evidence. To request removal, use the "Opt-out" form; no reason is needed.
```

- [ ] **Step 2: Replace the Support section**

Replace `## Support` and everything through the RR-B-32 paragraph (before `## Version`) with:

```markdown
## Support

Open a [new issue](https://github.com/jgsystemsconsulting/awesome-mbse-community/issues/new/choose) and pick a form:

- Suggest a person or organization: the "Suggest an entry" form
- Request removal: the "Opt-out" form, or the private advisory route for a request that should not be public
- Broken link or CI failure: the "Bug report" form
- Security: private advisory (see [SECURITY.md](SECURITY.md))
```

The RR-B-32 paragraph is deleted with no replacement.

- [ ] **Step 3: Lint and grep**

```bash
npx -y awesome-lint@2.3.0 README.md
npx -y markdownlint-cli2 README.md CONTRIBUTING.md
grep -n "RR-B-32\|improvement form" README.md CONTRIBUTING.md
grep -n -P "\x{2014}" README.md CONTRIBUTING.md CHANGELOG.md .github/ISSUE_TEMPLATE/*.yml
```

Expected: lint exit 0 / 0 issues; both greps print nothing.

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: README Support names the shipped forms, drop phantom improvement-form note"
```

### Task 4: CHANGELOG Unreleased line

**Files:**
- Modify: `CHANGELOG.md:6`

**Interfaces:**
- Consumes: Tasks 1-3 outcomes.
- Produces: none downstream.

**Model:** flash

- [ ] **Step 1: Add a Fixed section under Unreleased**

Directly under `## [Unreleased]` add:

```markdown

### Fixed

- Issue forms (bug report, suggest-entry, opt-out) gained the `name` and
  `description` keys GitHub requires, so they show in the issue chooser.
  CONTRIBUTING section 1 and the README Support section now describe the
  shipped forms and the private advisory route; the phantom improvement-form
  note is gone.
```

- [ ] **Step 2: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs: changelog note for issue-form intake fixes"
```

### Task 5: Repo settings (labels, private vulnerability reporting)

**Files:**
- No tracked file changes. Two repo-settings actions via `gh`, run from the repo checkout with the owner login.

**Interfaces:**
- Consumes: nothing.
- Produces: labels `entry` and `opt-out` exist; private vulnerability reporting enabled (the SECURITY advisory route becomes live for outsiders).

**Model:** standard

- [ ] **Step 1: Create the two labels**

```bash
gh label list
gh label create entry --repo jgsystemsconsulting/awesome-mbse-community --description "Suggested person or organization entry" --color 0e8a16
gh label create opt-out --repo jgsystemsconsulting/awesome-mbse-community --description "Removal request under the People policy" --color 5319e7
```

Expected: `gh label list` first shows only `bug` and `sweep-report`; each create returns the new label. A re-run after partial failure answers HTTP 422 "already exists", which is harmless; check `gh label list` before retrying. If a 4xx other than that appears, stop and report.

- [ ] **Step 2: Enable private vulnerability reporting**

```bash
gh api -X PUT repos/jgsystemsconsulting/awesome-mbse-community/private-vulnerability-reporting
gh api repos/jgsystemsconsulting/awesome-mbse-community/private-vulnerability-reporting
```

Expected: PUT returns 204; GET returns `{"enabled":true}`. Needs admin; on 4xx stop and report (no email or other channel substitute).

- [ ] **Step 3: No commit (repo settings only)**

Nothing to commit; record the outputs in the PR body.

### Task 6: Full verification sweep

**Files:**
- No file changes. Runs the spec's pre-merge verification.

**Interfaces:**
- Consumes: all prior tasks.
- Produces: evidence for the PR body and the release-gate pass.

**Model:** standard

- [ ] **Step 1: Schema check**

Re-run the Task 1 Step 4 script. Expected: three `OK` lines, exit 0.

- [ ] **Step 2: Lint trio and release gate**

```bash
npx -y awesome-lint@2.3.0 README.md
npx -y markdownlint-cli2 README.md CONTRIBUTING.md
python scripts/check_release.py
```

Expected: exit 0, 0 issues, and `release gate: PASS`.

- [ ] **Step 3: Stale-text greps**

```bash
grep -n "RR-B-32\|improvement form" README.md CONTRIBUTING.md
grep -n "arrive with a later effort" README.md CONTRIBUTING.md
grep -n -P "\x{2014}" README.md CONTRIBUTING.md CHANGELOG.md .github/ISSUE_TEMPLATE/*.yml
```

Expected: all print nothing.

- [ ] **Step 4: Settings state**

```bash
gh label list
gh api repos/jgsystemsconsulting/awesome-mbse-community/private-vulnerability-reporting
```

Expected: labels include `bug`, `entry`, `opt-out`; GET returns `{"enabled":true}`.

- [ ] **Step 5: PR CI green**

Push the branch and open the PR; the `link-check (PR)` jobs and `validate` must pass. Post-merge chooser checks (spec Verification items 10-12) are maintainer browser checks on the default branch and are listed in the PR body as follow-ups.
