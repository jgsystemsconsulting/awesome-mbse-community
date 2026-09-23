---
date: 2026-09-22
package: P4 release-gate-truth
repo: awesome-mbse-community
status: draft
classification: subsystem slice (release-gate script plus its contributor-facing contract)
---

# Spec: release-gate-truth (P4)

## Decision

Extend `scripts/check_release.py` so release version identity is
cross-checked (CITATION.cff version, the RELEASE-INFO Tag line, and the
newest CHANGELOG semver section against the RELEASE-INFO Version; release
dates stay unenforced), and document the
landing-chip sync duty in the PR template and CONTRIBUTING so external
contributors can pass the gate on the first try. Fix the stale
"awesome-stpa" module docstring. The landing truth gate itself stays; the
landing stays a derived copy.

## Problem

The gate treats the RELEASE-INFO `Version` field as source of truth and
compares it only to the landing `version` chip (check_release.py L79-90).
`CITATION.cff` `version:` and the RELEASE-INFO `Tag:` line are never read, and
no CHANGELOG section is tied to the same value. The PR template instructs
"Version files (CHANGELOG, RELEASE-INFO, CITATION) updated together", but a PR
that updates one and lags the others passes `validate` green. Published
citation metadata can diverge from the tagged release while the gate prints
PASS.

Separately, the landing-chip duty is undocumented for contributors:
`validate.yml` runs the gate on every PR to main, and the gate requires
`docs/index.html` chips (entries, version, sweep) and section-index fragments
to match README and RELEASE-INFO, but neither CONTRIBUTING nor the PR template
mentions `docs/index.html`. A first-time entry PR fails on a requirement
documented only inside the gate script's comments.

author-leaf: fallback (inline); research: skipped (all facts repo-internal)

## Research

- Repo file `scripts/check_release.py`: `landing_chip()` (L67-72) parses
  `<dt>name</dt><dd>value</dd>` pairs from `docs/index.html`; the version
  assertion (L79-90) compares the chip to `Version:` in RELEASE-INFO only;
  the sweep assertion (L93-101) compares the `sweep` chip to the README badge;
  `curated_walk()` and the entries/fragments assertions run after; `main`
  tail prints all `fails` and `release gate: PASS` on success (L187-193).
- `CITATION.cff` L4: `version: 0.1.0`. `RELEASE-INFO.txt` L2/L4:
  `Version: 0.1.0` / `Tag: v0.1.0`. `CHANGELOG.md` L6/L16: `## [Unreleased]`
  and `## [0.1.0] - 2026-09-22`.
- `.github/workflows/validate.yml` runs `python scripts/check_release.py`;
  the step fails the PR on non-zero exit. The four link-check jobs are
  path-filtered (link-check-pr.yml `paths:` filter) and run only when README,
  CONTRIBUTING, or workflow files change.
- `.github/PULL_REQUEST_TEMPLATE.md` L4: "Version files (CHANGELOG,
  RELEASE-INFO, CITATION) updated together".
- CONTRIBUTING.md has no landing-chip or `docs/index.html` mention (grep
  clean on 2026-09-22).

## Codebase context

- The gate is a single flat script; assertions append to `fails: list[str]`
  and the script exits non-zero when any exist. Fail-closed is the existing
  pattern: missing or ambiguous reads append failures.
- Version-bearing files: `RELEASE-INFO.txt` (Version, Built, Tag),
  `CITATION.cff` (version, date-released), `CHANGELOG.md` (sections). The
  tag convention is `v` + version (`v0.1.0`).
- The landing gate comment block (L52-57) already states the source-of-truth
  rule: README and RELEASE-INFO are sources; chips and fragments are derived
  copies.
- PRs to main run: lychee, awesome-lint 2.3.0 (README), markdownlint-cli2
  (README, CONTRIBUTING), privacy grep (README), and validate (the gate).
  Any CONTRIBUTING text added here must pass markdownlint (the template file
  is not CI-linted) and contain no em dashes.

## Scope

In scope:

1. New gate assertions: CITATION.cff `version:` equals RELEASE-INFO
   `Version:`; RELEASE-INFO `Tag:` equals `v` + Version; the newest
   semver-matching CHANGELOG `## [x.y.z]` heading equals Version. Missing or
   unreadable files keep appending failures (fail-closed).
2. Landing-chip duty documented in the PR template checklist and a short
   CONTRIBUTING subsection (sources of truth vs derived chips; what to touch
   when entries, sweep, or version change).
3. Docstring fix: "Adapted for awesome-stpa" replaced with the correct
   awesome-mbse-community identity.

Out of scope: removing or weakening the landing gate; auto-generating
docs/index.html; performing a version bump; CITATION.cff schema changes;
issue forms (P1, merged); markdownlint pin (P5); a full unit-test harness;
weekly sweep behavior; FORBIDDEN_CONTENT glob changes.

## Design

### Gate assertions (scripts/check_release.py)

Insert after the existing version-chip assertion, inside the
`if release_info is not None:` version branch, keeping the flat
append-to-`fails` style:

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

Note: the newest CHANGELOG release section is `rel[0]` because Keep a
Changelog lists newest first; `[Unreleased]` does not match the semver
pattern. If a future bump keeps `[Unreleased]` above, the assertion still
compares the first semver hit.

### Docstring

Replace the docstring's second sentence with:

```
Standalone model for awesome-mbse-community: no src/ layout, no package
install, no scripts beyond the gate itself.
```

### PR template

Replace the L4 checklist line with:

```markdown
- [ ] Version files (CHANGELOG, RELEASE-INFO, CITATION) updated together, and docs/index.html chips matched (entries, sweep, version)
```

### CONTRIBUTING

Add a short subsection directly after the "Local link-check" section:

```markdown
## Landing page and version files

`docs/index.html` is a derived copy. `README.md` is the source of truth for
the sweep badge, curated sections, and entry count; `RELEASE-INFO.txt` is the
source for the version. When a PR adds or removes an entry, or touches
version files, update the landing chips (`entries`, `sweep`, `version`) and
the section-index list to match. The same applies when only the README sweep
badge changes: update the `sweep` chip. The release gate in CI fails
otherwise.
CHANGELOG, RELEASE-INFO.txt, and CITATION.cff carry the same version on every
release.
```

## Approaches considered

1. Gate-only. Assertions land but contributors still hit the undocumented
   chip requirement. Rejected; the onboarding bite is the HIGH half of this
   package.
2. Docs-only. Contributors learn the rule but drift stays possible.
   Rejected.
3. Gate assertions plus the contributor contract (chosen). One PR makes
   drift fail CI and names the duty where contributors actually read.

## Verification

1. `python scripts/check_release.py` prints `release gate: PASS`, exit 0 on
   the unchanged tree (all version files currently agree at 0.1.0).
2. Negative probes (temporary, not committed), each executed with its output
   pasted in the PR body, file restored after each: (a) change CITATION.cff
   version to 9.9.9 and observe the CITATION mismatch line; (b) change
   RELEASE-INFO Tag to v9.9.9 and observe the Tag mismatch line; (c) change
   the newest CHANGELOG semver heading to [9.9.9] and observe the CHANGELOG
   mismatch line.
3. `npx -y markdownlint-cli2 README.md CONTRIBUTING.md` reports 0 issues;
   `grep -n -P "\x{2014}" CONTRIBUTING.md .github/PULL_REQUEST_TEMPLATE.md`
   prints nothing. The em dash inside check_release.py's FORBIDDEN_CONTENT
   regex (L35) is pre-existing and functional; the published-prose ban does
   not apply to it.
4. CI on the PR: validate green and (because this PR touches CONTRIBUTING
   and the template) the path-filtered link-check jobs green.
5. `grep -n "awesome-stpa" scripts/check_release.py` prints nothing.

## Risks and assumptions

- The CHANGELOG assertion assumes newest-release-first ordering; if the file
  ever reorders, the gate fails loudly rather than silently passing.
- `read_source` failures append "unreadable source file" already, so missing
  CITATION/CHANGELOG stay fail-closed.
- Landing chips are checked only when `docs/index.html` parses; unchanged
  behavior.

## Open questions

None.
