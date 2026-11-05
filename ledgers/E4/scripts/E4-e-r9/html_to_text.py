"""Render a lesson HTML page to numbered plain text (one block per line), for reading in full."""
import html
import re
import sys
from html.parser import HTMLParser

BLOCK = {"p", "div", "li", "h1", "h2", "h3", "h4", "tr", "pre", "section", "ul", "ol", "table", "figcaption", "dt", "dd", "details", "summary", "blockquote", "header", "footer", "article", "aside", "nav"}
SKIP = {"script", "style", "svg"}


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.buf = []
        self.skip = 0
        self.attrs_stack = []
        self.line_no_src = None

    def flush(self):
        t = re.sub(r"[ \t\r\f\v]+", " ", "".join(self.buf)).strip()
        if t:
            self.out.append(t)
        self.buf = []

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1
            return
        if tag in BLOCK:
            self.flush()
        if tag == "br":
            self.flush()
        if tag == "li":
            self.buf.append("- ")
        if tag in ("td", "th"):
            self.buf.append(" | ")

    def handle_endtag(self, tag):
        if tag in SKIP:
            self.skip -= 1
            return
        if tag in BLOCK:
            self.flush()

    def handle_data(self, data):
        if self.skip == 0:
            self.buf.append(data.replace("\n", " "))


def main(path):
    src = open(path, encoding="utf-8").read()
    p = P()
    p.feed(src)
    p.flush()
    for i, line in enumerate(p.out, 1):
        print(f"{i:04d} {html.unescape(line)}")


if __name__ == "__main__":
    main(sys.argv[1])
