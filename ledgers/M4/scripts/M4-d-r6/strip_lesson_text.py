import sys, html, re
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.out=[]; self.skip=0
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style'): self.skip+=1
        if tag in ('p','li','h1','h2','h3','h4','h5','tr','dt','dd','pre','div','section','figcaption'): self.out.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script','style'): self.skip-=1
    def handle_data(self, d):
        if not self.skip: self.out.append(d)
src=open(sys.argv[1],encoding='utf-8').read()
p=P(); p.feed(src)
txt=''.join(p.out)
txt=re.sub(r'[ \t]+',' ',txt); txt=re.sub(r'\n\s*\n+','\n',txt)
open(sys.argv[2],'w',encoding='utf-8').write(txt)
