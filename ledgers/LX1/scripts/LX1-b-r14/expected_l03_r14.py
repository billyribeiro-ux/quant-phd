"""Round 14: programmatic check of the L03 expected block (page lines 327-382) against exact Fraction values. Run: python -I expected_l03_r14.py <checkout>"""
import re
import sys
from fractions import Fraction
import math

ROOT = sys.argv[1]
s = open(f"{ROOT}/course/modules/LX/LX1/L03.html", encoding="utf-8").read()
exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', s, re.S).group(1)
exp = exp.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
lines = exp.splitlines()


def rhu(x):
    return math.floor(x + Fraction(1, 2))


def fd(x, places):
    scaled = rhu(x * 10**places)
    whole, frac = divmod(scaled, 10**places)
    return f"{whole}.{frac:0{places}d}"


D, A0, H, delta = 1_000_000, 4_000_000, 12, Fraction(1, 50)
bad = 0
checked = 0


def block(m):
    out = []
    for t in range(H + 1):
        P = (1 - delta) ** min(t, m)
        V = Fraction(D) / P
        A = A0 - (V - D)
        L = V / A
        psi = L - Fraction(D) / A0
        fall = psi
        out.append(f"  t = {t:2d}: index {fd(P, 4)}; real debt {rhu(V)} cents; leverage {fd(L, 4)}; premium {fd(psi, 4)}; output fall {fd(100 * fall, 2)} percent")
    return out


for label, m in (("X", 12), ("Y", 4)):
    header = f"economy {label}, parity held for {m} of {H} periods:"
    i = lines.index(header)
    expected_rows = lines[i + 1 : i + 1 + H + 1]
    for e, a in zip(expected_rows, block(m)):
        checked += 1
        if e != a:
            bad += 1
            print("MISMATCH", label, repr(e), repr(a))
print("rows checked", checked, "mismatches", bad)
print("baseline line:", lines[2], "| expected:", fd(Fraction(D) / Fraction(A0), 4))
sys.exit(0 if bad == 0 else 1)
