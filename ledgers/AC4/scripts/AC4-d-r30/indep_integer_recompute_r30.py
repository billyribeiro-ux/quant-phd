# Independent recomputation of the L07 and L08 printed counts from the stated model, in integer arithmetic.
import random
from fractions import Fraction as F
rng = random.Random(20261027)
cases = []
for i in range(1, 201):
    v = rng.randrange(3000, 5001, 100)
    p_m = v + rng.randrange(500, 3001, 100)
    K = rng.randrange(6000, 12001, 500)
    E = rng.randint(4000, min(9000, K))
    q = rng.randint(1000, 8000)
    r = v + rng.randint(-1500, 4000)
    cases.append((i, v, p_m, K, E, q, r))
cases.append((0, 4000, 6000, 10000, 8000, 5000, 5200))  # boundary
fits = [c for c in cases if c[5] <= c[3]]
over = len(cases) - len(fits)
nonempty = empty = 0
sign_ok = supp0 = mid_ok = sum_ok = 0
feas = []
for (cid, v, p, K, E, q, r) in cases:
    if q > K:
        continue
    D = max(0, q + E - K)
    surplus = q * (r - v) - D * (p - v)                   # integer
    tmin = F(v) + F(D * (p - v), q)                       # exact
    tmax = F(r)
    ne = tmin <= tmax
    if ne: nonempty += 1
    else: empty += 1
    sign_ok += (ne == (surplus >= 0))
    supp0 += (F(q) * (tmin - v) - D * (p - v) == 0)
    if ne:
        feas.append(cid)
        mid = (tmin + tmax) / 2
        mid_ok += (tmin <= mid <= tmax)
        ok = True
        for t in (tmin, tmax, mid):
            ok &= (q * (t - v) - D * (p - v)) + q * (r - t) == surplus
        sum_ok += ok
print("q>K:", over, "fits:", len(fits), "nonempty:", nonempty, "empty:", empty)
print("sign:", sign_ok, "supplier zero:", supp0, "midpoint inside:", mid_ok, "sum identity:", sum_ok)
print("boundary: surplus", 5000*(5200-4000) - 3000*2000, "tmin", F(4000) + F(3000*2000, 5000))
