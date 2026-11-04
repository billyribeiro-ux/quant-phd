"""Independent Part A rows for L03 (exact Fractions, own rounding). Usage: python -I l03_partA_r4.py <L03.html>"""
import math, re, sys
from fractions import Fraction
D, N0, delta, H = 1_000_000, 4_000_000, Fraction(1, 50), 12
def rnd(x, p):
    return Fraction(math.floor(x * 10**p + Fraction(1, 2)), 10**p)
def fmt(x, p):
    v = rnd(x, p); w, f = divmod(int(v * 10**p), 10**p); return f"{w}.{f:0{p}d}"
C = N0 + D
def lev(v): return v / (C - v)
L0 = lev(Fraction(D))
rows = []
for label, m in (("X", 12), ("Y", 4)):
    for t in range(H + 1):
        P = (1 - delta) ** min(t, m)
        V = Fraction(D) / P
        L = lev(V)
        psi = L - L0
        f = psi
        rows.append(f"  t = {t:2d}: index {fmt(P,4)}; real debt {int(rnd(V,0))} cents; leverage {fmt(L,4)}; premium {fmt(psi,4)}; output fall {fmt(100*f,2)} percent")
text = open(sys.argv[1], encoding="utf-8").read()
exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1)
exp = exp.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
exp_lines = [l for l in exp.splitlines() if l.startswith("  t =")]
print("expected t-rows", len(exp_lines), "my rows", len(rows))
mism = [(a, b) for a, b in zip(exp_lines, rows) if a != b]
print("mismatches", len(mism))
for a, b in mism[:5]: print(" exp", a, "\n mine", b)
print("baseline leverage", fmt(L0, 4))
