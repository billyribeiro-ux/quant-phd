import sys, re
from html.parser import HTMLParser
BLOCK=('p','li','h1','h2','h3','h4','tr','pre','div','section','summary','table','ul','ol','details','dt','dd')
class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out=[]; self.skip=0
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style'): self.skip+=1
        if tag in BLOCK: self.out.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script','style'): self.skip-=1
        if tag in BLOCK: self.out.append('\n')
    def handle_data(self, d):
        if self.skip==0: self.out.append(d)
p=P(); p.feed(open(sys.argv[1],encoding='utf-8').read())
t=''.join(p.out)
t=re.sub(r'[ \t]+',' ',t)
t=re.sub(r'\n\s*\n+','\n',t)
print(t)
