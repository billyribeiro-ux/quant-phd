"""Render a lesson page to plain text, one block per line, for line-by-line reading.

Usage: python -I html_to_text.py <page.html> <out.txt>
Skips <script> and <style>; keeps <math>/<code> text; marks <dfn>, <details>, <summary>, <li>, <tr>.
"""
import html.parser
import sys

BLOCK = {"p", "div", "section", "h1", "h2", "h3", "h4", "li", "tr", "table", "pre", "details", "summary",
         "blockquote", "figure", "figcaption", "ol", "ul", "dt", "dd", "caption", "header", "footer", "nav", "article"}


class Render(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0
        self.attrs_stack: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style"):
            self.skip += 1
            return
        if tag in BLOCK:
            self.out.append("\n")
        if tag == "td" or tag == "th":
            self.out.append(" | ")
        if tag == "tr":
            self.out.append("\n")
        a = dict(attrs)
        if tag == "section" and a.get("class"):
            self.out.append(f"\n[SECTION class={a.get('class')} id={a.get('id')}]\n")
        if tag == "dfn":
            self.out.append(f"[DFN id={a.get('id')} concept={a.get('data-concept')}]")
        if tag == "a" and a.get("class") == "concept":
            self.out.append(f"[CONCEPT-LINK {a.get('data-concept')}]")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip = max(0, self.skip - 1)
            return
        if tag in BLOCK:
            self.out.append("\n")

    def handle_data(self, data: str) -> None:
        if self.skip:
            return
        self.out.append(data)


def main() -> None:
    src, dst = sys.argv[1], sys.argv[2]
    r = Render()
    with open(src, encoding="utf-8") as fh:
        r.feed(fh.read())
    text = "".join(r.out)
    lines = [ln.rstrip() for ln in text.split("\n")]
    cleaned: list[str] = []
    for ln in lines:
        ln = " ".join(ln.split())
        if ln or (cleaned and cleaned[-1]):
            cleaned.append(ln)
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write("\n".join(f"{i + 1:4d}: {ln}" if ln else "" for i, ln in enumerate(cleaned)) + "\n")


if __name__ == "__main__":
    main()
