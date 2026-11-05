"""Word counts for the two exemplars and the Summary, per the page's definition: a word is a run of characters between spaces.

Reads course/modules/SC/SC1/project.html; counts the memo-text paragraphs of each exemplar (headings excluded, the
annotation asides excluded), and the Summary paragraph of each exemplar. Also prints the blind passage text (no
annotation, no data attributes, no official-scoring paragraph) for the blind scoring.
"""

from __future__ import annotations

import html
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

PAGE = Path(sys.argv[1])


class Passages(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.exemplar: str | None = None
        self.depth_memo = 0
        self.in_memo = False
        self.in_h = False
        self.in_aside = 0
        self.current: list[str] = []
        self.blocks: list[tuple[str, str, str]] = []  # (exemplar, heading, text)
        self.heading = ""
        self.in_p = False
        self.p_text: list[str] = []
        self.verdicts: dict[str, str] = {}
        self.in_verdict: str | None = None
        self.verdict_text: list[str] = []
        self.ex_stack: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        cls = a.get("class") or ""
        if tag == "article" and a.get("class") == "exemplar":
            self.exemplar = a.get("id")
        if tag == "p" and "exemplar-verdict" in cls:
            self.in_verdict = self.exemplar
            self.verdict_text = []
        if tag == "div" and "memo-text" in cls:
            self.in_memo = True
        if tag == "aside":
            self.in_aside += 1
        if self.in_memo and tag == "h5":
            self.in_h = True
            self.heading = ""
        if self.in_memo and tag == "p" and self.in_aside == 0:
            self.in_p = True
            self.p_text = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "h5":
            self.in_h = False
        if tag == "p" and self.in_verdict is not None and self.in_p is False:
            self.verdicts[self.in_verdict] = "".join(self.verdict_text)
            self.in_verdict = None
        if tag == "p" and self.in_p:
            self.in_p = False
            if self.exemplar:
                self.blocks.append((self.exemplar, self.heading, "".join(self.p_text)))
        if tag == "div" and self.in_memo and self.in_aside == 0:
            pass
        if tag == "aside":
            self.in_aside -= 1
        if tag == "article":
            self.exemplar = None

    def handle_data(self, data: str) -> None:
        if self.in_verdict is not None:
            self.verdict_text.append(data)
        if self.in_h:
            self.heading += data
        if self.in_p:
            self.p_text.append(data)


text = PAGE.read_text(encoding="utf-8")
parser = Passages()
parser.feed(text)
for ex in ("exemplar-a", "exemplar-b"):
    body = [(h, t) for e, h, t in parser.blocks if e == ex]
    words = sum(len(re.findall(r"\S+", t)) for _, t in body)
    print(f"{ex}: body paragraphs {len(body)}, words {words}")
    for h, t in body:
        print(f"   [{h}] {len(re.findall(r'\S+', t))} words")
    summ = [t for h, t in body if h == "Summary"]
    if summ:
        print(f"   Summary words: {len(re.findall(r'\S+', summ[0]))}")
print()
print("VERDICT (official, for reference only):")
for k, v in parser.verdicts.items():
    print(k, "::", v)
