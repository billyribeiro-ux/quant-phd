"""Checks every href and id reference in project.html: local files exist and fragment ids exist in the target."""
import pathlib, re, sys
from html.parser import HTMLParser
root = pathlib.Path(sys.argv[1]).resolve()
page = root / "course/modules/LX/LX1/project.html"
ids_cache = {}
class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=set(); self.hrefs=[]
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "id" in d: self.ids.add(d["id"])
        if tag == "a" and "href" in d: self.hrefs.append(d["href"])
        if "data-concept" in d and tag=="dfn": pass
def ids_of(path):
    if path not in ids_cache:
        p = P(); p.feed(path.read_text(encoding="utf-8")); ids_cache[path] = p.ids
    return ids_cache[path]
me = P(); me.feed(page.read_text(encoding="utf-8"))
bad = 0
for h in me.hrefs:
    if h.startswith(("http://", "https://", "mailto:")):
        print("external", h); continue
    target, _, frag = h.partition("#")
    tpath = page if target == "" else (page.parent / target).resolve()
    if not tpath.exists():
        print("MISSING FILE", h); bad += 1; continue
    if frag and frag not in ids_of(tpath):
        print("MISSING ID", h, "in", tpath.relative_to(root)); bad += 1; continue
    print("ok", h)
print("bad", bad, "hrefs", len(me.hrefs))
