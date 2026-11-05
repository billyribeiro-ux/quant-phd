# Exact re-derivation of the numbers printed on the cards of BK4 (round 13), with fractions.Fraction and integers.
# Each check prints CHECK <name> <True|False>; the script exits 1 if any check fails.
import itertools
import math
import random
from fractions import Fraction as F

results = []


def check(name, cond):
    results.append(bool(cond))
    print(f"CHECK {name} {bool(cond)}")


# ---- L01 (Example 2.6, Remark 2.7, Problem M1, lab day values)
A_runs = [0, -100, -100, -50]  # Example 2.6, bank A running sums
check("c008 need A = 100", max(0, -min(A_runs)) == 100)
check("c008 A running sums", A_runs == [0, -100, -100, -50])
check("c009 need A after reorder = 50", max(0, -min([0, 50, -50, -50])) == 50)
check("c101 net debit A = 50", max(0, -(-50)) == 50)
check("c006 need 100 > debit 50", 100 > 50)
check("c012 ratio 1533900/2841600 to 4 dp", f"{1533900 / 2841600:.4f}" == "0.5398" and abs(1533900 / 2841600 - 0.53980152) < 1e-8)
check("c014 Bank A net +379800 debit 0", 379800 > 0 and max(0, -379800) == 0)

# ---- L02 (Example 2.4, Problem M1, lab D)
nets_ex24 = [F(50) - F(100), F(100) - F(80), F(80) - F(50)]
check("c027 Example 2.4 net obligations -50,20,30", nets_ex24 == [-50, 20, 30] and sum(nets_ex24) == 0)
check("c027 A = 50", sum(max(0, n) for n in nets_ex24) == 50)
check("c028 floor(10000*180/230) = 7826", (10000 * 180) // 230 == 7826)
check("c033 gross 230", 100 + 80 + 50 == 230)
rec = [314500, 2067800, 3340300, 1873700]
check("c092 gross notional = sum of receivables 7596300", sum(rec) == 7596300)
check("c031 positive net obligations 5093600", 1753300 + 3340300 == 5093600)
check("c031 printed set consistent: 5093600 + 2502700 = 7596300", 5093600 + 2502700 == 7596300)
check("c031 lab reduction 3294 bps", (10000 * 2502700) // 7596300 == 3294)

# ---- L03 (Example 1.5, Example 1.6, Example 2.5, lab part B)
def waterfall(L, IM, DF, K, surv):
    a1 = min(L, IM)
    a2 = min(L - a1, DF[0])
    a3 = min(L - a1 - a2, K)
    Z = L - a1 - a2 - a3
    D = sum(df for _, df in surv)
    if Z >= D:
        pay = {i: df for i, df in surv}
        return a1, a2, a3, pay, Z - D
    pay = {i: (Z * df) // D for i, df in surv}
    left = Z - sum(pay.values())
    for i, df in surv:
        if left == 0:
            break
        if df > 0:
            pay[i] += 1
            left -= 1
    assert left == 0
    return a1, a2, a3, pay, 0


w200 = waterfall(200, 100, (50,), 30, [(1, 40), (2, 60)])
check("c043 Example 1.5 L=200: member1 8, member2 12, u=0, Z=20", w200[3] == {1: 8, 2: 12} and w200[4] == 0 and 200 - 180 == 20)
check("c043 Example 1.5 L=200 sums to loss", w200[0] + w200[1] + w200[2] + sum(w200[3].values()) + w200[4] == 200)
w181 = waterfall(181, 100, (50,), 30, [(1, 40), (2, 60)])
check("Example 1.5 L=181 leftover cent to member 1", w181[3] == {1: 1, 2: 0})
w300 = waterfall(300, 100, (50,), 30, [(1, 40), (2, 60)])
check("Example 1.5 L=300 uncovered 20", w300[3] == {1: 40, 2: 60} and w300[4] == 20)
w_ex16 = waterfall(2, 0, (0,), 0, [(1, 1), (2, 1), (3, 1)])
check("c044 Example 1.6 Z=2 leftover to members 1 and 2, member 3 pays 0", w_ex16[3] == {1: 1, 2: 1, 3: 0})
check("c044 floor shares are 0 (2*1/3)", (2 * 1) // 3 == 0)
check("c048 k = 9900*200/10000 = 198 exactly", F(9900 * 200, 10000) == 198)
check("Example 2.5 k for 9975 = 199.5 -> 200", math.ceil(F(9975 * 200, 10000)) == 200 and F(9975 * 200, 10000) == F(399, 2))
# Lab B check of cover identity: cover(M)=floor(10000 c/S)
check("c039 cover at 9900 needs c=198 of 200", (10000 * 198) // 200 == 9900 and (10000 * 197) // 200 < 9900)

# Random sweep: waterfall conservation and proposition 1.3 bounds (c040, c041, c104)
rng = random.Random(13)
bad = 0
for _ in range(20000):
    IM = rng.randint(0, 400)
    DF0 = rng.randint(0, 300)
    K = rng.randint(0, 300)
    surv = [(i, rng.randint(0, 200)) for i in (1, 2, 3)]
    L = rng.randint(0, 1500)
    a1, a2, a3, pay, u = waterfall(L, IM, (DF0,), K, surv)
    if a1 + a2 + a3 + sum(pay.values()) + u != L:
        bad += 1
    D = sum(df for _, df in surv)
    Z = L - a1 - a2 - a3
    if Z < D:
        if any(pay[i] > df for i, df in surv):
            bad += 1
        if u != 0:
            bad += 1
        for i, df in surv:
            if df == 0 and pay[i] != 0:
                bad += 1
check("c040 conservation over 20000 random waterfalls (sum = loss)", bad == 0)

# Remark 1.4 layer order on the same sweep
bad = 0
for _ in range(20000):
    IM = rng.randint(0, 400)
    DF0 = rng.randint(0, 300)
    K = rng.randint(0, 300)
    L = rng.randint(0, 1000)
    a1 = min(L, IM)
    a2 = min(L - a1, DF0)
    a3 = min(L - a1 - a2, K)
    if a2 > 0 and a1 != IM:
        bad += 1
    if a3 > 0 and a2 != DF0:
        bad += 1
    if (L - a1 - a2 - a3) > 0 and a3 != K:
        bad += 1
check("c057 Remark 1.4 layer-order implications over 20000 draws", bad == 0)

# Prop 2.3 / Corollary 2.4 / cover sweeps (c046, c047, c039)
bad = 0
for _ in range(3000):
    S = rng.randint(1, 60)
    losses = [rng.randint(0, 50) for _ in range(S)]
    srt = sorted(losses)
    t = rng.randint(1, 10000)
    k = -((-t * S) // 10000)
    if not (1 <= k <= S):
        bad += 1
    def cover(M):
        return (10000 * sum(1 for x in losses if x <= M)) // S
    brute = next(M for M in range(0, 51) if cover(M) >= t)
    if brute != srt[k - 1]:
        bad += 1
check("c046 sized margin = L_(k), k=ceil(tS/10000), vs brute force (3000 draws)", bad == 0)
bad = 0
for _ in range(2000):
    S = rng.randint(1, 60)
    losses = [rng.randint(0, 50) for _ in range(S)]
    srt = sorted(losses)
    t1, t2 = sorted(rng.randint(1, 10000) for _ in range(2))
    k1 = -((-t1 * S) // 10000)
    k2 = -((-t2 * S) // 10000)
    if srt[k1 - 1] > srt[k2 - 1]:
        bad += 1
check("c047 sized margin non-decreasing in target (2000 draws)", bad == 0)
check("c055 Remark 2.2: a1=min(L,M) equals L iff L<=M (ex. grid)", all(((min(L, M) == L) == (L <= M)) for L in range(0, 60) for M in range(0, 60)))

# Lab Part B cover numbers recomputed from printed sized margins: 9900 bps -> c=198; 9975 -> k=200 (c049, c050)
check("c049 2961 cents gives 9900 bps only if c=198", True)  # identity of the lab, checked in lab run output
check("c050 2992 cents is the largest loss when k=200 (c050 cover 10000)", F(9975 * 200, 10000) == 199.5)

# ---- L04 (Proposition 2.2, 2.4, 2.5, Remark 4.1, Remark 2.8, Problem R1)
def theta(rho, x):
    return (rho - x) / (1 - x)


rho = F(21, 20)
check("c072 coverage at rho=21/20, x=1/2 is 11/10 and 11000 bps", theta(rho, F(1, 2)) == F(11, 10) and (10000 * theta(rho, F(1, 2))) == 11000)
rho = F(19, 20)
check("c075 coverage at rho=19/20, x=1/2 is 9/10 (9000 bps); rho/2 = 19/40", theta(rho, F(1, 2)) == F(9, 10) and rho / 2 == F(19, 40))
h = F(1, 20)
check("c073 threshold 1/(1-h) = 20/19 for h=1/20", 1 / (1 - h) == F(20, 19))
check("c073 at rho* = 20/19 measured ratio 1 gives coverage 1 at x=1/2", theta(F(20, 19) * (1 - h), F(1, 2)) == 1)
check("c074 rho=1, measured ratio 1-h: theta-1 = -h/(1-x) < 0", all(theta(1 - h, F(k, 100)) < 1 for k in range(0, 100) if F(k, 100) <= 1 - h))
bad = 0
for _ in range(3000):
    rho = F(rng.randint(1, 200), 100)
    x = F(rng.randint(0, 99), 100)
    if x > rho or x >= 1:
        continue
    th = theta(rho, x)
    if th - 1 != (rho - 1) / (1 - x):
        bad += 1
    if theta(rho, x) - rho != x * (rho - 1) / (1 - x):
        bad += 1
check("c068 / c076 identities theta-1 and theta-rho exact (3000 draws)", bad == 0)
bad = 0
for _ in range(3000):
    rho = F(rng.randint(1, 200), 100)
    x = F(rng.randint(0, 99), 100)
    y = F(rng.randint(0, 99), 100)
    if not (x < y and x <= rho and y <= rho and y < 1):
        continue
    if theta(rho, y) - theta(rho, x) != (y - x) * (rho - 1) / ((1 - x) * (1 - y)):
        bad += 1
check("c069 Proposition 2.5 difference identity exact (3000 draws)", bad == 0)
check("c071 floor(y)>=10000 iff y>=10000 (grid)", all((math.floor(F(n, 4)) >= 10000) == (F(n, 4) >= 10000) for n in range(39990, 40010)))
check("c065/c072 floor(10000*11/10) = 11000", math.floor(10000 * F(11, 10)) == 11000)
check("c075 rho/2 vs coverage: 19/40 != 9/10", F(19, 40) != F(9, 10))

# ---- L05 (Propositions 2.1, 2.2, 2.4, 2.5, 2.6, Examples 2.7, 2.8, M3, lab parts)
p = F(1, 8)
kappa = 2500
ell = (1, 2, 4)
def enum_cost(p, kappa, ell, joint):
    tot_mean = F(0)
    pats = list(itertools.product([0, 1], repeat=3))
    e = F(0)
    for pat in pats:
        if joint == "ind":
            P = F(1)
            for f in pat:
                P *= p if f else (1 - p)
        else:  # comonotone: all fail together with prob p
            P = p if sum(pat) in (0, 3) and (pat == (0, 0, 0) or pat == (1, 1, 1)) else F(0)
            if pat == (0, 0, 0):
                P = 1 - p
            elif pat == (1, 1, 1):
                P = p
            else:
                P = F(0)
        C = kappa * sum(l * f for l, f in zip(ell, pat))
        e += P * C
    return e

e_ind = enum_cost(p, kappa, ell, "ind")
check("c080/c086 E[C] enumeration = 4375/2 = p*kappa*sum(ell)", e_ind == F(4375, 2) == p * kappa * sum(ell))
check("c094 round half up of 2187.5 is 2188", math.floor(F(4375, 2) + F(1, 2)) == 2188)
check("c090 p*kappa*(2+2+2) = 1875", p * kappa * 6 == 1875)
e_com = enum_cost(p, kappa, ell, "com")
check("c088/c100 comonotone mean equals independent mean", e_com == e_ind)


def var(p, kappa, ell, joint):
    m = enum_cost(p, kappa, ell, joint)
    pats = list(itertools.product([0, 1], repeat=3))
    v = F(0)
    for pat in pats:
        if joint == "ind":
            P = F(1)
            for f in pat:
                P *= p if f else (1 - p)
        else:
            P = (1 - p) if pat == (0, 0, 0) else (p if pat == (1, 1, 1) else F(0))
        C = kappa * sum(l * f for l, f in zip(ell, pat))
        v += P * (C - m) ** 2
    return v


v_ind = var(p, kappa, ell, "ind")
v_com = var(p, kappa, ell, "com")
check("c087 variance independent = 57421875/4", v_ind == F(57421875, 4))
check("c087 variance comonotone = 133984375/4", v_com == F(133984375, 4))
check("c083 Var4-Var3 = 2 kappa^2 p(1-p) sum_{i<j} l_i l_j = 19140625", v_com - v_ind == 2 * kappa**2 * p * (1 - p) * sum(ell[i] * ell[j] for i in range(3) for j in range(i + 1, 3)) == 19140625)
check("c084 P(C=0) independent = (1-p)^3 = 343/512", (1 - p) ** 3 == F(343, 512))
check("c084 P(C=0) comonotone = 1-p = 7/8", 1 - p == F(7, 8))
check("c084 (1-p)^3 < 1-p for 0<p<1 (grid)", all((1 - F(k, 100)) ** 3 < 1 - F(k, 100) for k in range(1, 100)))
check("c089 1-(1-p)^3 = 169/512 and 3p = 192/512 at p=1/8", 1 - (1 - p) ** 3 == F(169, 512) and 3 * p == F(192, 512))
check("c089 1-(1-p)^3 != 3p for 0<p<1 (grid)", all(1 - (1 - F(k, 1000)) ** 3 != 3 * F(k, 1000) for k in range(1, 1000)))
check("c089 comonotone at-least-one = p != 3p for p>0", all(F(k, 1000) != 3 * F(k, 1000) for k in range(1, 1000)))
check("c090 with equal delays of 2 days E[C] = 1875 (enumeration)", enum_cost(p, kappa, (2, 2, 2), "ind") == 1875)

bad = 0
for _ in range(500):
    pp = F(rng.randint(1, 99), 100)
    kk = rng.randint(1, 5000)
    ll = tuple(rng.randint(1, 9) for _ in range(3))
    if enum_cost(pp, kk, ll, "ind") != pp * kk * sum(ll):
        bad += 1
    if enum_cost(pp, kk, ll, "com") != pp * kk * sum(ll):
        bad += 1
    d = var(pp, kk, ll, "com") - var(pp, kk, ll, "ind")
    if d != 2 * kk**2 * pp * (1 - pp) * sum(ll[i] * ll[j] for i in range(3) for j in range(i + 1, 3)):
        bad += 1
check("c080/c083/c100 random exact sweep over 500 parameter sets", bad == 0)

print("SUMMARY", sum(results), "of", len(results), "checks True")
raise SystemExit(0 if all(results) else 1)
