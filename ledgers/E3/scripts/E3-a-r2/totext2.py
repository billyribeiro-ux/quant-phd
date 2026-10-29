import sys
from html.parser import HTMLParser
BLOCK = {"p","li","h1","h2","h3","h4","div","tr","section","pre","dt","dd","table","br","ul","ol","th","td","span"}
class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []; self.skip = 0; self.buf = []
    def handle_starttag(self, tag, attrs):
        if tag in ("script","style"): self.skip += 1
        if tag in BLOCK and tag not in ("span","td","th"): self.out.append("\n")
    def handle_endtag(self, tag):
        if tag in ("script","style"): self.skip -= 1
        if tag in BLOCK and tag not in ("span","td","th"): self.out.append("\n")
        if tag in ("td","th"): self.out.append(" | ")
    def handle_data(self, data):
        if not self.skip: self.out.append(data)
p = P(); p.feed(open(sys.argv[1], encoding="utf-8").read())
text = "".join(p.out)
for line in text.split("\n"):
    s = " ".join(line.split())
    if s: print(s)
