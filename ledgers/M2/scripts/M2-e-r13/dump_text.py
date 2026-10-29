"""Dump each M2 lesson as plain text with line numbers, and cards grouped by lesson."""
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
BLOCK = {"p", "li", "tr", "h1", "h2", "h3", "h4", "div", "section", "dt", "dd", "pre", "table", "ul", "ol", "details", "summary", "td", "th"}


class T(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        if tag == "td" or tag == "th":
            self.parts.append(" | ")
        if tag in BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1
        if tag in BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


for path in sorted(ROOT.glob("L*.html")):
    p = T()
    p.feed(path.read_text(encoding="utf-8"))
    text = "".join(p.parts)
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in text.split("\n")]
    lines = [ln for ln in lines if ln]
    (OUT / f"{path.stem}.txt").write_text("\n".join(f"{i+1:4d}: {ln}" for i, ln in enumerate(lines)) + "\n", encoding="utf-8")

cards = json.loads((ROOT / "cards.json").read_text(encoding="utf-8"))
by: dict[str, list] = {}
for c in cards:
    by.setdefault(c["lesson"], []).append(c)
for lesson, cs in sorted(by.items()):
    with (OUT / f"cards_{lesson}.txt").open("w", encoding="utf-8") as fh:
        for c in cs:
            fh.write(f"[{c['id']}] grade={c.get('grade')} basis={c.get('basis')!r}\n  FRONT: {c['front']}\n  BACK: {c['back']}\n")
print({k: len(v) for k, v in by.items()})
