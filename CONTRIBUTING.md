# Contributing

**Lint is mandatory.** awesome-lint on README.md must pass on every PR to main.

Thanks for helping keep this the definitive directory of the people and
organizations behind free and open systems-engineering and MBSE knowledge. Read
this before opening a PR; the CI gates enforce most of it.

The fastest path: open the "Suggest an entry" issue form with the evidence,
or open a pull request that edits `README.md` directly.

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

## 2. Inclusion bar

An entry is accepted only if **all five** hold:

1. **On-topic**: the person or org contributes free or open knowledge to systems
   engineering or MBSE: open source, open models, libraries, blogs, videos, free
   courses, open papers, public standards work, or public community organizing
   (working groups, events, forums).
2. **Substantive**: at least one named, checkable contribution that passes this
   bar on its own. Being well known, being certified, or having a LinkedIn
   presence is not a contribution. Not pure vendor marketing.
3. **Live**: the entry link resolves, and at least one cited qualifying
   contribution is publicly reachable at seed or PR time.
4. **Not duplicative**: same canonical URL, or the same person or org under a
   different URL or name variant, means duplicate. One entry per identity, ever
   (see section 6).
5. **Legally linkable**: everything cited is public. We **link**, we never
   re-host.

## 3. Entry format

One line per entry, **hyphen separator** (` - `, never an en/em dash;
awesome-lint rejects those), tags as **inline code spans inside the sentence
before the terminal period**, year parenthesized as the last token:

```text
- [Entry Name](https://example.com) - One-line factual description `who` `domain` `contribution` (YYYY).
```

- **Description:** factual, one line, **at most 140 characters** (measured from
  the first character after ` - ` to the last character before the first tag).
  State what the entry did, not how good it is: "Maintains X", "Authored Y",
  "Leads Z". No quality adjectives, no rankings.
- **One link per entry.** A second home (another profile, a project site) may
  appear as a code span or scheme-less text in the description, never as a
  second hyperlink and never as a bare URL (markdownlint MD034). A second-home
  code span never directly abuts the tag run: keep a word of prose or
  punctuation between them.
- **Primary-link precedence.** Individuals: GitHub profile when the free work
  lives there; else personal professional site; else institutional public
  profile. Orgs: GitHub org when that is the contribution home; else the
  primary public site.
- **Identity rules.** One entry per person and one per org across all their
  contributions and domains; the `domain` tag carries the primary one, and
  breadth shows in the description. One-person brands are listed as the human,
  with the brand named in the description (MBSE4U is listed as Tim Weilkiens).
  Each qualifying contribution is cited as evidence under exactly one entry,
  the org's or the person's, never both.
- **Sections are alphabetical** by entry name, case-insensitive, on the link
  text as written. This is the visible proof that nothing here is ranked.

## 4. Tag vocabulary, cardinality & order

Tags appear in this fixed order, drawn **only** from this vocabulary:

`who → domain → tool → contribution → standard → year`

| Axis | Cardinality | Values |
| ------ | ------------- | -------- |
| `who` (contributor type) | exactly 1 | `individual` · `company` · `research-group` · `community-org` |
| `domain` | exactly 1 | `MBSE-general` · `SysMLv2` · `SysML-general` · `Capella` · `Archimate` · `EA` · `RE` · `STPA` · `DE` |
| `tool` | 0 or more | `Cameo` · `CATIA-Magic` · `Capella` · `Archi` · `Sparx-EA` · `SysON` · `other-tool` |
| `contribution` | exactly 1 (dominant form) | `open-source` · `model` · `course` · `book` · `paper` · `blog` · `video` · `standards` · `community` |
| `standard` | 0 or 1 | `standard` (the entry authored or maintains a public normative document) |
| `year` | exactly 1 | `(YYYY)` (see section 5) |

- The `who` value must match the entry's section: Individual practitioners ->
  `individual`, Companies and vendors -> `company`, Academic and research
  groups -> `research-group`, Community organizations and standards bodies ->
  `community-org`.
- `domain` is the primary domain of the qualifying contribution. MagicGrid-method
  contributions take `MBSE-general`. Sparx/EA-tool contributions take `EA`
  with tool `Sparx-EA`.
- `other-tool` graduates to its own tag only once 3 or more entries share it.
- For an OMG/INCOSE normative document use `standards` as the contribution plus
  the `standard` tag, and omit `paper`.

## 5. The year rule (`YYYY`)

`(YYYY)` = the year of the entry's **most recent qualifying contribution**:

- a repo -> its latest tagged release, or the latest default-branch commit if
  untagged;
- a paper -> its publication year;
- a blog -> the substantive post's year; a video or talk -> its publication year;
- a course -> its current cohort year;
- a standard -> the latest published edition;
- an ongoing public community role (working-group or committee lead, community
  or event organizer) -> the current year, refreshed at each sweep while the
  role is held.

**Trivial edits (typo fixes) don't count.** The year token is also the staleness
anchor for the sweep prune (People policy clause 6).

## 6. Canonical-URL rule (dedupe)

Before deciding "is this a duplicate", canonicalize both URLs: force `https`,
lowercase the host, strip a trailing slash, drop the query string and fragment
unless they're semantically required. If the canonical forms match, it's a
duplicate.

On top of that, **identity dedupe**: two entries are duplicates when the
canonical URLs match **or** the evidence shows the same person or org behind
both, including name variants and brand-versus-person pairs. The primary-link
precedence rules in section 3 decide which URL survives.

## Editorial neutrality

This list is maintained by JG Systems Consulting Ltd., a commercial vendor of
SysML/Cameo consulting and tooling. To keep it trustworthy:

- JG Systems Consulting is listed, if it qualifies, under the **same inclusion
  bar** as every other vendor.
- The JG entry sits next to **at least 1 genuine competing entry** in the same
  section.
- **Position follows alphabetical order, never preference.**

> **Table of Contents:** the `## Contents` ToC is hand-maintained and lists only
> the top-level sections (a flat ToC keeps awesome-lint happy). If you add or
> rename a **top-level** section, update the ToC by hand; sub-sections are not
> listed. CI validates every ToC anchor resolves (lychee
> `--include-fragments anchor-only`).

## People policy

1. **Public professional info only.** Entries are built from work output: repos,
   papers, posts, talks, courses, public roles. Nothing else.
2. **Contribution-based criteria.** An entry exists because of a named, checkable
   free contribution. No popularity metrics, no follower counts, no
   certifications as a qualifying contribution, no rankings.
3. **No personal data.** No email addresses, postal addresses, phone numbers,
   personal social accounts, photos, family, health, or private employer
   details. An employer or institution is named only when the contribution is
   inseparable from the public role (for example a university lab lead). CI
   enforces the email part (the privacy grep job).
4. **Opt-out.** Removal on request, no questions, no argument, at any time: open
   an issue, open a PR removing your own entry, or reach the maintainer through
   any public channel. No re-add without fresh consent. The maintainer keeps a
   private opt-out register (identities only, outside the repo) and checks it
   before every harvest, sweep, and entry addition, so an opted-out person is
   never silently re-added. The CHANGELOG logs that an entry was removed on
   request, without naming the person.
5. **Corrections.** Wrong or stale attribution is fixed on report, before the
   next sweep.
6. **Staleness.** At each quarterly sweep, an entry is pruned when its most
   recent qualifying contribution is 3 or more years old (entry year at or
   before sweep year minus 3). Prunes are logged in the CHANGELOG. Three years,
   not the family's six-month badge lapse: academic and book publishing gaps run
   long, and the badge measures this list's maintenance, not contributor
   activity.
7. **Ported rules.** Section 5 (year rule) and section 6 (canonical-URL rule)
   are ported from the hub CONTRIBUTING.md rules, with the people readings
   above. Editorial neutrality is the hub's section 7 adapted to this list.
   The hub's Model Gallery section does not apply here (this list holds no
   model entries).

## Local link-check

No install needed; check your changed links with Docker:

```sh
docker run --rm -v "$PWD:/d" -w /d lycheeverse/lychee --include-fragments anchor-only README.md
```

Or open a **draft PR** and let CI check it for you.

## Landing page and version files

`docs/index.html` is a derived copy. `README.md` is the source of truth for
the sweep badge, curated sections, and entry count; `RELEASE-INFO.txt` is the
source for the version. When a PR adds or removes an entry, or touches
version files, update the landing chips (`entries`, `sweep`, `version`) and
the section-index list to match. The same applies when only the README sweep
badge changes: update the `sweep` chip. The release gate in CI fails
otherwise. CHANGELOG, RELEASE-INFO.txt, and CITATION.cff carry the same
version on every release.

## Maintenance cadence

The maintainers run a **quarterly sweep** (add, verify, prune per People policy
clause 6), logged in `CHANGELOG.md` with the date, and update the *Last full
sweep* badge at the top of the README each time. Over six months without a
sweep, the badge says maintenance lapsed.
