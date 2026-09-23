---
date: 2026-09-22
package: P5 pin-markdownlint-runbook
repo: awesome-mbse-community
status: draft
classification: single-file CI change
---

# Spec: pin-markdownlint-runbook (P5)

author-leaf: fallback (inline); research: skipped (repo-internal; the pinned version is whatever `npx -y markdownlint-cli2 --version` reports on this tree, a repo-verifiable fact, not a web lookup)

## Decision

Pin the PR markdownlint job to the same explicit version discipline as the
awesome-lint job: `npx -y markdownlint-cli2@<version>`, where `<version>` is
the version this repo's CI resolves today (recorded in Verification). One
line changes in `.github/workflows/link-check-pr.yml`.

## Problem

The markdownlint job installs via unpinned `npx -y markdownlint-cli2`, so
every matching PR executes whatever version npm serves that day, while
awesome-lint@2.3.0 and all action SHAs are pinned in the same file. A
compromised or breaking publish changes CI behavior or worse; this is the
repo's one floating supply-chain input on the public PR path.

## Research

- `.github/workflows/link-check-pr.yml` L64 (current):
  `run: npx -y markdownlint-cli2 "README.md" "CONTRIBUTING.md"`; L54 shows
  the pinned pattern `run: npx awesome-lint@2.3.0 README.md`.
- Current resolved version observed locally on 2026-09-22: recorded in the
  Verification section (run `npx -y markdownlint-cli2 --version`).
- No other workflow file invokes markdownlint.

## Scope

In scope: pin the markdownlint-cli2 version in `link-check-pr.yml` only.
Out of scope: lychee accept codes, schedule workflow, new lint tools, branch
protection, the local runbook (P6).

## Design

Replace L64 with:

```yaml
        run: npx -y markdownlint-cli2@<version> "README.md" "CONTRIBUTING.md"
```

`<version>` is filled by Verification step 1. Nothing else in the file
changes.

## Verification

1. `npx -y markdownlint-cli2 --version` locally: `markdownlint-cli2 v0.23.3`;
   use `0.23.3` for `<version>`.
2. `npx -y markdownlint-cli2@<version> "README.md" "CONTRIBUTING.md"`
   reports 0 issues.
3. YAML sanity: `python -c "import yaml,sys; yaml.safe_load(open('.github/workflows/link-check-pr.yml')); print('ok')"`.
4. CI on the PR: markdownlint job green.

## Risks and assumptions

- The pinned version freezes behavior; future upgrades are deliberate bumps
  of this line. Accepted and intended.

## Open questions

None.
