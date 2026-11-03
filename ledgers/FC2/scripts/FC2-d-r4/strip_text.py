"""Extract the visible text of a lesson or project page (scripts, styles and tags removed), one block per line.

Usage: python -I strip_text.py <file.html>
"""

import html.parser
import re
import sys
from pathlib import Path


class Text(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style", "nav", "header", "footer"):
            self.skip += 1
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "h5", "dt", "dd", "tr", "pre", "div", "section", "article"):
            self.out.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style", "nav", "header", "footer"):
            self.skip = max(0, self.skip - 1)

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.out.append(data)


parser = Text()
parser.feed(Path(sys.argv[1]).read_text(encoding="utf-8"))
text = "".join(parser.out)
text = re.sub(r"[ \t]+", " ", text)
text = re.sub(r"\n\s*\n+", "\n", text)
sys.stdout.write(text.strip() + "\n")
