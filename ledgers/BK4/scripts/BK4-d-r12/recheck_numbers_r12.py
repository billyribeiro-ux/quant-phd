# Independent recomputation of the numbers and identities cited by the BK4 cards (round 12), exact Fractions, plus
# randomized checks of the general identities that cards state (Props 2.2, 2.4, 2.5, 2.6, Prop 2.5 difference, Prop 1.2).
import itertools
import math
import random
from fractions import Fraction as F

out = []
def check(name, got, want):
    ok = got == want
    out.append(f"{'PASS' if ok else 'FAIL'} {name}: got {got} want {want}")

# L01
check("c012 share 1533900/2841600 to 4dp", round(1533900 / 2841600, 4), 0.5398)
check("c004/c006 Example 2.6 Need_A", max(0, -min(0, -100, -100, -50)), 100)
# Example 2.6 nets: A pays 100 (-100), receives 50 from C (+50): net -50
check("c101 Debit_A = max(0, -(-100+50))", max(0, -(-100 + 50)), 50)
check("c009 Remark 2.7 need after reorder", max(0, -min(0, 50, -50, -50)), 50)

# L02
check("c028 floor(10000*180/230)", (10000 * 180) // 230, 7826)
check("c027 netted amount Example 2.4", sum(max(0, n) for n in (-50, 20, 30)), 50)
check("c031 positive net obligations (Lab 1 Part C values)", 1753300 + 3340300, 5093600)
check("c092 receivables sum (Lab 1 Part B)", 314500 + 2067800 + 3340300 + 1873700, 7596300)

# L03
check("c048 k for 9900 bps, S=200", -((-9900 * 200) // 10000), 198)
check("c048 tS/10000", F(9900 * 200, 10000), F(198))
check("c050 k for 9975, S=200", -((-9975 * 200) // 10000), 200)
check("c043 example 1.5 survivors (residual 20)", (20 * 40) // 100, 8)
check("c043 example 1.5 survivors (residual 20) m2", (20 * 60) // 100, 12)
check("c044 example 1.6 leftover", 2 - sum((2 * 1) // 3 for _ in range(3)), 2)

# L04
rho = F(21, 20); x = F(1, 2)
check("c072 theta at rho=21/20, x=1/2", (rho - x) / (1 - x), F(11, 10))
check("c072 bps", math.floor(10000 * (rho - x) / (1 - x)), 11000)
rho2 = F(19, 20)
check("c075 theta at rho=19/20, x=1/2", (rho2 - x) / (1 - x), F(9, 10))
check("c075 rho/2", rho2 / 2, F(19, 40))
check("c073 threshold 1/(1-h), h=1/20", 1 / (1 - F(1, 20)), F(20, 19))
check("c072 / Remark 2.8 theta(19/20, 1/7)", (rho2 - F(1, 7)) / (1 - F(1, 7)), F(113, 120))
check("c072 bps 113/120", math.floor(10000 * F(113, 120)), 9416)

# L05
p = F(1, 8)
check("c086 Example 2.8 expected cost", p * 2500 * (1 + 2 + 4), F(4375, 2))
check("c094 rounding half up of 4375/2", math.floor(F(4375, 2) + F(1, 2)), 2188)
check("c090 M3 closed form equal delays 2", p * 2500 * (2 + 2 + 2), 1875)
check("c089 1-(7/8)^3 = 169/512", 1 - (1 - p) ** 3, F(169, 512))
check("c089 3p = 192/512", 3 * p, F(192, 512))
check("c087 Var_4 closed form", p * (1 - p) * 2500 ** 2 * (1 + 2 + 4) ** 2, F(133984375, 4))
check("c087 Var_3 closed form", p * (1 - p) * 2500 ** 2 * (1 + 4 + 16), F(57421875, 4))
check("c083 difference = 2 k^2 p(1-p) sum_{i<j} l_i l_j", 2 * 2500 ** 2 * p * (1 - p) * (1 * 2 + 1 * 4 + 2 * 4),
      F(133984375, 4) - F(57421875, 4))

# Randomized identity checks (exact fractions)
rng = random.Random(12)
def rnd_frac():
    return F(rng.randint(1, 999), rng.randint(1000, 1999))
bad = 0
for _ in range(2000):
    rho_ = F(rng.randint(1, 3000), 1000)
    a = rnd_frac() * F(1, 2)
    xx = min(a, rho_ * F(9, 10))  # keeps 0<=x<1 and x<=rho
    if not (0 <= xx < 1 and xx <= rho_):
        continue
    th = (rho_ - xx) / (1 - xx)
    if th - 1 != (rho_ - 1) / (1 - xx):
        bad += 1
    if th - rho_ != xx * (rho_ - 1) / (1 - xx):
        bad += 1
    yy = xx + (1 - xx) * F(rng.randint(1, 99), 100)
    if 0 <= yy < 1 and yy <= rho_ and xx < yy:
        thy = (rho_ - yy) / (1 - yy)
        if thy - th != (yy - xx) * (rho_ - 1) / ((1 - xx) * (1 - yy)):
            bad += 1
out.append(f"{'PASS' if bad == 0 else 'FAIL'} random Prop 2.4/2.5/2.6 identities over admissible shares: failures {bad}")

# Prop 2.5 difference and Prop 2.1/2.2 enumeration for random parameters
bad = 0
for _ in range(500):
    pp = F(rng.randint(1, 99), 100)
    kap = rng.randint(1, 5000)
    ls = [rng.randint(0, 6) for _ in range(3)]
    pats = list(itertools.product((0, 1), repeat=3))
    mean = 0
    e2 = 0
    for pat in pats:
        pr = F(1)
        for xi in pat:
            pr *= pp if xi else (1 - pp)
        cost = kap * sum(l * xi for l, xi in zip(ls, pat))
        mean += pr * cost
        e2 += pr * cost * cost
    if mean != pp * kap * sum(ls):
        bad += 1
    var3 = e2 - mean ** 2
    mean4 = pp * kap * sum(ls)
    var4 = pp * (kap * sum(ls)) ** 2 - mean4 ** 2 + 0 * (1 - pp)
    var_formula3 = pp * (1 - pp) * kap ** 2 * sum(l * l for l in ls)
    if var3 != var_formula3:
        bad += 1
    diff = var4 - var3
    pair = sum(ls[i] * ls[j] for i in range(3) for j in range(i + 1, 3))
    if diff != 2 * kap ** 2 * pp * (1 - pp) * pair:
        bad += 1
out.append(f"{'PASS' if bad == 0 else 'FAIL'} random Prop 2.1/2.2/2.5 enumeration and difference identities: failures {bad}")

# Prop 2.6: P(C=0) under A3 and A4 for random p in (0,1), l_i>=1, kappa>=1
bad = 0
for _ in range(500):
    pp = F(rng.randint(1, 99), 100)
    if not (pp * (1 - pp) > 0):
        continue
    a3 = (1 - pp) ** 3
    a4 = 1 - pp
    if not (a3 < a4):
        bad += 1
out.append(f"{'PASS' if bad == 0 else 'FAIL'} Prop 2.6 (1-p)^3 < 1-p over random p: failures {bad}")

# Netting identities (L02 Prop 2.2, 2.3): random trade sets with distinct payer/receiver
bad = 0
for _ in range(500):
    members = rng.randint(2, 6)
    trades = []
    for _t in range(rng.randint(1, 8)):
        a, b = rng.sample(range(members), 2)
        trades.append((a, b, rng.randint(1, 1000)))
    G = sum(t[2] for t in trades)
    rec = [sum(t[2] for t in trades if t[1] == m) for m in range(members)]
    pay = [sum(t[2] for t in trades if t[0] == m) for m in range(members)]
    n = [rec[m] - pay[m] for m in range(members)]
    A = sum(max(0, x) for x in n)
    if sum(rec) != G or sum(pay) != G or sum(n) != 0:
        bad += 1
    if A != sum(max(0, -x) for x in n):
        bad += 1
    if not (0 <= A <= G):
        bad += 1
    eq = all(rec[m] == 0 or pay[m] == 0 for m in range(members))
    if (A == G) != eq:
        bad += 1
out.append(f"{'PASS' if bad == 0 else 'FAIL'} netting Props 2.2 and 2.3 over random trade sets: failures {bad}")

# Prop 1.2 and 1.3 (waterfall) over random inputs
bad = 0
for _ in range(3000):
    IM = rng.randint(0, 500); DF_d = rng.randint(0, 300); K = rng.randint(0, 300)
    surv = [rng.randint(0, 200) for _ in range(rng.randint(1, 4))]
    L = rng.randint(0, 1500)
    a1 = min(L, IM); a2 = min(L - a1, DF_d); a3 = min(L - a1 - a2, K)
    Z = L - a1 - a2 - a3
    D = sum(surv)
    if Z >= D:
        pays = list(surv); u = Z - D
    else:
        pays = [Z * d // D for d in surv] if D > 0 else [0] * len(surv)
        left = Z - sum(pays)
        for i, d in enumerate(surv):
            if left == 0:
                break
            if d > 0:
                pays[i] += 1; left -= 1
        if left != 0:
            bad += 1
        u = 0
        if any(pays[i] > surv[i] for i in range(len(surv))):
            bad += 1
    if a1 + a2 + a3 + sum(pays) + u != L:
        bad += 1
out.append(f"{'PASS' if bad == 0 else 'FAIL'} waterfall Prop 1.2 conservation and Prop 1.3 bounds over random inputs: failures {bad}")

print("\n".join(out))
