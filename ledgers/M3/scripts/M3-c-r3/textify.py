"""Dump the learner-visible text of a lesson page, one block per line, with TeX kept.

Usage: python -I textify.py <page.html> > out.txt
Keeps the text of every element; <pre> blocks are kept verbatim; <script>/<style> dropped.
"""
import sys
from html.parser import HTMLParser

BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "div", "section", "tr", "pre", "summary", "dt", "dd", "td", "th", "figcaption", "blockquote", "ol", "ul", "table", "thead", "tbody", "details", "header", "footer", "main", "nav", "article"}


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.buf = []
        self.skip = 0
        self.pre = 0
        self.attrs_stack = []

    def flush(self):
        text = "".join(self.buf)
        self.buf = []
        if self.pre:
            self.out.append(text)
            return
        text = " ".join(text.split())
        if text:
            self.out.append(text)

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
            return
        if tag == "pre":
            self.flush()
            self.pre += 1
        if tag in BLOCK:
            self.flush()
        if tag == "li":
            self.buf.append("- ")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1
            return
        if tag == "pre":
            self.flush()
            self.pre -= 1
        if tag in BLOCK:
            self.flush()

    def handle_data(self, data):
        if self.skip:
            return
        if self.pre:
            self.buf.append(data)
        else:
            self.buf.append(data)


def main():
    src = open(sys.argv[1], encoding="utf-8").read()
    p = P()
    p.feed(src)
    p.flush()
    for i, line in enumerate(p.out, 1):
        print(f"{i:04d} {line}")


if __name__ == "__main__":
    main()
