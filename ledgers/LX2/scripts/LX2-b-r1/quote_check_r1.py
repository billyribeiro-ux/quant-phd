# Checks every quoted span inside data-cite claims of a lesson page against the source text fetched with plain curl.
import html, re, sys
from pathlib import Path

FETCH = Path('/tmp/lx2b-r1-fetch')
PAGE = Path(sys.argv[1])
SRC = {
    'cfandcode': ['std_iii-a.txt', 'std_vi-a.txt', 'std_vi-b.txt'],
    'frb2026fed': ['sr2602.txt', 'sr2602_attach.txt'],
}

def norm(s):
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    s = s.replace('—', '-').replace('–', '-')
    return re.sub(r'\s+', ' ', s).strip()

def load(name):
    p = FETCH / name
    return norm(p.read_text(encoding='utf-8', errors='replace')) if p.exists() else None

src_text = {k: [x for x in (load(f) for f in files) if x] for k, files in SRC.items()}
page = PAGE.read_text(encoding='utf-8')
claims = re.findall(r'<span class="claim"([^>]*)>(.*?)</span>', page, flags=re.S)
bad = 0
for attrs, body in claims:
    m = re.search(r'data-cite="([^"]+)"', attrs)
    if not m:
        continue
    cite = m.group(1)
    loc = re.search(r'data-locator="([^"]*)"', attrs)
    raw_text = html.unescape(re.sub(r'<[^>]+>', '', body))
    for q in re.findall(r'“(.*?)”', raw_text):
        qn = norm(q).rstrip('.,;:')
        ok = qn.lower() in ' '.join(src_text.get(cite, [])).lower()
        bad += 0 if ok else 1
        print(('OK  ' if ok else 'MISS'), cite, '|', (loc.group(1) if loc else '')[:70], '|', qn[:90])
print('claims', len(claims), 'missing quotes', bad)
