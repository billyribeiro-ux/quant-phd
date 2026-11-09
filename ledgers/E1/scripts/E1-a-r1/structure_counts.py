"""Structural counts for E1 hub and lessons L01-L03 (verifier round 1, slice a).

Reads the four pages from the repository path given as argv[1] and prints counts that
the verifier compares with BUILDER_RULES 4.2, 5.1 and the plan.
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(sys.argv[1])
PAGES = ["index.html", "L01.html", "L02.html", "L03.html"]


class Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.skip = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style"):
            self.skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)


def text_of(html: str) -> str:
    parser = Text()
    parser.feed(html)
    return " ".join(parser.parts)


for name in PAGES:
    html = (ROOT / "course/modules/E/E1" / name).read_text(encoding="utf-8")
    print(f"== {name}")
    if name != "index.html":
        m = re.search(r'<p class="why-it-matters">(.*?)</p>', html, re.S)
        words = len(text_of(m.group(1)).split()) if m else -1
        print(f"  why-it-matters words: {words} (limit 120)")
        print(f"  misconceptions: {len(re.findall(r'<li class=\"misconception\"', html))} (min 3)")
        print(f"  problems: {len(re.findall(r'<div class=\"problem\"', html))}")
        for tier in ("mechanics", "proof", "empirical", "research"):
            block = re.search(rf'data-tier="{tier}">(.*?)</div>\s*</div>', html, re.S)
            n = len(re.findall(r'class="problem"', block.group(1))) if block else -1
            print(f"    tier {tier}: {n} (min 3)")
        print(f"  solutions: {len(re.findall(r'<details class=\"solution\">', html))}")
        print(f"  quiz items: {len(re.findall(r'<li class=\"item\"', html))} (8-15)")
        print(f"  key-results rows: {len(re.findall(r'<tr><td>', html))}")
        print(f"  dfn tags: {re.findall(r'<dfn[^>]*>', html)}")
        print(f"  concept links: {sorted(set(re.findall(r'data-concept=\"([^\"]+)\"', html)))}")
        print(f"  lab sections: {len(re.findall(r'<section class=\"lab', html))}")
    else:
        print(f"  data-hours-lessons/project: {re.findall(r'data-hours-(?:lessons|project)=\"\\d+\"', html)}")
        print(f"  objectives: {len(re.findall(r'<li><strong>(Derive|Compute|Compare|Prove|State|Show|Explain)', html))}")
        print(f"  lesson cards: {len(re.findall(r'class=\"card\" href=', html))}")
        print(f"  placement items: {len(re.findall(r'<li class=\"item\"', html))}")
        print(f"  placement skill items: {len(re.findall(r'data-skill', html))}")
