"""Render a lesson HTML page to plain text, one block per line (verifier scratch tool)."""
import sys
from html.parser import HTMLParser

BLOCK = {"p", "li", "div", "section", "h1", "h2", "h3", "h4", "tr", "dt", "dd", "table", "ul", "ol", "figure", "article", "header", "footer", "blockquote", "pre", "details", "summary", "br"}
SKIP = {"script", "style", "svg", "noscript"}


class T(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0
        self.buf = []

    def flush(self):
        text = " ".join("".join(self.buf).split())
        if text:
            self.out.append(text)
        self.buf = []

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1
        if tag in BLOCK:
            self.flush()
        if tag == "img":
            self.buf.append(f"[img {dict(attrs).get('alt', '')}]")

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
    p = T()
    with open(src, encoding="utf-8") as fh:
        p.feed(fh.read())
    p.flush()
    with open(dst, "w", encoding="utf-8") as fh:
        for i, line in enumerate(p.out, 1):
            fh.write(f"{i:04d}| {line}\n")


if __name__ == "__main__":
    main()
