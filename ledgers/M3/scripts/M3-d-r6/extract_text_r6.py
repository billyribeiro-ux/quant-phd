"""Round-4 verifier: plain text of each M3 lesson page (tags stripped, script and style removed), for card checks.

Usage (from the checkout root): .venv/bin/python -I ledgers/M3/scripts/M3-d-r6/extract_text_r4.py
"""

import html
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path.cwd()
OUT = ROOT / "ledgers/M3/scripts/M3-d-r6/out/text"


class Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list) -> None:  # type: ignore[type-arg]
        if tag in ("script", "style"):
            self.skip += 1
        if tag in ("p", "li", "div", "h1", "h2", "h3", "h4", "h5", "tr", "section", "pre", "dd", "dt"):
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)


for n in range(1, 10):
    src = (ROOT / f"course/modules/M/M3/L0{n}.html").read_text(encoding="utf-8")
    parser = Text()
    parser.feed(src)
    text = "".join(parser.parts)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    (OUT / f"L0{n}.txt").write_text(text, encoding="utf-8")
    print(f"L0{n}: {len(text)} chars, {text.count(chr(10))} lines")
