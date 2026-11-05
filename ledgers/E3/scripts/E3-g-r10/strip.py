"""Extract readable text from a lesson page: drop script/style, keep TeX source, one block per line."""
import html
import re
import sys
from html.parser import HTMLParser

BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "div", "tr", "section", "header", "figure", "table", "ul", "ol", "dt", "dd", "pre", "blockquote", "details", "summary", "caption"}


class T(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        if tag in BLOCK or tag == "br":
            self.out.append("\n")
        if tag in ("td", "th"):
            self.out.append(" | ")

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1
        if tag in BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


src = open(sys.argv[1], encoding="utf-8").read()
p = T()
p.feed(src)
text = "".join(p.out)
lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in text.split("\n")]
lines = [ln for ln in lines if ln]
print("\n".join(lines))
