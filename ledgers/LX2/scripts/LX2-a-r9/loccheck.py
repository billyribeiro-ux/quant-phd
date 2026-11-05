import re, sys, html, subprocess
sys.path.insert(0, '/tmp/lx2a_r9_dl')
from quotecheck import norm
def pages(pdf, offset):
    n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
    out = {}
    for i in range(1, n + 1):
        t = subprocess.run(['pdftotext', '-f', str(i), '-l', str(i), pdf, '-'], capture_output=True, text=True).stdout
        t = t.replace('-\n', '').replace('\n', ' ')
        t = norm(t).replace('*', ' ')
        t = re.sub(r'\s+', ' ', t)
        out[i + offset] = t
    return out
SRC = {'gpo1983dirks': pages('USREPORTS-463-646.pdf', 645), 'gpo1997united': pages('USREPORTS-521-642.pdf', 641)}
def locset(loc):
    s = set()
    for a, b in re.findall(r'pp?\. (\d{3})(?:[-–](\d{3}))?', loc):
        s.add(int(a)); 
        if b: s.update(range(int(a), int(b) + 1))
    for chunk in re.findall(r'(?:,|and) (\d{3})\b', loc):
        s.add(int(chunk))
    return s
text = open(sys.argv[1], encoding='utf-8').read()
for m in re.finditer(r'<span class="claim"[^>]*data-grade="[^"]*" data-cite="([^"]*)" data-locator="([^"]*)"[^>]*>(.*?)</span>', text, re.S):
    cites, loc, body = m.group(1).split(), html.unescape(m.group(2)), re.sub(r'<[^>]+>', '', m.group(3))
    quotes = re.findall(r'“([^”]{15,})”', body)
    cited = [c for c in cites if c in SRC]
    if not quotes or not cited: continue
    L = locset(loc)
    if not L: 
        print('NOLOC', loc, '|', body[:60]); continue
    for q in quotes:
        qn = norm(q).strip(' .,;:').replace("'", "'")
        pieces = [p.strip(' .,;:') for p in re.split(r'\[[^\]]*\]|\.\.\.|…', qn) if len(p.split()) >= 5]
        if not pieces: continue
        found = set()
        for c in cited:
            for pg, tx in SRC[c].items():
                if all(p.replace("‘", "'").replace("’", "'") in tx.replace("‘", "'").replace("’", "'") for p in pieces[:1]):
                    found.add(pg)
        ok = bool(found & L)
        print('OK ' if ok else 'CHK', cited, loc, 'found_pages=', sorted(found), '|', qn[:60])
