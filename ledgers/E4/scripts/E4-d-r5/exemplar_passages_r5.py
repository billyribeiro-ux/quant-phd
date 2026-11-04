"""Print only the passage text of each exemplar (no verdict, no annotation, no data-scores) for blind scoring.

Usage: python -I exemplar_passages_r5.py <path-to-project.html> <exemplar-id>
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

src = Path(sys.argv[1]).read_text(encoding="utf-8")
target = sys.argv[2]
start = src.index(f'id="{target}"')
end = src.index("</article>", start)
block = src[start:end]


class Passage(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.depth_stack: list[str] = []
        self.out: list[str] = []
        self.in_passage = 0
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        cls = a.get("class") or ""
        if tag == "div" and "passage" in cls.split():
            self.in_passage += 1
        if self.in_passage and tag in ("h5", "p", "li", "h4"):
            self.out.append("\n")
        if tag in ("aside",) or "annotation" in cls.split():
            self.skip += 1
        if tag in ("ul", "ol") and self.skip == 0:
            pass

    def handle_endtag(self, tag: str) -> None:
        if tag == "aside" and self.skip:
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if self.in_passage and not self.skip:
            self.out.append(data)


p = Passage()
p.feed(block)
text = "".join(p.out)
print(re.sub(r"\n\s*\n+", "\n", text).strip())
