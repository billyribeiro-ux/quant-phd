"""Plain-text dump of an M4 page for verifier reading: python -I dump_text.py <page.html> <out.txt>."""
import html.parser
import sys


class Dump(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style"):
            self.skip += 1
        if tag in ("p", "li", "h1", "h2", "h3", "tr", "div", "pre", "section", "dt", "dd", "summary"):
            self.out.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style") and self.skip:
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.out.append(data)


def main() -> None:
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, encoding="utf-8") as fh:
        parser = Dump()
        parser.feed(fh.read())
    text = "".join(parser.out)
    lines = [ln.rstrip() for ln in text.splitlines()]
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write("\n".join(ln for ln in lines if ln.strip()) + "\n")


if __name__ == "__main__":
    main()
