"""Check every concept link and local lesson anchor in the E4 slice pages resolves to an id on its target page."""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "course"
e4 = root / "modules/E/E4"
concepts_html = (root / "concepts.html").read_text(encoding="utf-8")
concept_ids = set(re.findall(r'id="([^"]+)"', concepts_html))
bad = 0
for name in ("index.html", "L01.html", "L02.html", "L03.html"):
    html = (e4 / name).read_text(encoding="utf-8")
    page_ids = set(re.findall(r'id="([^"]+)"', html))
    for href in re.findall(r'href="([^"]+)"', html):
        if href.startswith("../../../concepts.html#"):
            anchor = href.split("#", 1)[1]
            ok = anchor in concept_ids
            target = "concepts.html"
        elif href.startswith("#"):
            anchor = href[1:]
            ok = anchor in page_ids
            target = name
        elif re.match(r"^(L0\d|index|project)\.html#", href) or re.match(r"^L0\d\.html$", href):
            if "#" in href:
                file, anchor = href.split("#", 1)
                tpath = e4 / file
                tids = set(re.findall(r'id="([^"]+)"', tpath.read_text(encoding="utf-8")))
                ok = anchor in tids
                target = file
            else:
                ok = (e4 / href).exists()
                anchor = ""
                target = href
        else:
            continue
        if not ok:
            bad += 1
            print(f"BROKEN {name}: {href} -> {target}#{anchor}")
print("broken links:", bad)
