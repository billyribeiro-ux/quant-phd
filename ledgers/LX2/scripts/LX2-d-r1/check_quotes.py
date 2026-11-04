import re, json, sys
sys.path.insert(0, '/tmp/lx2d-src')
from norm import *
src = {
 'COMPS-1884': norm(load_pdf_txt('/tmp/lx2d-src/COMPS-1884.txt')),
 'COMPS-1885': norm(load_pdf_txt('/tmp/lx2d-src/COMPS-1885.txt')),
 'USREPORTS-463-646': norm(load_pdf_txt('/tmp/lx2d-src/USREPORTS-463-646.txt')),
 'USREPORTS-521-642': norm(load_pdf_txt('/tmp/lx2d-src/USREPORTS-521-642.txt')),
 'sr2602a1': norm(load_pdf_txt('/tmp/lx2d-src/att.txt')),
 'sr2602': norm(load_pdf_txt('/tmp/lx2d-src/letter.txt')),
 'cfa-standards-iii-a': norm(load_html_txt('/tmp/lx2d-src/cfa-standards-of-practice-iii-a.html')),
 'cfa-standards-vi-a': norm(load_html_txt('/tmp/lx2d-src/cfa-standards-of-practice-vi-a.html')),
}
cards = json.load(open('/Users/billyribeiro/.fanout/wt/verifyE1-LX2-d/course/modules/LX/LX2/cards.json'))
for c in cards:
    text = c['back'] + ' ' + c['front']
    quotes = re.findall(r'“([^”]+)”', text)
    for q in quotes:
        qn = norm(q).strip(' .,;:')
        # strip bracket editing marks like [A] and [s]
        qn2 = re.sub(r'\[[a-zA-Z]\]', '', qn)
        pieces = [p.strip(' .,;:') for p in re.split(r'\.\.\.|…', qn2) if p.strip(' .,;:')]
        found = [k for k, v in src.items() if all(p in v for p in pieces)]
        status = 'FOUND in ' + ','.join(found) if found else 'NOT FOUND in any source'
        print(c['id'], status, '|', q[:110])
