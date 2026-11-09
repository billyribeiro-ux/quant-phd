import sys, pathlib
from html.parser import HTMLParser
BLOCK = {"p","li","div","h1","h2","h3","h4","h5","h6","pre","tr","section","details","summary","br","ol","ul","table","dt","dd","figure","header","footer"}
class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []; self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"): self.skip += 1
        if tag in BLOCK: self.out.append("\n")
    def handle_endtag(self, tag):
        if tag in ("script", "style"): self.skip -= 1
        if tag in BLOCK: self.out.append("\n")
    def handle_data(self, data):
        if not self.skip: self.out.append(data)
src = pathlib.Path(sys.argv[1]); dst = pathlib.Path(sys.argv[2])
p = P(); p.feed(src.read_text(encoding="utf-8")); p.close()
text = "".join(p.out)
lines = [l.strip() for l in text.splitlines() if l.strip()]
dst.write_text("\n".join(lines) + "\n", encoding="utf-8")
