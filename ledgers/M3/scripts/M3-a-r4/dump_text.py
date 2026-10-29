"""Render a lesson page to numbered plain text (tags stripped, pre blocks kept) for reading. Usage: dump_text.py <html>"""
import html, re, sys
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        if tag in ("p", "li", "tr", "h1", "h2", "h3", "div", "pre", "section", "table", "dt", "dd", "summary"):
            self.out.append("\n")
        if tag == "td" or tag == "th":
            self.out.append(" | ")
    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1
    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)

src = open(sys.argv[1], encoding="utf-8").read()
p = P()
p.feed(src)
text = "".join(p.out)
lines = [re.sub(r"[ \t]+", " ", l).strip() for l in text.split("\n")]
n = 0
for l in lines:
    if l:
        n += 1
        print(f"{n:04d}: {l}")
