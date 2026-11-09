import sys, re
from html.parser import HTMLParser
BLOCK = {'p','li','div','tr','h1','h2','h3','h4','section','table','ul','ol','dt','dd','figcaption','caption','pre','blockquote','fieldset','label','thead','tbody','th','td'}
class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out=[]; self.skip=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag in ('script','style'): self.skip+=1; return
        if tag in BLOCK: self.out.append('\n')
        if tag=='span' and 'claim' in (a.get('class') or ''):
            self.out.append(' {{CLAIM grade=%s cite=%s loc=%s}} ' % (a.get('data-grade'), a.get('data-cite'), a.get('data-locator')))
        if tag=='a' and a.get('href'): self.out.append('[href:%s]' % a['href'])
        if tag=='h2' or tag=='h1': pass
    def handle_endtag(self, tag):
        if tag in ('script','style'): self.skip-=1; return
        if tag in BLOCK: self.out.append('\n')
    def handle_data(self, d):
        if self.skip: return
        self.out.append(d)
src=open(sys.argv[1],encoding='utf-8').read()
p=P(); p.feed(src)
txt=''.join(p.out)
txt=re.sub(r'[ \t]+',' ',txt)
txt=re.sub(r'\n\s*\n+','\n',txt)
print(txt)
