---
date: 2026-09-22
package: P3 entry-policy-gates
repo: awesome-mbse-community
status: draft
classification: subsystem slice (curated-entry policy enforcement in the release gate)
---

# Spec: entry-policy-gates (P3)

author-leaf: fallback (inline); research: skipped (all facts repo-internal)

## Decision

Extend the curated walk in `scripts/check_release.py` with four fail-closed
checks taken straight from CONTRIBUTING: tag vocabulary with fixed order,
who-tag vs section pairing, case-insensitive alphabetical order of entries
within each curated section, and the 140-character description limit with a
single-hyperlink rule. Failures name the section and the offending line.
validate.yml keeps running the gate; no workflow change and no committed test
harness.

## Problem

CONTRIBUTING says "the CI gates enforce most of it", but the only structural
entry check is the loose `ENTRY_RX` bullet-grammar regex (link, hyphen
separator, trailing year). Nothing validates tag vocabulary, tag order, or
who-vs-section pairing; nothing enforces the alphabetical ordering that
CONTRIBUTING calls "the visible proof that nothing here is ranked"; the
140-character description limit and the one-hyperlink rule are unchecked. A
policy-breaking or ranking-shaped entry merges green today.

## Research

- `scripts/check_release.py` curated walk: `CURATED_SECTIONS` tuple of the
  four section titles; `ENTRY_RX` at L136; `curated_walk()` iterates
  headings, counts entries, and appends `curated entry malformed in
  {section}: {line[:60]}` on grammar failures. `landing_chip(html,
  "entries")` must equal the curated total, so entry-count-affecting fixes
  here stay count-neutral or the landing chip must be updated in the same PR.
- CONTRIBUTING section 3: description at most 140 characters, measured from
  the first character after ` - ` to the last character before the first
  tag; one link per entry (a second home may appear as a code span or
  scheme-less text, never a second hyperlink or bare URL). Section 4: tag
  axes and cardinality, fixed order `who domain [tool...] contribution
  [standard] (YYYY)`; who values `individual`, `company`, `research-group`,
  `community-org` map 1:1 to the four curated sections; domain values
  `MBSE-general SysMLv2 SysML-general Capella Archimate EA RE STPA DE`; tool
  values `Cameo CATIA-Magic Capella Archi Sparx-EA SysON other-tool` (open
  set pending graduation); contribution values `open-source model course
  book paper blog video standards community`; `standard` 0 or 1; year is
  the `(YYYY)` terminal token already required by ENTRY_RX.
- Current README has 59 curated entries (landing `entries` chip = 59) and
  the gate passes; all who-tags pair correctly with their sections on a
  spot read of the Individual practitioners section.
- The functional em dash in check_release.py L35 (FORBIDDEN_CONTENT) must
  remain.

## Scope

In scope: the four new checks inside `curated_walk()` (or immediately after
it, sharing its heading/line iteration); failure messages carrying section
and line text; gate PASS on the current tree, or an explicit list of entry
edits required to reach PASS (applied in the same PR, keeping the entries
chip in sync).

Out of scope: re-curation beyond fixes needed to pass; year-rule live
verification; URL identity dedupe; version cross-checks (P4, merged);
doc rewrites; tag vocabulary changes; a committed test harness; sweep
automation.

## Design

Parse each entry line (already matched by `ENTRY_RX`) into: link text,
description, and the trailing tag run.

**Tag run.** The tag run is the maximal sequence of trailing backticked
tokens immediately before the terminal `(YYYY).` token, period included in
the anchor. Extract it by anchoring at the end: strip the trailing
`(YYYY).`, then collect backticked tokens backward, stopping at the first
token that is not a known vocabulary word (a CONTRIBUTING-legal second-home
code span adjacent to the tag run therefore ends collection and is reported
by the unknown-tag check if it ever occurs; keep prose or punctuation
between it and the tags per CONTRIBUTING). Code spans inside the description
are never mistaken for tags. A backticked `(YYYY)` cannot reach these
checks: ENTRY_RX's terminal `\(\d{4}\)\.$` already rejects such lines as
malformed grammar.

**Description.** The description is the text between the ` - ` separator
that follows the link's closing parenthesis and the start of the tag run,
stripped. (Anchoring at the separator after `)` avoids misparsing link text
that itself contains ` - `.)

**Bare-URL detection.** Remove all markdown `[text](url)` spans and all
backticked code spans from the line, then search `https?://\S+` on the
remainder.

For each entry, in walk order, per curated section:

1. **Vocabulary and order.** Map each tag-run token to an axis via the
   CONTRIBUTING vocabulary tables; unknown token -> fail `unknown tag in
   {section}: {token} ({line[:60]})`. Tokens valid on two axes (today only
   `Capella`: domain and tool) take the axis assignment that keeps the rank
   sequence non-decreasing, where rank is `who=0, domain=1, tool=2,
   contribution=3, standard=4` (so a `Capella` between domain and
   contribution is the tool; when rank alone leaves a dual-axis token
   ambiguous, choose the assignment that also satisfies cardinality,
   preferring the lower rank). Order must be non-decreasing in rank and
   cardinality must hold: exactly one who, exactly one domain, exactly one
   contribution, zero or more tools, zero or one standard; violations ->
   fail `tag order or cardinality in {section}: {tokens}`. A line with an
   empty tag run -> fail `missing tags in {section}: {line[:60]}`.
2. **Who pairing.** The rank-0 tag must equal the section's expected who
   value (dict from CURATED_SECTIONS); else fail `who tag {got} does not
   match section {section}`.
3. **Alphabetical order.** Keep the previous link text per section
   (casefold); if `current.casefold() < previous.casefold()`, fail
   `entries out of alphabetical order in {section}: {previous} >
   {current}`.
4. **Description length and single link.** With the description bounded at
   the tag-run start (see above): len > 140 -> fail `description over 140
   chars in {section} ({n})`. More than one markdown hyperlink in the line
   -> fail `second hyperlink in {section} ({line[:60]})`; a remaining
   `https?://` hit after removing link spans -> fail `bare URL in {section}
   ({line[:60]})`.

All failures append to `fails`; the script exits non-zero as today. No new
CLI surface, no config.

## Approaches considered

1. Separate lint script. Rejected: CONTRIBUTING promises one gate; two
   runners double the fail-closed surface.
2. Enforce inside ENTRY_RX with one mega-regex. Rejected: unreadable and
   still misses cross-line alphabetical order.
3. Structured per-entry checks in the walk (chosen). Readable failures,
   fail-closed, stdlib only.

## Verification

1. `python scripts/check_release.py` on the tree: PASS, exit 0 (expected;
   current entries conform on inspection). If it fails, the spec's fallback
   applies: fix the listed entries in the same PR (content-neutral fixes
   only: tag order, casing, description trim) and update nothing else; the
   entries count must not change.
2. Negative probes (temporary, restored, outputs in the PR body), one per
   failure mode: (a) swap two adjacent entries -> alphabetical failure;
   (b) change a who tag to the wrong value -> pairing failure; (c) append an
   unknown backticked token -> vocabulary failure; (d) lengthen a
   description past 140 -> length failure; (e) add a second hyperlink ->
   single-link failure; (f) reorder valid tokens (standard before
   contribution) -> tag-order failure; (g) append a bare `https://` URL ->
   bare-URL failure; (h) strip one entry's tags entirely -> `missing tags`
   failure. Each probe: gate exit 1 with the new message, restore, gate
   PASS.
3. `python -m py_compile scripts/check_release.py` exit 0.
4. CI on the PR: validate plus path-filtered link-check jobs green (README
   is in the path filter; any entry fix shows up there).

## Risks and assumptions

- Vocabulary tables duplicate CONTRIBUTING content. Accepted: the gate is
  the enforcement point; drift shows up as loud failures, not silent ones.
- Tool axis is an open set pending `other-tool` graduation; unknown tool
  tokens fail until CONTRIBUTING admits them. This is the intended
  fail-closed behavior.
- Casefold comparison matches CONTRIBUTING's "case-insensitive" wording;
  stable for ASCII names.

## Open questions

None.
