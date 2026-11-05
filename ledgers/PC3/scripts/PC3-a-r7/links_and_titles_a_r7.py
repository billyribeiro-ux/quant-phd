"""Round 7: hrefs, concept links, anchors, prerequisite titles, P0.1 entries, closure (run with -I from checkout root)."""
import html.parser
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "tools")
import coursekit  # noqa: E402

ROOT = Path(".").resolve()
PAGES = ["course/modules/PC/PC3/index.html", "course/modules/PC/PC3/L01.html",
         "course/modules/PC/PC3/L02.html", "course/modules/PC/PC3/L03.html"]


class Collect(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs, self.concepts, self.ids, self.dfns = [], [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "href" in a:
            self.hrefs.append(a["href"])
        if "id" in a:
            self.ids.append(a["id"])
        if a.get("data-concept") is not None:
            if tag == "dfn":
                self.dfns.append((a["data-concept"], a.get("id")))
            else:
                self.concepts.append((tag, a["data-concept"], a.get("href")))


concept_ids = set(re.findall(r'id="([^"]+)"', (ROOT / "course/concepts.html").read_text(encoding="utf-8")))
for page in PAGES:
    c = Collect()
    c.feed((ROOT / page).read_text(encoding="utf-8"))
    print(f"== {page}: {len(c.hrefs)} hrefs, {len(c.concepts)} concept links, {len(c.dfns)} dfn with data-concept")
    internal = [h for h in c.hrefs if not h.startswith("http")]
    for h in internal:
        if h.startswith("#"):
            ok = h[1:] in c.ids
            if not ok:
                print("  MISSING anchor", h)
        else:
            tgt = h.split("#")[0]
            frag = h.split("#")[1] if "#" in h else None
            path = (ROOT / Path(page).parent / tgt).resolve() if tgt else None
            if path is None or not path.exists():
                print("  MISSING file", h)
            elif frag and "concepts.html" in tgt and frag not in concept_ids:
                print("  MISSING concept id", h)
    for tag, cid, href in c.concepts:
        flag = "" if href is None else ""
        if cid == "p01" or cid.startswith("P0"):
            print("  P0.1 link", cid, href)
        if href and "concepts.html#" in href and href.split("#")[1] != cid:
            print("  href/data-concept mismatch", cid, href)
    print("  concept links:", sorted({cid for _, cid, _ in c.concepts}))
    print("  dfns:", c.dfns)
    print("  external refs:", [h for h in c.hrefs if h.startswith("http")])

print("== prerequisite titles (curriculum.json)")
cur = json.loads((ROOT / "curriculum/curriculum.json").read_text(encoding="utf-8"))
modules = {}
for part in cur.get("program", {}).get("parts", []) if isinstance(cur.get("program"), dict) else []:
    pass
def walk(o):
    if isinstance(o, dict):
        if "id" in o and "title" in o and "prereqs" in o:
            modules[o["id"]] = o
        for v in o.values():
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)
walk(cur)
pc3 = modules["PC3"]
print("PC3:", pc3["title"], pc3["hours"], pc3["prereqs"], pc3["tier"])
for p in ["M4", "CS2", "FC2", "M1", "M2", "AC1", "CF1", "CS1", "E1", "FC1", "P0.1"]:
    print(p, modules.get(p, {}).get("title"))
print("closure coursekit:", sorted(coursekit.prerequisite_closure("PC3")))
