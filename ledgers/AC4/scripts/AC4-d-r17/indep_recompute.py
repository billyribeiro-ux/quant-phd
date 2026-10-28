"""Independent integer-only recomputation of the L07 and L08 printed counts (does not import the lab twins)."""
import random
from itertools import combinations

SEED = 20261027
# L07: same draw order as the generator on the page (v, p_m, capacity, external, q, r_net per case)
rng = random.Random(SEED)
rows = []
for cid in range(1, 201):
    v = rng.randrange(3000, 5001, 100)
    p_m = v + rng.randrange(500, 3001, 100)
    K = rng.randrange(6000, 12001, 500)
    E = rng.randint(4000, min(9000, K))
    q = rng.randint(1000, 8000)
    r = v + rng.randint(-1500, 4000)
    rows.append((cid, v, p_m, K, E, q, r))
over = [x for x in rows if x[5] > x[3]]
fits = [x for x in rows if x[5] <= x[3]]
empty = feas = binding = exact_ok = 0
for cid, v, p, K, E, q, r in fits:
    D = max(0, q + E - K)
    # t_min <= r  <=>  q*v + D*(p-v) <= q*r  (multiply by q>0, integers only)
    nonempty = q * v + D * (p - v) <= q * r
    sigma = q * (r - v) - D * (p - v)
    assert nonempty == (sigma >= 0)
    if nonempty:
        feas += 1
        if D > 0:
            binding += 1
    else:
        empty += 1
    exact_ok += 1
print("L07 over", len(over), "fits", len(fits), "empty", empty, "feasible", feas, "binding", binding, "checked", exact_ok)
print("L07 fraction binding/feasible = %.4f, empty/fits = %.4f" % (binding / feas, empty / len(fits)))
# first six rows, D and t_min in cents (t_min*q exact as a fraction numerator/denominator)
for cid, v, p, K, E, q, r in rows[:6]:
    if q <= K:
        D = max(0, q + E - K)
        print(cid, v, p, K, E, q, D, "t_min=%.4f" % (v + D * (p - v) / q), "t_max=", r, "empty" if v * q + D * (p - v) > q * r else "feasible")
# L08: integer comparisons
rng = random.Random(SEED)
divs = []
for i in range(8):
    C = rng.randrange(20_000, 200_001, 1000)
    oi = 5 * rng.randint(C // 125, C // 31)
    divs.append(("SIM-" + chr(ord("A") + i), C, oi))
rate_bp, tax_bp = 900, 2000
disc = 0
pairs = 0
for a, b in combinations(divs, 2):
    pairs += 1
    ri_a = a[2] * 10000 - rate_bp * a[1]   # scaled by 10000
    ri_b = b[2] * 10000 - rate_bp * b[1]
    r_a = a[2] * b[1] - b[2] * a[1]        # sign of OI_a/C_a - OI_b/C_b, scaled by C_a*C_b
    if (ri_a - ri_b) != 0 and r_a != 0 and ((ri_a - ri_b) > 0) != (r_a > 0):
        disc += 1
print("L08 discordant pairs", disc, "of", pairs)
for n, C, oi in divs:
    ri = oi * 10000 - rate_bp * C
    eva = oi * (10000 - tax_bp) - rate_bp * C
    print(n, C, oi, "RI=%.2f" % (ri / 10000), "EVA=%.2f" % (eva / 10000))
