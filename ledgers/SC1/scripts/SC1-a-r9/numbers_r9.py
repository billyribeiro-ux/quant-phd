"""SC1 slice a, round 9: independent re-derivation of the numbers printed or quoted on L01-L03.

Run with: .venv/bin/python -I ledgers/SC1/scripts/SC1-a-r9/numbers_r9.py
Nothing here imports the lab twins; the lab numbers are recomputed from the seeded generator and from closed forms.
"""

from __future__ import annotations

import math
import random
import re
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = ROOT / "course" / "modules" / "SC" / "SC1"

# ---------- L03: printed mean/se/z versus recomputation -----------------------------------------------
# The printed table is parsed from the page's expected block, then compared with the theoretical SE.
text = (PAGES / "L03.html").read_text(encoding="utf-8")
block = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
assert block is not None
rows = re.findall(
    r"N =\s*(\d+) steps: mean ([\d.]+), se ([\d.]+), z = (-?[\d.]+)",
    block.group(1),
)
horizons = [1, 2]
assert len(rows) == 16, len(rows)
max_gap = (0.0, None)
max_abs_z_other = 0.0
max_abs_z = (0.0, None)
for idx, (n_str, mean_s, se_s, z_s) in enumerate(rows):
    H = horizons[idx // 8]
    N = int(n_str)
    printed_se = float(se_s)
    printed_z = float(z_s)
    printed_mean = float(mean_s)
    theory = H * math.sqrt(2 / N) / 20
    gap = printed_se / theory - 1
    if abs(gap) > abs(max_gap[0]):
        max_gap = (gap, (H, N, printed_se, theory))
    # z recomputed from the printed mean and printed se (rounded), to show the printed z is consistent
    z_recomputed = (printed_mean - H) / printed_se
    assert abs(z_recomputed - printed_z) < 0.02, (H, N, z_recomputed, printed_z)
    if abs(printed_z) > max_abs_z[0]:
        max_abs_z = (abs(printed_z), (H, N))
print(f"L03 largest |z| = {max_abs_z[0]} at H, N = {max_abs_z[1]}")
zs_sorted = sorted((abs(float(r[3])) for r in rows), reverse=True)
print(f"L03 |z| values in descending order (top 3): {zs_sorted[:3]}")
print(
    f"L03 largest relative gap printed se / (H sqrt(2/N)/20) - 1 = {max_gap[0] * 100:.2f} percent at H, N, printed, theory = "
    f"{max_gap[1]}"
)
# per-row gap list for the record
for idx, (n_str, _, se_s, _) in enumerate(rows):
    H = horizons[idx // 8]
    N = int(n_str)
    theory = H * math.sqrt(2 / N) / 20
    print(f"  H={H} N={N:3d} printed_se={float(se_s):.4f} theory={theory:.6f} gap={(float(se_s) / theory - 1) * 100:+.2f}%")

# H=1, N=1 and H=2, N=128 theoretical values quoted on the page
print(f"L03 theory H=1,N=1: sqrt(2)/20 = {math.sqrt(2) / 20:.6f} (page: 0.0707)")
print(f"L03 theory H=2,N=128: 2*sqrt(2/128)/20 = {2 * math.sqrt(2 / 128) / 20:.6f} (page: 0.0125)")

# exact t-squared sums and closed form (E2 at L03:350 uses H=2, N=8)
for H, N in [(1, 2), (2, 8), (2, 128), (1, 128)]:
    s = sum(
        ((Fraction(H) * (j + 1) / N) ** 2 - (Fraction(H) * j / N) ** 2) ** 2 for j in range(N)
    )
    closed = Fraction(H) ** 4 * (4 * N * N - 1) / (3 * N**3)
    print(f"L03 exact H={H} N={N}: sum={s} = {float(s):.6f}; closed form equal: {s == closed}")

# ---------- L02: observed suprema and bounds, recomputed from the same seeded coefficients ------------
SEED = 20260101
LEVELS = 8
rng = random.Random(SEED)
xi0 = rng.gauss(0.0, 1.0)
coeffs = [[rng.gauss(0.0, 1.0) for _ in range(2 ** (m - 1))] for m in range(1, LEVELS + 1)]
print(f"L02 xi0 = {xi0!r}")
within = 0
for m in range(1, LEVELS + 1):
    sup_unrounded = max(abs(c) for c in coeffs[m - 1]) * 2 ** (-(m + 1) / 2)
    bound = math.sqrt(4 * m * math.log(2)) * 2 ** (-(m + 1) / 2)
    within += sup_unrounded <= bound
    print(f"L02 m={m}: sup={sup_unrounded:.12f} (printed {sup_unrounded:.6f}) bound={bound:.12f} ({bound:.6f})")
print(f"L02 levels within bound: {within} of {LEVELS}")
print(f"L02 twice the level-1 sup = {2 * max(abs(c) for c in coeffs[0]) * 2 ** -1:.12f}, "
      f"doubled printed = {2 * 0.116589:.6f}")
print(f"L02 sqrt(4 log 2) = {math.sqrt(4 * math.log(2)):.9f}, half = {math.sqrt(4 * math.log(2)) / 2:.9f}")

# Sigma_8 - Sigma_4 grid sup and bounds sum, grid 2^-10
def hat(m: int, j: int, t: float) -> float:
    centre = (2 * j - 1) / 2**m
    return max(0.0, 1.0 - 2**m * abs(t - centre))


def sigma(levels: int, t: float) -> float:
    total = xi0 * t
    for m in range(1, levels + 1):
        for j in range(1, 2 ** (m - 1) + 1):
            total += coeffs[m - 1][j - 1] * 2 ** (-(m + 1) / 2) * hat(m, j, t)
    return total


grid = [i / 2**10 for i in range(2**10 + 1)]
tail_sup = max(abs(sigma(8, t) - sigma(4, t)) for t in grid)
tail_bounds = sum(math.sqrt(4 * m * math.log(2)) * 2 ** (-(m + 1) / 2) for m in range(5, 9))
print(f"L02 grid sup |Sigma_8 - Sigma_4| = {tail_sup:.6f} (page 0.348139); bounds 5..8 sum = {tail_bounds:.6f} (page 1.309399)")

# ---------- L02 dyadic-count arithmetic (E2 and quiz) ----------------------------------------------------
total = sum((2**n + 1) * (9 - n) for n in range(5))
print(f"L02 dyadic cases = {total} (page 216); per depth = {[(2**n + 1) * (9 - n) for n in range(5)]}")

# ---------- L01 lab arithmetic -----------------------------------------------------------------------------
print("L01 dyadic check: 3 times x 5 depths =", 3 * 5, "; grid pairs 9*9 =", 9 * 9)
print("L01 Cov(B_{1/4},B_{5/8}) =", min(Fraction(1, 4), Fraction(5, 8)))
