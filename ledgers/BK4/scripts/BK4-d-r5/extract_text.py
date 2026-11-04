"""Render a lesson or project HTML page to plain text, one block per line (stdlib only).

Usage: python3 -I extract_text.py <page.html>  -> writes the text to stdout.
Keeps TeX source inside \\( \\) and \\[ \\] unchanged so every displayed symbol can be read.
"""
import sys
from html.parser import HTMLParser

BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "tr", "div", "section", "pre", "table", "ul", "ol", "dt", "dd", "figcaption", "summary", "details", "blockquote"}


class Render(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0
        self.pre = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
            return
        if tag == "svg":
            self.skip += 1
            return
        if tag in BLOCK:
            self.out.append("\n")
        if tag == "pre":
            self.pre += 1
        if tag == "td" or tag == "th":
            self.out.append(" | ")
        if tag == "br":
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "svg") and self.skip:
            self.skip -= 1
            return
        if tag == "pre":
            self.pre -= 1
        if tag in BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if self.skip:
            return
        self.out.append(data)


def main():
    path = sys.argv[1]
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    r = Render()
    r.feed(raw)
    text = "".join(r.out)
    lines = []
    for line in text.split("\n"):
        s = " ".join(line.split()) if line.strip() else ""
        if s or (lines and lines[-1] != ""):
            lines.append(s)
    sys.stdout.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
