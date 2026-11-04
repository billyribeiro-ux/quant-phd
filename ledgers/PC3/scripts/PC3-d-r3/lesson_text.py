"""Dump a PC3 lesson page as numbered plain text (tags stripped, math kept as TeX).

usage: python -I lesson_text.py <path-to-html>
"""
import html.parser
import sys


class Dump(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list) -> None:  # type: ignore[type-arg]
        if tag in ("script", "style"):
            self.skip += 1
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "tr", "div", "section", "dt", "dd", "pre", "br"):
            self.out.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.out.append(data)


def main() -> None:
    d = Dump()
    with open(sys.argv[1], encoding="utf-8") as fh:
        d.feed(fh.read())
    text = "".join(d.out)
    lines = [ln.rstrip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln.strip()]
    for i, ln in enumerate(lines, 1):
        print(f"{i:4d} {ln}")


if __name__ == "__main__":
    main()
