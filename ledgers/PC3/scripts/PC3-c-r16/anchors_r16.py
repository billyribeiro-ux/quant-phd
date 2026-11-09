"""Check every fragment link in project.html resolves to an id on the target page, and every local file exists.

Usage: python -I anchors_r16.py <repo root>
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
base = root / "course/modules/PC/PC3"
src = (base / "project.html").read_text(encoding="utf-8")
ids_here = set(re.findall(r'\sid="([^"]+)"', src))
bad = []
for href in re.findall(r'href="([^"]+)"', src):
    if href.startswith(("http://", "https://", "mailto:")):
        bad.append(("external", href))
        continue
    path, _, frag = href.partition("#")
    target = base / path if path else base / "project.html"
    if path and not target.exists():
        bad.append(("missing file", href))
        continue
    if frag:
        ids = ids_here if not path else set(re.findall(r'\sid="([^"]+)"', target.read_text(encoding="utf-8")))
        if frag not in ids:
            bad.append(("missing anchor", href))
print("links checked:", len(re.findall(r'href="([^"]+)"', src)), "problems:", bad)
