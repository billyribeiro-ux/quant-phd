import sys, re, html
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.out=[]; self.skip=0
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style'): self.skip+=1
        if tag in ('p','li','tr','h1','h2','h3','h4','pre','div','section','br','td','th'): self.out.append('\n')
        if tag=='td' or tag=='th': self.out.append(' | ')
    def handle_endtag(self, tag):
        if tag in ('script','style'): self.skip-=1
    def handle_data(self, d):
        if not self.skip: self.out.append(d)
p=P(); p.feed(open(sys.argv[1], encoding='utf-8').read())
txt=''.join(p.out)
txt=re.sub(r'\n\s*\n+', '\n', txt)
print(txt)
