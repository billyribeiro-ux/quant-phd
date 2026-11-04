"""Round-5 structure counts for E4 slice a (hub and L01-L03): BUILDER_RULES 4.2 minimums and section order."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

root = Path(sys.argv[1]) / "course" / "modules" / "E" / "E4"


class Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style"):
            self.skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)


def words_of(fragment: str) -> int:
    p = Text()
    p.feed(fragment)
    return len(re.findall(r"\S+", "".join(p.parts)))


for name in ("L01", "L02", "L03"):
    src = (root / f"{name}.html").read_text(encoding="utf-8")
    why = re.search(r'<p class="why-it-matters">(.*?)</p>', src, re.S)
    print(name, "why_it_matters_words", words_of(why.group(1)) if why else None)
    order = [m.group(0) for m in re.finditer(r'<(?:p class="why-it-matters"|section class="lab"|section class="canon-breaks"|section class="misconceptions"|section class="problem-set"|section id="key-results"|section class="quiz"|section class="references")', src)]
    print(name, "order", [o.split('"')[1] if '"' in o else o for o in order])
    print(name, "misconceptions", len(re.findall(r'<li class="misconception">', src)))
    print(name, "problems_by_tier", {t: len(re.findall(r'class="problem" id="[MPER]\d"', s)) for t, s in re.findall(r'<div class="tier" data-tier="(\w+)">(.*?)</div>\s*</div>', src, re.S)})
    print(name, "solutions", len(re.findall(r'<details class="solution">', src)))
    print(name, "quiz_items", len(re.findall(r'<li class="item"', src)), "explain", len(re.findall(r'<div class="explain" hidden>', src)))
    print(name, "key_rows", len(re.findall(r'<tr><td>', src)))
    print(name, "hours_eyebrow", re.findall(r'data-hours="(\d+)"', src))

hub = (root / "index.html").read_text(encoding="utf-8")
print("hub objectives", len(re.findall(r'<ol class="objectives">(.*?)</ol>', hub, re.S)[0].split("<li>")) - 1 + 0)
print("hub lesson cards", len(re.findall(r'class="card" href="L0\d\.html"', hub)))
print("hub placement items", len(re.findall(r'<li class="item"', hub)), "skill", len(re.findall(r'data-skill', hub)))
print("hub hours", re.findall(r'data-hours-(lessons|project)="(\d+)"', hub))
