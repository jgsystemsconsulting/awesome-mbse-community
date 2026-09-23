# Release gate truth (P4) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the release gate fail on version-identity drift (CITATION.cff, Tag, CHANGELOG) and make the landing-chip duty visible to contributors.

**Architecture:** Three new fail-closed assertions inside the existing version `else` branch of `scripts/check_release.py`, one docstring fix, one PR-template checklist line replacement, one new CONTRIBUTING subsection. No workflow changes.

**Tech Stack:** Python (stdlib re, pathlib), markdown, markdownlint-cli2.

**Spec:** docs/superpowers/specs/2026-09-22-release-gate-truth.md

## Research

All facts repo-internal; line anchors verified by two review rounds: `landing_chip()` at check_release.py L67-72, version assertion L79-90 with the `else` branch at L85 guarding `version_hits[0]`, `read_source` fail-closed at L59-64. GitHub form-schema research not applicable to this package; research: skipped (all facts repo-internal).

## Global Constraints

- Gate stays fail-closed: every parse failure appends to `fails`; nothing may pass silently.
- New assertions live inside the existing `else:` branch that guards `version_hits[0]` (check_release.py L85).
- Published prose (CONTRIBUTING, PR template) contains no em dashes; `grep -n -P "\x{2014}" CONTRIBUTING.md .github/PULL_REQUEST_TEMPLATE.md` prints nothing. The functional U+2014 in check_release.py L35 (FORBIDDEN_CONTENT regex) is exempt and must not be removed.
- `npx -y markdownlint-cli2 README.md CONTRIBUTING.md` reports 0 issues after prose edits.
- `python scripts/check_release.py` must print `release gate: PASS` on the untouched tree (all files agree at 0.1.0).
- No changes to docs/index.html, workflows, CITATION.cff, RELEASE-INFO.txt, or CHANGELOG content beyond what the spec specifies (none here).

---

### Task 1: Gate assertions and docstring

**Files:**
- Modify: `scripts/check_release.py:6-7` (docstring), `scripts/check_release.py:85-91` (insert inside else branch)

**Interfaces:**
- Consumes: existing `fails`, `read_source`, `release_info`, `version_hits` symbols.
- Produces: three new failure modes (CITATION version mismatch/ambiguous, Tag mismatch/ambiguous, CHANGELOG newest-release mismatch/absent). Later tasks and validate.yml rely on exit behavior only.

**Model:** standard

- [ ] **Step 1: Fix the docstring**

Replace the docstring's second sentence:

```python
"""Release gate (RR-B-15): required files, forbidden paths, forbidden
content, headers present. Exits non-zero on any failure.

Standalone model for awesome-mbse-community: no src/ layout, no package
install, no scripts beyond the gate itself."""
```

- [ ] **Step 2: Insert the three assertions inside the version else branch**

Inside the existing `else:` (the branch that runs the landing-chip comparison), after that comparison, add:

```python
        # inside the existing else branch that guards version_hits[0]
        citation = read_source("CITATION.cff")
        if citation is not None:
            cff_hits = re.findall(r'(?:^version:\s*)"?([^"\s]+)"?\s*$', citation, re.M)
            if len(cff_hits) != 1:
                fails.append(
                    f"CITATION.cff version missing or ambiguous: {len(cff_hits)} matches"
                )
            elif cff_hits[0] != version_hits[0]:
                fails.append(
                    f"CITATION.cff version {cff_hits[0]} != RELEASE-INFO Version {version_hits[0]}"
                )
        tag_hits = re.findall(r"(?m)^Tag: v(\S+)\s*$", release_info)
        if len(tag_hits) != 1:
            fails.append(
                f"RELEASE-INFO Tag missing or not in 'Tag: v<version>' format: {len(tag_hits)} matches"
            )
        elif tag_hits[0] != version_hits[0]:
            fails.append(f"RELEASE-INFO Tag v{tag_hits[0]} != Version {version_hits[0]}")
        changelog = read_source("CHANGELOG.md")
        if changelog is not None:
            rel = re.findall(r"(?m)^## \[(\d+\.\d+\.\d+)\]", changelog)
            if not rel:
                fails.append("CHANGELOG has no semver release section")
            elif rel[0] != version_hits[0]:
                fails.append(
                    f"CHANGELOG newest release {rel[0]} != RELEASE-INFO Version {version_hits[0]}"
                )
```

Note: the CITATION regex strips optional surrounding double quotes (CFF legal quoting) before comparing. The CHANGELOG regex takes the first semver section (Keep a Changelog lists newest first; `[Unreleased]` does not match).

- [ ] **Step 3: Run the gate**

Run: `python scripts/check_release.py`
Expected: `release gate: PASS (scanned 1 files)`, exit 0.

- [ ] **Step 4: Negative probe (a) CITATION**

Temporarily change CITATION.cff `version: 0.1.0` to `version: 9.9.9`, run the gate, capture the `CITATION.cff version 9.9.9 != RELEASE-INFO Version 0.1.0` failure and non-zero exit, restore the file, re-run the gate to PASS.

- [ ] **Step 5: Negative probe (b) Tag**

Temporarily change RELEASE-INFO.txt `Tag: v0.1.0` to `Tag: v9.9.9`, capture `RELEASE-INFO Tag v9.9.9 != Version 0.1.0`, restore, re-run PASS.

- [ ] **Step 6: Negative probe (c) CHANGELOG**

Temporarily change CHANGELOG.md `## [0.1.0] - 2026-09-22` to `## [9.9.9] - 2026-09-22`, capture `CHANGELOG newest release 9.9.9 != RELEASE-INFO Version 0.1.0`, restore, re-run PASS.

- [ ] **Step 7: Commit**

```bash
git add scripts/check_release.py
git commit -m "feat: release gate cross-checks CITATION, Tag, and CHANGELOG against Version"
```

### Task 2: PR template and CONTRIBUTING contract

**Files:**
- Modify: `.github/PULL_REQUEST_TEMPLATE.md:4`
- Modify: `CONTRIBUTING.md` (new subsection after "## Local link-check", before the next existing heading)

**Interfaces:**
- Consumes: chip names from the gate (`entries`, `sweep`, `version`).
- Produces: contributor-facing contract text; no downstream consumers.

**Model:** flash

- [ ] **Step 1: Replace the version-files checklist line**

Replace:

```markdown
- [ ] Version files (CHANGELOG, RELEASE-INFO, CITATION) updated together
```

with:

```markdown
- [ ] Version files (CHANGELOG, RELEASE-INFO, CITATION) updated together, and docs/index.html chips matched (entries, sweep, version)
```

- [ ] **Step 2: Add the CONTRIBUTING subsection**

Insert after the "Local link-check" section's content, before the next `## ` heading:

```markdown
## Landing page and version files

`docs/index.html` is a derived copy. `README.md` is the source of truth for
the sweep badge, curated sections, and entry count; `RELEASE-INFO.txt` is the
source for the version. When a PR adds or removes an entry, or touches
version files, update the landing chips (`entries`, `sweep`, `version`) and
the section-index list to match. The same applies when only the README sweep
badge changes: update the `sweep` chip. The release gate in CI fails
otherwise. CHANGELOG, RELEASE-INFO.txt, and CITATION.cff carry the same
version on every release.
```

- [ ] **Step 3: Lint and grep**

```bash
npx -y markdownlint-cli2 README.md CONTRIBUTING.md
grep -n -P "\x{2014}" CONTRIBUTING.md .github/PULL_REQUEST_TEMPLATE.md
grep -n "awesome-stpa" scripts/check_release.py
```

Expected: 0 issues; both greps print nothing.

- [ ] **Step 4: Commit**

```bash
git add .github/PULL_REQUEST_TEMPLATE.md CONTRIBUTING.md
git commit -m "docs: landing-chip and version-file duties in PR template and CONTRIBUTING"
```

### Task 3: Verification sweep

**Files:** none (runs the spec's verification).

**Interfaces:**
- Consumes: Tasks 1-2.
- Produces: PR-body evidence.

**Model:** standard

- [ ] **Step 1: Full gate and lint run**

```bash
python scripts/check_release.py
npx -y markdownlint-cli2 README.md CONTRIBUTING.md
```

Expected: PASS exit 0; 0 issues.

- [ ] **Step 2: Confirm greps**

```bash
grep -n "awesome-stpa" scripts/check_release.py
grep -n -P "\x{2014}" CONTRIBUTING.md .github/PULL_REQUEST_TEMPLATE.md
```

Expected: both empty.

- [ ] **Step 3: PR evidence**

Push the branch, open the PR with body containing: summary, the three negative-probe outputs from Task 1, gate PASS output, lint output. CI (validate plus the path-filtered link-check jobs, which run because CONTRIBUTING changed) must be green.
