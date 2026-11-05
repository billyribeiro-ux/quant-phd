import html, re, sys
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0
        self.buf = []
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "pre"):
            if tag == "pre":
                self.buf.append("[PRE]")
            else:
                self.skip += 1
        if tag in ("p", "li", "tr", "h1", "h2", "h3", "h4", "div", "section", "dt", "dd", "pre", "table"):
            self.flush()
    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip = max(0, self.skip - 1)
        if tag == "pre":
            self.buf.append("[/PRE]")
        if tag in ("p", "li", "tr", "h1", "h2", "h3", "h4", "div", "section", "dt", "dd", "pre", "table", "td", "th"):
            self.flush()
    def handle_data(self, d):
        if self.skip == 0:
            self.buf.append(d)
    def flush(self):
        s = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        if s:
            self.out.append(s)
        self.buf = []

p = P()
p.feed(open(sys.argv[1], encoding="utf-8").read())
p.flush()
for i, line in enumerate(p.out, 1):
    print(f"{i}: {line}")
