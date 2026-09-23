# Pin markdownlint (P5) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Pin the PR markdownlint job to `markdownlint-cli2@0.23.3`.

**Architecture:** One line in `.github/workflows/link-check-pr.yml`.

**Tech Stack:** GitHub Actions YAML, npx.

**Spec:** docs/superpowers/specs/2026-09-22-pin-markdownlint.md

## Research

`npx -y markdownlint-cli2 --version` reports `v0.23.3` on this tree (2026-09-22); npm latest is 0.23.3. research: skipped (repo-internal).

## Global Constraints

- Only L64 of link-check-pr.yml changes; everything else byte-identical.
- Pinned lint must report 0 issues on README + CONTRIBUTING.

---

### Task 1: Pin the version

**Files:**
- Modify: `.github/workflows/link-check-pr.yml:64`

**Interfaces:**
- Consumes: nothing. Produces: pinned lint job.

**Model:** flash

- [ ] **Step 1: Edit the line**

Replace:

```yaml
        run: npx -y markdownlint-cli2 "README.md" "CONTRIBUTING.md"
```

with:

```yaml
        run: npx -y markdownlint-cli2@0.23.3 "README.md" "CONTRIBUTING.md"
```

- [ ] **Step 2: Verify**

```bash
npx -y markdownlint-cli2@0.23.3 "README.md" "CONTRIBUTING.md"
python -c "import yaml; yaml.safe_load(open('.github/workflows/link-check-pr.yml')); print('ok')"
git diff --stat
```

Expected: 0 issues; `ok`; only the workflow file changed (1 line).

- [ ] **Step 3: Commit, push, PR**

```bash
git add .github/workflows/link-check-pr.yml
git commit -m "ci: pin markdownlint-cli2 to 0.23.3"
git push -u origin p5-pin-markdownlint
gh pr create --base main --title "ci: pin markdownlint-cli2 (P5)" --body "Pins the PR markdownlint job to markdownlint-cli2@0.23.3, matching the awesome-lint@2.3.0 pin discipline. Local run of the pinned version: 0 issues."
```

CI markdownlint job must be green on the PR.
