"""Round-3 independent recomputation of every number in LX1 slice a (L01, L02, hub).

Written by the verifier from the page prose, not from the lab twins. Run: python3 -I this_file
"""
import math
import random
from fractions import Fraction as F


def rhu(x):
    return math.floor(x + F(1, 2))


def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    return cond


out = []
# ---- L01 closed form
d1, r, g = F(400), F(9, 100), F(3, 100)
F0 = d1 / (r - g)
q = (1 + g) / (1 + r)
out.append(check(f"L01 F0 = 20000/3: {F0} rounds {rhu(F0)}", F0 == F(20000, 3) and rhu(F0) == 6667))
out.append(check(f"L01 q = 103/109: {q}", q == F(103, 109)))
out.append(check(f"L01 q to 6 dp 0.944954: {float(q):.6f}", f"{float(q):.6f}" == "0.944954"))
for N in (10, 60, 200):
    S = sum(d1 * (1 + g) ** (s - 1) / (1 + r) ** s for s in range(1, N + 1))
    res = F0 * q**N
    print(f"  N={N} S_N rounds {rhu(S)} residual F0 q^N = {float(res):.4f} rounds {rhu(res)}")
    out.append(check(f"L01 identity exact N={N}", S == F0 * (1 - q**N)))
# expected block: N=10 sum 2882, residual 3785; N=60 sum 6444 residual 223; N=200 sum 6667 residual 0
S10 = sum(d1 * (1 + g) ** (s - 1) / (1 + r) ** s for s in range(1, 11))
S60 = sum(d1 * (1 + g) ** (s - 1) / (1 + r) ** s for s in range(1, 61))
out.append(check("L01 N=10 sum 2882 and residual 3785", rhu(S10) == 2882 and rhu(F0 * q**10) == 3785))
out.append(check("L01 N=60 sum 6444 and residual 223", rhu(S60) == 6444 and rhu(F0 * q**60) == 223))
# Prop 2.2 witness
F1 = d1 / (F(1, 100) * 0 + r - F(1, 100))
F3 = d1 / (r - F(3, 100))
out.append(check(f"L01 witness F0(1%)=5000 F0(3%)=20000/3: {F1} {F3}", F1 == 5000 and F3 == F(20000, 3)))
out.append(check("L01 witness gaps +1000 and -2000/3", F(6000) - F1 == 1000 and F(6000) - F3 == F(-2000, 3)))
# Section 5 bullet 2 / misconception 2: PV of single 400-cent dividend at 9%
pv = F(400) / (1 + r)
out.append(check(f"L01 PV 400/1.09 = 40000/109 = {float(pv):.4f} rounds {rhu(pv)}", pv == F(40000, 109) and rhu(pv) == 367))
# Mechanics 1/2
F0m = F(250) / (F(10, 100) - F(4, 100))
F3m = F(250) * (1 + F(4, 100)) ** 3 / (F(10, 100) - F(4, 100))
out.append(check(f"L01 Mech1 F0=12500/3={float(F0m):.2f} rounds {rhu(F0m)}", F0m == F(12500, 3) and rhu(F0m) == 4167))
out.append(check(f"L01 Mech2 F3={float(F3m):.4f} rounds {rhu(F3m)}", rhu(F3m) == 4687 and F(1, 1) * (F(104, 100)) ** 3 == F(1124864, 1000000)))
# Mechanics 3: d1=100 r=g=5%, S10 = 20000/21 (= 952.38)
S10m = sum(F(100) / (F(105, 100)) for _ in range(10))
out.append(check(f"L01 Mech3 S10 = 20000/21 = {float(S10m):.2f}", S10m == F(20000, 21)))
# Empirical 1/2
out.append(check("L01 Emp1 9/13 = 0.6923", f"{9/13:.4f}" == "0.6923"))
out.append(check("L01 Emp2 13-9=4", 13 - 9 == 4))
# Empirical 3: fundamental at t=9, 2175/8698
f9 = d1 * (1 + g) ** 9 / (r - g)
print(f"  L01 F_9 exact {float(f9):.6f}")
out.append(check(f"L01 Emp3 F_9 to two places 8698.49 ({float(f9):.4f})", f"{float(f9):.2f}" == "8698.49" and rhu(f9) == 8698))
out.append(check(f"L01 Emp3 printed ratio 2175/8698 = {float(F(2175,8698)):.6f} -> 25.01 pct", f"{100*float(F(2175,8698)):.2f}" == "25.01"))
out.append(check("L01 Emp3 exact 0.25 * F_9 is 2174.62 cents", abs(float(F(1,4)*f9) - 2174.62) < 0.01))
# Research 1: g* with 400/(0.09-g)=6000
gstar = r - F(400, 6000)
out.append(check(f"L01 Res1 g*={float(gstar):.6f} (2.33 pct)", f"{float(gstar):.6f}" == "0.023333" and f"{100*float(gstar):.2f}" == "2.33"))
# Quiz: F2 = 400*1.03^2/0.06 = 7072.67 rounds 7073
F2 = d1 * (1 + g) ** 2 / (r - g)
out.append(check(f"L01 quiz F2={float(F2):.4f} rounds {rhu(F2)}", f"{float(F2):.2f}" == "7072.67" and rhu(F2) == 7073))
out.append(check("L01 quiz 1000/1.25=800 (hub skill check)", F(1000) / F(125, 100) == 800))
out.append(check("L01 quiz 1.03/1.09 = 103/109", F(103, 100) / F(109, 100) == F(103, 109)))
out.append(check("L01 quiz 6666.67 = 20000/3", f"{float(F0):.2f}" == "6666.67"))

# ---- L01 Lab 1 recomputation (independent of twin): wedge path, seeded
SEED = 20261103
def path(rate_growth):
    return None
rng = random.Random(SEED)
gaps = []
wedges = []
for t in range(13):
    fund = rhu(d1 * (1 + g) ** t / (r - g))
    w = F(rng.randint(-8, 25), 100)
    wedges.append(w)
    price = rhu(d1 * (1 + g) ** t / (r - g) * (1 + w))
    gaps.append(price - fund)
pos = sum(1 for x in gaps if x > 0)
print("  L01 gaps", gaps, "positive", pos, "largest", max(gaps), "at", gaps.index(max(gaps)))
out.append(check(f"L01 Part B 9 of 13 positive ({pos})", pos == 9))
out.append(check("L01 Part B largest 2175 at t=9", max(gaps) == 2175 and gaps.index(2175) == 9))
exp_gaps = [-200, 68, 141, 146, 301, 0, -398, 2050, 676, 2175, 2151, -92, 285]
out.append(check("L01 Part B gaps match expected block", gaps == exp_gaps))
rng = random.Random(SEED)
alt = 0
for t in range(13):
    w = F(rng.randint(-8, 25), 100)
    price = rhu(d1 * (1 + g) ** t / (r - g) * (1 + w))
    altf = rhu(d1 * (1 + F(1, 100)) ** t / (r - F(1, 100)))
    if price - altf > 0:
        alt += 1
out.append(check(f"L01 Part C 13 of 13 under 1pct ({alt})", alt == 13))

# ---- L02 numbers
P = [F(100)]
changes = []
rng = random.Random(20261104)
for _ in range(12):
    c = rng.randint(-4, 3)
    changes.append(c)
    P.append(P[-1] * (1 + F(c, 100)))
D = 1_000_000
V = [D * F(100) / p for p in P]
Vc = [rhu(v) for v in V]
print("  L02 changes", changes)
print("  L02 cents", Vc)
exp_changes = [-1, 1, 1, 3, -4, -1, 2, -4, -3, 3, 2, -4]
exp_cents = [1000000, 1010101, 1000100, 990198, 961357, 1001414, 1011529, 991695, 1033016, 1064965, 1033946, 1013673, 1055909]
out.append(check("L02 change sequence matches Part A", changes == exp_changes))
out.append(check("L02 real values match Part B", Vc == exp_cents))
falls = [t for t in range(1, 13) if P[t] < P[t - 1]]
rises = [t for t in range(1, 13) if V[t] > V[t - 1]]
out.append(check(f"L02 Part C 6 falls and 6 rises, equal sets: {falls} {rises}", len(falls) == 6 and falls == rises))
steps = [Vc[t] - Vc[t - 1] for t in range(1, 13)]
out.append(check(f"L02 largest rise 42236 at t=12 (steps {max(steps)} at {steps.index(max(steps))+1})", max(steps) == 42236 and steps.index(42236) + 1 == 12))
out.append(check("L02 identity exact all t", all(V[t] / V[t - 1] == P[t - 1] / P[t] for t in range(1, 13))))
out.append(check("L02 telescoped exact", V[12] / V[0] == P[0] / P[12]))
ratio = float(V[12] / V[0])
out.append(check(f"L02 V12/V0 six dp = 1.055909 ({ratio:.9f})", f"{ratio:.6f}" == "1.055909"))
p12_unr = float(P[12])
print(f"  L02 P12 unrounded {p12_unr:.10f}")
trunc8 = math.floor(P[12] * 10**8) / 10**8  # the page writes 94.70509914 followed by an ellipsis: a truncation
out.append(check(f"L02 E3 P12 printed 94.7051 and truncated 8dp 94.70509914 (unrounded {P[12].numerator}/{P[12].denominator})", f"{p12_unr:.4f}" == "94.7051" and f"{trunc8:.8f}" == "94.70509914"))
out.append(check(f"L02 E3 100/94.70509914 = {100/94.70509914:.8f} ~ 1.05590935", f"{100/94.70509914:.6f}" == "1.055909" and f"{100/float(P[12]):.6f}" == "1.055909"))
out.append(check(f"L02 E3 100/94.7051 = {100/94.7051:.7f} 1.0559093", f"{100/94.7051:.6f}" == "1.055909"))
out.append(check("L02 V1 E2 1010101.0101", f"{float(V[1]):.4f}" == "1010101.0101"))
out.append(check("L02 M1 V1 = 2500 (2000*100/80)", F(2000) * 100 / 80 == 2500))
out.append(check("L02 M2 V2/V1 = 18/17 = 90/85", F(90, 85) == F(18, 17)))
out.append(check(f"L02 M2 18/17 = {float(F(18,17)):.10f}", f"{float(F(18,17)):.10f}" == "1.0588235294"))
out.append(check("L02 M3 200000/95 = 2105.263 rounds 2105", rhu(F(200000, 95)) == 2105 and f"{float(F(200000,95)):.4f}" == "2105.2632"))
out.append(check("L02 E2 1000000*100/99 = 1010101.0101", f"{float(F(1000000*100,99)):.4f}" == "1010101.0101"))
out.append(check("L02 1.25 = 100/80", F(100, 80) == F(5, 4)))
out.append(check("L02 price-path kappa: 1/(2/5)=5/2", 1 / F(2, 5) == F(5, 2)))
out.append(check("L02 fall-to-rise factor 100/80 = 1.25", F(100, 80) == F(125, 100)))
print("ALL PASS" if all(out) else "SOME FAIL")
