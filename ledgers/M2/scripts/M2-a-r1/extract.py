"""Extract readable text from a course page: keeps TeX source, marks dfn/concept/grade/tags.

Usage: python -I extract.py <file.html> > out.txt
"""
import sys
from html.parser import HTMLParser

SKIP = {"script", "style", "head"}
BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "tr", "div", "section", "table", "pre", "summary", "details", "figcaption", "caption", "ul", "ol", "dt", "dd", "blockquote", "header", "footer", "article", "td", "th"}


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0
        self.line_start = True

    def emit(self, s):
        self.out.append(s)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in SKIP:
            self.skip += 1
            return
        if self.skip:
            return
        if tag in BLOCK:
            self.emit("\n")
        if tag == "dfn":
            self.emit("[DFN:%s|%s]" % (a.get("id", ""), a.get("data-concept", "")))
        if tag == "a" and "concept" in (a.get("class") or ""):
            self.emit("[LINK:%s]" % a.get("data-concept", a.get("href", "")))
        if tag == "span" and a.get("data-grade"):
            self.emit("[GRADE:%s]" % a.get("data-grade"))
        if tag == "details":
            self.emit("\n[DETAILS]")
        if tag == "section" and a.get("class"):
            self.emit("\n[SECTION class=%s id=%s]" % (a.get("class"), a.get("id", "")))
        if tag == "div" and a.get("class") and any(c in a.get("class") for c in ("block", "quiz", "rung", "ladder")):
            self.emit("\n[DIV class=%s %s]" % (a.get("class"), " ".join("%s=%s" % (k, v) for k, v in attrs if k.startswith("data-"))))
        if tag == "pre" or tag == "code":
            self.emit("\n[%s]" % tag.upper())
        if tag == "img":
            self.emit("[IMG %s]" % a.get("alt", ""))
        if tag == "svg":
            self.emit("[SVG]")
        if tag == "input":
            self.emit("[INPUT %s]" % " ".join("%s=%s" % (k, v) for k, v in attrs))
        if tag == "li":
            self.emit("\n  - ")

    def handle_endtag(self, tag):
        if tag in SKIP:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag in BLOCK:
            self.emit("\n")

    def handle_data(self, data):
        if self.skip:
            return
        self.emit(data)


def main():
    p = P()
    with open(sys.argv[1], encoding="utf-8") as f:
        p.feed(f.read())
    text = "".join(p.out)
    lines = [ln.rstrip() for ln in text.split("\n")]
    out = []
    blank = False
    for ln in lines:
        if not ln.strip():
            if not blank:
                out.append("")
            blank = True
        else:
            out.append(ln.strip() if not ln.startswith("  - ") else ln.rstrip())
            blank = False
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
