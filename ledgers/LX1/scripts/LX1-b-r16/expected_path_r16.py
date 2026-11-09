"""LX1-b round 16: independent recomputation (Fraction only, no twin code) of the L03 expected path rows and key lines.

Compares every row of the page's expected block (L03.html lines 331-357) with values rebuilt from first principles:
index P_t, real debt V_t rounded half up to a cent, leverage L_t and premium psi_t to four decimals, output fall to two
percent. Run: .venv/bin/python -I expected_path_r15.py <checkout>
"""

import math
import re
import sys
from fractions import Fraction as F
from pathlib import Path

root = Path(sys.argv[1])
lines = (root / "course/modules/LX/LX1/L03.html").read_text(encoding="utf-8").split("\n")
expected = lines[330:357]  # L03.html lines 331-343 economy X rows, 344 economy Y header, 345-357 economy Y rows

D, A0, delta = F(1_000_000), F(4_000_000), F(1, 50)


def half_up(x: F, places: int = 0) -> str:
    n = math.floor(x * 10**places + F(1, 2))
    whole, frac = divmod(n, 10**places) if places else (n, 0)
    return f"{whole}.{frac:0{places}d}" if places else str(whole)


def mine(m: int, t: int) -> str:
    P = (1 - delta) ** min(t, m)
    V = D / P
    A = A0 - (V - D)
    L = V / A
    psi = L - D / A0
    fall = psi
    return (f"  t = {t:2d}: index {half_up(P, 4)}; real debt {half_up(V)} cents; leverage {half_up(L, 4)}; "
            f"premium {half_up(psi, 4)}; output fall {half_up(100 * fall, 2)} percent")


mine_rows = [mine(12, t) for t in range(13)]
mine_rows_y = [mine(4, t) for t in range(13)]
ok_x = all(expected[i] == mine_rows[i] for i in range(13))
ok_y = all(expected[14 + i] == mine_rows_y[i] for i in range(13))
print("economy X rows equal independent recomputation:", ok_x)
print("economy Y rows equal independent recomputation:", ok_y)
for i in range(13):
    if expected[i] != mine_rows[i]:
        print("X mismatch", expected[i], "|", mine_rows[i])
    if expected[14 + i] != mine_rows_y[i]:
        print("Y mismatch", expected[14 + i], "|", mine_rows_y[i])
print("line 330 (header of X):", lines[329][:50], "| line 344 (header of Y):", lines[343][:50])
