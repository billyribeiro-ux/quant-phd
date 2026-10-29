import sys, html.parser
class P(html.parser.HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.out=[]; s.skip=0; s.pre=0
    def handle_starttag(s,tag,attrs):
        if tag in('script','style'): s.skip+=1
        if tag=='pre': s.pre+=1; s.out.append('\n[PRE] ')
        if tag in('p','li','h1','h2','h3','h4','tr','div','section','pre','dt','dd'): s.out.append('\n')
    def handle_endtag(s,tag):
        if tag in('script','style'): s.skip-=1
        if tag=='pre': s.pre-=1
    def handle_data(s,d):
        if not s.skip: s.out.append(d)
p=P(); p.feed(open(sys.argv[1],encoding='utf8').read())
txt=''.join(p.out)
print('\n'.join(l.strip() for l in txt.split('\n') if l.strip()))
