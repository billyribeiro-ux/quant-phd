"""Extract numbered visible text from LX1 lesson pages (round 2 verifier, slice d).

Usage: python -I extract_text.py <page.html> > out.txt
Block-level tags become line breaks so each output line is one block; <script> and <style> are dropped.
"""
import html
import re
import sys
from html.parser import HTMLParser

BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "tr", "dt", "dd", "div", "section", "table", "caption",
         "th", "td", "summary", "figcaption", "pre", "blockquote", "details", "ul", "ol", "header", "footer"}


class Ext(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.buf: list[str] = []
        self.skip = 0

    def flush(self) -> None:
        text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        if text:
            self.out.append(text)
        self.buf = []

    def handle_starttag(self, tag: str, attrs: list) -> None:  # type: ignore[type-arg]
        if tag in ("script", "style"):
            self.skip += 1
        if tag in BLOCK:
            self.flush()

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip -= 1
        if tag in BLOCK:
            self.flush()

    def handle_data(self, data: str) -> None:
        if self.skip == 0:
            self.buf.append(data)


def main() -> None:
    src = open(sys.argv[1], encoding="utf-8").read()
    p = Ext()
    p.feed(src)
    p.flush()
    for i, line in enumerate(p.out, 1):
        print(f"{i:4d}  {line}")


if __name__ == "__main__":
    main()
