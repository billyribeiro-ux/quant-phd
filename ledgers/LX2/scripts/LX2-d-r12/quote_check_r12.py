"""Check every quoted passage in LX2 lesson claim spans and cards against the scratch source text.

Sources: COMPS-1884 (1933 Act), COMPS-1885 (1934 Act) normalised text, dirks/ohagan normalised text,
cfa normalised text, SR 26-2 attachment text. Prints FOUND / NOT FOUND per quote.
"""
import re, sys, html, json, unicodedata
SRC = '/Users/billyribeiro/.fanout/scratch-LX2-d-r11/src/'
def norm(s):
    s = html.unescape(s)
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    s = s.replace('–', '-').replace('—', '-').replace('−', '-').replace(' ', ' ')
    s = re.sub(r'[­]', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s.lower()
sources = {}
for key, fn in [('1884', 'c1884.norm.txt'), ('1885', 'c1885.norm.txt'), ('dirks', 'dirks.norm.txt'), ('ohagan', 'ohagan.norm.txt'), ('cfa3', 'cfa-iii-a.norm.txt'), ('cfa6a', 'cfa-vi-a.norm.txt')]:
    sources[key] = norm(open(SRC + fn, encoding='utf-8', errors='replace').read())
sr = open(SRC + 'sr2602a1.txt', encoding='utf-8', errors='replace').read()
sources['sr'] = norm(sr)
srh = open(SRC + 'sr2602.htm', encoding='utf-8', errors='replace').read()
sources['srh'] = norm(re.sub(r'<[^>]+>', ' ', srh))
def find_quotes(text):
    return re.findall(r'“([^”]{6,})”', text)
def check(label, text, srckeys):
    qs = find_quotes(text)
    for q in qs:
        nq = norm(q).strip(' ,.;:')
        hit = [k for k in srckeys if nq in sources[k]]
        status = 'FOUND' if hit else 'NOT FOUND'
        print(f"{status:9} [{label}] {hit or ''} :: {q[:160]}")
if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'lessons':
        for L, keys in [('L01', ['1884', '1885']), ('L02', ['dirks', 'ohagan']), ('L03', []), ('L04', ['srh', 'sr', 'cfa3', 'cfa6a'])]:
            t = open(f'course/modules/LX/LX2/{L}.html', encoding='utf-8').read()
            # keep only text inside claim spans that cite a source key
            for m in re.finditer(r'<span class="claim"[^>]*data-cite="([^"]*)"[^>]*>(.*?)</span>', t, re.S):
                cite = m.group(1)
                body = re.sub(r'<[^>]+>', ' ', m.group(2))
                check(f'{L} cite={cite}', body, keys if keys else ['1884', '1885', 'dirks', 'ohagan', 'sr', 'srh', 'cfa3', 'cfa6a'])
            # also quotes in <p> or <li> text that are not claim spans
            body_all = re.sub(r'<[^>]+>', ' ', t)
    if mode == 'cards':
        cards = json.load(open('course/modules/LX/LX2/cards.json', encoding='utf-8'))
        for c in cards:
            check(c['id'], c['back'] + ' ' + c['front'], ['1884', '1885', 'dirks', 'ohagan', 'sr', 'srh', 'cfa3', 'cfa6a'])
