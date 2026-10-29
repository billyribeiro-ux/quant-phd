"""Extract readable text (with line numbers of source) from a lesson page.

Usage: python -I extract.py <html file> > out.txt
Each output line is prefixed with the source line number where its text starts.
"""

from __future__ import annotations

import sys
from html.parser import HTMLParser

BLOCK = {
    "p", "div", "li", "h1", "h2", "h3", "h4", "tr", "section", "summary", "figcaption",
    "dt", "dd", "table", "ul", "ol", "details", "pre", "th", "td", "caption", "header", "footer",
}


class Extractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lines: list[tuple[int, str]] = []
        self.buf: list[str] = []
        self.buf_line: int | None = None
        self.skip = 0

    def _flush(self) -> None:
        text = "".join(self.buf)
        text = " ".join(text.split())
        if text and self.buf_line is not None:
            self.lines.append((self.buf_line, text))
        self.buf = []
        self.buf_line = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        line, _ = self.getpos()
        if tag in ("script", "style"):
            self.skip += 1
            return
        if tag in BLOCK:
            self._flush()
            self.buf_line = line
        if tag == "br":
            self.buf.append(" ")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip = max(0, self.skip - 1)
            return
        if tag in BLOCK:
            self._flush()

    def handle_data(self, data: str) -> None:
        if self.skip:
            return
        if self.buf_line is None:
            self.buf_line = self.getpos()[0]
        self.buf.append(data)


def main() -> None:
    path = sys.argv[1]
    src = open(path, encoding="utf-8").read()
    ex = Extractor()
    ex.feed(src)
    ex._flush()
    for line, text in ex.lines:
        print(f"{line:5d} {text}")


if __name__ == "__main__":
    main()
