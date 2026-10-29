import sys
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.depth=0; self.bad=[]; self.stack=[]
    def handle_starttag(self, tag, attrs):
        if tag=='p': self.stack.append(self.getpos()[0])
    def handle_endtag(self, tag):
        if tag=='p':
            if not self.stack: self.bad.append(('stray </p>', self.getpos()[0]))
            else: self.stack.pop()
for f in sys.argv[1:]:
    p=P(); p.feed(open(f,encoding='utf-8').read())
    print(f, 'stray </p> lines:', [l for k,l in p.bad], 'unclosed <p> starts:', p.stack)
