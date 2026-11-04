"""LX2-d round 6: convert a lesson page to plain text, one block per line, keeping line numbers of the source."""
import sys
from html.parser import HTMLParser

BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "tr", "div", "section", "dt", "dd", "pre", "figcaption", "blockquote", "summary", "td", "th"}


class P(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.cur: list[str] = []
        self.skip = 0
        self.line = 1
        self.start_line = 1

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag in ("script", "style"):
            self.skip += 1
        if tag in BLOCK:
            self.flush()
            self.start_line = self.getpos()[0]
        if tag == "br":
            self.flush()

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style") and self.skip:
            self.skip -= 1
        if tag in BLOCK:
            self.flush()

    def handle_data(self, data: str) -> None:
        if self.skip:
            return
        if not self.cur:
            self.start_line = self.getpos()[0]
        self.cur.append(data)

    def flush(self) -> None:
        text = " ".join("".join(self.cur).split())
        if text:
            self.out.append(f"L{self.start_line}: {text}")
        self.cur = []


def main() -> None:
    p = P()
    with open(sys.argv[1], encoding="utf-8") as fh:
        p.feed(fh.read())
    p.flush()
    print("\n".join(p.out))


if __name__ == "__main__":
    main()
