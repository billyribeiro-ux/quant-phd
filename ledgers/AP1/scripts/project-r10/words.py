import html, re
from html.parser import HTMLParser
src = open("/tmp/verify-ap1-r10-m/course/modules/AP/AP1/project.html", encoding="utf-8").read()
class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack=[]; self.blocks=[]; self.cur=None; self.in_ex=None
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=="article" and a.get("class")=="exemplar": self.in_ex=a["id"]
        if tag=="p" and self.in_ex: self.cur=[]; self.pcls=a.get("class")
        if tag=="aside": self.skip=True
        if tag=="h5" and self.in_ex: self.cur_h5=[]
    def handle_endtag(self, tag):
        if tag=="aside": self.skip=False
        if tag=="p" and self.cur is not None and self.in_ex:
            self.blocks.append((self.in_ex, self.heading, "".join(self.cur))); self.cur=None
        if tag=="h5" and self.in_ex and getattr(self,"cur_h5",None) is not None:
            self.heading="".join(self.cur_h5); self.cur_h5=None
    def handle_data(self, d):
        if getattr(self,"cur_h5",None) is not None: self.cur_h5.append(d)
        if self.cur is not None and not getattr(self,"skip",False): self.cur.append(d)
p=P(); p.heading=""; p.feed(src)
for ex in ("exemplar-a","exemplar-b"):
    tot=0; rows=[]
    for e,h,t in p.blocks:
        if e!=ex or h.startswith("Appendix"): continue
        n=len(html.unescape(t).split()); tot+=n; rows.append((h,n))
    print(ex, rows, "total", tot)
