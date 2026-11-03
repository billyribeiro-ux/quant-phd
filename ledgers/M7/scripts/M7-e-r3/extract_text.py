"""Extract visible text of M7 lesson pages, one line per block, for card-by-card checking.

Usage: python -I extract_text.py <html> <out.txt>
"""
import sys
from html.parser import HTMLParser

BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "div", "tr", "section", "dt", "dd", "pre", "figcaption", "caption", "th", "td", "summary", "blockquote", "table", "ul", "ol"}
SKIP = {"script", "style"}


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.buf = []
        self.skip = 0

    def flush(self):
        text = "".join(self.buf)
        text = " ".join(text.split())
        if text:
            self.out.append(text)
        self.buf = []

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1
        if tag in BLOCK or tag == "br":
            self.flush()

    def handle_endtag(self, tag):
        if tag in SKIP and self.skip:
            self.skip -= 1
        if tag in BLOCK:
            self.flush()

    def handle_data(self, data):
        if not self.skip:
            self.buf.append(data)


def main():
    src, dst = sys.argv[1], sys.argv[2]
    p = P()
    with open(src, encoding="utf-8") as fh:
        p.feed(fh.read())
    p.flush()
    with open(dst, "w", encoding="utf-8") as fh:
        for i, line in enumerate(p.out, 1):
            fh.write(f"{i:04d} {line}\n")


if __name__ == "__main__":
    main()
