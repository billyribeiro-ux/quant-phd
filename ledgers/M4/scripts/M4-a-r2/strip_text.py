import sys, html, re
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.out=[]; s.skip=0
    def handle_starttag(s,tag,attrs):
        if tag in ('script','style'): s.skip+=1
        if tag in ('p','li','h1','h2','h3','tr','div','section','pre','summary','td','th','footer','details'):
            s.out.append('\n')
        a=dict(attrs)
        if tag=='section' or tag=='div' and 'class' in a: s.out.append(f"\n[{tag} {a.get('id','')} {a.get('class','')} {a.get('data-locator','')}]")
    def handle_endtag(s,tag):
        if tag in ('script','style'): s.skip-=1
    def handle_data(s,d):
        if not s.skip: s.out.append(d)
p=P(); p.feed(open(sys.argv[1],encoding='utf-8').read())
t=''.join(p.out)
t=re.sub(r'[ \t]+',' ',t)
t=re.sub(r'\n\s*\n+','\n',t)
print(t)
