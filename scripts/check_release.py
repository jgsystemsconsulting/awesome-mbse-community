# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: CC0-1.0
"""Release gate (RR-B-15): required files, forbidden paths, forbidden
content, headers present. Exits non-zero on any failure.

Standalone model for awesome-mbse-community: no src/ layout, no package
install, no scripts beyond the gate itself."""
import pathlib
import re
import subprocess
import sys

fails: list[str] = []

REQUIRED = [
    "README.md", "LICENSE", "COPYRIGHT", "NOTICE", "CHANGELOG.md",
    "SECURITY.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md",
    "RELEASE-INFO.txt", "CITATION.cff",
    "docs/DISTRIBUTION.md", "docs/index.html",
    "scripts/check_release.py",
]
for f in REQUIRED:
    if not pathlib.Path(f).is_file():
        fails.append(f"required file missing: {f}")

tracked = subprocess.run(["git", "ls-files"], capture_output=True, text=True,
                         check=True).stdout.splitlines()
FORBIDDEN_PATH_PARTS = ["__pycache__", ".venv", ".worktrees", ".pytest_cache",
                        ".ruff_cache", ".bak"]
for f in tracked:
    if any(part in f for part in FORBIDDEN_PATH_PARTS):
        fails.append(f"forbidden tracked path: {f}")

FORBIDDEN_CONTENT = [re.compile(r"BEGIN [A-Z ]*PRIVATE KEY"),
                     re.compile(r"CONFIDENTIAL\s+[-—]\s+Not for external distribution")]
SCAN_GLOBS = ["scripts/*.py"]
scanned: set[pathlib.Path] = set()
for g in SCAN_GLOBS:
    for path in pathlib.Path(".").glob(g):
        scanned.add(path)
        text = path.read_text(encoding="utf-8", errors="ignore")
        for rx in FORBIDDEN_CONTENT:
            if rx.search(text):
                fails.append(f"forbidden content in {path}: {rx.pattern}")

HEADER_SENTINEL = "Copyright (c) 2026 JG Systems Consulting Ltd"
for g in SCAN_GLOBS:
    for path in pathlib.Path(".").glob(g):
        if HEADER_SENTINEL not in path.read_text(encoding="utf-8", errors="ignore")[:600]:
            fails.append(f"header missing: {path}")

# --- landing truth gate ---
# Sources of truth: README.md (sweep badge, curated ## headings, entry bullets)
# and RELEASE-INFO.txt (Version). docs/index.html chips and section-index
# fragments are derived copies. Edit the landing to match the sources, never
# the reverse. Assertions A1-A6: version, sweep, entries, headings, fragments,
# entry grammar.

def read_source(path):
    try:
        return pathlib.Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        fails.append(f"unreadable source file: {path}")
        return None


def landing_chip(html, name):
    hits = re.findall(rf"<dt>{re.escape(name)}</dt>\s*<dd>([^<]*)</dd>", html)
    if len(hits) != 1:
        fails.append(f"landing chip missing or ambiguous: {name}")
        return None
    return hits[0].strip()


release_info = read_source("RELEASE-INFO.txt")
readme = read_source("README.md")
html = read_source("docs/index.html")

if release_info is not None:
    version_hits = re.findall(r"(?m)^Version: (\S+)\s*$", release_info)
    if len(version_hits) != 1:
        fails.append(
            f"RELEASE-INFO Version field missing or ambiguous: {len(version_hits)} matches"
        )
    else:
        chip_version = landing_chip(html, "version") if html is not None else None
        if chip_version is not None and chip_version != version_hits[0]:
            fails.append(
                f"landing version chip {chip_version} != RELEASE-INFO Version {version_hits[0]}"
            )
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

if readme is not None:
    sweep_hits = re.findall(r"!\[Last full sweep: (\d{4}-\d{2})\]", readme)
    if len(sweep_hits) != 1:
        fails.append(f"README sweep badge missing or ambiguous: {len(sweep_hits)} matches")
    else:
        chip_sweep = landing_chip(html, "sweep") if html is not None else None
        if chip_sweep is not None and chip_sweep != sweep_hits[0]:
            fails.append(
                f"landing sweep chip {chip_sweep} != README sweep badge {sweep_hits[0]}"
            )

CURATED_SECTIONS = (
    "Individual practitioners",
    "Companies and vendors",
    "Academic and research groups",
    "Community organizations and standards bodies",
)
ENTRY_RX = re.compile(r"^- \[[^\]]+\]\(https?://[^)\s]+\)\s+-\s+.+\(\d{4}\)\.$")


def curated_walk(readme):
    """Count grammar-valid bullets under curated headings and tally exact ## hits."""
    count = 0
    heading_hits = {title: 0 for title in CURATED_SECTIONS}
    current = None
    in_fence = False
    for raw in readme.splitlines():
        line = raw.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        stripped = line.strip()
        if stripped.startswith("## ") and not stripped.startswith("###"):
            # Exact presence uses stripped == "## " + title for curated titles only
            current = stripped[3:].strip()
            if stripped == "## " + current and current in heading_hits:
                heading_hits[current] += 1
            continue
        if current in heading_hits and line and re.match(r"^[-*] \[", line):
            probe = "- " + line[2:] if line.startswith("* ") else line
            if ENTRY_RX.match(probe):
                count += 1
            else:
                fails.append(f"curated entry malformed in {current}: {line[:60]}")
    return count, heading_hits


curated_count = None
heading_hits = {}
if readme is not None:
    curated_count, heading_hits = curated_walk(readme)

chip_entries = landing_chip(html, "entries") if html is not None else None
if chip_entries is not None:
    if not re.fullmatch(r"[0-9]+", chip_entries):
        fails.append(f"landing entries chip not an integer: {chip_entries}")
    elif curated_count is not None and int(chip_entries) != curated_count:
        fails.append(f"landing entries chip {chip_entries} != curated count {curated_count}")


def github_slug(title):
    return re.sub(r"[^\w\s-]", "", title.lower()).strip().replace(" ", "-")


for title, hits in heading_hits.items():
    if hits == 0:
        fails.append(f"curated heading missing from README: {title}")
    elif hits > 1:
        fails.append(f"curated heading duplicated in README ({hits}x): {title}")

if html is not None:
    blocks = re.findall(r'<ul class="section-index">(.*?)</ul>', html, re.DOTALL)
    if len(blocks) != 1:
        fails.append(f"landing section-index list missing or ambiguous: {len(blocks)} found")
    else:
        lis = re.findall(r"<li\b[^>]*>.*?</li>", blocks[0], re.DOTALL)
        if len(lis) != 4:
            fails.append(f"section-index li count {len(lis)} != 4")
        else:
            fragments = []
            for li in lis:
                hrefs = re.findall(r'href="[^"#]*#([^"]+)"', li)
                if len(hrefs) != 1:
                    fails.append(f"section-index li href missing or ambiguous: {li[:60]}")
                    fragments = None
                    break
                fragments.append(hrefs[0])
            if fragments is not None:
                expected = [github_slug(t) for t in CURATED_SECTIONS]
                for got, want in zip(fragments, expected):
                    if got != want:
                        fails.append(f"section-index fragment mismatch: {got} != {want}")

if fails:
    print("RELEASE GATE FAILED:")
    for f in fails:
        print(f"  - {f}")
    sys.exit(1)
assert scanned, "scan globs matched nothing; fix SCAN_GLOBS"
print(f"release gate: PASS (scanned {len(scanned)} files)")
