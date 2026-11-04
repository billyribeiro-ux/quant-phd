"""Render a lesson HTML page as line-numbered plain text for slice-e card verification.

Usage: python -I html_to_text.py <page.html>  (writes to stdout)
Keeps visible text and math source; drops script/style and lab source blocks (pre without class "expected").
"""

from __future__ import annotations

import html.parser
import re
import sys
from pathlib import Path

BLOCK = {
    "p",
    "li",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "tr",
    "div",
    "section",
    "pre",
    "dt",
    "dd",
    "table",
    "ul",
    "ol",
    "blockquote",
    "figure",
    "figcaption",
    "header",
    "footer",
    "details",
    "summary",
    "article",
    "aside",
    "nav",
}


class Renderer(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.buf: list[str] = []
        self.skip = 0
        self.code = 0

    def flush(self) -> None:
        text = re.sub(r"[ \t]+", " ", "".join(self.buf)).strip()
        if text:
            self.out.append(text)
        self.buf = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style"):
            self.skip += 1
            return
        if tag == "pre" and dict(attrs).get("class") != "expected":
            self.flush()
            self.code += 1
            self.out.append("[CODE BLOCK: lab source omitted from this rendering]")
            return
        if self.code:
            return
        if tag in BLOCK:
            self.flush()
        if tag == "dfn":
            self.buf.append("[DFN:" + (dict(attrs).get("id") or "") + "]")
        if tag == "li":
            self.buf.append("- ")
        if tag == "br":
            self.flush()

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip = max(0, self.skip - 1)
            return
        if tag == "pre" and self.code:
            self.code -= 1
            return
        if self.code:
            return
        if tag in BLOCK:
            self.flush()

    def handle_data(self, data: str) -> None:
        if not self.skip and not self.code:
            self.buf.append(data.replace("\n", " "))


def main() -> None:
    renderer = Renderer()
    renderer.feed(Path(sys.argv[1]).read_text(encoding="utf-8"))
    renderer.flush()
    for i, line in enumerate(renderer.out, 1):
        print(f"{i:04d}| {line}")


if __name__ == "__main__":
    main()
