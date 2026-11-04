import html.parser, re, sys
class T(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.p=[]
    def handle_data(self, d): self.p.append(d)
src=open(sys.argv[1],encoding='utf-8').read()
for ident in ("exemplar-a","exemplar-b"):
    s=src.index(f'<article class="exemplar" id="{ident}"'); e=src.index('</article>',s)
    chunk=src[s:e]
    memos=re.findall(r'<div class="memo-text">(.*?)</div>', chunk, flags=re.S)
    tot=0
    for i,m in enumerate(memos):
        t=T(); t.feed(m); txt="".join(t.p)
        n_space=len([w for w in txt.split(" ") if w])
        n_ws=len(txt.split())
        tot+=n_space
        print(ident, "passage", i, "words(split ' ')", n_space, "words(split ws)", n_ws)
    print(ident, "TOTAL memo words split ' ':", tot, "| memo divs:", len(memos))
