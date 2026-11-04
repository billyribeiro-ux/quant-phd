"""Round-5 link and id check for PC3 slice a (index, L01-L03): every relative href resolves to an existing file,
every concepts.html#anchor exists in course/concepts.html, every fragment href (#id) exists on its page, and every
data-concept link is defined in its owner page. Run from the checkout root with .venv/bin/python -I.
"""

import re
from pathlib import Path

ROOT = Path.cwd()
PAGES = ["index", "L01", "L02", "L03"]
base = ROOT / "course/modules/PC/PC3"
concepts = (ROOT / "course/concepts.html").read_text(encoding="utf-8")
bad = []
for name in PAGES:
    path = base / f"{name}.html"
    text = path.read_text(encoding="utf-8")
    ids = set(re.findall(r'\sid="([^"]+)"', text))
    for href in re.findall(r'href="([^"]+)"', text):
        if href.startswith("http") or href.startswith("mailto:"):
            bad.append((name, href, "EXTERNAL"))
            continue
        if href.startswith("#"):
            if href[1:] and href[1:] not in ids:
                bad.append((name, href, "missing fragment id"))
            continue
        target, _, frag = href.partition("#")
        tpath = (path.parent / target).resolve()
        if not tpath.exists():
            bad.append((name, href, "missing file"))
            continue
        if frag and tpath.name == "concepts.html":
            if f'id="{frag}"' not in concepts:
                bad.append((name, href, "missing concept anchor"))
        elif frag and tpath.name.endswith(".html"):
            if f'id="{frag}"' not in tpath.read_text(encoding="utf-8"):
                bad.append((name, href, "missing anchor in target page"))
    for cid in set(re.findall(r'data-concept="([^"]+)"', text)):
        if f'id="{cid}"' not in concepts and f'id="c-{cid}"' not in concepts and f'"{cid}"' not in concepts:
            bad.append((name, cid, "concept id not in concepts.html"))
    print(f"{name}: hrefs={len(set(re.findall(r'href=\"([^\"]+)\"', text)))} ids={len(ids)}")
print("PROBLEMS:", bad if bad else "none")
