import html, re, sys
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.out=[]; self.skip=0
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style'): self.skip+=1
        if tag in ('p','li','h1','h2','h3','h4','dt','dd','tr','pre','section','div','table','ul','ol','dl','br'): self.out.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script','style'): self.skip-=1
        if tag in ('p','li','h1','h2','h3','h4','dt','dd','tr','pre','section','div','table','ul','ol','dl'): self.out.append('\n')
    def handle_data(self, d):
        if not self.skip: self.out.append(d)
src = open(sys.argv[1], encoding='utf-8').read()
p = P(); p.feed(src)
txt = ''.join(p.out)
lines = [re.sub(r'[ \t]+',' ',l).strip() for l in txt.split('\n')]
lines = [l for l in lines if l]
print('\n'.join(html.unescape(l) for l in lines))
