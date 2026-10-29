"""Round-7 verifier script: plain-text dump of each CS2 lesson and of its expected lab blocks.

Strips tags (keeps the text of <pre> blocks), unescapes entities, and writes one line per block element.
Usage: python dump_text_r7.py <checkout-root> <out-dir>
"""

from __future__ import annotations

import html
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class Extract(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lines: list[str] = []
        self.buf: list[str] = []
        self.skip = 0
        self.expected: list[str] = []
        self.in_expected = False
        self.exp_buf: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        cls = dict(attrs).get("class") or ""
        if tag in ("script", "style"):
            self.skip += 1
        if tag == "pre" and "expected" in cls:
            self.in_expected = True
            self.exp_buf = []
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "h5", "dd", "dt", "tr", "div", "section", "article", "pre"):
            self.flush()

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip = max(0, self.skip - 1)
        if tag == "pre" and self.in_expected:
            self.expected.append("\n".join(self.exp_buf))
            self.in_expected = False
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "h5", "dd", "dt", "tr", "div", "section", "article", "pre"):
            self.flush()

    def handle_data(self, data: str) -> None:
        if self.skip:
            return
        if self.in_expected:
            self.exp_buf.append(data)
        self.buf.append(data)

    def flush(self) -> None:
        text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        if text:
            self.lines.append(text)
        self.buf = []


def main() -> None:
    root, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    for page in sorted((root / "course/modules/CS/CS2").glob("*.html")):
        parser = Extract()
        parser.feed(page.read_text(encoding="utf-8"))
        parser.flush()
        (out / f"{page.stem}.txt").write_text("\n".join(parser.lines) + "\n", encoding="utf-8")
        (out / f"{page.stem}.expected.txt").write_text(
            "\n\n----\n".join(parser.expected) + "\n", encoding="utf-8"
        )
        print(page.stem, len(parser.lines), "lines", len(parser.expected), "expected blocks")
    _ = html


if __name__ == "__main__":
    main()
