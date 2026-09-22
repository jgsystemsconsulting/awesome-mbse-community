---
date: 2026-09-22
package: P1 issue-intake-surface
repo: awesome-mbse-community
status: draft
classification: architectural (intake subsystem spanning forms, docs, and repo settings)
---

# Spec: issue-intake-surface (P1)

## Decision

Restore the issue intake surface by adding the two schema-required keys
(`name`, `description`) to the three existing issue forms, leaving
`config.yml` as it is, and rewriting the contributor-facing prose so it
describes the forms that ship. Two repo-settings fixes ride along because the
routing check surfaced them: the `entry` and `opt-out` labels the forms
reference do not exist, and private vulnerability reporting is disabled, which
makes the advertised advisory route dead for outsiders. No new form types, no
file renames, no gate or landing changes.

## Problem

GitHub requires every issue form to begin with `name`, `description`, and
`body`. All three forms in `.github/ISSUE_TEMPLATE/` start at `title:` and
omit the first two keys. `config.yml` sets `blank_issues_enabled: false`, so a
contributor with read access sees only the chooser's configured forms and
contact links. Of those, the Hub issues link leaves the repo and the
Security advisory link is dead until private vulnerability reporting is
enabled, so no usable intake path exists. The documented suggest, opt-out, and bug-report paths are dead
while README Support and CHANGELOG 0.1.0 claim they are live.

Live state checked on 2026-09-22 with the owner account:

- A one-off PyYAML check of the three forms reports `missing name; missing
  description` for each file (schema check, section Verification).
- `gh label list` shows `bug` and `sweep-report` but no `entry` and no
  `opt-out`. GitHub does not create missing labels from a form, so two of the
  three forms would route unlabelled even after the metadata fix.
- `GET /repos/jgsystemsconsulting/awesome-mbse-community/private-vulnerability-reporting`
  returns `{"enabled":false}`. Outsiders cannot open the advisory URL that
  SECURITY.md and the `Security advisory` contact link point at.
- `npx -y awesome-lint@2.3.0 README.md` and
  `npx -y markdownlint-cli2 README.md CONTRIBUTING.md` both pass on the
  current tree, so any lint failure after this work is caused by this work.

Prose defects in the same subsystem:

- `CONTRIBUTING.md` section 1 says "(Structured issue and PR templates arrive
  with a later effort.)" while the forms and the PR template exist.
- `README.md` Support (L115-116) documents an "improvement form" and an
  auditor code (RR-B-32). No such form exists in the tree, and the code means
  nothing to a reader.

## Research

- GitHub issue form syntax. "All issue form configuration files must begin
  with `name`, `description`, and `body` key-value pairs." `name` must be
  unique across all templates. `title` and `labels` are optional. A label
  that does not exist in the repository is not added to the issue.
  https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms
- Template chooser configuration. A template `name` "must be more than 3
  characters. If it's not, the template won't be shown when creating an
  issue." Templates list alphanumerically, YAML before Markdown. With
  `blank_issues_enabled: false`, Read and Triage roles see only the
  configured templates; Write and above also see a "Blank issue" entry
  marked "Maintainers only". Config takes effect once merged to the default
  branch.
  https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository
- Validation errors. Missing `name` raises "Required top level key `name` is
  missing".
  https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/common-validation-errors-when-creating-issue-forms
- Form body schema (element types, `id`, `attributes`, `validations`). The
  existing bodies conform; no body edits are needed for validity.
  https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema
- Private vulnerability reporting REST endpoints. `GET` returns the boolean;
  `PUT` enables it and returns 204; the caller needs admin access.
  https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28
- Parent-supplied source
  https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-in-your-repository/syntax-for-githubs-form-schema
  returned HTTP 404 on 2026-09-22. GitHub moved the section to the
  `using-templates-to-encourage-useful-issues-and-pull-requests` path above;
  the content matches the parent's summary.
- Negative result. The GraphQL field `Repository.issueTemplates` lists
  Markdown templates only. Checked against `ansible/ansible` (five YAML forms
  on disk, one `.md` template returned). It cannot serve as the chooser
  acceptance check.

## Codebase context

Sources: `C:\Users\gower\AppData\Local\Temp\rrl\pkg-bundle.md` (repo survey
and 2026-09-22 findings I1, I2, I3, advisory a-14) and work package P1 in
`docs/superpowers/packages/2026-09-22-awesome-mbse-community-packages.md`.

- `.github/ISSUE_TEMPLATE/`: `bug_report.yml`, `suggest-entry.yml`,
  `opt-out.yml` (each `title`, `labels`, `body`), `config.yml`
  (`blank_issues_enabled: false`, contact links `Security advisory` and `Hub
  issues`). The advisory URL in `config.yml` is byte-identical to the one in
  `SECURITY.md`.
- `.github/PULL_REQUEST_TEMPLATE.md`: four-line checklist, includes "no em
  dashes". Not touched here; P2 extends it.
- `CONTRIBUTING.md`: intro "fastest path" sentence (L9-10) and section 1
  (L12-19) describe free-form issues and the stale template claim. People
  policy clause 4 already says "open an issue" for opt-out and stays as is.
- `README.md`: Usage (L101-106) names the forms in lowercase prose; Support
  (L108-116) lists four bullets plus the RR-B-32 paragraph. `## Support` is
  not a curated section, so `scripts/check_release.py` ignores it.
- CI on a PR touching README or CONTRIBUTING: lychee (README only, github.com
  requests carry `GITHUB_TOKEN`, accepts 200 to 299 and 429), awesome-lint
  2.3.0 (README only), markdownlint-cli2 (README and CONTRIBUTING, MD013 off),
  privacy grep (README only), and `validate.yml` running
  `scripts/check_release.py`.
- awesome-lint 2.3.0 `list-item` rule skips any list item whose paragraph
  begins with a plain text node and validates items that begin with a link.
  Support bullets therefore must keep starting with text; links may follow.
- Chooser link `https://github.com/jgsystemsconsulting/awesome-mbse-community/issues/new/choose`
  answers an anonymous GET with 302 to the login page, which returns 200.
  lychee follows redirects and accepts the final 200.
- `CHANGELOG.md` follows Keep a Changelog and has an empty `## [Unreleased]`.
- `docs/index.html` has no reference to the forms. No landing edit.

## Scope

In scope (package P1, plus two routing fixes found during the sanity check):

1. Add `name` and `description` to the three forms.
2. Leave `config.yml` unchanged after verifying its routing (below).
3. Create the `entry` and `opt-out` labels (repo settings).
4. Enable private vulnerability reporting (repo settings, admin).
5. Rewrite the CONTRIBUTING intro sentence and section 1.
6. Rewrite README Usage wording and the Support section; delete the RR-B-32
   paragraph.
7. Add one sentence to the opt-out form body pointing at the private route.
8. Add a `### Fixed` line under `## [Unreleased]` in CHANGELOG.
9. Verify pre-merge by lint and a one-off schema check, and post-merge in the
   chooser.

Out of scope: new form types (including the improvement form), renaming form
files for chooser order, `docs/index.html`, `scripts/check_release.py`, entry
tag or alphabetical CI enforcement, the markdownlint pin, weekly sweep
behaviour, hub issue routing, `SECURITY.md` edits, People policy edits, PR
template edits (P2), committing any new script.

## Design

Target texts in this section are normative. The implementer may re-wrap lines
and fix typos but must keep the form names, links, and stated facts.

### Issue forms

Insert `name` and `description` as the first two keys of each file and leave
`title`, `labels`, and `body` unchanged, except for the one-sentence addition
in the opt-out body. The chooser shows `name` and `description`; the existing
markdown blocks render inside the form and stay. Names are unique, longer than
three characters, and match the wording used in README and CONTRIBUTING.

`bug_report.yml` head:

```yaml
name: Bug report
description: Report a broken or hijacked link, or a CI failure.
title: "[Bug] "
labels: [bug]
body:
```

`suggest-entry.yml` head:

```yaml
name: Suggest an entry
description: Propose a person or organization, with one checkable contribution as evidence.
title: "[Suggest] "
labels: [entry]
body:
```

`opt-out.yml` in full:

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

Chooser order follows filename: Bug report, Opt-out, Suggest an entry. Three
items; acceptable. Renaming files to force order is a non-goal.

### config.yml and routing

No edit. Verified facts that make the current file correct: blank issues stay
disabled so read-role contributors see only the three forms plus the two
contact links; the `Security advisory` URL equals the one in `SECURITY.md`;
the `Hub issues` target `jgsystemsconsulting/awesome-mbse` has issues enabled.
Hub routing is out of scope.

Two settings actions make the routing real. They run once by an admin before
merge. The PUT is idempotent; the two `gh label create` calls are not (a
re-run answers HTTP 422 "already exists", which is harmless), so check
`gh label list` first when re-running after a partial failure:

```sh
gh label create entry --repo jgsystemsconsulting/awesome-mbse-community --description "Suggested person or organization entry" --color 0e8a16
gh label create opt-out --repo jgsystemsconsulting/awesome-mbse-community --description "Removal request under the People policy" --color 5319e7
gh api -X PUT repos/jgsystemsconsulting/awesome-mbse-community/private-vulnerability-reporting
```

Label colours are placeholders the maintainer may change. The PUT returns 204
and needs admin on the repo; the `gh` login is the owner account.

### CONTRIBUTING.md

Replace the intro sentence at L9-10 with:

```markdown
The fastest path: open the "Suggest an entry" issue form with the evidence,
or open a pull request that edits `README.md` directly.
```

Replace section 1 (L12-19) with:

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
People policy clause 4). Security reports go through the private advisory route in
SECURITY.md.
```

Wording is normative. The implementer may re-wrap lines but must keep the form
names, the chooser link, and the two facts (forms exist, PR template exists).
Gate duties (landing chips, release gate) belong to P2 and stay out.

### README.md

Usage (L103-106) becomes:

```markdown
Browse by section, or search the Contents. Open a profile link to see the
person or organization behind a contribution. To suggest a person or
organization, use the "Suggest an entry" issue form with the contribution
evidence. To request removal, use the "Opt-out" form; no reason is needed.
```

Support (L108-116) becomes:

```markdown
## Support

Open a [new issue](https://github.com/jgsystemsconsulting/awesome-mbse-community/issues/new/choose) and pick a form:

- Suggest a person or organization: the "Suggest an entry" form
- Request removal: the "Opt-out" form, or the private advisory route for a request that should not be public
- Broken link or CI failure: the "Bug report" form
- Security: private advisory (see [SECURITY.md](SECURITY.md))
```

The RR-B-32 paragraph is deleted with no replacement. Every bullet starts
with plain text so awesome-lint skips it; the two links are markdown links so
markdownlint MD034 stays quiet; `SECURITY.md` is a relative link to an
existing file for lychee.

### CHANGELOG.md

Under `## [Unreleased]` add:

```markdown
### Fixed

- Issue forms (bug report, suggest-entry, opt-out) gained the `name` and
  `description` keys GitHub requires, so they show in the issue chooser.
  CONTRIBUTING section 1 and the README Support section now describe the
  shipped forms and the private advisory route; the phantom improvement-form
  note is gone.
```

### SECURITY.md

No edit. The route it describes becomes live when private vulnerability
reporting is enabled.

## Approaches considered

1. Metadata only. Add `name` and `description`, touch nothing else. Forms
   appear, but two of three route unlabelled, the advisory link stays dead,
   and CONTRIBUTING keeps contradicting the tree. Rejected.
2. Metadata, prose alignment, and the two settings fixes. Every path the
   README advertises works end to end after one PR and three commands.
   Chosen.
3. Approach 2 plus an improvement form and numeric filename prefixes for
   chooser order. Adds a form type the package excludes and renames files
   that CHANGELOG and deep links already name. Rejected.

## Verification

Pre-merge, run locally and paste results in the PR body. Nothing new is
committed.

1. Schema check (one-off, PyYAML is present in the local Python 3.14):

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

   Expected: three `OK` lines, exit 0. On the current tree it exits 1 with
   `missing name; missing description` for each file.
2. `npx -y awesome-lint@2.3.0 README.md` exits 0.
3. `npx -y markdownlint-cli2 README.md CONTRIBUTING.md` reports 0 issues.
4. `python scripts/check_release.py` prints `release gate: PASS`.
5. `grep -n "RR-B-32\|improvement form" README.md CONTRIBUTING.md` and
   `grep -n "arrive with a later effort" README.md CONTRIBUTING.md` print
   nothing.
6. `grep -n -P "\x{2014}" README.md CONTRIBUTING.md CHANGELOG.md .github/ISSUE_TEMPLATE/*.yml`
   prints nothing (em dash ban).
7. `gh label list`, run inside the repo checkout, includes `bug`, `entry`,
   `opt-out`.
8. `gh api repos/jgsystemsconsulting/awesome-mbse-community/private-vulnerability-reporting`
   returns `{"enabled":true}`.
9. The PR CI (`link-check (PR)` four jobs and `validate`) is green.

Post-merge, on the default branch, by a maintainer in a browser:

10. The chooser at `/issues/new/choose` lists exactly three forms with the
    names and descriptions above and the two contact links. If a read-role
    account is available, confirm it sees no blank-issue entry;
    `blank_issues_enabled: false` already guarantees this in configuration.
11. Each deep link `/issues/new?template=bug_report.yml`,
    `?template=suggest-entry.yml`, `?template=opt-out.yml` renders its fields
    with the required markers.
12. Optional smoke: file one issue from the Suggest form, confirm the `entry`
    label lands, close it.

## Risks and assumptions

- Enabling private vulnerability reporting needs admin. If the PUT returns
  4xx, stop and report; do not substitute an email or other channel (People
  policy forbids email addresses in the README, and SECURITY.md is out of
  scope here).
- Issue templates read from the default branch only, so the chooser check
  cannot run on the PR. The schema check stands in pre-merge.
- The chooser URL returns a login redirect to anonymous clients. lychee
  accepts the final 200 today. If GitHub starts answering 404 to anonymous
  clients, swap the README link target to
  `https://github.com/jgsystemsconsulting/awesome-mbse-community/issues`.
- The RR-B-32 note may have been copied from a sibling spoke that does ship
  an improvement form. Removing the note here changes no auditor behaviour
  because the file it describes never existed in this repo. If a family
  checklist requires the form, that is a new form type for the backlog.
- Label colours and descriptions are editorial; the label names are not.

## Open questions

None. The one admin dependency (private vulnerability reporting) has a known
owner: the `gh` login used for the live checks is the repository owner.
