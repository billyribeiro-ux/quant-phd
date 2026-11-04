"""Check that every fragment link on BK4 project.html resolves to an id in the same page or in index.html / L05.html."""

from __future__ import annotations

import re
import sys
from pathlib import Path

base = Path(sys.argv[1])
project = (base / "project.html").read_text(encoding="utf-8")
index = (base / "index.html").read_text(encoding="utf-8")
ids_project = set(re.findall(r'\sid="([^"]+)"', project))
ids_index = set(re.findall(r'\sid="([^"]+)"', index))
bad: list[str] = []
for target in re.findall(r'href="([^"]+)"', project):
    if target.startswith("http"):
        bad.append(f"external link {target}")
        continue
    path, _, frag = target.partition("#")
    if path in ("", "project.html"):
        if frag and frag not in ids_project:
            bad.append(f"missing #{frag} on project.html")
    elif path == "index.html":
        if frag and frag not in ids_index:
            bad.append(f"missing #{frag} on index.html")
    else:
        if not (base / path).exists() and not (base / path.replace("../../../", "")).exists():
            bad.append(f"file not in tree: {path}")
print("anchor problems:", bad if bad else "none")
print("project ids:", len(ids_project), "index ids:", len(ids_index))
