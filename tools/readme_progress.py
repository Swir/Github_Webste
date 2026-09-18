#!/usr/bin/env python3
"""Generate/check SWIR README progress SVGs for GITHUB WEBSITE.

This repository currently has no canonical measurable product roadmap, so product
progress is deliberately N/A. Release versions, commit counts and documentation
work are never converted into a fake completion percentage.
"""
from __future__ import annotations
from pathlib import Path
import argparse
import re

ROOT = Path(__file__).resolve().parents[1]
NAME = "GITHUB WEBSITE"
CARD = ROOT / "assets/readme/progress-card.svg"
MINI = ROOT / "assets/readme/progress-mini.svg"
README = ROOT / "README.md"

def card() -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="180" viewBox="0 0 1200 180" role="img" aria-labelledby="title desc">
<title id="title">{NAME} product progress</title><desc id="desc">Product progress is N/A because this repository has no canonical measurable product roadmap.</desc>
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#02050A"/><stop offset="1" stop-color="#07111C"/></linearGradient><linearGradient id="c" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#0088FF"/><stop offset="1" stop-color="#62E5FF"/></linearGradient></defs>
<rect x="1" y="1" width="1198" height="178" rx="22" fill="url(#bg)" stroke="#62E5FF" stroke-opacity=".25"/>
<text x="50" y="38" fill="#62E5FF" font-family="Segoe UI,Arial,sans-serif" font-size="15" font-weight="700" letter-spacing="3">SWIR PROGRESS</text>
<text x="50" y="72" fill="#F4FAFF" font-family="Segoe UI,Arial,sans-serif" font-size="27" font-weight="800">{NAME}</text>
<text x="50" y="97" fill="#8DA8B8" font-family="Segoe UI,Arial,sans-serif" font-size="14">Measured scope: product progress</text>
<rect x="50" y="116" width="1100" height="20" rx="10" fill="#08131F" stroke="#62E5FF" stroke-opacity=".16"/>
<path d="M70 126H1130" stroke="url(#c)" stroke-width="2" stroke-dasharray="8 12" opacity=".32"/>
<text x="50" y="158" fill="#8DA8B8" font-family="Segoe UI,Arial,sans-serif" font-size="12">Status: no canonical measurable roadmap · progress counter unavailable</text>
<text x="1145" y="96" text-anchor="end" fill="#F4FAFF" font-family="Segoe UI,Arial,sans-serif" font-size="34" font-weight="800">N/A</text>
</svg>
'''

def mini() -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="72" viewBox="0 0 900 72" role="img" aria-labelledby="title desc">
<title id="title">{NAME} product progress</title><desc id="desc">Product progress is N/A because this repository has no canonical measurable product roadmap.</desc>
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#02050A"/><stop offset="1" stop-color="#07111C"/></linearGradient></defs>
<rect x="1" y="1" width="898" height="70" rx="15" fill="url(#bg)" stroke="#62E5FF" stroke-opacity=".25"/>
<text x="24" y="28" fill="#F4FAFF" font-family="Segoe UI,Arial,sans-serif" font-size="14" font-weight="700">{NAME}</text>
<text x="24" y="50" fill="#8DA8B8" font-family="Segoe UI,Arial,sans-serif" font-size="11">Product progress · no canonical measurable roadmap</text>
<rect x="430" y="27" width="360" height="16" rx="8" fill="#08131F" stroke="#62E5FF" stroke-opacity=".15"/>
<text x="865" y="43" text-anchor="end" fill="#62E5FF" font-family="Segoe UI,Arial,sans-serif" font-size="18" font-weight="800">N/A</text>
</svg>
'''

def legacy_meter(text: str) -> bool:
    return any(re.search(p, text) for p in (r"[█▓▒░]{5,}", r"\[(?:\s*[#=\-]){6,}\s*\]"))

def expected() -> dict[Path, str]:
    return {CARD: card(), MINI: mini()}

def check() -> int:
    ok = True
    for path, wanted in expected().items():
        got = path.read_text(encoding="utf-8") if path.exists() else ""
        if got != wanted:
            print(f"stale or missing: {path.relative_to(ROOT)}")
            ok = False
    readme = README.read_text(encoding="utf-8")
    for rel in ("assets/readme/progress-card.svg", "assets/readme/progress-mini.svg"):
        if rel not in readme:
            print(f"README missing embed: {rel}")
            ok = False
    if legacy_meter(readme):
        print("README contains a retired character progress meter")
        ok = False
    return 0 if ok else 1

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        return check()
    for path, content in expected().items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")
    return check()

if __name__ == "__main__":
    raise SystemExit(main())
