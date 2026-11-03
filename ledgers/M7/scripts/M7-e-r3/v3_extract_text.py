"""Extract line-numbered visible text of one M7 lesson page (verifier round 3, slice e).

Usage: python -I v3_extract_text.py <page.html> > out.txt
Block-level tags end a line; <script>/<style> content is skipped; the raw
text of <pre> and <code> is kept on its own lines so lab output is visible.
"""
import sys
from html.parser import HTMLParser

BLOCK = {"p", "li", "div", "h1", "h2", "h3", "h4", "h5", "h6", "pre", "tr", "dt", "dd",
         "section", "figcaption", "summary", "blockquote", "ol", "ul", "table", "details", "dl", "td", "th"}


class Extract(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lines: list[str] = []
        self.buf: list[str] = []
        self.skip = 0

    def flush(self) -> None:
        text = "".join(self.buf)
        self.buf = []
        for raw in text.split("\n"):
            s = " ".join(raw.split())
            if s:
                self.lines.append(s)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style"):
            self.skip += 1
        if tag in BLOCK:
            self.flush()
        if tag == "br":
            self.flush()

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip -= 1
        if tag in BLOCK:
            self.flush()

    def handle_data(self, data: str) -> None:
        if self.skip == 0:
            self.buf.append(data)


def main() -> None:
    path = sys.argv[1]
    parser = Extract()
    with open(path, encoding="utf-8") as fh:
        parser.feed(fh.read())
    parser.flush()
    for i, line in enumerate(parser.lines, 1):
        print(f"{i:04d} {line}")


if __name__ == "__main__":
    main()
