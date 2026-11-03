"""Dump the visible text of a page with html.parser (script and style skipped, block tags start new lines).

Usage: python -I text_dump.py <html file> <out file>
"""

import re
import sys
from html.parser import HTMLParser

BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "div", "section", "tr", "dt", "dd", "pre", "figcaption", "caption", "header", "table", "ul", "ol", "article", "br"}


class Dump(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list) -> None:  # type: ignore[type-arg]
        if tag in ("script", "style"):
            self.skip += 1
        if tag in BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip -= 1
        if tag in BLOCK:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)


d = Dump()
d.feed(open(sys.argv[1], encoding="utf-8").read())
text = "".join(d.parts)
lines = [re.sub(r"\s+", " ", ln).strip() for ln in text.splitlines()]
open(sys.argv[2], "w", encoding="utf-8").write("\n".join(ln for ln in lines if ln) + "\n")
