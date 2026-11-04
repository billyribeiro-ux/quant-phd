# ruff: noqa: E501
"""Round-5 verifier (CS2-d): plain-text dump of each CS2 lesson, project and hub page (HTML tags removed).

Writes /tmp/cs2d_r5_text/<page>.txt. Used by cards_checks_delta_r5.py and by the reading of the lesson text in the round.
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = Path("/tmp/cs2d_r5_text")
OUT.mkdir(parents=True, exist_ok=True)


class Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.out: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style"):
            self.skip += 1
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "section", "tr", "pre", "div", "dt", "dd", "figcaption"):
            self.out.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.out.append(data)


for page in sorted((ROOT / "course/modules/CS/CS2").glob("*.html")):
    parser = Text()
    parser.feed(page.read_text(encoding="utf-8"))
    text = re.sub(r"\n\s*\n+", "\n", "".join(parser.out))
    (OUT / f"{page.name}.txt").write_text(text, encoding="utf-8")
    print("wrote", page.name, len(text))
