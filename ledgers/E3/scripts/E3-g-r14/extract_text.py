"""Render a lesson page to readable text, marking claim spans and dfn/concept links.

Usage: python -I extract_text.py <page.html> <out.txt>
Claim spans become [CLAIM grade=X cite=... loc=...] ... [/CLAIM]; math is kept as its TeX source.
"""
import html.parser
import re
import sys

BLOCK = {"p", "li", "div", "h1", "h2", "h3", "h4", "tr", "section", "details", "summary", "dt", "dd", "table", "ul", "ol", "figure", "figcaption", "blockquote", "pre"}


class R(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0
        self.stack = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):
            self.skip += 1
            return
        if self.skip:
            return
        if tag in BLOCK or tag == "br":
            self.out.append("\n")
        if tag == "span" and "claim" in (a.get("class") or ""):
            tags = []
            if a.get("data-grade"):
                tags.append("grade=" + a["data-grade"])
            if a.get("data-cite"):
                tags.append("cite=" + a["data-cite"])
            if a.get("data-locator"):
                tags.append("loc=" + a["data-locator"])
            self.out.append("[CLAIM " + " ".join(tags) + "]")
            self.stack.append("claim")
        elif tag == "dfn":
            self.out.append("[DFN " + (a.get("data-concept") or "") + "]")
        elif tag == "a" and "concept" in (a.get("class") or ""):
            self.out.append("[CONCEPT " + (a.get("data-concept") or "") + "]")
        elif tag == "details":
            self.out.append("\n[DETAILS " + (a.get("class") or "") + "]")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag in BLOCK:
            self.out.append("\n")
        if tag == "span" and self.stack and self.stack[-1] == "claim":
            self.stack.pop()
            self.out.append("[/CLAIM]")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def main():
    src, dst = sys.argv[1], sys.argv[2]
    raw = open(src, encoding="utf-8").read()
    p = R()
    p.feed(raw)
    text = "".join(p.out)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    open(dst, "w", encoding="utf-8").write(text)
    print(dst, len(text))


if __name__ == "__main__":
    main()
