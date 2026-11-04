import re, sys
sys.path.insert(0, '/tmp/lx2d-src')
from norm import load_pdf_txt
def pagemap(path, hdr):
    lines = load_pdf_txt(path).split('\n')
    cur = None; out = []
    for i, ln in enumerate(lines):
        m = re.match(r'^\s*(\d{3})\s+OCTOBER TERM', ln) or re.match(r'^\s*DIRKS v\. SEC\s+(\d{3})\s*$', ln) or re.match(r'^\s*O\'?HAGAN.*?\s+(\d{3})\s*$', ln)
        if m:
            cur = int(m.group(1))
        out.append((i, cur, ln))
    return out
def find(path, phrase, hdr=None):
    res = []
    for i, cur, ln in pagemap(path, hdr):
        if re.search(phrase, re.sub(r'\s+', ' ', ln), re.I):
            res.append((i, cur, ln.strip()[:120]))
    return res
