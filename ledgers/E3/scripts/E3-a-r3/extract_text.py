"""Extract visible text from a page, one block per line, with the line number of each block's source tag."""
import html.parser
import sys


class Ext(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.out = []
        self.line = 1

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "dt", "dd", "td", "th", "section", "div", "tr", "figcaption", "caption"):
            self.out.append(f"\n[{self.getpos()[0]}:{tag}] ")
        if tag == "section" and dict(attrs).get("class", "").startswith("lab"):
            self.out.append(f"\n[{self.getpos()[0]}:LAB-SECTION {dict(attrs).get('class')}] ")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1

    def handle_data(self, data):
        if self.skip == 0:
            self.out.append(" ".join(data.split()) + " ")


p = Ext()
p.feed(open(sys.argv[1], encoding="utf-8").read())
text = "".join(p.out)
print("\n".join(l for l in text.split("\n") if l.strip()))
