"""Extract the visible text of each M3 lesson page (and project.html) into plain-text files for grep (verifier round 3).

Tags are stripped with html.parser; <script> and <style> are dropped; block elements become newlines. Output goes to
ledgers/M3/scripts/M3-d-r3/out3/lesson_text/<page>.txt. Run from the checkout root with -I.
"""

import html.parser
import re
from pathlib import Path

ROOT = Path.cwd()
OUT = ROOT / "ledgers/M3/scripts/M3-d-r3/out3/lesson_text"
BLOCK = {"p", "div", "li", "h1", "h2", "h3", "h4", "h5", "tr", "section", "dt", "dd", "pre", "br", "article", "ol", "ul"}


class Extract(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs) -> None:  # type: ignore[no-untyped-def]
        if tag in ("script", "style"):
            self.skip += 1
        if tag in BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style") and self.skip:
            self.skip -= 1
        if tag in BLOCK:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)


OUT.mkdir(parents=True, exist_ok=True)
for page in sorted((ROOT / "course/modules/M/M3").glob("*.html")):
    parser = Extract()
    parser.feed(page.read_text(encoding="utf-8"))
    text = "".join(parser.parts)
    text = re.sub(r"[ \t\xa0]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    (OUT / f"{page.stem}.txt").write_text(text, encoding="utf-8")
    print(page.stem, len(text))
