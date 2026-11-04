import sys, html
from html.parser import HTMLParser
BLOCK = {"p","li","h1","h2","h3","h4","div","section","tr","pre","ol","ul","header","table","dt","dd","blockquote","figcaption","details","summary"}
class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out=[]; self.skip=0; self.pre=0
    def handle_starttag(self, tag, attrs):
        if tag in ("script","style"): self.skip+=1; return
        if tag=="pre": self.pre+=1
        if tag in BLOCK: self.out.append("\n")
        if tag in ("h1","h2","h3","h4"): self.out.append("\n## ")
        if tag=="br": self.out.append("\n")
        if tag=="li": self.out.append("- ")
        if tag=="tr": self.out.append("\n|")
        if tag in ("td","th"): self.out.append(" ")
    def handle_endtag(self, tag):
        if tag in ("script","style"): self.skip-=1; return
        if tag=="pre": self.pre-=1
        if tag in BLOCK: self.out.append("\n")
    def handle_data(self, d):
        if self.skip: return
        self.out.append(d)
p=P(); p.feed(open(sys.argv[1],encoding="utf-8").read())
txt="".join(p.out)
import re
txt=re.sub(r"\n[ \t]*\n+", "\n", txt)
sys.stdout.write(txt)
