"""Render a lesson HTML page as numbered plain text with markers for dfn, concept links, grades and details.

Usage: python -I extract_text.py <page.html>
"""

from __future__ import annotations

import html
import re
import sys
from html.parser import HTMLParser

BLOCK = {"p", "div", "li", "h1", "h2", "h3", "h4", "tr", "section", "details", "summary", "ul", "ol", "table", "pre", "header", "figure", "figcaption", "caption", "blockquote", "dt", "dd", "span"}


class R(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0
        self.script = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if tag in ("script", "style"):
            self.script = True
            return
        if tag == "dfn":
            self.out.append(f"[DFN:{a.get('data-concept') or a.get('id')}]")
        if tag == "a" and a.get("class") and "concept" in a.get("class", ""):
            self.out.append(f"[LINK:{a.get('data-concept')}]")
        if tag == "span" and a.get("data-grade"):
            self.out.append(f"[GRADE:{a.get('data-grade')}]")
        if tag == "details":
            self.out.append("\n[DETAILS " + (a.get("class") or "") + "]")
        if tag == "h2" or tag == "h3":
            self.out.append(f"\n\n## <{tag} id={a.get('id')}> ")
        elif tag in BLOCK:
            self.out.append("\n")
        if tag == "li":
            self.out.append("- ")
        if tag == "tr":
            self.out.append("\n| ")
        if tag in ("td", "th"):
            self.out.append(" | ")
        if tag == "div" and a.get("class") and "block" in a.get("class", ""):
            self.out.append(f"\n[BLOCK {a.get('class')}] ")
        if tag == "img":
            self.out.append(f"[IMG alt={a.get('alt')!r}]")
        if tag == "svg":
            self.out.append("[SVG]")
        if tag == "script":
            self.script = True

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.script = False
        if tag in BLOCK:
            self.out.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.script:
            self.out.append(data)


def main() -> None:
    raw = open(sys.argv[1], encoding="utf-8").read()
    # Strip the head and the nav chrome; keep the main element.
    m = re.search(r"<main.*?</main>", raw, re.S)
    body = m.group(0) if m else raw
    r = R()
    r.feed(body)
    text = "".join(r.out)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
