#!/usr/bin/env python3
"""Build a JGSC landing site from the shell + a site config.

Usage:
    python tools/build.py --config site.config.json --out docs

Does:
    1. Renders shell/index.html.template with the config (nav, sections,
       masthead, hero, footer, OG/Twitter, JSON-LD).
    2. Renders the title-card PNG (per-repo QR, name, tagline, chips, facts)
       to <out>/title-card.png.
    3. Copies static assets (fonts, favicons, emblem, .nojekyll) into <out>.

The output is a complete, self-contained GitHub Pages site. Re-run any time
the config changes: the build is deterministic and free.

stdlib only, plus qrcode (pip install qrcode) and Chrome for the card render.
"""
import argparse
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
FONTDIR = (ROOT / "shell" / "fonts").as_posix()
EMBLEM = (ROOT / "docs" / "images" / "jgs-emblem.png")


def render_card(cfg, out_png: pathlib.Path) -> None:
    """Render the title-card PNG (name, tagline, chips, facts, QR)."""
    import qrcode

    card = cfg.get("card", {})
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,
                       box_size=3, border=0)
    qr.add_data(cfg["qr_url"])
    qr.make(fit=True)
    scratch = pathlib.Path(tempfile.mkdtemp())
    qr_img = qr.make_image(fill_color="#0a0a0b", back_color="#f4f2ec")
    qr_img.save(scratch / "qr.png")

    tpl = (HERE / "card-template.html").read_text(encoding="utf-8")
    chips = "\n".join(f'    <div class="chip">{c}</div>' for c in card.get("chips", []))
    facts = "\n".join(
        f'        <div class="fact">{f["t"]} <i>{f["d"]}</i></div>'
        for f in card.get("facts", []))
    html = (tpl
            .replace("__FONTDIR__", FONTDIR)
            .replace("__EMBLEM__", EMBLEM.as_posix())
            .replace("__QR__", (scratch / "qr.png").as_posix())
            .replace("__KICKER__", card.get("kicker", "Skill overview"))
            .replace("__NAME__", cfg["display_name"])
            .replace("__TAGLINE__", card.get("sub", cfg["tagline"]))
            .replace("__CHIPS__", chips)
            .replace("__FACTS__", facts)
            .replace("__LICNOTE__", card.get("lic_note", cfg.get("lic_note", "")))
            .replace("__URL__", cfg["repo_url"].replace("https://", "")))
    tmp_html = scratch / "card.html"
    tmp_html.write_text(html, encoding="utf-8")

    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--window-size=1280,720", f"--screenshot={out_png.resolve()}",
                    "file:///" + tmp_html.as_posix()],
                   check=True, capture_output=True, timeout=120)
    if not out_png.is_file() or out_png.stat().st_size < 5000:
        sys.exit(f"RENDER FAILED: {out_png} missing or too small")


def render_site(cfg, out_dir: pathlib.Path) -> None:
    tpl = (ROOT / "shell" / "index.html.template").read_text(encoding="utf-8")

    nav = "\n".join(
        f'    <a href="#{s["id"]}">{s["label"]}</a>' for s in cfg["sections"])
    sections = "\n\n".join(
        f'<section id="{s["id"]}"><div class="wrap">\n'
        f'  <div class="shead"><span class="label">&sect;{s["num"]} &middot; {s["label"]}</span><h2>{s["heading"]}</h2></div>\n'
        f'  {s["html"]}\n'
        f'</div></section>'
        for s in cfg["sections"])

    fc = cfg["footer_cells"]
    footer_cells = (
        f'    <div class="tcell"><span class="tl">Product</span><b>{fc["product"]}</b></div>\n'
        f'    <div class="tcell"><span class="tl">Rev</span><b>{fc["rev"]}</b></div>\n'
        f'    <div class="tcell"><span class="tl">Licence</span><b>{fc["licence"]}</b></div>\n'
        f'    <div class="tcell"><span class="tl">Repository</span><b>{fc["repository"]}</b></div>\n'
        f'    <div class="tcell"><span class="tl">Engine</span><b>{fc["engine"]}</b></div>\n'
        f'    <div class="tcell"><span class="tl">Owner</span><b>{fc["owner"]}</b></div>')
    footer_note = f'<p class="fnote">{cfg["footer_note"]}</p>'

    for key, val in {
        "{{PAGE_TITLE}}": cfg["page_title"],
        "{{DISPLAY_NAME}}": cfg["display_name"],
        "{{DOC_ID}}": cfg["doc_id"],
        "{{REV}}": cfg["rev"],
        "{{CLASSIFICATION}}": cfg["classification"],
        "{{LICENCE_LABEL}}": cfg["licence_label"],
        "{{AUTHOR_ORG}}": cfg["author_org"],
        "{{REPO_URL}}": cfg["repo_url"],
        "{{PAGES_BASE}}": cfg["pages_base"],
        "{{LICENSE_URL}}": cfg["license_url"],
        "{{OG_DESCRIPTION}}": cfg["og_description"],
        "{{HERO_LEAD}}": cfg["hero_lead"],
        "{{HERO_SUB}}": cfg["hero_sub"],
        "{{CTAS}}": cfg["ctas"],
        "{{NAV_ITEMS}}": nav,
        "{{SECTIONS}}": sections,
        "{{FOOTER_CELLS}}": footer_cells,
        "{{FOOTER_NOTE_PLACEHOLDER}}": footer_note,
    }.items():
        tpl = tpl.replace(key, val)

    if "{{" in tpl:
        i = tpl.find("{{")
        sys.exit(f"UNRENDERED TOKEN in output: {tpl[i:i+40]}")
    (out_dir / "index.html").write_text(tpl, encoding="utf-8", newline="\n")


def copy_assets(out_dir: pathlib.Path) -> None:
    shutil.copyfile(ROOT / "shell" / "site.css", out_dir / "site.css")
    fonts_out = out_dir / "fonts"
    fonts_out.mkdir(parents=True, exist_ok=True)
    for f in (ROOT / "shell" / "fonts").glob("*.woff2"):
        shutil.copyfile(f, fonts_out / f.name)
    for f in (ROOT / "docs").glob("*.png"):
        dst = out_dir / f.name
        if f.resolve() != dst.resolve():
            shutil.copyfile(f, dst)
    for name in ("favicon.ico", "favicon-32x32.png", "apple-touch-icon.png"):
        src = ROOT / "docs" / name
        dst = out_dir / name
        if src.is_file() and src.resolve() != dst.resolve():
            shutil.copyfile(src, dst)
    (out_dir / ".nojekyll").touch()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="site.config.json")
    ap.add_argument("--out", default="docs")
    a = ap.parse_args()
    cfg = json.loads(pathlib.Path(a.config).read_text(encoding="utf-8"))
    out_dir = pathlib.Path(a.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    render_card(cfg, out_dir / "title-card.png")
    render_site(cfg, out_dir)
    copy_assets(out_dir)
    print(f"site built: {out_dir.resolve()} ({(out_dir / 'index.html').stat().st_size} bytes index, "
          f"{(out_dir / 'title-card.png').stat().st_size} bytes card)")


if __name__ == "__main__":
    main()
