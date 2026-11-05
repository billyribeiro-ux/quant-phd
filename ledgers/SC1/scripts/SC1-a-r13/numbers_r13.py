"""Independent re-derivation of the SC1 slice-a lab numbers (L01, L02, L03) and the hub's rung-2 count.

Re-implements the seeded draw order of each lab from its description; does not import the twins.
"""
import itertools
import math
import random
from fractions import Fraction

# ---- L02: seeded partial sum (SEED 20260101, LEVELS 8, GRID_DEPTH 10) -------------------------
def hat(m, j, t):
    centre = (2 * j - 1) / 2**m
    return max(0.0, 1.0 - 2**m * abs(t - centre))

def l2_draws(seed):
    rng = random.Random(seed)
    xi0 = rng.gauss(0.0, 1.0)
    coeffs = [[rng.gauss(0.0, 1.0) for _ in range(2 ** (m - 1))] for m in range(1, 9)]
    return xi0, coeffs

def partial_sum(xi0, coeffs, levels, t):
    total = xi0 * t
    for m in range(1, levels + 1):
        for j in range(1, 2 ** (m - 1) + 1):
            total += coeffs[m - 1][j - 1] * 2 ** (-(m + 1) / 2) * hat(m, j, t)
    return total

xi0, coeffs = l2_draws(20260101)
print("L02 xi_{1,1} unrounded:", repr(coeffs[0][0]), " |xi_{1,1}|=", f"{abs(coeffs[0][0]):.9f}")
print("L02 level-1 sup unrounded:", repr(abs(coeffs[0][0]) * 2 ** -1), f"{abs(coeffs[0][0]) * 2 ** -1:.9f}")
print("L02 2x printed 0.116589 =", 2 * 0.116589, " 2x unrounded=", 2 * abs(coeffs[0][0]) * 2 ** -1)
obs = [max(abs(c) for c in coeffs[m - 1]) * 2 ** (-(m + 1) / 2) for m in range(1, 9)]
bnd = [math.sqrt(4 * m * math.log(2)) * 2 ** (-(m + 1) / 2) for m in range(1, 9)]
for m in range(8):
    print(f"L02 m={m+1} sup={obs[m]:.9f} bound={bnd[m]:.9f} within={obs[m] <= bnd[m]}")
print("L02 sum of bounds levels 5-8 =", f"{sum(bnd[4:]):.9f}")
grid = [i / 2**10 for i in range(2**10 + 1)]
tail = max(abs(partial_sum(xi0, coeffs, 8, t) - partial_sum(xi0, coeffs, 4, t)) for t in grid)
print("L02 grid sup |Sigma_8-Sigma_4| =", f"{tail:.9f}", " <= sum of observed sups levels5-8:", tail <= sum(obs[4:]))
print("L02 sum observed sups levels 5-8 =", f"{sum(obs[4:]):.9f}")
# bounds on the level-m term sup, exactly: sup_t |Y_m| equals max|c| 2^{-(m+1)/2} at centres (grid-exact for m<=10)
ok = 0
for m in range(1, 9):
    gsup = max(abs(sum(coeffs[m - 1][j - 1] * hat(m, j, t) for j in range(1, 2 ** (m - 1) + 1)) * 2 ** (-(m + 1) / 2)) for t in grid)
    ok += gsup == max(abs(c) for c in coeffs[m - 1]) * 2 ** (-(m + 1) / 2)
print("L02 grid-sup equals formula levels:", ok, "of 8")
# seed sweep for 'holds for every seed' (count identity and grid identity)
bad_count = 0
bad_grid = 0
for seed in range(0, 500):
    x0, cs = l2_draws(seed)
    cases = 0
    eq = 0
    for n in range(5):
        for k in range(2**n + 1):
            t = k / 2**n
            base = partial_sum(x0, cs, n, t)
            for lv in range(n, 9):
                cases += 1
                eq += partial_sum(x0, cs, lv, t) == base
    if (eq, cases) != (216, 216):
        bad_count += 1
    for m in range(1, 9):
        gsup = max(abs(sum(cs[m - 1][j - 1] * hat(m, j, t) for j in range(1, 2 ** (m - 1) + 1)) * 2 ** (-(m + 1) / 2)) for t in grid)
        if gsup != max(abs(c) for c in cs[m - 1]) * 2 ** (-(m + 1) / 2):
            bad_grid += 1
print("L02 seeds 0-499: count identity failures", bad_count, "; grid identity failures", bad_grid)

# ---- L03: seeded simulation (SEED 20260503, PATHS 400, LEVELS 0..7) -------------------------
rng = random.Random(20260503)
rows = []
for H in (1.0, 2.0):
    for k in range(8):
        N = 2**k
        sd = math.sqrt(H / N)
        sums = []
        for _ in range(400):
            tot = 0.0
            for _ in range(N):
                inc = rng.gauss(0.0, sd)
                tot += inc * inc
            sums.append(tot)
        mean = sum(sums) / 400
        var = sum((v - mean) ** 2 for v in sums) / 399
        se = math.sqrt(var / 400)
        z = (mean - H) / se
        theo = H * math.sqrt(2 / N) / 20
        rows.append((H, N, mean, se, z, theo, se / theo - 1))
print("L03 cells (H, N, mean, se, z, theo_se, gap):")
for r in rows:
    print("  H=%g N=%3d mean=%.4f se=%.4f z=%.2f theo=%.6f gap=%+.3f%%" % (r[0], r[1], r[2], r[3], r[4], r[5], 100 * r[6]))
zs = sorted((abs(r[4]) for r in rows), reverse=True)
print("L03 max |z| =", f"{zs[0]:.4f}", " second =", f"{zs[1]:.4f}", " all |z|<=3:", all(z <= 3 for z in zs))
print("L03 max |gap| % =", f"{100 * max(abs(r[6]) for r in rows):.4f}", " all < 14%:", all(abs(r[6]) < 0.14 for r in rows))
worst = max(rows, key=lambda r: abs(r[6]))
print("L03 worst cell H=%g N=%d" % (worst[0], worst[1]))
# printed-value gap at (H=2,N=1) from the 4dp printed se 0.1601
print("L03 gap from printed 0.1601 at H=2,N=1 = %.4f%%" % (100 * (0.1601 / (2 * math.sqrt(2) / 20) - 1)))
# closed forms
for H, N in [(1, 2), (2, 8), (2, 128), (1, 128)]:
    print(f"closed form H={H} N={N}: {Fraction(H)**4 * (4*N*N - 1) / (3 * N**3)} = {float(Fraction(H)**4 * (4*N*N - 1) / (3 * N**3)):.6f}")
print("L03 sqrt(2)/20 =", f"{math.sqrt(2)/20:.6f}", " 2*(1/8)/20 =", 2 * (1/8) / 20)

# ---- rung-2 count in the hub (index.html line 143): walks of n steps whose max reaches a ----
def reach(n, a):
    c = 0
    for steps in itertools.product((1, -1), repeat=n):
        s = 0
        mx = 0
        for x in steps:
            s += x
            mx = max(mx, s)
        c += mx >= a
    return c
print("hub reach(n=2,a=1) =", reach(2, 1), " reach(n=6,a=2) =", reach(6, 2))

# ---- L01 exact checks ----
TIMES = (Fraction(1), Fraction(3, 4), Fraction(5, 2))
print("L01 dyadic sums equal t:", sum(
    sum((t / 2**n for _ in range(2**n)), Fraction(0)) == t for t in TIMES for n in range(5)), "of 15")
