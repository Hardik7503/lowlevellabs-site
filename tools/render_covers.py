#!/usr/bin/env python3
"""Render article cover images: content/covers/<slug>.svg -> assets/covers/<slug>.png

Covers are 1200x630 SVGs (the standard social-preview shape) using IBM Plex fonts.
They are rendered to PNG so they look identical everywhere, including link previews.

Requirements (only needed when a cover changes):
    pip install playwright pillow && python3 -m playwright install chromium

Fonts: by default loaded from Google Fonts. To render offline, point LLL_FONT_DIR at a
folder containing the IBM Plex .woff2 files (IBMPlexSans-*.woff2, IBMPlexMono-*.woff2,
IBMPlexSansCondensed-*.woff2).

Usage, from the repository root:
    python3 tools/render_covers.py            # all covers
    python3 tools/render_covers.py my-slug    # one cover
"""
import os
import pathlib
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "content/covers"
OUT = ROOT / "assets/covers"
WIDTH, HEIGHT, SCALE = 1200, 630, 2       # rendered at 2x, saved at 1600x840


def font_css():
    d = os.environ.get("LLL_FONT_DIR")
    if not d:
        return ('<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&'
                'family=IBM+Plex+Sans+Condensed:wght@500;600&family=IBM+Plex+Sans:wght@400;500;600&display=block" rel="stylesheet">')
    faces = []
    for fam, prefix in (("IBM Plex Sans", "IBMPlexSans-"), ("IBM Plex Mono", "IBMPlexMono-"),
                        ("IBM Plex Sans Condensed", "IBMPlexSansCondensed-")):
        for weight, name in ((400, "Regular"), (500, "Medium"), (600, "SemiBold")):
            f = next(pathlib.Path(d).rglob(f"{prefix}{name}.woff2"), None)
            if f:
                faces.append(f"@font-face{{font-family:'{fam}';font-weight:{weight};src:url('{f.as_uri()}')}}")
    return "<style>" + "".join(faces) + "</style>"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    only = set(sys.argv[1:])
    svgs = [p for p in sorted(SRC.glob("*.svg")) if not only or p.stem in only]
    css = font_css()
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=SCALE)
        for svg in svgs:
            html = f"<!doctype html><html><head>{css}<style>html,body{{margin:0}}svg{{display:block}}</style></head><body>{svg.read_text()}</body></html>"
            tmp = OUT / f".{svg.stem}.html"
            tmp.write_text(html)
            page.goto(tmp.as_uri(), wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            raw = OUT / f".{svg.stem}.png"
            page.screenshot(path=str(raw), clip={"x": 0, "y": 0, "width": WIDTH, "height": HEIGHT})
            img = Image.open(raw).convert("RGB").resize((1600, 840), Image.LANCZOS)
            dest = OUT / f"{svg.stem}.png"
            img.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(dest, optimize=True)
            raw.unlink()
            tmp.unlink()
            print(f"{dest.relative_to(ROOT)}  {dest.stat().st_size // 1024} KB")
        browser.close()


if __name__ == "__main__":
    main()
