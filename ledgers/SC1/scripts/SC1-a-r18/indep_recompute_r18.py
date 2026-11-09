"""SC1-a round 18: independent recomputation of the numbers the slice states (not imported from the twins)."""

import math
import random
from fractions import Fraction

# --- L03: simulated sums, re-derived with the same RNG order as the lab (seed 20260503, 400 paths) ---
SEED, PATHS = 20260503, 400
rng = random.Random(SEED)
rows = []
for H in (1.0, 2.0):
    for k in range(8):
        N = 2**k
        sd = math.sqrt(H / N)
        sums = []
        for _ in range(PATHS):
            tot = 0.0
            for _ in range(N):
                x = rng.gauss(0.0, sd)
                tot += x * x
            sums.append(tot)
        mean = sum(sums) / PATHS
        var = sum((v - mean) ** 2 for v in sums) / (PATHS - 1)
        se = math.sqrt(var / PATHS)
        theo = H * math.sqrt(2 / N) / 20
        z = (mean - H) / se
        rows.append((H, N, mean, se, z, theo, se / theo - 1))
print("L03 rows (H, N, mean, se, z, theoretical se, gap):")
for H, N, mean, se, z, theo, gap in rows:
    print(f"  H={H:g} N={N:3d} mean={mean:.4f} se={se:.4f} z={z:+.2f} theo={theo:.6f} gap={100*gap:+.2f}%")
print(f"max |z| = {max(abs(r[4]) for r in rows):.2f}; second largest |z| = {sorted(abs(r[4]) for r in rows)[-2]:.2f}")
print(f"max |gap| = {100*max(abs(r[6]) for r in rows):.2f}% at H={max(rows, key=lambda r: abs(r[6]))[0]:g}, N={max(rows, key=lambda r: abs(r[6]))[1]}")
print(f"printed-value gap at H=2,N=1: {100*(0.1601/(2*math.sqrt(2)/20)-1):.2f}%")
print(f"all |z| <= 3: {all(abs(r[4]) <= 3 for r in rows)}")

# --- L03 exact s^2 sums and closed form at all 16 pairs ---
def exact(H, N):
    pts = [H * Fraction(j, N) for j in range(N + 1)]
    return sum(((b * b - a * a) ** 2 for a, b in zip(pts, pts[1:])), Fraction(0))
ok = all(exact(Fraction(H), 2**k) == Fraction(H) ** 4 * (4 * 4**k - 1) / (3 * (2**k) ** 3) for H in (1, 2) for k in range(8))
print(f"L03 exact s^2 sums equal closed form at 16 pairs: {ok}")
print(f"L03 H=2,N=8 sum = {float(exact(Fraction(2), 8)):.6f}; H=1,N=2 sum = {float(exact(Fraction(1), 2)):.6f}")

# --- L03 Prop 2.4(a) bound check on random partitions ---
r = random.Random(7)
worst = 0.0
for _ in range(2000):
    H = Fraction(r.randint(1, 9), r.randint(1, 4))
    cuts = sorted({Fraction(0), H, *[H * Fraction(r.randint(1, 999), 1000) for _ in range(r.randint(1, 12))]})
    mesh = max(b - a for a, b in zip(cuts, cuts[1:]))
    s = sum(((b * b - a * a) ** 2 for a, b in zip(cuts, cuts[1:])), Fraction(0))
    worst = max(worst, float(s / (4 * H**3 * mesh)))
print(f"Prop 2.4(a) max ratio over random partitions: {worst:.4f} (must be <= 1)")

# --- L02 identities over more seeds (docstring: hold for every seed) ---
def hat(m, j, t):
    c = (2 * j - 1) / 2.0**m
    return max(0.0, 1.0 - 2.0**m * abs(t - c))

def psum(xi0, coeffs, levels, t):
    tot = xi0 * t
    for m in range(1, levels + 1):
        sc = 2 ** (-(m + 1) / 2)
        for j in range(1, 2 ** (m - 1) + 1):
            tot += coeffs[m - 1][j - 1] * sc * hat(m, j, t)
    return tot

bad_dy = bad_sup = 0
for seed in range(60):
    rr = random.Random(seed)
    xi0 = rr.gauss(0.0, 1.0)
    coeffs = [[rr.gauss(0.0, 1.0) for _ in range(2 ** (m - 1))] for m in range(1, 9)]
    cases = eq = 0
    for n in range(5):
        for k in range(2**n + 1):
            t = k / 2**n
            base = psum(xi0, coeffs, n, t)
            for lv in range(n, 9):
                cases += 1
                eq += psum(xi0, coeffs, lv, t) == base
    bad_dy += cases - eq
    grid = [i / 2**10 for i in range(2**10 + 1)]
    for m in range(1, 9):
        sc = 2 ** (-(m + 1) / 2)
        gs = max(abs(sum(coeffs[m - 1][j - 1] * hat(m, j, t) for j in range(1, 2 ** (m - 1) + 1)) * sc) for t in grid)
        lt = max(abs(c) for c in coeffs[m - 1]) * sc
        bad_sup += gs != lt
print(f"L02 dyadic-fixed mismatches over 60 seeds: {bad_dy} (cases per seed = 216)")
print(f"L02 grid-sup vs formula mismatches over 60 seeds x 8 levels: {bad_sup}")

# --- L02 level bound closed forms (Prop 2.4 step 1) and E3 numbers ---
lam1 = math.sqrt(4 * math.log(2))
print(f"L02 lambda_1 = {lam1:.6f}; lambda_1/2 = {lam1/2:.6f}; 2*0.116589 = {2*0.116589:.7f} (E3 claims |xi_11| rounds to 0.233179)")
print(f"L02 M_m check m=1..8: " + ", ".join(f"{math.sqrt(4*m*math.log(2))*2**(-(m+1)/2):.6f}" for m in range(1, 9)))

# --- L01 numbers ---
print("L01 dyadic sums equal t for depths 0..4 and t in {1,3/4,5/2}:",
      all(sum((t / 2**n for _ in range(2**n)), Fraction(0)) == t for t in (Fraction(1), Fraction(3, 4), Fraction(5, 2)) for n in range(5)))

# --- Rung 2 walk count (index.html:143): walks of n=6 steps whose maximum reaches a=2 ---
cnt = 0
for bits in range(2**6):
    pos = mx = 0
    for i in range(6):
        pos += 1 if (bits >> i) & 1 else -1
        mx = max(mx, pos)
    cnt += mx >= 2
print(f"Rung 2 count n=6, a=2: {cnt}; n=2, a=1: {sum(1 for b in range(4) if max(0, *(__import__('itertools').accumulate([1 if (b>>i)&1 else -1 for i in range(2)]))) >= 1)}")
print(f"Placement: 7/9 = {100*7/9:.1f}%, 8/9 = {100*8/9:.1f}%")
