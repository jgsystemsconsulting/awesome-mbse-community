# Local preflight runbook (P6) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** CONTRIBUTING documents a local recipe for every check CI runs.

**Architecture:** One section replacement in CONTRIBUTING.md. The spec's Design block is the exact replacement text, including the four-backtick outer fence.

**Tech Stack:** Markdown; the commands themselves (docker, npx, grep, python).

**Spec:** docs/superpowers/specs/2026-09-22-pr-lint-local-runbook.md

## Research

CI commands verified against `.github/workflows/link-check-pr.yml` (lychee action, awesome-lint@2.3.0, markdownlint-cli2@0.23.3, privacy grep) and `.github/workflows/validate.yml` (release gate). research: skipped (repo-internal).

## Global Constraints

- Only the "Local link-check" section changes; everything before and after is untouched.
- No em dashes; `npx -y markdownlint-cli2@0.23.3 "README.md" "CONTRIBUTING.md"` reports 0 issues after the edit.
- The rendered section must contain one code block with the five commands (fence nesting correct).

---

### Task 1: Replace the section

**Files:**
- Modify: `CONTRIBUTING.md` (the "## Local link-check" section, before "## Landing page and version files")

**Interfaces:**
- Consumes: spec Design block verbatim.
- Produces: contributor-facing runbook.

**Model:** flash

- [ ] **Step 1: Apply the replacement**

Copy the four-backtick-fenced block from the spec's Design section (the inner content, without the outer fence) over the current "Local link-check" section body. Retitle to "## Local checks".

- [ ] **Step 2: Execute the recipes as verification**

```bash
npx -y awesome-lint@2.3.0 README.md
npx -y markdownlint-cli2@0.23.3 "README.md" "CONTRIBUTING.md"
grep -nE '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9-.]+\b' README.md
python scripts/check_release.py
```

Expected: exit 0; 0 issues; grep prints nothing; gate PASS. (Docker lychee recipe optional to run; CI covers it.)

- [ ] **Step 3: Lint and em dash grep**

```bash
npx -y markdownlint-cli2@0.23.3 "README.md" "CONTRIBUTING.md"
grep -n -P "\x{2014}" CONTRIBUTING.md
```

Expected: 0 issues; nothing.

- [ ] **Step 4: Commit, push, PR**

```bash
git add CONTRIBUTING.md
git commit -m "docs: local preflight recipes for every CI check"
git push -u origin p6-local-runbook
gh pr create --base main --title "docs: local preflight runbook (P6)" --body "Extends the Local link-check section into a full local preflight runbook: lychee (with token and CI flags), awesome-lint@2.3.0, pinned markdownlint-cli2@0.23.3, privacy grep, and the release gate. All recipes executed locally; outputs in this PR."
```

CI markdownlint job (runs because CONTRIBUTING changed) and validate must be green.
