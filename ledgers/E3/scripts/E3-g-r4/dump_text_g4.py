"""Dump a lesson HTML file to numbered plain text, one block per line (stdlib only).

Usage: python -I dump_text_g3.py <input.html> <output.txt>
Math source (\\( ... \\), \\[ ... \\]) is kept verbatim as written in the HTML.
"""
import html.parser
import sys

BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "div", "section", "header", "tr", "pre", "dt", "dd",
         "blockquote", "figcaption", "summary", "table", "ul", "ol", "details", "th", "td", "caption"}
SKIP = {"script", "style", "nav", "svg"}


class Dump(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lines: list[str] = []
        self.buf: list[str] = []
        self.skip = 0
        self.pre = 0

    def flush(self) -> None:
        text = "".join(self.buf)
        self.buf = []
        if self.pre:
            for ln in text.split("\n"):
                self.lines.append(ln)
            return
        text = " ".join(text.split())
        if text:
            self.lines.append(text)

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag in SKIP:
            self.skip += 1
            return
        if tag == "pre":
            self.flush()
            self.pre += 1
        if tag in BLOCK:
            self.flush()
        if tag == "br":
            self.flush()

    def handle_endtag(self, tag: str) -> None:
        if tag in SKIP:
            self.skip -= 1
            return
        if tag == "pre":
            self.flush()
            self.pre -= 1
        if tag in BLOCK:
            self.flush()

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.buf.append(data)


def main() -> None:
    src, dst = sys.argv[1], sys.argv[2]
    p = Dump()
    with open(src, encoding="utf-8") as fh:
        p.feed(fh.read())
    p.flush()
    with open(dst, "w", encoding="utf-8") as fh:
        for i, ln in enumerate(p.lines, 1):
            fh.write(f"{i:04d}| {ln}\n")
    print(f"{dst}: {len(p.lines)} lines")


if __name__ == "__main__":
    main()
