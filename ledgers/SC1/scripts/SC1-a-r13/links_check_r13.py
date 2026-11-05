"""Check every concepts.html#id and intra-page #anchor link in the SC1 slice pages resolves (index, L01-L03)."""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
concepts = (root / "course/concepts.html").read_text(encoding="utf-8")
concept_ids = set(re.findall(r'id="([^"]+)"', concepts))
bad = []
total = 0
for page in ["index", "L01", "L02", "L03"]:
    path = root / f"course/modules/SC/SC1/{page}.html"
    text = path.read_text(encoding="utf-8")
    ids_here = set(re.findall(r'id="([^"]+)"', text))
    for href in re.findall(r'href="([^"]+)"', text):
        if href.startswith("http"):
            bad.append((page, href, "external"))
            continue
        total += 1
        if "concepts.html#" in href:
            anchor = href.split("#", 1)[1]
            if anchor not in concept_ids:
                bad.append((page, href, "missing in concepts.html"))
        elif href.startswith("#"):
            if href[1:] not in ids_here:
                bad.append((page, href, "missing intra-page id"))
        elif "#" in href:
            target, anchor = href.split("#", 1)
            tpath = (path.parent / target).resolve()
            if tpath.exists():
                ttext = tpath.read_text(encoding="utf-8")
                if f'id="{anchor}"' not in ttext:
                    bad.append((page, href, "anchor missing in target page"))
            else:
                bad.append((page, href, "target page missing"))
print("links checked:", total, "problems:", bad)
