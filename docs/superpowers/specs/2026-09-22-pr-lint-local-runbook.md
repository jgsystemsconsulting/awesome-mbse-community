---
date: 2026-09-22
package: P6 pr-lint-local-runbook
repo: awesome-mbse-community
status: draft
classification: docs-only (CONTRIBUTING local preflight recipes)
---

# Spec: pr-lint-local-runbook (P6)

author-leaf: fallback (inline); research: skipped (repo-internal; CI commands copied from the workflow files)

## Decision

Extend CONTRIBUTING's "Local link-check" section into a complete local
preflight runbook: recipes for every check CI runs (lychee, awesome-lint
2.3.0, the pinned markdownlint-cli2, the privacy grep, and
`python scripts/check_release.py`), each command copied from CI where
possible so local and CI behavior match.

## Problem

CONTRIBUTING calls awesome-lint mandatory and lists the other CI checks, but
the only local recipe is a Docker lychee one-liner. A contributor without
Docker, or wanting a full preflight, cannot reproduce the mandatory gates
and iterates through CI failures instead.

## Research

- CI commands (`.github/workflows/link-check-pr.yml`): lychee job (CI uses
  the `lycheeverse/lychee-action` rather than Docker, with `GITHUB_TOKEN`,
  args include `--accept 200..=299,429`, `--max-concurrency 4`, and
  `--include-fragments anchor-only`); awesome-lint:
  `npx awesome-lint@2.3.0 README.md`; markdownlint (pinned in P5):
  `npx -y markdownlint-cli2@0.23.3 "README.md" "CONTRIBUTING.md"`;
  privacy grep: `grep -nE '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9-.]+\b' README.md`
  (fails if any match).
- validate.yml: `python scripts/check_release.py` (needs Python 3 with
  stdlib only).
- CONTRIBUTING "Local link-check" section currently: Docker lychee one-liner
  (`docker run --rm -v "$PWD:/d" -w /d lycheeverse/lychee --include-fragments
  anchor-only README.md`) plus the draft-PR advice; it omits CI's `--accept`
  flag and token note.

## Scope

In scope: rewrite/extend the "Local link-check" section (retitle "Local
checks") with the five recipes and a one-line token note for lychee on
GitHub-rate-limited links. No other CONTRIBUTING changes; no workflow
changes; no new scripts.

Out of scope: new lint tools; lychee `--accept 429` policy change; privacy
grep scope; weekly sweep; gate logic.

## Design

Replace the "## Local link-check" section body (through the draft-PR line,
before "## Landing page and version files") with the block below. Nesting
note: the outer fence in this Design block uses four backticks so the inner
```sh fences survive; the `sh` language tag satisfies markdownlint MD040.

````markdown
## Local checks

Run the same checks CI runs. Docker is needed only for the link check;
everything else needs Node 20, Python 3 (standard library only), and GNU grep
(Linux, WSL, or Git Bash).

```sh
# Link check (README). Set a token first to avoid github.com rate limits:
#   export GITHUB_TOKEN=<your token>
docker run --rm -v "$PWD:/d" -w /d -e GITHUB_TOKEN lycheeverse/lychee \
  --include-fragments anchor-only --accept 200..=299,429 README.md

# Awesome-list lint (mandatory; -y skips the npx install prompt CI does not have):
npx -y awesome-lint@2.3.0 README.md

# Markdown lint:
npx -y markdownlint-cli2@0.23.3 "README.md" "CONTRIBUTING.md"

# Privacy grep (People policy clause 3; must print nothing):
grep -nE '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9-.]+\b' README.md

# Release gate:
python scripts/check_release.py
```

Or open a **draft PR** and let CI check it for you.
````

Deliberate deviations from the CI invocations, stated so nobody chases
them: the local lychee line drops `--max-concurrency 4` and `--no-progress`
(interactive progress is fine locally) and writes `--include-fragments
anchor-only` in space form (equivalent to CI's equals form); awesome-lint
gains `-y` (no install prompt). Everything else matches CI byte-for-byte.

## Verification

1. Each command runs locally and matches CI's outcome: lychee PASS (or
   link failures that are real), awesome-lint exit 0, markdownlint 0
   issues, grep prints nothing, gate prints PASS.
2. `npx -y markdownlint-cli2@0.23.3 "README.md" "CONTRIBUTING.md"`: 0
   issues with the new section.
3. `grep -n -P "\x{2014}" CONTRIBUTING.md .github/PULL_REQUEST_TEMPLATE.md`:
   nothing.
4. CI on the PR: markdownlint and validate green (CONTRIBUTING is in the
   path filter, so the lint job runs).

## Risks and assumptions

- The Docker lychee line with `-e GITHUB_TOKEN` requires the variable to be
  set locally; the runbook says so in one clause.
- Commands drift if CI changes; the section names the workflow file as the
  source of truth.

## Open questions

None.
