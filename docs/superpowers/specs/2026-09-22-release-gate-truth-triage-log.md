| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| M1 em-dash grep over touched files unsatisfiable (spec.md:L189-190) | R1 | R1 | Genuine | Verified: check_release.py L35 has a functional U+2014 in FORBIDDEN_CONTENT; scope the grep to CONTRIBUTING.md and the PR template |
| M2 quoted CITATION.cff version false-fails (spec.md:L108) | R1 | R1 | Genuine | Regex captures a quoted scalar verbatim; CFF allows quotes, so strip them before the compare |
| A1 CHANGELOG heading regex rejects prerelease tags (spec.md:L124) | R1 | R1 | Design | Spec explicitly scopes the pattern to plain x.y.z; prerelease releases are not a repo convention |
| A2 Tag without v prefix mislabeled as absence (spec.md:L117-119) | R1 | R1 | Advisory-skipped | Gate already fails closed on 0 matches; message polish only on a fixed-format maintainer-edited field |
| A3 Decision calls CHANGELOG tie optional (spec.md:L15) | R1 | R1 | Genuine | Contradicts the unconditional assertion in Scope and Design; drop "optional" |
| A4 CONTRIBUTING draft omits sweep-only trigger (spec.md:L164-166) | R1 | R1 | Genuine | Sweep badge change with no entry change still requires the sweep chip update |
| A5 Template says entry count, chip is entries (spec.md:L152) | R1 | R1 | Genuine | One-word alignment with chip names used by the gate and the CONTRIBUTING draft |
| A6 Only CITATION negative probe executed (spec.md:L186-189) | R1 | R1 | Genuine | Two extra temporary-edit runs cost nothing; a mental repeat is not verification |
| A7 "Fully cross-checked" oversells (spec.md:L13-15) | R1 | R1 | Genuine | Dates stay unenforced; reword to name exactly the three enforced fields |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Em-dash grep unsatisfiable (functional L35 em dash) | saboteur | MAJ | Genuine | Fixed (Round 1) |
| CFF quoted-version false-fail | saboteur, auditor | MAJ | Genuine | Fixed (Round 1; quote-stripping regex) |
| CHANGELOG prerelease headings rejected | saboteur | ADV | Design | Wontfix (Round 1; repo declares plain semver releases, fails loudly) |
| Tag-without-v mislabeled as absence | saboteur | ADV | Design | Wontfix (Round 1; fail-closed, format documented in CONTRIBUTING text) |
| Decision/Scope CHANGELOG optionality mismatch | new_hire | ADV | Genuine | Fixed (Round 1) |
| Sweep-only trigger missing | new_hire | ADV | Genuine | Fixed (Round 1) |
| 'entry count' vs entries chip name | new_hire | ADV | Genuine | Fixed (Round 1) |
| Only CITATION probe executed | auditor | ADV | Genuine | Fixed (Round 1) |
| 'fully cross-checked' oversells | auditor | ADV | Genuine | Fixed (Round 1) |

Fixes applied: 7
Inflation rate: 0% (0 of 2 CRITICAL+MAJOR triaged FP/Design)
Validation: SKIP

## Round 2 Summary (confirmation wave)

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| All six round-1 fixes | saboteur | - | resolved by this change | Confirmed (Round 2) |

Fixes applied: 0
Inflation rate: n/a
Validation: SKIP

## Converged: Round 2

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR. Confirmation wave: all six locs resolved.
Total rounds: 2  |  Total fixes: 7
Document is ready.
