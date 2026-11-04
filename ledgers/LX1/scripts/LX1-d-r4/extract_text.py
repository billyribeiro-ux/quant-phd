"""Extract readable text from a lesson page, one output line per source block, with source line numbers."""
import html
import re
import sys
from html.parser import HTMLParser

BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "div", "section", "tr", "pre", "dt", "dd", "figcaption", "blockquote", "td", "th", "ul", "ol", "table", "caption"}


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.buf = []
        self.line = 1
        self.start_line = 1
        self.skip = 0

    def flush(self):
        text = "".join(self.buf)
        text = re.sub(r"[ \t]+", " ", text).strip()
        if text:
            self.out.append(f"{self.start_line:5d}: {text}")
        self.buf = []
        self.start_line = self.line

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        if tag in BLOCK:
            self.flush()
        if tag == "br":
            self.buf.append(" ")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1
        if tag in BLOCK:
            self.flush()

    def handle_data(self, data):
        if self.skip:
            return
        self.line += data.count("\n")
        self.buf.append(data.replace("\n", " "))


def main(path):
    src = open(path, encoding="utf-8").read()
    p = P()
    p.feed(src)
    p.flush()
    print("\n".join(p.out))


if __name__ == "__main__":
    main(sys.argv[1])
