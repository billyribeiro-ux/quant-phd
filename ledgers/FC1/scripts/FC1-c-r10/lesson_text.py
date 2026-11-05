"""Write plain-text versions of the FC1 lesson pages and the project page into out/lessons/ (verifier, round 10).

Strips tags and scripts, keeps the TeX source between \\( and \\) and the text of each element on its own line.
Usage: python -I ledgers/FC1/scripts/FC1-c-r10/lesson_text.py
"""

from __future__ import annotations

import html
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "course" / "modules" / "FC" / "FC1"
OUT = ROOT / "ledgers" / "FC1" / "scripts" / "FC1-c-r10" / "out" / "lessons"
BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "tr", "dt", "dd", "pre", "div", "section", "figcaption", "caption", "th", "td"}


class Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style", "svg"):
            self.skip += 1
        if tag in BLOCK or tag == "br":
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style", "svg") and self.skip:
            self.skip -= 1
        if tag in BLOCK:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)


def convert(path: Path) -> str:
    parser = Text()
    parser.feed(path.read_text(encoding="utf-8"))
    text = "".join(parser.parts)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    lines = [ln.strip() for ln in text.split("\n")]
    out: list[str] = []
    for ln in lines:
        if ln or (out and out[-1]):
            out.append(ln)
    return "\n".join(out) + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name in ("L01.html", "L02.html", "L03.html", "L04.html", "L05.html", "project.html", "index.html"):
        (OUT / (name.replace(".html", ".txt"))).write_text(convert(SRC / name), encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
