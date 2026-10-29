import html.parser, sys
BLOCK = {"p", "div", "h1", "h2", "h3", "h4", "li", "tr", "pre", "section", "summary", "details", "table", "ol", "ul", "span"}
class P(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []; self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "svg"): self.skip += 1
        if tag in BLOCK and tag != "span": self.out.append("\n")
        if tag == "td": self.out.append(" | ")
        if tag == "br": self.out.append("\n")
    def handle_endtag(self, tag):
        if tag in ("script", "style", "svg") and self.skip: self.skip -= 1
        if tag in BLOCK and tag != "span": self.out.append("\n")
    def handle_data(self, d):
        if not self.skip: self.out.append(d)
p = P(); p.feed(open(sys.argv[1], encoding="utf-8").read())
text = "".join(p.out)
import re
text = re.sub(r"\n\s*\n+", "\n", text)
print(text)
