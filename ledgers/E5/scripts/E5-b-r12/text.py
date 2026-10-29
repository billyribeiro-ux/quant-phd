import sys, html
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.out=[]; s.skip=0
    def handle_starttag(s,t,a):
        if t in('script','style'): s.skip+=1
        if t in('p','li','h1','h2','h3','h4','div','tr','pre','details','summary','dt','dd','section'): s.out.append('\n')
    def handle_endtag(s,t):
        if t in('script','style'): s.skip-=1
    def handle_data(s,d):
        if not s.skip: s.out.append(d)
p=P(); p.feed(open(sys.argv[1],encoding='utf-8').read())
import re
txt=''.join(p.out)
txt=html.unescape(txt)
txt=re.sub(r'\n\s*\n+','\n',txt)
print(txt)
