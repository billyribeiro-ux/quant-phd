import sys
from html.parser import HTMLParser
src = open(sys.argv[1], encoding='utf-8').read().split('\n')
BLOCK = {'h1','h2','h3','h4','h5','h6','p','li','ul','ol','div','br','tr','td','th','section','article','aside','table','dd','dt','pre'}
class Memo(HTMLParser):
    def __init__(self, sep_blocks):
        super().__init__(convert_charrefs=True)
        self.depth = 0; self.stack = []; self.out = []; self.sep = sep_blocks; self.active = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'div' and d.get('class') == 'memo-text':
            self.active.append(len(self.stack))
        self.stack.append(tag)
        if self.sep and tag in BLOCK and self.active: self.out.append(' ')
    def handle_endtag(self, tag):
        # pop to matching tag
        while self.stack:
            t = self.stack.pop()
            if self.sep and t in BLOCK and self.active: self.out.append(' ')
            if t == tag: break
        if self.active and len(self.stack) == self.active[-1]:
            self.active.pop(); self.out.append(' ')
    def handle_data(self, data):
        if self.active: self.out.append(data)
def count(lines_from, lines_to, sep):
    p = Memo(sep)
    p.feed('\n'.join(src[lines_from-1:lines_to]))
    text = ''.join(p.out)
    return len(text.split()), text
for name, a, b in [('A',650,702),('B',703,766)]:
    n0, t0 = count(a,b,False); n1, t1 = count(a,b,True)
    print(name, 'no-separator words:', n0, '| block-separated words:', n1)
    if name=='B':
        print('contains raw <gamma text:', '0<\\gamma<1' in t0 or '<\\gamma' in t0)
        open('/tmp/e3d-r1-wc/B_text.txt','w').write(t1)
        open('/tmp/e3d-r1-wc/A_text.txt','w').write(count(650,702,True)[1])
