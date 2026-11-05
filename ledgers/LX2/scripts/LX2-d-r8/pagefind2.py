import re, sys
def load(path, kind):
    raw = open(path, encoding='utf-8', errors='replace').read()
    out = []
    for idx, chunk in enumerate(raw.split('\x0c')):
        lines = [l for l in chunk.split('\n') if l.strip()]
        num = '?'
        for l in lines[:4]:
            if kind == 'ohagan':
                m = re.search(r'^\s*(\d{3})\s+UNITED STATES', l) or re.search(r'Cite as: 521 U\. S\. 642 \(1997\)\s+(\d{3})\s*$', l)
            else:
                m = re.search(r'^\s*(\d{3})\s+OCTOBER TERM|^\s*(\d{3})\s+Opinion of the Court|Opinion of the Court\s+(\d{3})\s*$|^\s*(\d{3})\s+Opinion', l) or re.search(r'463 U\. S\.\s+(\d{3})\s*$', l)
            if m:
                num = next(g for g in m.groups() if g) if m.lastindex else m.group(1)
                break
        flat = re.sub(r'(\w)- (\w)', r'\1\2', chunk)
        flat = re.sub(r'\s+', ' ', flat).replace('’', "'").replace('‘', "'")
        flat = flat.replace('“', '"').replace('”', '"')
        out.append((idx, num, flat))
    return out
if __name__ == '__main__':
    path, kind = sys.argv[1], sys.argv[2]
    pgs = load(path, kind)
    print('chunks', len(pgs), 'with page number', sum(1 for _, n, _ in pgs if n != '?'))
    for ph in sys.argv[3:]:
        ph2 = ph.replace('’', "'").replace('“', '"').replace('”', '"')
        hits = [(idx, n) for idx, n, flat in pgs if ph2 in flat]
        print(hits if hits else 'NOT FOUND', '<-', ph[:90])
