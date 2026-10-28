import sys, pathlib, re
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s): super().__init__(); s.out=[]; s.skip=0
    def handle_starttag(s,tag,attrs):
        if tag in ('script','style'): s.skip+=1
        if tag in ('p','li','h1','h2','h3','h4','tr','div','section','pre','dt','dd','br'): s.out.append('\n')
    def handle_endtag(s,tag):
        if tag in ('script','style'): s.skip-=1
    def handle_data(s,d):
        if not s.skip: s.out.append(d)
src=pathlib.Path(sys.argv[1]).read_text()
p=P(); p.feed(src)
txt=''.join(p.out)
txt=re.sub(r'\n\s*\n+','\n',txt)
pathlib.Path(sys.argv[2]).write_text(txt)
print(sys.argv[2], len(txt))
