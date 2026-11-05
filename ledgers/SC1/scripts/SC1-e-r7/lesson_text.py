"""Strip tags from an SC1 lesson page, keep the math source, and print one block per source line.

Usage: python -I lesson_text.py <page.html>. Script/style blocks are removed. Entities are unescaped so the
text shows the characters the reader sees in the source (\\( ... \\) is kept as written).
"""
import re
import sys
from html import unescape
from html.parser import HTMLParser


class Strip(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0
        self.line = None

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "tr", "div", "pre", "section", "details", "summary", "td"):
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


p = Strip()
p.feed(open(sys.argv[1], encoding="utf-8").read())
text = "".join(p.out)
text = re.sub(r"\n\s*\n+", "\n", text)
sys.stdout.write(text)
