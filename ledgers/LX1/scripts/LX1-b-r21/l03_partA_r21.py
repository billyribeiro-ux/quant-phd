"""Re-derive every Part A table line of LX1 L03 from the model equations with exact Fractions, and compare with the page."""

from __future__ import annotations

import math
import re
import sys
from fractions import Fraction as F

ROOT = sys.argv[1]
text = open(f"{ROOT}/course/modules/LX/LX1/L03.html", encoding="utf-8").read()
expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1)
lines = expected.splitlines()


def rhu(x: F) -> int:
    return math.floor(x + F(1, 2))


def fixed(x: F, places: int) -> str:
    scaled = rhu(x * 10**places)
    whole, frac = divmod(scaled, 10**places)
    return f"{whole}.{frac:0{places}d}"


D, K0, delta = F(1_000_000), F(4_000_000), F(1, 50)
mismatch = 0
checked = 0
for m, label in ((12, "X"), (4, "Y")):
    for t in range(13):
        P = (1 - delta) ** min(t, m)
        V = D / P
        K = K0 - (V - D)
        L = V / K
        L0 = D / K0
        psi = L - L0
        f = psi
        line = f"  t = {t:2d}: index {fixed(P, 4)}; real debt {rhu(V)} cents; leverage {fixed(L, 4)}; premium {fixed(psi, 4)}; output fall {fixed(100 * f, 2)} percent"
        idx = lines.index(f"economy {label}, parity held for {m} of 12 periods:")
        page = lines[idx + 1 + t]
        checked += 1
        if page != line:
            mismatch += 1
            print("MISMATCH", label, t, "\n page:", page, "\n mine:", line)
print(f"Part A rows checked {checked}, mismatches {mismatch}")
print("baseline line page:", [l for l in lines if l.startswith("baseline")][0], "mine:", fixed(D / K0, 4))
