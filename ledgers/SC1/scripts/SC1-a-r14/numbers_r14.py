"""Round-14 SC1-a: independent recomputation of every printed or prose number in L02 (lab, E3, bounds) and L03 (se gaps, z)."""
import math
import random
from fractions import Fraction

# ---- L02 lab: replicate the seeded draws in the page's own order (independent re-implementation) ----
SEED = 20260101
LEVELS = 8
rng = random.Random(SEED)
xi0 = rng.gauss(0.0, 1.0)
coeffs = [[rng.gauss(0.0, 1.0) for _ in range(2 ** (m - 1))] for m in range(1, LEVELS + 1)]
print("xi0 =", repr(xi0))
print("xi_{1,1} =", repr(coeffs[0][0]), " |xi_{1,1}| =", abs(coeffs[0][0]))
for m in range(1, LEVELS + 1):
    sup = max(abs(c) for c in coeffs[m - 1]) * 2 ** (-(m + 1) / 2)
    bound = math.sqrt(4 * m * math.log(2)) * 2 ** (-(m + 1) / 2)
    print(f"m={m}: sup={sup!r} ({sup:.6f})  bound={bound!r} ({bound:.6f})  within={sup <= bound}")
b58 = sum(math.sqrt(4 * m * math.log(2)) * 2 ** (-(m + 1) / 2) for m in range(5, 9))
print(f"sum of bounds levels 5..8 = {b58!r} ({b58:.6f})")
print("sqrt(4 log 2) =", math.sqrt(4 * math.log(2)), " half =", math.sqrt(4 * math.log(2)) / 2)
print("2*sup_1 unrounded (for E3):", 2 * max(abs(c) for c in coeffs[0]) * 2 ** -1)

def hat(m, j, t):
    return max(0.0, 1.0 - 2.0 ** m * abs(t - (2 * j - 1) / 2.0 ** m))

def partial(levels, t):
    total = xi0 * t
    for m in range(1, levels + 1):
        for j in range(1, 2 ** (m - 1) + 1):
            total += coeffs[m - 1][j - 1] * 2 ** (-(m + 1) / 2) * hat(m, j, t)
    return total

grid = [i / 2 ** 10 for i in range(2 ** 10 + 1)]
gap = max(abs(partial(8, t) - partial(4, t)) for t in grid)
print(f"grid sup |Sigma_8 - Sigma_4| = {gap!r} ({gap:.6f})")
# exact-ish check of the grid supremum by a finer grid of the same kernel (hat peaks are on the 2^-10 grid)
fine = [i / 2 ** 14 for i in range(2 ** 14 + 1)]
gapf = max(abs(partial(8, t) - partial(4, t)) for t in fine)
print(f"fine grid 2^-14 sup = {gapf!r} ({gapf:.6f})  (grid sup should be <= this)")

# ---- E2 counts of L02 ----
pts = {n: 2 ** n + 1 for n in range(5)}
print("E2 total:", sum(pts[n] * (9 - n) for n in range(5)), "points:", sum(pts.values()))

# ---- L03 standard-error gaps (printed values, four decimals) ----
printed = {
    1: [(1, 1, 0.0718), (1, 2, 0.0538), (1, 4, 0.0373), (1, 8, 0.0249), (1, 16, 0.0174), (1, 32, 0.0131), (1, 64, 0.0092), (1, 128, 0.0063),
        (2, 1, 0.1601), (2, 2, 0.0934), (2, 4, 0.0772), (2, 8, 0.0475), (2, 16, 0.0364), (2, 32, 0.0256), (2, 64, 0.0190), (2, 128, 0.0125)],
}
worst = (0, None)
for _, rows in printed.items():
    for H, N, se in rows:
        theory = H * math.sqrt(2 / N) / 20
        gap_pct = (se / theory - 1) * 100
        print(f"H={H} N={N:3d} printed se={se:.4f} theory={theory:.6f} gap={gap_pct:+.2f}%")
        if abs(gap_pct) > abs(worst[0]):
            worst = (gap_pct, (H, N))
print("largest |gap| =", worst)
print("E3 theory H=2,N=128:", 2 * math.sqrt(2 / 128) / 20)
print("H=2,N=1 ratio:", 0.1601 / (2 * math.sqrt(2) / 20) - 1)
print("L03 E2 H=2 N=8 exact:", Fraction(2 ** 4 * (4 * 64 - 1), 3 * 512), float(Fraction(2 ** 4 * (4 * 64 - 1), 3 * 512)))
print("L01 3/64*16:", Fraction(3, 64) * 16, " 1/(1+1)?", math.sqrt(1 / 4))
print("L03 H=1 N=2 closed form:", Fraction(1 * (4 * 4 - 1), 3 * 8))
print("harmonic check: 1/m bound 1 + k/2 for k=10 lower bound:", 1 + 10 / 2)
print("m=2 Lambda_{2,1}(1/4), (0), (1/2):", hat(2, 1, 0.0), hat(2, 1, 0.25), hat(2, 1, 0.5))
print("sum_{m>=1} m r^m with r=2^-1/2 =", sum(m * 2 ** (-m / 2) for m in range(1, 400)), " r/(1-r)^2 =", (2 ** -0.5) / (1 - 2 ** -0.5) ** 2)
print("sum_{m>=1} 2^-m =", sum(2.0 ** -m for m in range(1, 200)))
print("Lemma2.1 2e^{-lam^2/2} at lam_m=sqrt(4m log2) equals 2*2^{-2m}:", [abs(2 * math.exp(-(4 * m * math.log(2)) / 2) - 2 * 2 ** (-2 * m)) < 1e-15 for m in range(1, 9)])
