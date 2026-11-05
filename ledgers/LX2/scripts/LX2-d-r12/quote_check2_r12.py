"""Lenient quotation check: strips brackets, section signs, dashes and all non-alphanumerics before matching.
Used only for the NOT FOUND rows of quote_check_r12.py (bracketed alterations, footnote and page-break artifacts)."""
import re, sys
sys.argv = sys.argv[:1] + sys.argv[1:]
exec(open(sys.argv[1]).read().split("if __name__ == '__main__':")[0]) if False else None
import importlib.util
spec = importlib.util.spec_from_file_location('q1', '/Users/billyribeiro/.fanout/wt/verifyE12-LX2-d/ledgers/LX2/scripts/LX2-d-r12/quote_check_r12.py')
q1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(q1)
def strip(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())
S = {k: strip(v) for k, v in q1.sources.items()}
for mode in ['lessons', 'cards']:
    pass
import json
out = []
for L, keys in [('L01', ['1884', '1885']), ('L02', ['dirks', 'ohagan']), ('L03', []), ('L04', ['srh', 'sr', 'cfa3', 'cfa6a'])]:
    t = open(f'course/modules/LX/LX2/{L}.html', encoding='utf-8').read()
    for m in re.finditer(r'<span class="claim"[^>]*data-cite="([^"]*)"[^>]*>(.*?)</span>', t, re.S):
        body = re.sub(r'<[^>]+>', ' ', m.group(2))
        for q in re.findall(r'“([^”]{6,})”', body):
            nq = strip(q)
            allk = keys or ['1884', '1885', 'dirks', 'ohagan', 'sr', 'srh', 'cfa3', 'cfa6a']
            hit = [k for k in allk if nq in S[k]]
            print(('FOUND' if hit else 'NOT FOUND'), f'[{L} cite={m.group(1)}]', hit, '::', q[:120])
cards = json.load(open('course/modules/LX/LX2/cards.json', encoding='utf-8'))
for c in cards:
    for q in re.findall(r'“([^”]{6,})”', c['back'] + ' ' + c['front']):
        nq = strip(q)
        hit = [k for k in ['1884', '1885', 'dirks', 'ohagan', 'sr', 'srh', 'cfa3', 'cfa6a'] if nq in S[k]]
        print(('FOUND' if hit else 'NOT FOUND'), f'[{c["id"]}]', hit, '::', q[:120])
