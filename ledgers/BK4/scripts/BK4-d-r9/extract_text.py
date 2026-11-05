"""Strip HTML from a lesson page to readable text, one block per line.

Usage: python -I extract_text.py <page.html> > out.txt
"""
import html
import re
import sys
from html.parser import HTMLParser

BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "div", "section", "tr", "dt", "dd", "figcaption", "td", "th", "blockquote", "pre"}


class Extract(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style", "svg"):
            self.skip += 1
            return
        if tag in BLOCK:
            self.out.append("\n")
        if tag == "br":
            self.out.append("\n")
        d = dict(attrs)
        if tag == "span" and d.get("class") and "math" in d.get("class", ""):
            self.out.append("")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style", "svg"):
            self.skip = max(0, self.skip - 1)
            return
        if tag in BLOCK:
            self.out.append("\n")

    def handle_data(self, data: str) -> None:
        if self.skip == 0:
            self.out.append(data)


def main() -> None:
    src = open(sys.argv[1], encoding="utf-8").read()
    p = Extract()
    p.feed(src)
    text = "".join(p.out)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    lines = [ln.strip() for ln in text.split("\n")]
    out: list[str] = []
    for ln in lines:
        if ln == "" and (not out or out[-1] == ""):
            continue
        out.append(ln)
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
