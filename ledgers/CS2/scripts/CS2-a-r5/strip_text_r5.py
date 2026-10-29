import sys
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.out=[]; self.skip=0
    def handle_starttag(self,t,a):
        if t in('script','style'): self.skip+=1
        if t in('p','li','h1','h2','h3','h4','tr','div','section','pre','details','summary','ol','ul','table','blockquote'): self.out.append('\n')
    def handle_endtag(self,t):
        if t in('script','style'): self.skip-=1
        if t in('p','li','h1','h2','h3','h4','tr','div','section','pre','details','summary'): self.out.append('\n')
    def handle_data(self,d):
        if not self.skip: self.out.append(d)
p=P(); p.feed(open(sys.argv[1],encoding='utf-8').read()); import re
print(re.sub(r'\n\s*\n+','\n',''.join(p.out)))
