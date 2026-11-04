"""Round-6 independent link and id check for the four PC3 slice pages (no tool logic reused).

Run: .venv/bin/python -I ledgers/PC3/scripts/PC3-a-r6/links_and_ids_a_r6.py  (from the checkout root)
Checks: every href to a local file resolves; every #fragment exists as an id in its target; every
data-concept used has a concepts.html id; every <dfn id> is unique; every data-concept dfn appears once.
"""

import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path.cwd()
PAGES = [
    "course/modules/PC/PC3/index.html",
    "course/modules/PC/PC3/L01.html",
    "course/modules/PC/PC3/L02.html",
    "course/modules/PC/PC3/L03.html",
]


class Scan(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[tuple[str, str]] = []
        self.ids: list[str] = []
        self.concepts: list[str] = []
        self.dfn_ids: list[tuple[str, str]] = []
        self.dfn_concepts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if a.get("id"):
            self.ids.append(a["id"] or "")
        if tag == "a" and a.get("href"):
            self.hrefs.append((a["href"] or "", a.get("data-concept") or ""))
        if a.get("data-concept"):
            if tag == "dfn":
                self.dfn_concepts.append(a["data-concept"] or "")
            else:
                self.concepts.append(a["data-concept"] or "")
        if tag == "dfn" and a.get("id"):
            self.dfn_ids.append((a["id"] or "", tag))


def scan(path: Path) -> Scan:
    s = Scan()
    s.feed(path.read_text(encoding="utf-8"))
    return s


problems = 0
cache: dict[Path, Scan] = {}
concept_index = scan(ROOT / "course/concepts.html")
concept_ids = set(concept_index.ids)
for page in PAGES:
    p = ROOT / page
    s = scan(p)
    cache[p] = s
    print(f"== {page}: hrefs={len(s.hrefs)} ids={len(s.ids)} concept-links={len(s.concepts)} dfn-concepts={len(s.dfn_concepts)}")
    for href, _ in s.hrefs:
        if href.startswith(("http://", "https://", "mailto:")):
            print("EXTERNAL", href)
            problems += 1
            continue
        target, _, frag = href.partition("#")
        tpath = p if target == "" else (p.parent / target).resolve()
        if not tpath.exists():
            print("MISSING FILE", page, href)
            problems += 1
            continue
        if frag:
            tgt = scan(tpath)
            if frag not in tgt.ids:
                print("MISSING FRAGMENT", page, href)
                problems += 1
    for c in s.concepts + s.dfn_concepts:
        if c not in concept_ids:
            print("CONCEPT NOT IN concepts.html", page, c)
            problems += 1
    ids = [i for i in s.ids if i]
    dups = {i for i in ids if ids.count(i) > 1}
    if dups:
        print("DUPLICATE IDS", page, sorted(dups))
        problems += 1
    dfn_c = s.dfn_concepts
    if len(dfn_c) != len(set(dfn_c)):
        print("DUPLICATE dfn concept", page, dfn_c)
        problems += 1
    print("  dfn data-concept list:", dfn_c)
print("protected P0.1 links:", [h for pg in PAGES for h, _ in scan(ROOT / pg).hrefs if "P0" in h])
print("PROBLEMS", problems)
