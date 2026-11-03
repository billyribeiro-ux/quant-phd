"""Dump a lesson HTML to numbered plain-text lines (tags stripped, pre/code kept verbatim).

Usage: python -I dump_text.py <in.html> <out.txt>
"""
import html
import re
import sys
from html.parser import HTMLParser

BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "div", "section", "pre", "tr", "dt", "dd", "summary", "figcaption", "ul", "ol", "table", "details", "br"}


class Dump(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.buf: list[str] = []
        self.pre = 0
        self.skip = 0

    def flush(self) -> None:
        text = "".join(self.buf)
        self.buf = []
        if self.pre:
            self.out.append(text)
            return
        text = re.sub(r"[ \t]+", " ", text).strip()
        if text:
            self.out.append(text)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style"):
            self.skip += 1
            return
        if tag == "pre":
            self.flush()
            self.pre += 1
        if tag in BLOCK:
            self.flush()

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip -= 1
            return
        if tag == "pre":
            self.pre -= 1
            self.flush()
        if tag in BLOCK:
            self.flush()

    def handle_data(self, data: str) -> None:
        if self.skip:
            return
        self.buf.append(data)


def main() -> None:
    src, dst = sys.argv[1], sys.argv[2]
    p = Dump()
    with open(src, encoding="utf-8") as fh:
        p.feed(fh.read())
    p.flush()
    lines = [ln for ln in p.out]
    with open(dst, "w", encoding="utf-8") as fh:
        for i, ln in enumerate(lines, 1):
            fh.write(f"{i:04d}| {ln}\n")
    print(dst, len(lines))


if __name__ == "__main__":
    main()
