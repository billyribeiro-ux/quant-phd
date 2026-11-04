"""Print the visible text of one lesson HTML, one line per source line, prefixed by its 1-based HTML line number.

Usage: python3 -I lesson_text.py <file.html>. Tags are removed, entities decoded, script and style bodies dropped.
"""
import html
import re
import sys
from html.parser import HTMLParser


class Visible(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style"):
            self.skip += 1
        if tag in ("p", "li", "tr", "h1", "h2", "h3", "h4", "div", "section", "dt", "dd", "pre", "details", "summary"):
            self.parts.append("\n")
        if tag == "td" or tag == "th":
            self.parts.append(" | ")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style") and self.skip:
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)


path = sys.argv[1]
src = open(path, encoding="utf-8").read().splitlines()
for n, line in enumerate(src, 1):
    p = Visible()
    p.feed(line)
    text = re.sub(r"\s+", " ", "".join(p.parts)).strip()
    if text:
        for piece in text.split(" \n") if "\n" in text else [text]:
            pass
        print(f"{n:4d}: {text}")
