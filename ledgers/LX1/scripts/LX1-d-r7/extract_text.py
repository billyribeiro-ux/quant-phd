"""Round-7 (LX1-d) extraction: strip HTML from L01-L04 into one text line per block, with line numbers.

Usage: python3 -I extract_text.py <checkout> <outdir>
Writes <outdir>/L01.txt .. L04.txt. Independent of the builder; no lesson text is edited.
"""
import html, re, sys
from html.parser import HTMLParser

BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "div", "section", "tr", "pre", "dt", "dd", "figcaption", "summary", "label", "td", "th", "ol", "ul", "table", "caption", "blockquote", "header", "footer", "article", "details"}
SKIP = {"script", "style", "svg"}


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lines = []
        self.buf = []
        self.skip = 0
        self.src_line = 1

    def flush(self, tag_line):
        s = re.sub(r"[ \t]+", " ", "".join(self.buf)).strip()
        if s:
            self.lines.append((tag_line, s))
        self.buf = []

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1
        if tag in BLOCK:
            self.flush(self.getpos()[0])
        if tag == "br":
            self.buf.append(" ")

    def handle_endtag(self, tag):
        if tag in SKIP:
            self.skip -= 1
        if tag in BLOCK:
            self.flush(self.getpos()[0])

    def handle_data(self, data):
        if not self.skip:
            self.buf.append(data)


def run(path):
    p = P()
    p.feed(open(path, encoding="utf-8").read())
    p.flush(0)
    return p.lines


if __name__ == "__main__":
    base, out = sys.argv[1], sys.argv[2]
    for L in ("L01", "L02", "L03", "L04"):
        lines = run(f"{base}/course/modules/LX/LX1/{L}.html")
        with open(f"{out}/{L}.txt", "w", encoding="utf-8") as fh:
            for ln, s in lines:
                fh.write(f"[{ln}] {s}\n")
        print(L, len(lines), "text blocks")
