"""Scan L08-L10 pages for start tags outside the HTML vocabulary (a raw '<' in math breaks the page).

Also reports every '<' that is followed by a letter inside a <pre> or math span, and counts the
'stock' and 'Bellman equation' words. Usage: python3 -I html_tag_scan.py <repo-root>
"""

import html.parser
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1]) / "course/modules/M/M5"
VOCAB = {
    "a", "abbr", "article", "aside", "b", "body", "br", "button", "caption", "code", "col", "colgroup", "dd", "details",
    "dfn", "div", "dl", "dt", "em", "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "head",
    "header", "hr", "html", "i", "input", "label", "legend", "li", "link", "main", "meta", "nav", "ol", "option", "p",
    "pre", "script", "section", "select", "small", "span", "strong", "style", "summary", "sub", "sup", "table", "tbody",
    "td", "textarea", "tfoot", "th", "thead", "title", "tr", "u", "ul", "svg", "path", "g", "line", "rect", "circle",
    "text", "desc", "polyline", "polygon", "ellipse", "defs", "use", "image", "mark", "time", "img", "source", "noscript",
    "iframe", "template", "canvas", "var", "kbd", "q", "cite", "blockquote", "address", "picture", "tspan",
}


class Scan(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.bad: list[tuple[int, str]] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:  # type: ignore[type-arg]
        if tag not in VOCAB:
            self.bad.append((self.getpos()[0], tag))


for name in ("L08.html", "L09.html", "L10.html"):
    text = (root / name).read_text(encoding="utf-8")
    sc = Scan()
    sc.feed(text)
    print(name, "unknown start tags:", sc.bad[:20], "count", len(sc.bad))
    raw = [i + 1 for i, ln in enumerate(text.splitlines()) if re.search(r"<[A-Za-z]", re.sub(r"<[^>]*>", "", ln))]
    print(name, "lines with a '<' followed by a letter outside tags:", raw[:20])
    for word in ("stock", "Bellman equation", "P4", "TODO", "TBD"):
        hits = [i + 1 for i, ln in enumerate(text.splitlines()) if word in ln]
        print(name, f"'{word}' lines:", hits)
