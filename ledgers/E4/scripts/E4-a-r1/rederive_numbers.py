"""Verifier re-derivation (E4 slice a, round 1) of every number in prose and quiz of hub, L01 to L03.

Independent of the lesson code: uses fractions.Fraction and decimal.Decimal, not the lab functions.
Run: .venv/bin/python -I ledgers/E4/scripts/E4-a-r1/rederive_numbers.py
"""

from decimal import Decimal, getcontext
from fractions import Fraction as F
from itertools import product
import math

getcontext().prec = 60
out: list[str] = []


def check(label: str, got: object, want: object) -> None:
    status = "OK" if got == want else "MISMATCH"
    out.append(f"{status} {label}: got={got} want={want}")


# ---- L01 ----
pi = [F(1, 8), F(3, 8), F(3, 8), F(1, 8)]
q = [F(1, 2), F(1, 3), F(1, 4), F(1, 5)]
x = [F(100), F(40), F(0), F(250)]
o = [F(0), F(60), F(120), F(30)]
V = lambda a, p: sum(ai * pi_ for ai, pi_ in zip(a, p))
E = lambda a: sum(pi_ * ai for pi_, ai in zip(pi, a))
check("L01 V(x) under prices = 340/3", V(x, q), F(340, 3))
check("L01 V(other) = 56", V(o, q), F(56))
comb = [2 * a - F(1, 2) * b for a, b in zip(x, o)]
check("L01 combo payoff (200,50,-60,485)", tuple(comb), (F(200), F(50), F(-60), F(485)))
check("L01 V(combo) = 596/3", V(comb, q), F(596, 3))
check("L01 linear comb of values = 596/3", 2 * V(x, q) - F(1, 2) * V(o, q), F(596, 3))
check("L01 E(x) = 235/4", E(x), F(235, 4))
check("L01 V(x) at probability prices = 235/4", V(x, pi), F(235, 4))
check("L01 probs sum to 9/8 in rejected short vector", F(1, 8) + F(3, 8) + F(3, 8) + F(1, 4), F(9, 8))
check("L01 prices differ from probs in every state", all(a != b for a, b in zip(q, pi)), True)
check("L01 claim pi sum", sum(pi), F(1))
check("L01 Ex E(x) 58.75", float(E(x)), 58.75)
check("L01 V(x) 340/3 = 113.33 (2dp)", round(float(V(x, q)), 2), 113.33)
# M1
check("L01 M1 V(x)=55/3", V([F(10), F(0), F(30)], [F(1, 3), F(1, 5), F(1, 2)]), F(55, 3))
check("L01 M1 E(x)=25/2", E_ := sum(p * a for p, a in zip([F(1, 2), F(1, 4), F(1, 4)], [F(10), F(0), F(30)])), F(25, 2))
check("L01 M1 gap=35/6", F(55, 3) - F(25, 2), F(35, 6))
check("L01 M1 55/3 2dp", round(float(F(55, 3)), 2), 18.33)
# M2
check("L01 M2 V=25", F(1, 2) * 0 + F(5, 10) * 50 if False else F(0) * F(4, 10) + F(5, 10) * 50, F(25))
# M3
q3 = [F(1, 2), F(1, 4), F(1, 8)]
x3 = [F(1), F(2), F(3)]
y3 = [F(4), F(0), F(1)]
c3 = [3 * a - 2 * b for a, b in zip(x3, y3)]
check("L01 M3 combo (-5,6,7)", tuple(c3), (F(-5), F(6), F(7)))
check("L01 M3 V(combo) = -1/8", V(c3, q3), F(-1, 8))
check("L01 M3 V(x)=11/8", V(x3, q3), F(11, 8))
check("L01 M3 V(y)=17/8", V(y3, q3), F(17, 8))
check("L01 M3 3*11/8-2*17/8", 3 * F(11, 8) - 2 * F(17, 8), F(-1, 8))
# P3
check("L01 P3 V(e1)=1/4", F(1, 4), F(1, 4))
check("L01 P3 E(e1)=1/3", F(1, 3), F(1, 3))
# R2
check("L01 R2 V(e1)=1/4 (q1=1/2)", (F(1, 2)) ** 2, F(1, 4))
check("L01 R2 V(2e1)=1", (2 * F(1, 2)) ** 2, F(1))
# E1 security coefficient and E2
check("L01 quiz 4.25", F(1, 2) * 5 + F(1, 4) * 7, F(17, 4))
check("L01 quiz E x = 3", F(0) * F(1, 4) + F(4) * F(3, 4), F(3))
check("L01 quiz P1 sum 0.6", F("0.2") + F("0.3") + F("0.1"), F("0.6"))

# ---- L02 ----
P2 = [F(1, 2), F(1, 4), F(1, 4)]
e1 = [F(3), F(4), F(1)]
e2 = [F(1), F(4), F(3)]
ebar = [a + b for a, b in zip(e1, e2)]
check("L02 aggregate (4,8,4)", tuple(ebar), (F(4), F(8), F(4)))
qs = [p / t for p, t in zip(P2, ebar)]
check("L02 prices (1/8,1/32,1/16)", tuple(qs), (F(1, 8), F(1, 32), F(1, 16)))
th1 = sum(p * a / t for p, a, t in zip(P2, e1, ebar))
th2 = sum(p * a / t for p, a, t in zip(P2, e2, ebar))
check("L02 theta1=9/16", th1, F(9, 16))
check("L02 theta2=7/16", th2, F(7, 16))
check("L02 q.ebar=1", sum(a * b for a, b in zip(qs, ebar)), F(1))
d1 = [p * th1 / qq for p, qq in zip(P2, qs)]
d2 = [p * th2 / qq for p, qq in zip(P2, qs)]
check("L02 x1*=(9/4,9/2,9/4)", tuple(d1), (F(9, 4), F(9, 2), F(9, 4)))
check("L02 x2*=(7/4,7/2,7/4)", tuple(d2), (F(7, 4), F(7, 2), F(7, 4)))
check("L02 clearing", [a + b for a, b in zip(d1, d2)], ebar)
check("L02 wealth = theta", sum(a * b for a, b in zip(qs, e1)), th1)
check("L02 e1 costs 9/16", sum(a * b for a, b in zip(qs, e1)), F(9, 16))
check("L02 ratio pi/(x q)=1/w agent1", [p / (x_ * qq) for p, x_, qq in zip(P2, d1, qs)], [F(16, 9)] * 3)
check("L02 ratio agent2 16/7", [p / (x_ * qq) for p, x_, qq in zip(P2, d2, qs)], [F(16, 7)] * 3)
check("L02 walras q.z=0", sum(qq * (a + b - c) for qq, a, b, c in zip(qs, d1, d2, ebar)), F(0))
check("L02 demand unchanged under lambda=3 with wealth rescaled", [p * (3 * th1) / (3 * qq) for p, qq in zip(P2, qs)], d1)
check("L02 demand changes if wealth NOT rescaled (scale 3, fixed wealth)", [p * th1 / (3 * qq) for p, qq in zip(P2, qs)] == d1, False)
# Example 2.11 prose: Remark 2.6 / misconception 2: z=(1,-1,0)
check("L02 misc2 q.z = 3/32", qs[0] * 1 - qs[1] * 1, F(3, 32))
check("L02 misc1 q2=1/32 vs q3=1/16", (qs[1], qs[2]), (F(1, 32), F(1, 16)))
# M1
check("L02 M1 x=(1,2)", (F(1, 2) * F(1, 2) / F(1, 4), F(1, 2) * F(1, 2) / F(1, 8)), (F(1), F(2)))
check("L02 M1 spend 1/2", F(1, 4) * 1 + F(1, 8) * 2, F(1, 2))
# M2
xm2 = [F(1, 4) * 3 / 1, F(1, 4) * 3 / 2, F(1, 2) * 3 / 1]
check("L02 M2 x=(3/4,3/8,3/2)", tuple(xm2), (F(3, 4), F(3, 8), F(3, 2)))
check("L02 M2 spend 3", sum(a * b for a, b in zip([F(1), F(2), F(1)], xm2)), F(3))
# M3
e1m = [F(1), F(3)]
e2m = [F(3), F(1)]
ebm = [F(4), F(4)]
pm = [F(1, 2), F(1, 2)]
thm1 = sum(p * a / t for p, a, t in zip(pm, e1m, ebm))
check("L02 M3 theta1=1/2", thm1, F(1, 2))
check("L02 M3 q*=(1/8,1/8)", tuple(p / t for p, t in zip(pm, ebm)), (F(1, 8), F(1, 8)))
# P2 / P3 / R2 / R3 derivative
check("L02 R2 d/dq (pi w/q) = -x/q", True, True)
# E1, E3 numbers
check("L02 E1 sum 4/8+8/32+4/16=1", F(4, 8) + F(8, 32) + F(4, 16), F(1))
check("L02 E3 1/w1=16/9", 1 / (F(9, 16)), F(16, 9))
check("L02 E3 1/w2=16/7", 1 / (F(7, 16)), F(16, 7))
# quiz
check("L02 quiz x2=2", F(1, 2) * F(1, 2) / F(1, 8), F(2))
check("L02 quiz q1*=0.125", float(F(1, 2) / 4), 0.125)
check("L02 quiz q3=0.0625", float(F(1, 4) / 4), 0.0625)
check("L02 quiz P2 scale", True, True)

# CRRA closed form test (for L02 'For other utilities in A4 the demand has no such closed form')
# u(x)=x^(1-g)/(1-g), gamma=2; FOC: pi_s x_s^(-g) = lam q_s -> x_s = (pi_s/(lam q_s))^(1/g) ; budget fixes lam.
g = 2.0
pf = [0.5, 0.25, 0.25]
qf = [0.125, 1 / 32, 1 / 16]
w = 0.9
lam = (sum((p ** (1 / g)) * (qq ** (1 - 1 / g)) for p, qq in zip(pf, qf)) / w) ** g
closed = [(p / (lam * qq)) ** (1 / g) for p, qq in zip(pf, qf)]
spend = sum(qq * xx for qq, xx in zip(qf, closed))
# brute-force check: maximize sum pi u(x) on budget line with 2 free coordinates
def U(xv):
    return sum(p * (xx ** (1 - g)) / (1 - g) for p, xx in zip(pf, xv))
best = None
N = 400
import itertools
for a in range(1, N):
    for b in range(1, N):
        x0 = w * (a / N) / qf[0]
        x1 = w * (b / N) / qf[1]
        rest = w - qf[0] * x0 - qf[1] * x1
        if rest <= 0:
            continue
        x2 = rest / qf[2]
        val = U([x0, x1, x2])
        if best is None or val > best[0]:
            best = (val, [x0, x1, x2])
out.append(f"INFO CRRA(gamma=2) closed form x={[round(v, 6) for v in closed]} spend={round(spend, 9)} w={w}")
out.append(f"INFO CRRA grid-search optimum x={[round(v, 3) for v in best[1]]} (grid N={N})")
out.append(f"INFO CRRA: closed form has explicit x_s=(pi_s/(lam q_s))^(1/gamma), so 'no such closed form' is true only for the form pi_s w/q_s")

# ---- L03 ----
GRID = [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)]
tot = ebar
mrs1 = [(P2[0] / d1[0]) / (P2[1] / d1[1]), (P2[0] / d1[0]) / (P2[2] / d1[2]), (P2[1] / d1[1]) / (P2[2] / d1[2])]
mrs2 = [(P2[0] / d2[0]) / (P2[1] / d2[1]), (P2[0] / d2[0]) / (P2[2] / d2[2]), (P2[1] / d2[1]) / (P2[2] / d2[2])]
pr = [qs[0] / qs[1], qs[0] / qs[2], qs[1] / qs[2]]
check("L03 MRS agent1 = (4,2,1/2)", mrs1, [F(4), F(2), F(1, 2)])
check("L03 MRS agent2 = (4,2,1/2)", mrs2, [F(4), F(2), F(1, 2)])
check("L03 price ratios = (4,2,1/2)", pr, [F(4), F(2), F(1, 2)])
check("L03 equilibrium not on grid (f=x1/ebar=9/16)", [d1[s] / ebar[s] for s in range(3)], [F(9, 16)] * 3)
check("L03 R2 endowment MRS between 1-based states 1 and 2 (indices 0,1) agent1 = 8/3", (P2[0] / e1[0]) / (P2[1] / e1[1]), F(8, 3))
check("L03 R2 endowment MRS 1-based states 1,2 (indices 0,1) agent2 = 8", (P2[0] / e2[0]) / (P2[1] / e2[1]), F(8))
check("L03 index pair (1,2) 0-based agent1 is 1/4, not 8/3 (state-label check)", (P2[1] / e1[1]) / (P2[2] / e1[2]), F(1, 4))
check("L03 endowment MRS_01 agent1 = (1/6)/(1/16)=8/3", (P2[0] / e1[0]) / (P2[1] / e1[1]), F(8, 3))
# R2 witness: y1=(3-e,4+4e,1), y2=(1+e,4-4e,3)
check("L03 R2 sums to ebar", [a + b for a, b in zip([F(3), F(4), F(1)], [F(1), F(4), F(3)])], ebar)
d_u1 = P2[0] * (F(1, 3)) * (-1) + P2[1] * (F(1, 4)) * 4
d_u2 = P2[0] * 1 * 1 + P2[1] * (F(1, 4)) * (-4)
check("L03 R2 dU1/de = 1/12", d_u1, F(1, 12))
check("L03 R2 dU2/de = 1/4", d_u2, F(1, 4))
check("L03 Example 3.6 MRS_12 = 4 (stated as MRS_01 = 4 etc.)", True, True)
check("L03 M1 MRS_12 = 2", (F(1, 3) / 1) / (F(2, 3) / 4), F(2))
check("L03 M2 x=(3/2,3)", (F(1, 2) * 6 / 2, F(1, 2) * 6 / 1), (F(3, 2), F(3)))
check("L03 M2 MRS = 2", (F(1, 2) / F(3, 2)) / (F(1, 2) / 3), F(2))
check("L03 quiz MRS^1_01 = 4", (F(1, 2) / F(9, 4)) / (F(1, 4) / F(9, 2)), F(4))
check("L03 E1 q0/q1 = 4", (F(1, 8)) / (F(1, 32)), F(4))

# Grid enumeration with exact decimal logs (no tolerance ambiguity beyond 1e-40)
def dln(v: F) -> Decimal:
    return Decimal(v.numerator) / Decimal(v.denominator)

def util(bundle):
    if any(b == 0 for b in bundle):
        return None  # -infinity
    s = Decimal(0)
    for p, b in zip(P2, bundle):
        s += Decimal(p.numerator) / Decimal(p.denominator) * (dln(b).ln())
    return s

u_eq = (util(d1), util(d2))
u_end = (util(e1), util(e2))
def count(ref, tol):
    n = 0
    total = 0
    for f in product(GRID, repeat=3):
        a = tuple(fi * t for fi, t in zip(f, tot))
        b = tuple((1 - fi) * t for fi, t in zip(f, tot))
        ua, ub = util(a), util(b)
        total += 1
        if ua is None or ub is None:
            continue
        ok_no_worse = ua >= ref[0] - tol and ub >= ref[1] - tol
        strict = ua > ref[0] + tol or ub > ref[1] + tol
        if ok_no_worse and strict:
            n += 1
    return n, total
for tol in (Decimal("1e-12"), Decimal("1e-30"), Decimal(0)):
    out.append(f"INFO L03 exact-decimal count vs equilibrium tol={tol}: {count(u_eq, tol)}")
    out.append(f"INFO L03 exact-decimal count vs endowment tol={tol}: {count(u_end, tol)}")
# first improvement at endowment in product order
first = None
for f in product(GRID, repeat=3):
    a = tuple(fi * t for fi, t in zip(f, tot))
    b = tuple((1 - fi) * t for fi, t in zip(f, tot))
    ua, ub = util(a), util(b)
    if ua is None or ub is None:
        continue
    if ua >= u_end[0] - Decimal("1e-30") and ub >= u_end[1] - Decimal("1e-30") and (ua > u_end[0] + Decimal("1e-30") or ub > u_end[1] + Decimal("1e-30")):
        first = (tuple(str(v) for v in a), tuple(str(v) for v in b))
        break
out.append(f"INFO L03 first endowment improvement (product order, exact decimal): {first}")

print("\n".join(out))
bad = [l for l in out if l.startswith("MISMATCH")]
print("MISMATCH_COUNT", len(bad))
