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
    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip -= 1
    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)

def dump(path):
    src = open(path, encoding='utf-8').read()
    lines = src.split('\n')
    # emit one text block per source line, keeping the source line number
    for i, line in enumerate(lines, 1):
        p = P()
        p.feed(line)
        t = ' '.join(''.join(p.out).split())
        if t:
            print(f'[{i}] {t}')

if __name__ == '__main__':
    dump(sys.argv[1])
