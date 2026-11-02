import html, re, sys, pathlib
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "div", "tr", "section", "br", "pre"):
            self.out.append("\n")
    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "div", "tr", "section", "pre"):
            self.out.append("\n")
    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)

src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
p = P()
p.feed(src)
text = "".join(p.out)
text = re.sub(r"[ \t]+", " ", text)
text = re.sub(r"\n\s*\n+", "\n", text)
sys.stdout.write(text)
