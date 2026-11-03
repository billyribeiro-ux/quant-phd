"""Convert a lesson page to line-numbered plain text, keeping TeX and pre/code content.

Usage: html_to_text.py <page.html> ; writes the text to stdout.
"""
import html
import re
import sys
from html.parser import HTMLParser

BLOCK = {"p", "div", "li", "h1", "h2", "h3", "h4", "h5", "tr", "section", "pre", "table", "ol", "ul", "details", "summary", "figcaption", "dt", "dd", "blockquote", "span"}


class Extract(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style", "svg"):
            self.skip += 1
            return
        if tag in BLOCK or tag == "br" or tag == "tr":
            self.out.append("\n")
        if tag == "td" or tag == "th":
            self.out.append(" | ")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style", "svg"):
            self.skip = max(0, self.skip - 1)
            return
        if tag in BLOCK:
            self.out.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.out.append(data)


src = open(sys.argv[1], encoding="utf-8").read()
p = Extract()
p.feed(src)
text = "".join(p.out)
text = re.sub(r"[ \t]+", " ", text)
lines = [ln.strip() for ln in text.split("\n")]
out: list[str] = []
for ln in lines:
    if ln == "" and (not out or out[-1] == ""):
        continue
    out.append(ln)
for i, ln in enumerate(out, 1):
    if ln:
        print(f"{i:04d}: {ln}")
