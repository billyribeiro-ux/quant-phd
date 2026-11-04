"""Recompute every Part A row of L03 Lab 1 (both economies) and compare with the page's expected block.

Independent of the twin: uses Fractions and its own half-up rounding. Usage: python -I l03_partA_rows.py <checkout>
"""
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
from pathlib import Path

checkout = Path(sys.argv[1])
page = (checkout / "course/modules/LX/LX1/L03.html").read_text(encoding="utf-8")
expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)
lines = expected.replace("&lt;", "<").replace("&gt;", ">").splitlines()

def hu(x: F, places: int) -> str:
    d = Decimal(x.numerator) / Decimal(x.denominator)
    return str(d.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))

D, N0, DEL, H = F(1_000_000), F(4_000_000), F(1, 50), 12
def row(m: int, t: int) -> str:
    P = (1 - DEL) ** min(t, m); V = D / P; N = N0 - (V - D); L = V / N
    L0 = D / N0; psi = L - L0
    return (f"  t = {t:2d}: index {hu(P, 4)}; real debt {hu(V, 0)} cents; leverage {hu(L, 4)}; "
            f"premium {hu(psi, 4)}; output fall {hu(100 * psi, 2)} percent")
bad = 0; checked = 0
exp_lines = [l for l in lines if l.startswith("  t =")]
mine = [row(12, t) for t in range(13)] + [row(4, t) for t in range(13)]
for a, b in zip(exp_lines, mine):
    checked += 1
    if a != b:
        bad += 1
        print("MISMATCH\n expected:", a, "\n mine:    ", b)
print("rows compared:", checked, "of expected", len(exp_lines), "mismatches:", bad)
print("hu(0.25,4)", hu(F(1,4),4), "hu(0.0269,...)", hu(F(1,1),0))
