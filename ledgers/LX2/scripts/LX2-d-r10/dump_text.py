"""Dump the visible text of an LX2 lesson page, one line per source line, with the source line number.

Usage: python3 -I dump_text.py <page.html>
Skips <script> and <style> content and HTML tags; keeps the text of every element.
"""
import sys
from html.parser import HTMLParser


class Dump(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.out: list[tuple[int, str]] = []
        self.buf = ""
        self.start = 1
        self.line = 1

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "tr", "pre", "dt", "dd", "div", "section", "td", "th"):
            self.flush()

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "tr", "pre", "dt", "dd", "section", "div", "td", "th"):
            self.flush()

    def handle_data(self, data):
        if self.skip:
            return
        if not self.buf.strip():
            self.start = self.line
        self.buf += data

    def flush(self):
        text = " ".join(self.buf.split())
        if text:
            self.out.append((self.start, text))
        self.buf = ""


def main() -> None:
    path = sys.argv[1]
    raw = open(path, encoding="utf-8").read()
    # Locate the source line of each text chunk by tracking start tags in the raw text
    parser = Dump()
    lines = raw.split("\n")
    # Feed line by line so that each flush records the current source line
    for n, ln in enumerate(lines, start=1):
        parser.line = n
        parser.feed(ln + "\n")
    parser.flush()
    for n, text in parser.out:
        print(f"{n}: {text}")


if __name__ == "__main__":
    main()
