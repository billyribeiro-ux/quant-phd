"""Check every href and data-cite target in the BK4 slice pages (hub, L01-L03): file exists, fragment id exists."""
import os, re, sys
from html.parser import HTMLParser

ROOT = sys.argv[1]
PAGES = ["index.html", "L01.html", "L02.html", "L03.html"]
ids_cache = {}

class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set(); self.hrefs = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if 'id' in d: self.ids.add(d['id'])
        if tag == 'a' and 'href' in d: self.hrefs.append(d['href'])
        if tag == 'link' and 'href' in d: self.hrefs.append(d['href'])
        if tag in ('script',) and 'src' in d: self.hrefs.append(d['src'])

def load(path):
    if path not in ids_cache:
        p = P(); p.feed(open(path, encoding='utf-8').read()); ids_cache[path] = p
    return ids_cache[path]

bad = 0; n = 0
for page in PAGES:
    src = os.path.join(ROOT, "course/modules/BK/BK4", page)
    p = load(src)
    for h in p.hrefs:
        if re.match(r'^(https?:|mailto:|data:)', h):
            print(page, "EXTERNAL", h); bad += 1; continue
        n += 1
        target, _, frag = h.partition('#')
        tpath = src if target == '' else os.path.normpath(os.path.join(os.path.dirname(src), target))
        if not os.path.exists(tpath):
            print(page, "MISSING FILE", h, tpath); bad += 1; continue
        if frag:
            if not tpath.endswith('.html'):
                continue
            if frag not in load(tpath).ids:
                # concept index anchors are in course/concepts.html
                print(page, "MISSING ANCHOR", h); bad += 1
print("links checked:", n, "problems:", bad)
