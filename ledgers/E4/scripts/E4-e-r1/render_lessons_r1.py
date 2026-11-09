"""Render one E4 lesson HTML page to numbered plain text, one block per line, for line-level reading."""

import html.parser
import re
import sys
from pathlib import Path

BLOCK: frozenset[str] = frozenset(
    {
        "p",
        "div",
        "li",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "tr",
        "section",
        "article",
        "dt",
        "dd",
        "pre",
        "table",
        "ul",
        "ol",
        "br",
        "figcaption",
        "blockquote",
        "details",
        "summary",
        "dfn",
        "td",
        "th",
    }
)
SKIP: frozenset[str] = frozenset({"script", "style"})


class TextParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in SKIP:
            self.skip += 1
        if tag in BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in SKIP:
            self.skip -= 1
        if tag in BLOCK:
            self.out.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.out.append(data)


def render(src: Path, dst: Path) -> None:
    parser = TextParser()
    parser.feed(src.read_text(encoding="utf-8"))
    lines = [re.sub(r"[ \t\r\f\v]+", " ", ln).strip() for ln in "".join(parser.out).split("\n")]
    kept = [ln for ln in lines if ln]
    dst.write_text("".join(f"{i:05d} {ln}\n" for i, ln in enumerate(kept, 1)), encoding="utf-8")


if __name__ == "__main__":
    render(Path(sys.argv[1]), Path(sys.argv[2]))
