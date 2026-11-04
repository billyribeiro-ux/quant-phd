"""Resolve every href and id-anchor of project.html (files and fragments) and list the data-concept links.

Usage: python -I links_check_r6.py <checkout-root>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
page_path = root / "course/modules/E/E4/project.html"
raw = page_path.read_text(encoding="utf-8")
hrefs = re.findall(r'href="([^"]+)"', raw)
problems = []
checked = 0
for h in sorted(set(hrefs)):
    if h.startswith(("http://", "https://", "mailto:")):
        problems.append(f"external href {h}")
        continue
    target, _, frag = h.partition("#")
    file = page_path if target == "" else (page_path.parent / target).resolve()
    if not file.exists():
        problems.append(f"missing file for {h}")
        continue
    checked += 1
    if frag:
        ids = set(re.findall(r'id="([^"]+)"', file.read_text(encoding="utf-8")))
        if frag not in ids:
            problems.append(f"missing anchor #{frag} in {file.relative_to(root)}")
concept = re.findall(r'data-concept="([^"]+)"', raw)
print("hrefs:", len(hrefs), "distinct:", len(set(hrefs)), "resolved:", checked)
print("data-concept links:", sorted(set(concept)))
print("problems:", problems if problems else "none")
