# Report stray or unclosed tags in L07-L12 (python -I). Void elements skipped.
from html.parser import HTMLParser
import sys
VOID = {"meta","link","img","input","br","hr","source","area","base","col","embed","param","track","wbr"}
class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack=[]; self.issues=[]
    def handle_starttag(self, tag, attrs):
        if tag not in VOID: self.stack.append((tag, self.getpos()))
    def handle_endtag(self, tag):
        if tag in VOID: return
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i][0]==tag:
                for t,pos in self.stack[i+1:]:
                    self.issues.append(f"unclosed <{t}> opened at line {pos[0]} before </{tag}> line {self.getpos()[0]}")
                del self.stack[i:]
                return
        self.issues.append(f"stray </{tag}> at line {self.getpos()[0]}")
for n in range(7,13):
    p=P(); src=open(f"course/modules/M/M2/L{n:02d}.html",encoding="utf-8").read()
    p.feed(src)
    print(f"L{n:02d}: {len(p.issues)} issue(s)")
    for i in p.issues[:10]: print("   ", i)
