"""Check every internal href in the slice-a pages: target file exists and the #fragment is an id in it."""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
pages = [root / "course/modules/M/M4" / n for n in ("index.html", "L01.html", "L02.html", "L03.html", "L04.html")]
bad = 0
total = 0
for page in pages:
    text = page.read_text(encoding="utf-8")
    for m in re.finditer(r'href="([^"]+)"', text):
        href = m.group(1)
        if href.startswith(("http:", "https:", "mailto:")):
            print("EXTERNAL", page.name, href)
            bad += 1
            continue
        total += 1
        target, _, frag = href.partition("#")
        tpath = (page.parent / target).resolve() if target else page.resolve()
        if not tpath.exists():
            print("MISSING FILE", page.name, href)
            bad += 1
            continue
        if frag:
            ttext = tpath.read_text(encoding="utf-8")
            if not re.search(r'id="%s"' % re.escape(frag), ttext):
                print("MISSING ANCHOR", page.name, href)
                bad += 1
print("internal links checked:", total, "problems:", bad)
# concept usage: every data-concept link resolves to a dfn in the same or an earlier page
dfns = {}
for page in pages:
    for m in re.finditer(r'<dfn id="(def-[^"]+)" data-concept="([^"]+)"', page.read_text(encoding="utf-8")):
        dfns.setdefault(m.group(2), []).append(page.name)
print("dfn concepts in slice a:", {k: v for k, v in dfns.items()})
