"""M2 slice a round 3: every internal href/fragment in index.html and L01-L06 resolves to a file and an id."""

from __future__ import annotations

import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
base = root / "course/modules/M/M2"
bad = 0
for name in ["index.html"] + [f"L{n:02d}.html" for n in range(1, 7)] + ["project.html"]:
    src = (base / name).read_text(encoding="utf-8")
    ids_here = set(re.findall(r'\sid="([^"]+)"', src))
    for href in re.findall(r'href="([^"]+)"', src):
        if href.startswith(("http://", "https://", "mailto:")):
            print(f"EXTERNAL {name}: {href}")
            bad += 1
            continue
        path, _, frag = href.partition("#")
        target = base / path if path else base / name
        if path and not target.exists():
            if (root / "course" / path.replace("../../../", "")).exists():
                target = root / "course" / path.replace("../../../", "")
            else:
                print(f"MISSING FILE {name}: {href}")
                bad += 1
                continue
        if frag:
            ids = set(re.findall(r'\sid="([^"]+)"', target.read_text(encoding="utf-8"))) if target != base / name else ids_here
            if frag not in ids:
                print(f"MISSING ANCHOR {name}: {href} (target {target.name})")
                bad += 1
    for src_attr in re.findall(r'src="([^"]+)"', src):
        if src_attr.startswith("http"):
            print(f"EXTERNAL SRC {name}: {src_attr}")
            bad += 1
print("link check problems:", bad)
