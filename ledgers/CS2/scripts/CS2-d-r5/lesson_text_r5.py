"""Extract the visible text of each CS2 lesson page (tags removed, entities unescaped), for the card checks."""
import html, re, sys
from html.parser import HTMLParser
from pathlib import Path

class T(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        if tag in ("p", "li", "pre", "tr", "dd", "dt", "h2", "h3", "h4", "div", "section"):
            self.out.append("\n")
    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1
    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)

src, dst = Path(sys.argv[1]), Path(sys.argv[2])
dst.mkdir(parents=True, exist_ok=True)
for f in sorted(src.glob("L[0-9][0-9].html")):
    p = T()
    p.feed(f.read_text(encoding="utf-8"))
    (dst / (f.stem + ".txt")).write_text("".join(p.out), encoding="utf-8")
print("wrote", len(list(dst.glob("L*.txt"))))
