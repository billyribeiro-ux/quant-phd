"""Plain-text view of a lesson page for line-by-line reading (no HTML tags).

Usage: python3 -I html_to_text.py <page.html> > out.txt
Block-level elements become line breaks; script/style content is dropped.
"""
import html.parser
import sys


BLOCK = {"p", "li", "div", "h1", "h2", "h3", "h4", "tr", "pre", "section", "details", "summary", "dt", "dd", "table", "ul", "ol", "figcaption", "header", "footer", "blockquote", "td", "th"}


class Extract(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style"):
            self.skip += 1
        if tag in BLOCK:
            self.out.append("\n")
        if tag == "td" or tag == "th":
            self.out.append(" | ")
        if tag == "br":
            self.out.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip -= 1
        if tag in BLOCK:
            self.out.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.out.append(data)


def main() -> None:
    parser = Extract()
    with open(sys.argv[1], encoding="utf-8") as fh:
        parser.feed(fh.read())
    text = "".join(parser.out)
    lines = [" ".join(line.split()) for line in text.split("\n")]
    prev_blank = False
    for line in lines:
        if not line:
            if not prev_blank:
                print()
            prev_blank = True
        else:
            print(line)
            prev_blank = False


if __name__ == "__main__":
    main()
