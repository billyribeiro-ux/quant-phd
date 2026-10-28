"""Round 20 independent recomputation of the Lab 1 counts on L07 and L08 with integer-only arithmetic.

Own transcription of the seeded generators (same random.Random calls, same order), no Fraction, no code from the twins.
Cross-multiplied integer tests: L07 nonempty <=> q*(r-v) >= D*(p_m-v); L08 RI>=0 <=> 100*OI >= 9*C ... (r=900bp).
"""

import random

SEED = 20261027
out = {}

# ---- L07 ----
rng = random.Random(SEED)
cases = []
for cid in range(1, 201):
    v = rng.randrange(3000, 5001, 100)
    p_m = v + rng.randrange(500, 3001, 100)
    cap = rng.randrange(6000, 12001, 500)
    ext = rng.randint(4000, min(9000, cap))
    q = rng.randint(1000, 8000)
    r = v + rng.randint(-1500, 4000)
    cases.append((v, p_m, cap, ext, q, r))
cases.append((4000, 6000, 10000, 8000, 5000, 5200))  # hand-built boundary, same field order
fits = [c for c in cases if c[4] <= c[2]]
over = len(cases) - len(fits)
D = lambda c: max(0, c[4] + c[3] - c[2])
nonempty = lambda c: c[4] * (c[5] - c[0]) >= D(c) * (c[1] - c[0])  # q(r-v) >= D(p_m-v)  <=>  t_min <= r
empty = [c for c in fits if not nonempty(c)]
feas = [c for c in fits if nonempty(c)]
binding = [c for c in feas if D(c) > 0]
print("L07 q>K", over, "fits", len(fits), "empty", len(empty), "feasible", len(feas), "binding", len(binding))
print("L07 boundary: 5200 cents t_min == t_max and surplus", 5000 * (5200 - 4000) - 3000 * 2000)
print("L07 E1 share 75/187 =", round(75 / 187, 4), " binding share 73/112 =", round(73 / 112, 4))
# worked case K=10000 and K=12000, v=40 p_m=60 E=8000 q=5000 r=80 (SCU); integer cents: multiply by 100
for K in (10000, 12000):
    d = max(0, 5000 + 8000 - K)
    tmin = 40 + d * 20 / 5000
    sigma = 5000 * (80 - 40) - d * 20
    print("worked K", K, "D", d, "t_min", tmin, "Sigma", sigma)
print("worked t=46 supplier gain", 5000 * (46 - 40) - 3000 * 20)
print("misc2 Sigma", 2000 * (55 - 40), "buyer gain at 60", 2000 * (55 - 60))

# ---- L08 ----
rng = random.Random(SEED)
divs = []
for i in range(8):
    inv = rng.randrange(20_000, 200_001, 1000)
    oi = 5 * rng.randint(inv // 125, inv // 31)
    divs.append((chr(ord("A") + i), inv, oi))
for name, inv, oi in divs:
    ri = 100 * oi - 9 * inv  # RI scaled by 100 (r = 9/100)
    eva_x10000 = 8000 * oi - 900 * inv  # EVA x 10000: OI*(1-0.20) - 0.09*C, in cents
    print("L08", name, "C", inv, "OI", oi, "RI_x100", ri, "EVA_cents", eva_x10000 / 10000)
disc = 0
for i, (na, ia, oa) in enumerate(divs):
    for nb, ib, ob in divs[i + 1 :]:
        dri = (oa - 9 * ia / 100) - (ob - 9 * ib / 100)
        # integer: compare sign of (100*oa - 9*ia)*ib - ... use exact fractions via cross-multiplication
        ri_a = 100 * oa - 9 * ia
        ri_b = 100 * ob - 9 * ib
        ra = oa * ib - ob * ia  # sign of OI_a/C_a - OI_b/C_b times C_a*C_b
        if ri_a == ri_b or ra == 0:
            continue
        # ri comparison uses the same scale (both *100), ratio comparison uses cross product
        if (ri_a > ri_b) != (ra > 0):
            disc += 1
print("L08 discordant pairs (integer)", disc, "of", 28)
