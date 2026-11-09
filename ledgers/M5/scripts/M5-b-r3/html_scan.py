"""Scan slice pages for start tags outside the HTML vocabulary (raw '<' in prose or math) and for figures."""
import html.parser
import re
import sys
from pathlib import Path

VOCAB = set("""a abbr article aside audio b blockquote body br button canvas caption code col colgroup dd del details
dfn div dl dt em fieldset figcaption figure footer form h1 h2 h3 h4 h5 h6 head header hr html i iframe img input ins kbd
label legend li link main mark meta nav noscript object ol optgroup option p picture pre q s samp script section
select small source span strong style sub summary sup svg table tbody td template textarea tfoot th thead time title
tr u ul var video wbr math""".split())

class Scan(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.bad = []
        self.figs = 0
    def handle_starttag(self, tag, attrs):
        if tag not in VOCAB:
            self.bad.append((self.getpos(), tag))
        if tag in ("svg", "figure", "img"):
            self.figs += 1

for name in ("L05", "L06", "L07"):
    path = Path(f"course/modules/M/M5/{name}.html")
    text = path.read_text(encoding="utf-8")
    s = Scan()
    s.feed(text)
    raw = [(i + 1, line.strip()[:120]) for i, line in enumerate(text.splitlines()) if re.search(r"<[A-Za-z]", line) and re.search(r"\\\(.*<[A-Za-z/!?].*\\\)", line)]
    print(name, "unknown start tags:", s.bad, "figure-like tags:", s.figs, "figures-js refs:", text.count("figures-"))
    print(name, "math spans with raw < before a letter:", raw)
