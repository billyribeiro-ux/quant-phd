"""Check every href/src in the hub and L01-L03 resolves to a file, and every #fragment to an id in that file (verifier r3)."""
import os
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
base = root / "course/modules/E/E1"
bad = 0
total = 0
for page in ["index.html", "L01.html", "L02.html", "L03.html"]:
    src = (base / page).read_text(encoding="utf-8")
    for href in re.findall(r'href="([^"]+)"', src) + re.findall(r'src="([^"]+)"', src):
        if href.startswith(("http:", "https:", "mailto:")):
            print(f"EXTERNAL {page}: {href}")
            bad += 1
            continue
        total += 1
        path, _, frag = href.partition("#")
        target = (base / path).resolve() if path else (base / page).resolve()
        if not target.exists():
            print(f"MISSING {page}: {href} -> {target}")
            bad += 1
            continue
        if frag and target.suffix == ".html":
            ids = set(re.findall(r'id="([^"]+)"', target.read_text(encoding="utf-8")))
            if frag not in ids:
                print(f"NOFRAG {page}: {href}")
                bad += 1
print(f"links checked {total}, problems {bad}")
