import sys, re, html
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.out=[]; s.skip=0
    def handle_starttag(s,tag,attrs):
        if tag in ('script','style'): s.skip+=1
        if tag in ('p','li','h2','h3','tr','div','pre','section','dt','dd','figcaption','summary','br'): s.out.append('\n')
        if tag=='td' or tag=='th': s.out.append(' | ')
        a=dict(attrs)
        if a.get('id'): s.out.append('[#%s]'%a['id'])
    def handle_endtag(s,tag):
        if tag in ('script','style'): s.skip-=1
    def handle_data(s,d):
        if not s.skip: s.out.append(d)
p=P(); p.feed(open(sys.argv[1],encoding='utf-8').read())
t=''.join(p.out)
t=re.sub(r'[ \t]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t)
sys.stdout.write(t)
