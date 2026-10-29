import sys, re, html
from html.parser import HTMLParser
BLOCK = {'p','div','li','h1','h2','h3','h4','tr','section','ul','ol','table','details','summary','pre','header','blockquote','dt','dd','figure','figcaption','caption'}
class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.out=[]; self.skip=0; self.lineno=1
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag in ('script','style'): self.skip+=1; return
        if tag in BLOCK: self.out.append('\n')
        if tag=='span' and 'grade' in (a.get('class') or ''): self.out.append(f"[GRADE {a.get('data-grade')}]")
        if tag=='a' and a.get('data-cite'): self.out.append(f"[CITE {a['data-cite']}]")
        if tag=='a' and a.get('data-concept'): self.out.append(f"[CONCEPT {a['data-concept']}]")
        if tag=='dfn': self.out.append(f"[DFN {a.get('data-concept') or '-'}]")
        if tag=='br': self.out.append('\n')
        if tag=='td' or tag=='th': self.out.append(' | ')
    def handle_endtag(self, tag):
        if tag in ('script','style'): self.skip-=1; return
        if tag in BLOCK: self.out.append('\n')
    def handle_data(self, d):
        if self.skip: return
        self.out.append(d)
p=P(); p.feed(open(sys.argv[1],encoding='utf-8').read())
txt=''.join(p.out)
txt=re.sub(r'[ \t\r\f\v]+',' ',txt)
txt=re.sub(r'\n\s*\n+','\n',txt)
sys.stdout.write(txt)
