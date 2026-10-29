"""Round 5 FC2-d: lossless text extraction with html.parser (keeps '<' in math)."""
import sys, pathlib
from html.parser import HTMLParser
BLOCK = {"p", "li", "tr", "h1", "h2", "h3", "h4", "h5", "div", "section", "pre", "br", "dt", "dd", "article"}
class T(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.out = []; self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"): self.skip += 1
        if tag in BLOCK: self.out.append("\n")
    def handle_endtag(self, tag):
        if tag in ("script", "style"): self.skip -= 1
        if tag in BLOCK: self.out.append("\n")
    def handle_data(self, data):
        if not self.skip: self.out.append(data)
src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
p = T(); p.feed(src)
txt = "".join(p.out)
lines = [" ".join(l.split()) for l in txt.split("\n")]
pathlib.Path(sys.argv[2]).write_text("\n".join(l for l in lines if l) + "\n", encoding="utf-8")
