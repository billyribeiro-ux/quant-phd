import html, re, sys
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip += 1
        if tag in ('p', 'li', 'div', 'h1', 'h2', 'h3', 'h4', 'tr', 'section', 'pre', 'br', 'summary', 'dt', 'dd', 'td', 'th'):
            self.out.append('\n')
        if tag == 'pre':
            self.out.append('\n[PRE]\n')
    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip -= 1
        if tag in ('p', 'li', 'div', 'h1', 'h2', 'h3', 'h4', 'tr', 'section', 'pre'):
            self.out.append('\n')
    def handle_data(self, d):
        if self.skip == 0:
            self.out.append(d)

src = open(sys.argv[1], encoding='utf-8').read()
p = P()
p.feed(src)
txt = ''.join(p.out)
txt = re.sub(r'[ \t]+', ' ', txt)
txt = re.sub(r'\n\s*\n+', '\n', txt)
sys.stdout.write(txt)
