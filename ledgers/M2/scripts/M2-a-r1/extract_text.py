import sys, html.parser, re
class P(html.parser.HTMLParser):
    def __init__(s):
        super().__init__(); s.out=[]; s.skip=0
    def handle_starttag(s,t,a):
        if t in('script','style','svg'): s.skip+=1
        if t in('p','li','h1','h2','h3','h4','tr','div','section','details','summary','table','dt','dd','pre','figcaption','td','th'): s.out.append('\n')
        if t in ('script','style','svg') : return
        if s.skip==0:
            ids=[v for k,v in a if k in('id','data-concept','href','data-hours-lessons','data-hours-project','data-skill','data-locator','data-key','class')]
            attrs=' '.join(f'{k}={v}' for k,v in a if k in('id','href','data-concept','data-locator','data-hours-lessons','data-hours-project','class','data-status','data-files'))
            if attrs and t in('a','section','main','dfn','span','p','div','table','tr','cite','dl','ol','ul','li','figure','details','code','pre'): s.out.append(f' [<{t} {attrs}>] ')
    def handle_endtag(s,t):
        if t in('script','style','svg'): s.skip=max(0,s.skip-1)
    def handle_data(s,d):
        if s.skip==0: s.out.append(d)
p=P(); p.feed(open(sys.argv[1],encoding='utf-8').read())
t=''.join(p.out)
t=re.sub(r'\n\s*\n+','\n',t)
print(t)
