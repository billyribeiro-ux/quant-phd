"""Round-12 slice e: every href on E3 project/index/L01-L08 pages resolves (file exists; #fragment is an id in the target).
Run from the checkout root with the venv python."""
import html.parser
import os
import re
import sys
from pathlib import Path

ROOT = Path(".").resolve()
E3 = ROOT / "course/modules/E/E3"
ids_cache = {}


class P(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.hrefs = set(), []
        self.line = 1

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "id" in d:
            self.ids.add(d["id"])
        if tag == "a" and "href" in d:
            self.hrefs.append((d["href"], self.getpos()[0]))


def ids_of(path):
    if path not in ids_cache:
        p = P()
        p.feed(open(path, encoding="utf-8").read())
        ids_cache[path] = p
    return ids_cache[path]


pages = [E3 / "project.html", E3 / "index.html"] + [E3 / f"L0{i}.html" for i in range(1, 9)]
bad = 0
total = 0
for page in pages:
    p = ids_of(str(page))
    for href, line in p.hrefs:
        total += 1
        if href.startswith(("http://", "https://", "mailto:")):
            print(f"EXTERNAL {page.name}:{line} {href}")
            continue
        target, _, frag = href.partition("#")
        tpath = page if target == "" else (page.parent / target).resolve()
        if not tpath.exists():
            print(f"MISSING-FILE {page.name}:{line} {href}")
            bad += 1
            continue
        if frag:
            if tpath.suffix != ".html":
                continue
            if frag not in ids_of(str(tpath)).ids:
                print(f"MISSING-ANCHOR {page.name}:{line} {href}")
                bad += 1
print(f"links checked: {total}; broken: {bad}")
# concept links resolve to concepts.html ids
concepts = ids_of(str(ROOT / "course/concepts.html")).ids
cl = 0
for page in pages:
    for m in re.finditer(r'data-concept="([^"]+)"[^>]*href="([^"]+)"|href="([^"]+)"[^>]*data-concept="([^"]+)"', page.read_text(encoding="utf-8")):
        cid = m.group(1) or m.group(4)
        href = m.group(2) or m.group(3)
        cl += 1
        if "concepts.html#" in href:
            frag = href.split("#", 1)[1]
            if frag not in concepts:
                print(f"CONCEPT-ANCHOR-MISSING {page.name} {href}")
                bad += 1
print("concept links checked:", cl, "broken total:", bad)
