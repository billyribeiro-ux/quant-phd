"""Extract visible text of a lesson page, one block per line, for reading (LX1 slice d)."""
import html.parser
import sys


class Extract(html.parser.HTMLParser):
    BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "tr", "section", "div", "table", "dt", "dd", "figcaption", "summary", "pre", "blockquote"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0
        self.buf: list[str] = []

    def flush(self) -> None:
        text = " ".join("".join(self.buf).split())
        if text:
            self.out.append(text)
        self.buf = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style", "svg"):
            self.skip += 1
        if tag in self.BLOCK:
            self.flush()
        if tag == "dfn":
            self.buf.append("[DFN " + dict(attrs).get("id", "") + "]")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style", "svg"):
            self.skip -= 1
        if tag in self.BLOCK:
            self.flush()

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.buf.append(data)


def main() -> None:
    parser = Extract()
    with open(sys.argv[1], encoding="utf-8") as fh:
        parser.feed(fh.read())
    parser.flush()
    for i, line in enumerate(parser.out, 1):
        print(f"{i:4d} {line}")


if __name__ == "__main__":
    main()
