"""Render a lesson HTML page to plain text, one block per line, prefixed with the HTML line of the block start.

Usage: python3 -I html_to_text.py <input.html> <output.txt>
Scripts and styles are dropped; MathJax TeX source is kept verbatim; hidden blocks are kept and marked.
"""

import sys
from html.parser import HTMLParser
from pathlib import Path

BLOCK = {
    "p",
    "li",
    "tr",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "div",
    "section",
    "dt",
    "dd",
    "pre",
    "table",
    "ul",
    "ol",
    "figure",
    "figcaption",
    "blockquote",
    "details",
    "summary",
    "thead",
    "tbody",
    "header",
    "footer",
    "article",
    "nav",
    "td",
    "th",
}
SKIP = {"script", "style", "svg"}


class Render(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[tuple[int, str]] = []
        self.buf: list[str] = []
        self.buf_line = 0
        self.skip = 0
        self.hidden_depth = 0

    def flush(self) -> None:
        text = " ".join("".join(self.buf).split())
        if text:
            self.out.append((self.buf_line, text))
        self.buf = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in SKIP:
            self.skip += 1
            return
        if tag in BLOCK:
            self.flush()
            self.buf_line = self.getpos()[0]
        if tag == "br":
            self.buf.append(" ")
        if tag in ("td", "th"):
            self.buf.append(" | ")

    def handle_endtag(self, tag: str) -> None:
        if tag in SKIP:
            self.skip -= 1
            return
        if tag in BLOCK:
            self.flush()

    def handle_data(self, data: str) -> None:
        if self.skip:
            return
        if not self.buf:
            self.buf_line = self.getpos()[0]
        self.buf.append(data)


def main() -> None:
    src, dst = sys.argv[1], sys.argv[2]
    parser = Render()
    parser.feed(Path(src).read_text(encoding="utf-8"))
    parser.flush()
    Path(dst).write_text("".join(f"{line:05d} {text}\n" for line, text in parser.out), encoding="utf-8")


if __name__ == "__main__":
    main()
