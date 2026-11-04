import html, re, sys
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.out=[]; self.skip=0
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style'): self.skip+=1
        if tag in ('p','li','h1','h2','h3','h4','dt','dd','tr','pre','div','section','br','table'):
            self.out.append('\n')
        if tag=='li': self.out.append('- ')
        if tag=='section':
            a=dict(attrs); self.out.append('\n[section '+(a.get('id') or '')+']\n')
    def handle_endtag(self,tag):
        if tag in ('script','style'): self.skip-=1
    def handle_data(self,d):
        if not self.skip: self.out.append(d)
p=P(); p.feed(open(sys.argv[1],encoding='utf-8').read())
t=''.join(p.out)
t=re.sub(r'[ \t]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t)
print(html.unescape(t))
