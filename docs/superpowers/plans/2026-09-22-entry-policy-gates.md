# Entry policy gates (P3) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** The release gate enforces tag vocabulary/order, who-vs-section pairing, per-section alphabetical order, description length, and the single-link rule for all curated entries.

**Architecture:** One new check function in `scripts/check_release.py`, invoked per curated-entry line inside the existing walk; failures append to `fails` as today. Spec is the authority: docs/superpowers/specs/2026-09-22-entry-policy-gates.md (its Design section is the parsing contract).

**Tech Stack:** Python stdlib (re). No new dependencies, no workflow change.

**Spec:** docs/superpowers/specs/2026-09-22-entry-policy-gates.md

## Research

All facts repo-internal. Verified anchors: `ENTRY_RX` at check_release.py L136; `curated_walk()` follows immediately; `fails` appends and non-zero exit at the tail; 59 curated entries (20+12+11+16) with landing `entries` chip = 59. research: skipped (all facts repo-internal).

## Global Constraints

- Fail-closed: any parse ambiguity appends a failure; nothing passes silently.
- stdlib only; no committed test harness (negative probes in Verification are the proof, captured in the PR body).
- The functional em dash in check_release.py L35 (FORBIDDEN_CONTENT regex) is untouched.
- Gate prints `release gate: PASS (scanned 1 files)` on the tree after the change (current entries conform); if it fails, apply only content-neutral entry fixes from the spec fallback and keep the entries count unchanged.
- `python -m py_compile scripts/check_release.py` exit 0.

---

### Task 1: Implement the entry policy checks

**Files:**
- Modify: `scripts/check_release.py` (inside/after `curated_walk()`)

**Interfaces:**
- Consumes: existing `CURATED_SECTIONS`, `ENTRY_RX`, `fails`, the walk's heading/line iteration.
- Produces: failure modes `unknown tag`, `tag order or cardinality`, `missing tags`, `who tag ... does not match section`, `entries out of alphabetical order`, `description over 140 chars`, `second hyperlink`, `bare URL` — each carrying the section and line text.

**Model:** deep

- [ ] **Step 1: Add vocabulary tables and the check function**

Add after `ENTRY_RX` (names and shape per the spec's Design):

```python
WHO_BY_SECTION = {
    "Individual practitioners": "individual",
    "Companies and vendors": "company",
    "Academic and research groups": "research-group",
    "Community organizations and standards bodies": "community-org",
}
AXIS_RANK = {"who": 0, "domain": 1, "tool": 2, "contribution": 3, "standard": 4}
CARDINALITY = {"who": 1, "domain": 1, "tool": None, "contribution": 1, "standard": (0, 1)}
VOCAB = {
    "who": {"individual", "company", "research-group", "community-org"},
    "domain": {"MBSE-general", "SysMLv2", "SysML-general", "Capella", "Archimate", "EA", "RE", "STPA", "DE"},
    "tool": {"Cameo", "CATIA-Magic", "Capella", "Archi", "Sparx-EA", "SysON", "other-tool"},
    "contribution": {"open-source", "model", "course", "book", "paper", "blog", "video", "standards", "community"},
    "standard": {"standard"},
}
```

- [ ] **Step 2: Write the per-entry check**

```python
def check_entry_policy(section, line):
    """Append failures for entry policy violations; return the casefolded link text."""
    body = line[2:]
    link_text = body[1:body.index("](")]
    # tag run: strip the trailing "(YYYY)." year token first, then collect
    # trailing backticked tokens backward
    m_year = re.search(r"\s*\(\d{4}\)\.$", body)
    if not m_year:
        # unreachable for ENTRY_RX matches; defensive, keeps fail-closed
        fails.append(f"missing tags in {section}: {line[:60]}")
        return link_text.casefold()
    core = body[:m_year.start()].rstrip()
    tokens = []
    m = re.search(r"`([^`]+)`$", core)
    while m:
        tokens.append(m.group(1))
        core = core[:m.start()].rstrip()
        m = re.search(r"`([^`]+)`$", core)
    tokens.reverse()
    if not tokens:
        fails.append(f"missing tags in {section}: {line[:60]}")
        return link_text.casefold()
    unknown = [t for t in tokens if not any(t in v for v in VOCAB.values())]
    for t in unknown:
        fails.append(f"unknown tag in {section}: {t} ({line[:60]})")
    if unknown:
        return link_text.casefold()
    # axis assignment: lowest rank that keeps the sequence non-decreasing
    # and satisfies cardinality (resolves dual-axis tokens like Capella)
    axes = []
    counts = dict.fromkeys(AXIS_RANK, 0)
    prev_rank = -1
    for t in tokens:
        placed = None
        for r, a in sorted((AXIS_RANK[a], a) for a in AXIS_RANK if t in VOCAB[a]):
            if r < prev_rank:
                continue
            cap = CARDINALITY[a]
            if cap is not None:
                limit = cap[1] if isinstance(cap, tuple) else cap
                if counts[a] >= limit:
                    continue
            placed = a
            break
        if placed is None:
            fails.append(f"tag order or cardinality in {section}: {tokens}")
            return link_text.casefold()
        axes.append(placed)
        counts[placed] += 1
        prev_rank = AXIS_RANK[placed]
    if counts["who"] != 1 or counts["domain"] != 1 or counts["contribution"] != 1:
        fails.append(f"tag order or cardinality in {section}: {tokens}")
        return link_text.casefold()
    if tokens[0] != WHO_BY_SECTION[section]:
        fails.append(f"who tag {tokens[0]} does not match section {section}")
    # description: after the " - " separator that follows the link's closing
    # paren, up to the tag run (rfind: the tag run is the trailing occurrence)
    paren_close = body.index(")", body.index("]("))
    desc_zone = body[paren_close + 1:]
    m_sep = re.match(r"\s+-\s+", desc_zone)
    desc_start = m_sep.end() if m_sep else 0
    tag_zone = desc_zone.rfind("`" + tokens[0] + "`")
    desc = desc_zone[desc_start:tag_zone].strip() if tag_zone != -1 else desc_zone[desc_start:].strip()
    if len(desc) > 140:
        fails.append(f"description over 140 chars in {section} ({len(desc)})")
    if len(re.findall(r"\]\(https?://[^)]+\)", line)) > 1:
        fails.append(f"second hyperlink in {section} ({line[:60]})")
    bare = re.sub(r"\[[^\]]*\]\([^)]*\)", "", line)
    bare = re.sub(r"`[^`]*`", "", bare)
    if re.search(r"https?://\S+", bare):
        fails.append(f"bare URL in {section} ({line[:60]})")
    return link_text.casefold()
```

Then, inside the walk where `ENTRY_RX` currently matches, call it and run the alphabetical check with per-section locals (`prev` and `prev_name` are new; initialize/reset them to `None` on every curated heading change; `curated_walk` currently only counts, so no existing ordering logic exists):

```python
        folded = check_entry_policy(current, probe)
        if prev is not None and folded < prev:
            fails.append(
                f"entries out of alphabetical order in {current}: {prev_name} > {probe_name}"
            )
        prev, prev_name = folded, probe_name
```

(`probe_name` is the entry's link text as already parsed in the walk; keep the failure message's `previous > current` shape.)

The implementer may adjust variable plumbing to the actual walk code; the failure messages, parsing rules, and fail-closed behavior are the contract.

- [ ] **Step 3: Compile and run**

```bash
python -m py_compile scripts/check_release.py
python scripts/check_release.py
```

Expected: compile clean; `release gate: PASS (scanned 1 files)`, exit 0. If entries fail, apply only content-neutral fixes per the spec fallback (tag order, casing, description trim; count unchanged) in a separate commit `fix: entry adjustments to satisfy policy gates`.

- [ ] **Step 4: Commit**

```bash
git add scripts/check_release.py
git commit -m "feat: gate enforces tag vocabulary/order, pairing, alphabetical order, description limits"
```

### Task 2: Negative probes

**Files:** none (temporary edits, restored).

**Interfaces:**
- Consumes: Task 1 checks.
- Produces: PR-body evidence.

**Model:** standard

- [ ] **Step 1: Run the eight probes**

Each probe: edit README (temporary), run `python scripts/check_release.py`, capture exit 1 and the expected message, restore the file, re-run to PASS. Probes: (a) swap two adjacent entries; (b) wrong who tag; (c) unknown backticked token; (d) description >140 chars; (e) second hyperlink; (f) standard before contribution; (g) bare `https://` URL in description; (h) strip all tags from one entry.

- [ ] **Step 2: Confirm clean state**

`git status --short` shows no README modification; gate PASS.

- [ ] **Step 3: No commit (probes are transient)**

### Task 3: PR evidence

**Files:** none.

**Model:** standard

- [ ] **Step 1: Push and open the PR**

Push the branch; `gh pr create --base main --title "feat: entry policy gates in the release gate (P3)"` with body: summary, gate PASS output, all eight probe outputs, py_compile output. CI (validate + path-filtered link-check jobs, README changed) green.
