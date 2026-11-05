import os, re, sys
from html.parser import HTMLParser
root = sys.argv[1]
page = os.path.join(root, "course/modules/E/E3/project.html")
class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.hrefs=[]; self.ids=set(); self.srcs=[]; self.concepts=[]; self.defs=[]
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        if "id" in d: self.ids.add(d["id"])
        if tag=="a" and "href" in d: self.hrefs.append((d["href"], d.get("data-concept")))
        if tag in ("script","link","img") and ("src" in d or "href" in d):
            self.srcs.append(d.get("src") or d.get("href"))
        if tag=="dfn" and "id" in d: self.defs.append(d["id"])
def parse(path):
    p=P(); p.feed(open(path,encoding="utf-8").read()); return p
p=parse(page)
base=os.path.dirname(page)
bad=[]
for href,_ in p.hrefs:
    if href.startswith(("http://","https://","mailto:")): print("EXTERNAL", href); continue
    f,_,frag=href.partition("#")
    target = page if f=="" else os.path.normpath(os.path.join(base,f))
    if f and not os.path.exists(target): bad.append(("MISSING FILE",href)); continue
    if frag:
        tp = parse(target) if target!=page else p
        if frag not in tp.ids: bad.append(("MISSING ID",href))
    print("OK" if True else "", href, "->", os.path.relpath(target,root), "#"+frag if frag else "")
for s in p.srcs:
    if s and not s.startswith(("http","data:","#")):
        t=os.path.normpath(os.path.join(base,s.split("#")[0]))
        if not os.path.exists(t): bad.append(("MISSING SRC",s))
print("BAD:", bad)
