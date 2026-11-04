import sys, html
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0
        self.pre = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('script', 'style', 'svg', 'head'):
            self.skip += 1
            return
        if tag == 'pre':
            self.pre += 1
            self.out.append('\n[PRE]\n')
        if tag in ('p', 'li', 'h1', 'h2', 'h3', 'h4', 'tr', 'div', 'section', 'dt', 'dd', 'summary', 'th', 'td', 'figcaption', 'label', 'option', 'br', 'blockquote', 'table', 'ul', 'ol', 'details'):
            self.out.append('\n')
        if tag == 'td' or tag == 'th':
            self.out.append(' | ')
        if tag == 'a' and 'href' in a:
            self.out.append('')
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'svg', 'head'):
            self.skip = max(0, self.skip - 1)
            return
        if tag == 'pre':
            self.pre = max(0, self.pre - 1)
            self.out.append('\n[/PRE]\n')
        if tag in ('p', 'li', 'h1', 'h2', 'h3', 'h4', 'tr', 'div', 'section', 'summary', 'pre', 'table'):
            self.out.append('\n')
    def handle_data(self, data):
        if self.skip:
            return
        self.out.append(data)

src = open(sys.argv[1], encoding='utf-8').read()
p = P()
p.feed(src)
text = ''.join(p.out)
lines = []
for ln in text.split('\n'):
    if ln.strip() == '' and (not lines or lines[-1] == ''):
        continue
    if ln.strip() == '':
        lines.append('')
        continue
    lines.append(ln.rstrip())
print('\n'.join(lines))
