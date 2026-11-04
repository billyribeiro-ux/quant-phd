"""Internal link and anchor scan of the slice pages, and the notation macro scan (registry in notation/notation.json)."""
import json
import os
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
base = root / "course/modules/M/M2"
bad = []
for page in ("L22.html", "L23.html", "L24.html"):
    s = (base / page).read_text(encoding="utf-8")
    for href in sorted(set(re.findall(r'href="([^"]+)"', s))):
        if href.startswith(("http", "#")):
            continue
        path, _, frag = href.partition("#")
        target = Path(os.path.normpath(base / page.replace(page, path))) if path else base / page
        ok = target.exists()
        anchor = True
        if frag and ok and target.suffix == ".html":
            anchor = ('id="%s"' % frag) in target.read_text(encoding="utf-8")
        if not ok or not anchor:
            bad.append((page, href))
print("broken internal links or anchors in L22-L24:", bad)
reg = json.loads((root / "notation/notation.json").read_text(encoding="utf-8"))
macros = set(reg["macros"])
for page in ("L22.html", "L23.html", "L24.html"):
    s = (base / page).read_text(encoding="utf-8")
    used = set(re.findall(r"\\[A-Za-z]+", s))
    custom = sorted(m for m in used if m in macros)
    print(page, "registered macros used:", custom, "| \\mathbb used:", "\\mathbb" in s)
