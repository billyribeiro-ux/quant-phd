"""Blind exemplar prose extractor (ruling 15).

For each exemplar article id given on the command line, prints the memo prose
with these dropped: <aside class="annotation">, <p class="exemplar-verdict">
(and anything with data-reveal), and no attribute values are ever printed, so
data-score(s) and data-level never reach the output.
"""
import sys
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "h5", "dt", "dd", "blockquote", "tr", "div", "section", "article", "aside"}


class Strip(HTMLParser):
    def __init__(self, root_id):
        super().__init__(convert_charrefs=True)
        self.root_id = root_id
        self.stack = []  # (tag, skipped)
        self.active = False
        self.out = []

    def _skipped(self):
        return any(s for _, s in self.stack)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if not self.active:
            if a.get("id") == self.root_id:
                self.active = True
                self.stack.append((tag, False))
            return
        if tag in VOID:
            return
        cls = (a.get("class") or "").split()
        skip = (tag == "aside" and "annotation" in cls) or ("exemplar-verdict" in cls) or ("data-reveal" in a)
        self.stack.append((tag, skip))
        if not self._skipped() and tag in BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if not self.active:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break
        if not self.stack:
            self.active = False
            self.out.append("\n")

    def handle_data(self, data):
        if self.active and not self._skipped():
            self.out.append(data)


def main(path, ids):
    html = open(path, encoding="utf-8").read()
    for rid in ids:
        p = Strip(rid)
        p.feed(html)
        text = "".join(p.out)
        lines = [" ".join(l.split()) for l in text.split("\n")]
        print(f"===== {rid} (prose only) =====")
        print("\n".join(l for l in lines if l))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
