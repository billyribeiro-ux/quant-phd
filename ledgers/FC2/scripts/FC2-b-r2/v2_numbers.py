"""FC2 slice b round 2: independent re-derivation of every displayed number in L04-L06 and their cards.

Run: python -I -W error ledgers/FC2/scripts/FC2-b-r2/v2_numbers.py   (prints PASS/FAIL per check)
"""

from __future__ import annotations

import math
from fractions import Fraction as F

results: list[tuple[str, bool, str]] = []


def check(name: str, got: object, want: object, ok: bool | None = None) -> None:
    passed = ok if ok is not None else (got == want)
    results.append((name, passed, f"got={got} want={want}"))


def close(x: float, y: float, tol: float) -> bool:
    return abs(x - y) <= tol


# ---- L04 Example 2.5 (A4: one-year factor 9/10; path 100,120,90,80,110; strike 100)
D = F(9, 10)
r = math.log(10 / 9)
check("L04 r=ln(10/9) to 5 places", round(r, 5), 0.10536, ok=round(r, 5) == 0.10536)
check("L04 hold to expiry 10*(9/10)^4", float(10 * D**4), 6.561, ok=close(float(10 * D**4), 6.561, 1e-12))
check("L04 hold to expiry to the cent", f"{float(10 * D**4):.2f}", "6.56")
check("L04 exercise at date 1 PV = 20*9/10", 20 * D, F(18))
check("L04 put best PV = 20*(9/10)^3", float(20 * D**3), 14.58, ok=close(float(20 * D**3), 14.58, 1e-12))
check("L04 call hold at t=1 = 10*(9/10)^3", float(10 * D**3), 7.29, ok=close(float(10 * D**3), 7.29, 1e-12))
check("L04 call hold at t=2 = 10*(9/10)^2", float(10 * D**2), 8.10, ok=close(float(10 * D**2), 8.10, 1e-12))
check("L04 call hold at t=3 = 10*(9/10)", float(10 * D), 9.00, ok=close(float(10 * D), 9.0, 1e-12))
check("L04 break-even call 100+8", 100 + 8, 108)
check("L04 break-even put 100-7", 100 - 7, 93)
check("L04 profit at 125 = 25-8", 25 - 8, 17)
# R1: 20000/729 = 27.43484..., S = 127.43484
check("L04 R1 S_tau to five decimals", f"{100 + 20000 / 729:.5f}", "127.43484")
check("L04 R1 identity 20*(10/9)^3 = 20000/729", F(20) * F(10, 9) ** 3, F(20000, 729))
# R3: path 100,90,95,110,150
check("L04 R3 best discounted intrinsic = 10*(9/10)^3", float(10 * D**3), 7.29, ok=close(float(10 * D**3), 7.29, 1e-12))
check("L04 R3 hold = 50*(9/10)^4 = 32.805", float(50 * D**4), 32.805, ok=close(float(50 * D**4), 32.805, 1e-9))
# E2 variant: last spot 90
check("L04 E2 put expiry 10*(9/10)^4 = 6.561", float(10 * D**4), 6.561, ok=close(float(10 * D**4), 6.561, 1e-12))
# E3 put at date 2 intrinsic 10 PV 8.10
check("L04 E3 put PV at 2 = 10*(9/10)^2 = 8.10", float(10 * D**2), 8.10, ok=close(float(10 * D**2), 8.10, 1e-12))
# Path intrinsic call values and best date
path = [100, 120, 90, 80, 110]
call_pv = [max(s - 100, 0) * D**t for t, s in enumerate(path)]
check("L04 call PV list best date", max(range(5), key=lambda t: call_pv[t]), 1)
put_pv = [max(100 - s, 0) * D**t for t, s in enumerate(path)]
check("L04 put PV list best date", max(range(5), key=lambda t: put_pv[t]), 3)

# ---- L05
check("L05 M1 put = 8 - 100 + 0.97*105", 8 - 100 + F(97, 100) * 105, F(985, 100))
check("L05 M1 display 9.85", f"{float(8 - 100 + F(97, 100) * 105):.2f}", "9.85")
check("L05 M2 lower bound max(50-38,0)", max(50 - F(95, 100) * 40, 0), 12)
check("L05 M2 initial value 3-50+38", 3 - 50 + F(95, 100) * 40, -9)
check("L05 M3 chord (15+4)/2", (15 + 4) / 2, 9.5)
check("L05 M3 second difference", 15 - 2 * 9 + 4, 1)
for k1, k2, k3 in [(8000, 9000, 10000), (80, 90, 120), (90, 100, 110), (8000, 11000, 12000)]:
    lam = F(k3 - k2, k3 - k1)
    check(f"L05 P1 weight reproduces K2 for {k1},{k2},{k3}", lam * k1 + (1 - lam) * k3, k2)
    check(f"L05 P1 weight in (0,1) for {k1},{k2},{k3}", 0 < lam < 1, True)
# lab grid
D5 = F(9, 10)
strikes = [8000, 9000, 10000, 11000, 12000]
calls = [int(max(10000 - D5 * k, 0) + F(max(10000 - k, 0), 10)) for k in strikes]
puts = [int(c - 10000 + D5 * k) for c, k in zip(calls, strikes)]
check("L05 lab calls cents", tuple(calls), (3000, 2000, 1000, 100, 0))
check("L05 lab puts cents", tuple(puts), (200, 100, 0, 0, 800))
check("L05 lab parity residual zero", [c - p - 10000 + D5 * k for c, p, k in zip(calls, puts, strikes)], [0] * 5)
payoff_bad = sum(
    1
    for k in strikes
    for s in (0, 5000, 8000, 9000, 10000, 11000, 12000, 15000)
    if (max(s - k, 0) - max(k - s, 0) - s + k) != 0
)
check("L05 payoff nonzero pairs of 40", payoff_bad, 0)


def convex_viol(ks, cs):
    out = []
    n = len(ks)
    for i in range(n):
        for j in range(i + 1, n):
            for kk in range(j + 1, n):
                k1, k2, k3 = ks[i], ks[j], ks[kk]
                lam = F(k3 - k2, k3 - k1)
                if cs[j] > lam * cs[i] + (1 - lam) * cs[kk]:
                    out.append((k1, k2, k3))
    return out


check("L05 synthetic convexity violations", len(convex_viol(strikes, calls)), 0)
pc = [c + (500 if k == 9000 else 0) for c, k in zip(calls, strikes)]
pp = [p + (500 if k == 9000 else 0) for p, k in zip(puts, strikes)]
cv = convex_viol(strikes, pc)
check("L05 planted convexity violated triples", len(cv), 3)
check("L05 planted convexity middle strike", sorted({t[1] for t in cv}), [9000])
check("L05 planted convexity triples set", sorted(cv), [(8000, 9000, 10000), (8000, 9000, 11000), (8000, 9000, 12000)])
check("L05 planted convexity keeps parity", [c - p - 10000 + D5 * k for c, p, k in zip(pc, pp, strikes)], [0] * 5)
pp2 = [p + (300 if k == 10000 else 0) for p, k in zip(puts, strikes)]
check("L05 planted parity cost -300", [c - p - 10000 + D5 * k for c, p, k in zip(calls, pp2, strikes)], [0, 0, -300, 0, 0])
# D = 1/100 claim
D2 = F(1, 100)
c80 = max(10000 - D2 * 8000, 0) + F(max(10000 - 8000, 0), 10)
p80 = c80 - 10000 + D2 * 8000
check("L05 docstring D=1/100 call at 80 exceeds spot", float(c80) > 10000, True)
check("L05 docstring D=1/100 put at 80 exceeds DK", float(p80) > float(D2 * 8000), True)
# E1 second differences in cents
check("L05 E1 second diff at 90", 3000 - 2 * 2000 + 1000, 0)
check("L05 E1 second diff at 100", 2000 - 2 * 1000 + 100, 100)
check("L05 E1 second diff at 110", 1000 - 2 * 100 + 0, 800)
check("L05 quiz second difference 20-2*10+1", 20 - 2 * 10 + 1, 1)
# E3
check("L05 E3 bound DK-S at 120", F(9, 10) * 120 - 100, 8)
check("L05 E3 call bound max(100-108,0)", max(100 - F(9, 10) * 120, 0), 0)
# canon example
check("L05 canon 100e^{-0.1}-50 to 2dp", f"{100 * math.exp(-0.1) - 50:.2f}", "40.48")
check("L05 R2 e^{0.1}*100 to 3dp", f"{100 * math.exp(0.1):.3f}", "110.517")
check("L05 R2 bound 120-110.517 to 2dp", f"{120 - 100 * math.exp(0.1):.2f}", "9.48")

# ---- L06
Rf = F(5, 4)
u, d = F(3, 2), F(1, 2)
q = (Rf - d) / (u - d)
check("L06 q example 1.5", q, F(3, 4))
Delta = (F(50) - 0) / ((u - d) * 100)
B = (u * 0 - d * 50) / ((u - d) * Rf)
check("L06 Delta", Delta, F(1, 2))
check("L06 B", B, F(-20))
check("L06 V0", Delta * 100 + B, F(30))
check("L06 V0 by q formula", (q * 50 + (1 - q) * 0) / Rf, F(30))
check("L06 example 1.6 cash", 35 - 50 + 20, 5)
check("L06 example 1.6 lent 5*5/4", 5 * Rf, F(25, 4))
up_total = F(25, 4) - 50 + (F(1, 2) * 150 - 25)
down_total = F(25, 4) + 0 + (F(1, 2) * 50 - 25)
check("L06 example 1.6 totals up", up_total, F(25, 4))
check("L06 example 1.6 totals down", down_total, F(25, 4))
# Example 3.4
S2 = {2: 225, 1: 75, 0: 25}
pay = {k: max(v - 100, 0) for k, v in S2.items()}
V11 = (q * pay[2] + (1 - q) * pay[1]) / Rf
V10 = (q * pay[1] + (1 - q) * pay[0]) / Rf
V00 = (q * V11 + (1 - q) * V10) / Rf
check("L06 Ex3.4 V11", V11, F(75))
check("L06 Ex3.4 V10", V10, F(0))
check("L06 Ex3.4 V00", V00, F(45))
closed = Rf ** -2 * (F(9, 16) * 125)
check("L06 Ex3.4 closed form", closed, F(45))
ev = q**2 * 225 + 2 * q * (1 - q) * 75 + (1 - q) ** 2 * 25
check("L06 misc E[S2]", ev, F(3125, 20))
check("L06 misc E[S2]=156.25", ev, F(625, 4))
check("L06 misc R_f^2 S0", Rf**2 * 100, F(625, 4))
check("L06 misc payoff at 156.25", F(625, 4) - 100, F(225, 4))
check("L06 misc discounted 56.25*16/25", F(225, 4) * F(16, 25), F(36))
check("L06 misc expected payoff 1125/16", q**2 * 125, F(1125, 16))
check("L06 misc discounted expectation 1125/16 / R^2", F(1125, 16) / Rf**2, F(45))
check("L06 misc discounted expected price = S0", ev / Rf**2, F(100))
# M1
qM1 = (Rf - d) / (2 - d)
V0M1 = (qM1 * 100) / Rf
check("L06 M1 q", qM1, F(1, 2))
check("L06 M1 V0", V0M1, F(40))
DeltaM2 = F(100) / ((2 - d) * 100)
BM2 = (2 * 0 - d * 100) / ((2 - d) * Rf)
check("L06 M2 Delta", DeltaM2, F(2, 3))
check("L06 M2 B", BM2, F(-80, 3))
check("L06 M2 cost", DeltaM2 * 100 + BM2, F(40))
# M3: u=2,d=1/2, S(2,k)
S2M3 = {2: 400, 1: 100, 0: 25}
pM3 = {k: max(v - 100, 0) for k, v in S2M3.items()}
V11M3 = (F(1, 2) * pM3[2] + F(1, 2) * pM3[1]) / Rf
V10M3 = (F(1, 2) * pM3[1] + F(1, 2) * pM3[0]) / Rf
check("L06 M3 V11", V11M3, F(120))
check("L06 M3 V10", V10M3, F(0))
check("L06 M3 V00", (F(1, 2) * V11M3 + F(1, 2) * V10M3) / Rf, F(48))
# E2 scaling
check("L06 E2 V0 at 200/200", (F(3, 4) * max(300 - 200, 0)) / Rf, F(60))
# E3 quote 28
cash0 = -28 + (50 - 20)
surplus = cash0
check("L06 E3 surplus after purchase", -28 + 30, 2)
up_e3 = 50 - F(1, 2) * 150 + 20 * Rf + surplus * Rf
dn_e3 = 0 - F(1, 2) * 50 + 20 * Rf + surplus * Rf
check("L06 E3 up payoff", up_e3, F(5, 2))
check("L06 E3 down payoff", dn_e3, F(5, 2))
# R1
check("L06 R1 bond B=-80", F(-100) / Rf, F(-80))
check("L06 R1 payoffs 50,0,-50", [1 * s - 100 for s in (150, 100, 50)], [50, 0, -50])
# R2
q_R2 = (1 - F(1, 2)) / (u - d)
check("L06 R2 q", q_R2, F(1, 2))
check("L06 R2 V0", (q_R2 * 50) / 1, F(25))
check("L06 R2 B", (u * 0 - d * 50) / ((u - d) * 1), F(-25))
# Lab: time-0 holdings and rebalancing
sh0 = (75 - 0) / ((u - d) * 100)
b0 = (u * 0 - d * 75) / ((u - d) * Rf)
check("L06 lab time-0 shares", sh0, F(3, 4))
check("L06 lab time-0 bond", b0, F(-30))
check("L06 lab time-0 cost", sh0 * 100 + b0, F(45))
shu = (125 - 0) / ((u - d) * 150)
bu = (u * 0 - d * 125) / ((u - d) * Rf)
check("L06 lab up holdings shares", shu, F(5, 6))
check("L06 lab up holdings bond", bu, F(-50))
check("L06 lab path uu", shu * 225 + bu * Rf, F(125))
check("L06 lab path ud", shu * 75 + bu * Rf, F(0))
check("L06 lab up wealth", sh0 * 150 + b0 * Rf, F(75))
check("L06 lab down wealth", sh0 * 50 + b0 * Rf, F(0))
check("L06 lab rebalance up cost", shu * 150 + bu, F(75))

bad = [x for x in results if not x[1]]
for name, ok, info in results:
    if not ok:
        print("FAIL", name, info)
print(f"checks: {len(results)} pass={len(results) - len(bad)} fail={len(bad)}")
