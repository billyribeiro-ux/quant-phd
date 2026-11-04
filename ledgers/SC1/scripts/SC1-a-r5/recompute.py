import math, random
from fractions import Fraction
# L02 seeded sample, same RNG order as the twin
SEED = 20260101; LEVELS = 8
rng = random.Random(SEED)
xi0 = rng.gauss(0.0, 1.0)
coeffs = [[rng.gauss(0.0, 1.0) for _ in range(2 ** (m - 1))] for m in range(1, LEVELS + 1)]
sup = [max(abs(c) for c in coeffs[m-1]) * 2 ** (-(m + 1) / 2) for m in range(1, LEVELS + 1)]
bnd = [math.sqrt(4 * m * math.log(2)) * 2 ** (-(m + 1) / 2) for m in range(1, LEVELS + 1)]
for m in range(LEVELS):
    print(f"m={m+1} unrounded sup {sup[m]!r} -> {sup[m]:.6f}; bound {bnd[m]:.9f} -> {bnd[m]:.6f}; ratio {sup[m]/bnd[m]:.4f}")
u1 = max(abs(c) for c in coeffs[0])
print("level1 |xi11| =", repr(u1), " 2*sup =", repr(2*sup[0]), f"{2*sup[0]:.7f}", f"round6 {2*sup[0]:.6f}")
print("twice printed 0.116589 =", 2*0.116589)
print("sqrt(4 log 2) =", math.sqrt(4*math.log(2)), " half:", math.sqrt(4*math.log(2))/2)
print("sum bounds 5..8:", sum(bnd[4:]), " grid sup |S8-S4| printed 0.348139")
# seed sweep for dyadic identity and grid-sup identity
def hat(m, j, t):
    centre = (2 * j - 1) / 2.0**m
    return max(0.0, 1.0 - 2.0**m * abs(t - centre))
def partial_sum(xi0, coeffs, levels, t):
    total = xi0 * t
    for m in range(1, levels + 1):
        scale = 2 ** (-(m + 1) / 2)
        for j in range(1, 2 ** (m - 1) + 1):
            total += coeffs[m - 1][j - 1] * scale * hat(m, j, t)
    return total
bad_dy = []; bad_grid = []; within_counts = []
grid = [i / 2**10 for i in range(2**10 + 1)]
for seed in range(50):
    r = random.Random(seed)
    x0 = r.gauss(0.0, 1.0)
    cs = [[r.gauss(0.0, 1.0) for _ in range(2 ** (m - 1))] for m in range(1, LEVELS + 1)]
    eq = 0; tot = 0
    for n in range(5):
        for k in range(2**n + 1):
            t = k / 2**n
            base = partial_sum(x0, cs, n, t)
            for lv in range(n, LEVELS + 1):
                tot += 1; eq += partial_sum(x0, cs, lv, t) == base
    if (eq, tot) != (216, 216): bad_dy.append((seed, eq, tot))
    for m in range(1, LEVELS + 1):
        sc = 2 ** (-(m + 1) / 2)
        gs = max(abs(sum(cs[m-1][j-1] * hat(m, j, t) for j in range(1, 2**(m-1)+1)) * sc) for t in grid)
        lvl = max(abs(c) for c in cs[m-1]) * 2 ** (-(m + 1) / 2)
        if gs != lvl: bad_grid.append((seed, m, gs, lvl))
    within_counts.append(sum(1 for m in range(1, LEVELS+1) if max(abs(c) for c in cs[m-1]) * 2**(-(m+1)/2) <= math.sqrt(4*m*math.log(2))*2**(-(m+1)/2)))
print("seeds with dyadic count != 216:", bad_dy)
print("seeds/levels where grid sup != formula:", bad_grid[:10], len(bad_grid))
print("within-bound counts across 50 seeds: min", min(within_counts), "max", max(within_counts))
