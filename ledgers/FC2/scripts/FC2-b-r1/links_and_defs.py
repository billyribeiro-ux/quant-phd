"""FC2-b round 1 verifier script: link targets, dfn duplicates, word counts and hours for L04-L06.

Run as: .venv/bin/python -I ledgers/FC2/scripts/FC2-b-r1/links_and_defs.py
"""

from __future__ import annotations

import re
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path.cwd().resolve()
FC2 = ROOT / "course/modules/FC/FC2"
PAGES = ["index.html", "L01.html", "L02.html", "L03.html", "L04.html", "L05.html", "L06.html", "L07.html",
         "L08.html", "project.html"]


class Collect(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.hrefs: list[tuple[str, str]] = []
        self.dfns: list[tuple[str, str]] = []  # (dfn text, id or '')
        self._in_dfn = False
        self._dfn_text = ""
        self._dfn_id = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"] or "")
        if tag == "a" and a.get("href"):
            self.hrefs.append((a["href"] or "", a.get("class") or ""))
        if tag == "dfn":
            self._in_dfn = True
            self._dfn_text = ""
            self._dfn_id = a.get("id") or ""

    def handle_endtag(self, tag: str) -> None:
        if tag == "dfn" and self._in_dfn:
            self.dfns.append((self._dfn_text.strip(), self._dfn_id))
            self._in_dfn = False

    def handle_data(self, data: str) -> None:
        if self._in_dfn:
            self._dfn_text += data


parsed: dict[str, Collect] = {}
for name in PAGES:
    c = Collect()
    c.feed((FC2 / name).read_text(encoding="utf-8"))
    parsed[name] = c

concepts_html = (ROOT / "course/concepts.html").read_text(encoding="utf-8")
concept_ids = set(re.findall(r'id="([^"]+)"', concepts_html))

problems = 0
print("== link targets from L04-L06 ==")
for name in ["L04.html", "L05.html", "L06.html"]:
    for href, cls in parsed[name].hrefs:
        if href.startswith("#") or href.startswith("http"):
            if href.startswith("#"):
                if href[1:] not in parsed[name].ids:
                    print(f"  MISSING local {name} {href}")
                    problems += 1
            continue
        path, _, frag = href.partition("#")
        target = (FC2 / path).resolve() if path else (FC2 / name)
        if path.startswith("../../../"):
            target = (ROOT / "course" / path.replace("../../../", "", 1)).resolve()
        if not target.exists():
            print(f"  MISSING file {name} -> {href}")
            problems += 1
            continue
        if frag:
            if target.name in PAGES and target.parent == FC2:
                ids = parsed[target.name].ids
            elif target.name == "concepts.html":
                ids = concept_ids
            else:
                ids = set(re.findall(r'id="([^"]+)"', target.read_text(encoding="utf-8")))
            if frag not in ids:
                print(f"  MISSING anchor {name} -> {href}")
                problems += 1
print(f"  link problems: {problems}")

print("== dfn ids and terms across FC2 pages (duplicates) ==")
terms: dict[str, list[str]] = defaultdict(list)
for name in PAGES:
    for text, did in parsed[name].dfns:
        terms[text.lower()].append(f"{name}:{did or '-'}")
for t, where in sorted(terms.items()):
    if len(where) > 1:
        print(f"  term {t!r} defined in {where}")
print("== L04-L06 dfn list ==")
for name in ["L04.html", "L05.html", "L06.html"]:
    print(f"  {name}: {parsed[name].dfns}")

print("== why-it-matters word counts ==")
for name in ["L04.html", "L05.html", "L06.html"]:
    text = (FC2 / name).read_text(encoding="utf-8")
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', text, re.S)
    body = re.sub(r"<[^>]+>", " ", m.group(1)) if m else ""
    body = re.sub(r"\\\((.*?)\\\)", r"\1", body)
    print(f"  {name}: {len(body.split())} words")

print("== hours ==")
for name in ["L04.html", "L05.html", "L06.html"]:
    text = (FC2 / name).read_text(encoding="utf-8")
    print(f"  {name}: " + " ".join(re.findall(r'(data-hours="\d+"|study hours)', text)))
idx = (FC2 / "index.html").read_text(encoding="utf-8")
print("  index:", re.findall(r'data-hours[a-z-]*="[^"]*"', idx))
