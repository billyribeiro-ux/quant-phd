"""Relative-link and anchor check for the E1 hub and lessons L01-L03 (verifier round 1, slice a).

Usage: python -I link_check.py <repo-root>. Every href/src resolves on disk, and every
'#fragment' names an id present in its target file.
"""

import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
MODULE = ROOT / "course/modules/E/E1"
PAGES = ["index.html", "L01.html", "L02.html", "L03.html"]
ID_RE = re.compile(r'\sid="([^"]+)"')
HREF_RE = re.compile(r'\s(?:href|src)="([^"]+)"')
failures = 0
for name in PAGES:
    src = MODULE / name
    text = src.read_text(encoding="utf-8")
    for target in sorted(set(HREF_RE.findall(text))):
        if target.startswith(("http:", "https:", "mailto:", "data:")):
            print(f"EXTERNAL {name}: {target}")
            failures += 1
            continue
        path_part, _, frag = target.partition("#")
        dest = src if path_part == "" else (MODULE / path_part).resolve()
        if not dest.exists():
            print(f"MISSING {name}: {target} -> {dest}")
            failures += 1
            continue
        if frag and dest.suffix == ".html":
            ids = set(ID_RE.findall(dest.read_text(encoding="utf-8")))
            if frag not in ids:
                print(f"NO-ANCHOR {name}: {target}")
                failures += 1
print(f"link_check failures={failures}")
