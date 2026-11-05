"""Statute and opinion locator checks for LX2 (round 12). Sources: the GovInfo COMPS-1884/1885 text and the
Supreme Court and SR 26-2 texts kept in the round-11 scratch directory; their sha256 is printed first."""
import re, hashlib
SRC = '/Users/billyribeiro/.fanout/scratch-LX2-d-r11/src/'
for f in ['COMPS-1884.pdf', 'COMPS-1885.pdf']:
    print(f, hashlib.sha256(open(SRC + f, 'rb').read()).hexdigest())
t1 = re.sub(r'\s+', ' ', open(SRC + 'c1884.norm.txt', encoding='utf-8', errors='replace').read())
t2 = re.sub(r'\s+', ' ', open(SRC + 'c1885.norm.txt', encoding='utf-8', errors='replace').read())
def show(label, text, pat, n=420):
    m = re.search(pat, text)
    print(f'[{label}]', (text[m.start():m.start() + n] if m else 'NOT FOUND'))
    print()
show('1933 s2(a)(8) registration statement', t1, r'\(8\) The term ‘‘registration statement')
show('1933 s2(a)(5) Commission', t1, r'\(5\) The term ‘‘Commission')
show('1933 s2 defines "in effect"?', t1[t1.find('DEFINITIONS SEC. 2'):t1.find('SEC. 3.')], r'in effect', 80)
show('1933 s8(b)', t1, r'\(b\) If it appears to the Commission that a registration', 380)
show('1933 s8(d) (round-12 L01 wording)', t1, r'\(d\) If it appears to the Commission at any time', 470)
show('1933 s8(e)', t1, r'\(e\) The Commission is hereby empowered', 200)
show('1933 s2(a)(19) EGC', t1, r'\(19\) The term ‘‘emerging growth company', 160)
show('1934 s15(d)(1) third sentence (bank clause)', t2, r'shall also be automatically suspended as to any fiscal year', 520)
