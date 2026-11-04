"""Independent exact recomputation of every Part A row of the L03 lab (verifier round 5).

Compares each printed row (index, real debt, leverage, premium, output fall) with the expected block on the page.
Uses fractions.Fraction and its own half-up rounding; does not import the twin.
Run with: python3 -I l03_partA_r5.py <checkout>
"""

from __future__ import annotations

import math
import re
import sys
from fractions import Fraction
from pathlib import Path

root = Path(sys.argv[1])
text = (root / "course/modules/LX/LX1/L03.html").read_text(encoding="utf-8")
expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1)
expected = expected.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").split("\n")

D, N0, H = 1_000_000, 4_000_000, 12
d = Fraction(1, 50)


def half_up(x: Fraction, places: int) -> str:
    n = math.floor(x * 10**places + Fraction(1, 2))
    whole, frac = divmod(n, 10**places)
    return f"{whole}.{frac:0{places}d}"


def row(m: int, t: int) -> str:
    P = (1 - d) ** min(t, m)
    V = Fraction(D) / P
    Nt = Fraction(N0) - (V - D)
    L = V / Nt
    L0 = Fraction(D, N0)
    psi = L - L0
    f = psi
    return (f"  t = {t:2d}: index {half_up(P, 4)}; real debt {math.floor(V + Fraction(1, 2))} cents; "
            f"leverage {half_up(L, 4)}; premium {half_up(psi, 4)}; output fall {half_up(100 * f, 2)} percent")


mismatch = 0
rows_checked = 0
blocks = {"economy X, parity held for 12 of 12 periods:": 12, "economy Y, parity held for 4 of 12 periods:": 4}
for header, m in blocks.items():
    i = expected.index(header)
    for t in range(H + 1):
        got = expected[i + 1 + t]
        want = row(m, t)
        rows_checked += 1
        if got != want:
            mismatch += 1
            print("MISMATCH", header, t, repr(got), repr(want))
print("Part A rows checked:", rows_checked, "mismatches:", mismatch)
print("baseline line:", expected[2], "| recomputed leverage L0:", half_up(Fraction(D, N0), 4))
