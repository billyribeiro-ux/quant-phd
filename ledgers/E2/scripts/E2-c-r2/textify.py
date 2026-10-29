import sys, html.parser
class P(html.parser.HTMLParser):
    def __init__(s):
        super().__init__(); s.out=[]; s.skip=0
    def handle_starttag(s,t,a):
        if t in('script','style'): s.skip+=1
        if t in('p','li','h1','h2','h3','h4','tr','div','section','pre','dt','dd','br','figcaption','summary'): s.out.append('\n')
        if t=='tr': pass
    def handle_endtag(s,t):
        if t in('script','style'): s.skip-=1
    def handle_data(s,d):
        if not s.skip: s.out.append(d)
p=P(); p.feed(open(sys.argv[1],encoding='utf-8').read())
import re
txt=''.join(p.out)
txt=re.sub(r'\n\s*\n+','\n',txt)
print(txt)
