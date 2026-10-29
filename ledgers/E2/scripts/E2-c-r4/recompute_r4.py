"""Independent recomputation of every number in E2 slice c (L07-L09), written fresh for round 4."""
import itertools
import math
import random
from fractions import Fraction as F

def hu(x):  # half up to whole cents, nonnegative or negative handled via floor(x+1/2)
    return math.floor(x + F(1, 2))

print("== L07 two-type revenue problem")
vL, vH = 6000, 10000
D = vH - vL
def pay_for(c_sign_pH):
    return None
pL_, pH_ = F(3, 10), F(7, 10)
c = pL_ * vL - pH_ * D
print("c(7/10) =", c, "exclusion revenue", pH_ * vH, "pooling revenue", vL)
# c as a function of pH: c = 6000 - 10000 pH
print("c zero at pH =", F(6000, 10000))
# Brute force over a fine grid of (qL,qH) with U_L = 0 and U_H = D*qL (minimal), check max revenue
def rev(qL, qH, pH):
    pL = 1 - pH
    tH = vH * qH - D * qL          # U_H = D qL, U_L = 0
    tL = vL * qL
    return pL * tL + pH * tH
def feasible(qL, qH):
    return 0 <= qL <= qH <= 1
for pH in [F(7, 10), F(1, 2), F(3, 5), F(1, 5), F(9, 10)]:
    grid = [F(k, 100) for k in range(101)]
    best = max((rev(a, b, pH), a, b) for a in grid for b in grid if feasible(a, b))
    cc = (1 - pH) * vL - pH * D
    print(f"pH={pH} c={cc} grid_max={best[0]} at qL={best[1]} qH={best[2]} formula={max(pH*vH, vL) if cc!=0 else vL}")
# c = 0 case: both q_L=0 and q_L=1 attain the max
pH = F(3, 5)
print("c=0 check: revenue(qL=0,qH=1)=", rev(F(0), F(1), pH), " revenue(qL=1,qH=1)=", rev(F(1), F(1), pH))
# Lab Part B grid
steps = [F(k, 4) for k in range(5)]
ok = []
for qL in steps:
    for qH in steps:
        if qL > qH:
            continue
        tL = vL * qL
        tH = vH * qH - D * qL
        # IC: L truthful U_L=vL qL - tL >=0 ; H truthful >= H report L; L report H <= truthful
        UL = vL * qL - tL
        UH = vH * qH - tH
        ic_H = UH >= vH * qL - tL
        ic_L = UL >= vL * qH - tH
        ir = UL >= 0 and UH >= 0
        if ic_H and ic_L and ir:
            ok.append((pL_ * tL + pH_ * tH, qL, qH))
print("grid pairs with qL<=qH:", sum(1 for a in steps for b in steps if a <= b), "passing:", len(ok))
print("max revenue", max(ok), "count achieving max", sum(1 for r in ok if r[0] == max(ok)[0]))
print("pool at 6000 revenue", pL_ * vL + pH_ * vL)
print("R1 decline tie-break revenue", pH_ * 6000)
print("M2 p_H=1/2 revenue", F(1, 2) * 6000 + F(1, 2) * (10000 - 4000))
print("M3 mixed menu revenue", F(3, 10) * 3000 + F(7, 10) * 8000)
print("E2 high-price-H-only revenue", F(3, 10) * 6000)

print("== L08 expected largest noise")
def em_formula(n, a):
    return -a + sum(1 - F(x + a + 1, 2 * a + 1) ** n for x in range(-a, a))
def em_pmf(n, a):
    cdf = lambda x: F(x + a + 1, 2 * a + 1) ** n if x >= -a else F(0)
    return sum(m * (cdf(m) - cdf(m - 1)) for m in range(-a, a + 1))
def em_enum(n, a):
    vals = range(-a, a + 1)
    tot = list(itertools.product(vals, repeat=n))
    return F(sum(max(t) for t in tot), len(tot))
for n, a in [(2, 1), (3, 1), (2, 2), (3, 2), (4, 1)]:
    print(n, a, em_formula(n, a), em_pmf(n, a), em_enum(n, a))
print("n=2 a=1 formula 4/9:", em_formula(2, 1) == F(4, 9))
e5 = em_formula(5, 2000)
print("n=5 a=2000 exact:", e5, "float", float(e5), "pmf-agree", e5 == em_pmf(5, 2000))
print("expected = 85418692002000/64048012001 ?", e5 == F(85418692002000, 64048012001))
print("continuous a(n-1)/(n+1) n=5 a=2000:", F(2000 * 4, 6), float(F(4000, 3)))
print("diff exact", float(e5 - F(4000, 3)), "diff with rounded figures", 1333.66656253 - 1333.3333333)
print("rounded 1333.67 vs 1333.33 differ by", round(1333.67 - 1333.33, 2))
print("n=3 a=1 =", em_formula(3, 1))
print("shade = half_up(E[M]) =", hu(e5), "; half_up(-20000*E[M]) =", hu(-20000 * e5))
print("20000*(1334 - E[M]) exact =", float(20000 * (1334 - e5)), "half_up =", hu(20000 * (1334 - e5)))
print("1333 - E[M] =", float(1333 - e5))
print("E[M] (n=2,a=1) continuous 1/3 minus discrete 4/9 =", F(4, 9) - F(1, 3))

print("== L08 simulation (fresh re-implementation)")
A, N, HW, VLO, VHI, SEED = 5, 20000, 2000, 5000, 15000, 20261028
def sim(shade):
    rng = random.Random(SEED)
    prof = []
    for _ in range(N):
        v = rng.randint(VLO, VHI)
        sig = [v + rng.randint(-HW, HW) for _ in range(A)]
        bids = [s - shade for s in sig]
        w = max(range(A), key=lambda i: (bids[i], -i))
        prof.append(v - bids[w])
    return prof
def se_total(p):
    n = len(p)
    s1 = sum(p); s2 = sum(x * x for x in p)
    return math.sqrt((n * s2 - s1 * s1) / (n - 1))
naive = sim(0)
shaded = sim(1334)
print("naive total", sum(naive), "SE", se_total(naive), "per-auction avg", sum(naive) / N)
print("shaded total", sum(shaded), "SE", se_total(shaded))
print("naive-exact diff", sum(naive) - (-26673331), "in SE", (sum(naive) - (-26673331)) / se_total(naive))
print("shaded-exact diff", sum(shaded) - 6669, "in SE", (sum(shaded) - 6669) / se_total(shaded))
print("shaded - naive", sum(shaded) - sum(naive), "== 1334*20000 ?", sum(shaded) - sum(naive) == 1334 * 20000)
print("per-auction naive avg", round(sum(naive) / N, 2), "exact per auction", round(float(-e5), 2))
print("SE per auction", round(se_total(naive) / N, 2))

print("== L09 fixed profiles")
def ranking(b):
    return sorted(range(len(b)), key=lambda i: (-b[i], i))
def pays(fmt, b, k):
    o = ranking(b); p = [0] * len(b); cl = b[o[k]]
    for i in o[:k]:
        p[i] = cl if fmt == "u" else b[i]
    return p
V = [9000, 5000, 6000, 7000]; B = [8000, 9500, 6500, 7000]
print("ranking", ranking(B), "uniform pays", pays("u", B, 2), "disc pays", pays("d", B, 2))
ru = sum(pays("u", B, 2)); rd = sum(pays("d", B, 2))
print("Ru", ru, "Rd", rd, "gap", rd - ru, "gap share", F(rd - ru, ru))
won = sum(V[i] for i in ranking(B)[:2]); top = sum(sorted(V, reverse=True)[:2])
print("won", won, "top", top, "eff", F(won, top), float(F(won, top)))
prof = list(itertools.product(range(4), repeat=4))
above = equal = below = 0
top3eq_count = 0
for b in prof:
    b = list(b)
    ru = sum(pays("u", b, 2)); rd = sum(pays("d", b, 2))
    if rd > ru: above += 1
    elif rd == ru: equal += 1
    else: below += 1
    o = sorted(b, reverse=True)
    if o[0] == o[1] == o[2]:
        top3eq_count += 1
    # equality iff top three equal
    assert (rd == ru) == (o[0] == o[1] == o[2]), b
print("256 profiles: above", above, "equal", equal, "below", below, "top3-equal count", top3eq_count)
print("share above", F(above, 256), float(F(above, 256)))
ok1 = all(
    sum(pays("u", list(b), 1)[ranking(list(b))[0]:ranking(list(b))[0]+1]) == sorted(b, reverse=True)[1]
    for b in prof
)
ok1b = all(pays("u", list(b), 1)[ranking(list(b))[0]] == sorted(b, reverse=True)[1] for b in prof)
ok1c = all(pays("d", list(b), 1)[ranking(list(b))[0]] == sorted(b, reverse=True)[0] for b in prof)
print("k=1 identity: uniform pays 2nd highest on all 256:", ok1b, "; discriminatory pays own bid:", ok1c)
print("R1 formula sum_{v=0..3}(4v+1) =", sum(4 * v + 1 for v in range(4)))
