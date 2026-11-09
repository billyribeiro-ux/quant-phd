"""Extract the two exemplars with annotations, verdicts and data attributes stripped, for blind scoring."""
import html.parser
import sys

SRC = sys.argv[1]


class Blind(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0  # depth inside stripped subtrees
        self.stack = []  # (tag, stripped?)
        self.in_exemplar = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class", "") or ""
        if self.skip or ("annotation" in cls.split()) or ("exemplar-verdict" in cls.split()) or ("data-reveal" in a) or ("data-reveal" in dict(attrs)):
            self.stack.append((tag, True))
            if tag not in ("br", "img", "meta", "input", "link"):
                self.skip += 1
            return
        self.stack.append((tag, False))
        if tag == "article" and "exemplar" in cls.split():
            self.out.append("\n=== " + (a.get("data-label") or "?") + " ===\n")
        if tag in ("h4", "h5", "p", "li", "h3"):
            self.out.append("\n")
        if tag == "li":
            self.out.append("- ")

    def handle_endtag(self, tag):
        if not self.stack:
            return
        t, stripped = self.stack.pop()
        if stripped:
            if t not in ("br", "img", "meta", "input", "link"):
                self.skip -= 1
        if tag in ("h4", "h5", "p"):
            self.out.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


p = Blind()
p.feed(open(SRC, encoding="utf-8").read())
text = "".join(p.out)
lines = [ln.rstrip() for ln in text.split("\n")]
keep = []
for ln in lines:
    if ln.strip() == "":
        if keep and keep[-1] == "":
            continue
    keep.append(ln)
print("\n".join(keep))
