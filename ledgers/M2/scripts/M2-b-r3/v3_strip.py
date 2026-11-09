"""Render a lesson HTML page as numbered text lines (tags removed, block boundaries kept).

Usage: python v3_strip.py <page.html> > out.txt
Keeps <pre>, <code>, <details> content; drops <script>/<style>. Lines are numbered by the
source line on which the block starts, so citations can be checked against the raw file.
"""
import sys
from html.parser import HTMLParser

BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "div", "section", "tr", "pre", "summary", "figcaption", "dt", "dd", "ul", "ol", "table", "header", "footer", "article", "details", "span"}


class P(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[tuple[int, str]] = []
        self.buf: list[str] = []
        self.start = 1
        self.skip = 0
        self.pre = 0

    def flush(self, line: int) -> None:
        text = "".join(self.buf)
        self.buf = []
        if self.pre:
            for ln in text.split("\n"):
                self.out.append((self.start, ln))
        else:
            t = " ".join(text.split())
            if t:
                self.out.append((self.start, t))
        self.start = line

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        line = self.getpos()[0]
        if tag in ("script", "style"):
            self.skip += 1
            return
        if tag in BLOCK:
            self.flush(line)
        if tag == "pre":
            self.pre += 1
        if tag == "li":
            self.buf.append("- ")
        if tag == "br":
            self.buf.append("\n")

    def handle_endtag(self, tag: str) -> None:
        line = self.getpos()[0]
        if tag in ("script", "style"):
            self.skip -= 1
            return
        if tag in BLOCK:
            self.flush(line)
        if tag == "pre":
            self.pre -= 1

    def handle_data(self, data: str) -> None:
        if self.skip:
            return
        self.buf.append(data)


def main() -> None:
    src = open(sys.argv[1], encoding="utf-8").read()
    p = P()
    p.feed(src)
    p.flush(len(src.splitlines()))
    for ln, t in p.out:
        print(f"{ln:5d} {t}")


if __name__ == "__main__":
    main()
