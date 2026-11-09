"""Round-11: word count of every <details class="solution"> on L04-L06 (html.parser, tags stripped)."""
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyF31-E4-b")


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_sol = False
        self.buf = []
        self.sols = []

    def handle_starttag(self, tag, attrs):
        if tag == "details" and dict(attrs).get("class") == "solution":
            self.in_sol = True
            self.buf = []

    def handle_endtag(self, tag):
        if tag == "details" and self.in_sol:
            self.sols.append(" ".join("".join(self.buf).split()))
            self.in_sol = False

    def handle_data(self, d):
        if self.in_sol:
            self.buf.append(d)


for page in ["L04", "L05", "L06"]:
    x = P()
    x.feed((ROOT / f"course/modules/E/E4/{page}.html").read_text(encoding="utf-8"))
    w = [len(s.split()) for s in x.sols]
    print(page, "solutions", len(w), "min words", min(w), "max words", max(w))
