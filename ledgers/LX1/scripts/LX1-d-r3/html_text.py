"""Print a numbered plain-text view of one lesson HTML file (tags stripped, script/style dropped).

Usage: python -I ledgers/LX1/scripts/LX1-d-r3/html_text.py <file.html>
"""
import html
import re
import sys
from html.parser import HTMLParser


class Extract(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lines: list[str] = []
        self.buf: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style", "svg"):
            self.skip += 1
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "div", "tr", "section", "br", "dt", "dd", "pre"):
            self.flush()

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style", "svg") and self.skip:
            self.skip -= 1
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "div", "tr", "section", "dt", "dd", "pre"):
            self.flush()

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.buf.append(data)

    def flush(self) -> None:
        text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        self.buf = []
        if text:
            self.lines.append(text)


def main() -> None:
    parser = Extract()
    with open(sys.argv[1], encoding="utf-8") as fh:
        parser.feed(fh.read())
    parser.flush()
    for i, line in enumerate(parser.lines, 1):
        print(f"{i:4d} {html.unescape(line)}")


if __name__ == "__main__":
    main()
