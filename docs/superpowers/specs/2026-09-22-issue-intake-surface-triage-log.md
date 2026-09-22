| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| Read-role sub-check in Check 10 has no sourced read-role account | R1 | R1 | Genuine | Named verifier is a maintainer, who per the spec's own research sees the blank-issue entry; sub-check cannot run as written |
| "Both are idempotent" claim for the label create and reporting PUT commands | R1 | R1 | Genuine | gh label create errors 422 already exists on re-run after partial failure, a path the spec's own risk section creates |
| Sample heads ending at body: could empty bodies on literal file replace | R1 | R1 | FP | Inflation-FP: spec L149-151 mandates inserting keys and leaving title, labels, and body unchanged; no replace instruction exists |
| Verification grep covers README only, not the CONTRIBUTING stale sentence | R1 | R1 | Genuine | Check 5 greps README only; markdownlint checks style, so a stale-sentence regression passes unnoticed |
| CONTRIBUTING field enumeration omits the required privacy checkbox | R1 | R1 | Genuine | suggest-entry.yml L47-53 has a required privacy checkbox absent from the normative enumeration |
| "removal of your own entry" conflicts with the opt-out form description | R1 | R1 | Genuine | Two normative texts in the same spec disagree on who may request removal; form says a person or organization entry |
| "both contact links leave the repo" claim in Problem | R1 | R1 | Genuine | Advisory URL stays in this repo's security tab and is dead only while reporting is disabled |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Check 10 read-role sub-check has no sourced read-role account | saboteur, auditor | CRIT | Genuine | Fixed (Round 1) |
| "Both are idempotent" false for gh label create | saboteur, new_hire, auditor | MAJ | Genuine | Fixed (Round 1) |
| Bug/suggest YAML heads end at body:; full-file replace could empty bodies | new_hire | ADV | Advisory-skipped | Skipped (Round 1; spec says leave body unchanged) |
| Verification grep covers README only | auditor | ADV | Genuine | Fixed (Round 1) |
| Suggest-field enumeration omits required privacy checkbox | auditor | ADV | Genuine | Fixed (Round 1) |
| "your own entry" vs "a person or organization entry" mismatch | saboteur | ADV | Genuine | Fixed (Round 1) |
| "both contact links leave the repo" imprecise | saboteur | ADV | Genuine | Fixed (Round 1) |

Fixes applied: 6
Inflation rate: 0% (0 of 2 CRITICAL+MAJOR findings triaged FP/Recurring/Design)
Validation: SKIP

## Round 2 Summary (confirmation wave)

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| All six round-1 fixes | saboteur, new_hire, auditor | - | resolved by this change | Confirmed (Round 2) |
| Check 5 greps each pattern in one file only | saboteur | ADV | Advisory-skipped | Fixed (Round 2, cheap) |

Fixes applied: 1
Inflation rate: n/a (0 CRITICAL+MAJOR findings this round)
Validation: SKIP

## Converged: Round 2

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR. Confirmation wave: all six round-1 locs resolved by every lens.
Total rounds: 2  |  Total fixes: 7
Document is ready.
