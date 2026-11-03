"""Independent recomputation of the numbers printed in cards E3-c078..c176 (L05-L08) and in prose
of L05-L08, with exact fractions and high-precision floats. Stdlib only.
Usage: python -I verify_numbers_g3.py
"""
import math
from fractions import Fraction as F
from decimal import Decimal, getcontext

getcontext().prec = 50

def p(label, value):
    print(f"{label}: {value}")

print("== L05 ==")
# Remark 1.5 / Corollary: CE at gamma=2 of c1 in {1,4} and {2,3}
p("CE(1,4 @1/2) gamma=2 exact", 1 / ((F(1, 2) * 1 + F(1, 2) * F(1, 4)) ))  # CE^-1 = E c^-1
p("CE(2,3 @1/2) gamma=2 exact", 1 / (F(1, 2) * F(1, 2) + F(1, 2) * F(1, 3)))
# Problem M1: c1 = 1 w.p. 1/4, 3 w.p. 3/4, gamma=2
p("M1 CE exact", 1 / (F(1, 4) * 1 + F(3, 4) * F(1, 3)))
p("M1 mean", F(1, 4) * 1 + F(3, 4) * 3)
# Lab tree: beta=9/10, psi=1/2 (a=-1), c0=2, gamma=2
beta, c0 = F(9, 10), F(2)
ce = F(8, 5)
v0 = 1 / ((1 - beta) / c0 + beta / ce)
p("V0 exact (a=-1)", v0)
u = F(0)
uc0 = -1 / c0
eu1 = F(1, 2) * (-1) + F(1, 2) * F(-1, 4)
U = (1 - beta) * uc0 + beta * eu1
p("U exact", U)
p("(1-gamma)U == V0^(1-gamma)", (-U) == 1 / v0)
# E2: probs 1/4, 3/4 for c1 = 1, 4
ce2 = 1 / (F(1, 4) + F(3, 4) * F(1, 4))
v2 = 1 / ((1 - beta) / c0 + beta / ce2)
p("E2 CE (16/7 expected)", ce2)
p("E2 V0 (160/71 expected)", v2)
# M2: beta=1/2, psi=1/2, c0=1, c1=3, a=-1
v_m2 = 1 / ((F(1, 2)) * 1 + F(1, 2) * F(1, 3))
p("M2 V0 (3/2 expected)", v_m2)
# M3 theta at gamma=2, psi=2: a=1/2
p("M3 theta (-2 expected)", (1 - 2) / (1 - F(1, 2)))
# Corollary 3.3 example at psi=2, gamma=2, beta=1/2
def ez(c0_, plan, b, g, psi):
    a = 1 - 1 / psi
    ce_ = (sum(pr * c ** (1 - g) for pr, c in plan)) ** (1 / (1 - g))
    return ((1 - b) * c0_ ** a + b * ce_ ** a) ** (1 / a)
def crra_u(c, g):
    return c ** (1 - g) / (1 - g)
def eu(c0_, plan, b, g):
    return (1 - b) * crra_u(c0_, g) + b * sum(pr * crra_u(c, g) for pr, c in plan)
p("L05 (4,4) U", eu(4.0, [(1.0, 4.0)], 0.5, 2.0))
p("L05 (1,10) U", eu(1.0, [(1.0, 10.0)], 0.5, 2.0))
p("L05 (4,4) V0", ez(4.0, [(1.0, 4.0)], 0.5, 2.0, 2.0))
p("L05 (1,10) V0", ez(1.0, [(1.0, 10.0)], 0.5, 2.0, 2.0))
# CE1 of the risky float tree at gamma=0.5,2,3
for g in (0.5, 2.0, 3.0):
    ce_g = (0.5 * 1.0 ** (1 - g) + 0.5 * 4.0 ** (1 - g)) ** (1 / (1 - g))
    p(f"L05 CE1 gamma={g}", f"{ce_g:.6f}")
# Remark 3.4 / Remark 2.3 deterministic
p("L05 remark 1.5 mean", F(5, 2))

print("== L06 ==")
p("EV", F(1, 2) * 1000 - F(1, 2) * 600)
p("lambda* (linear)", F(1, 2) * 1000 / (F(1, 2) * 600))
for lam in (F(1), F(3, 2), F(2)):
    p(f"W at lambda={lam}", F(1, 2) * 1000 - F(1, 2) * lam * 600)
p("combined at 2", F(1, 4) * 2000 + F(1, 2) * 400 - F(1, 4) * 2 * 1200)
p("separate sum at 2", 2 * (F(1, 2) * 1000 - F(1, 2) * 2 * 600))
p("power lambda* (sqrt(5/3))", math.sqrt(5 / 3))
p("power W at lambda=2, alpha=delta=0.5", f"{0.5*math.sqrt(1000) - 0.5*2*math.sqrt(600):.6f}")
p("R2 (L06) combined at 3/2", F(700) - 300 * F(3, 2))
p("R2 separate at 3/2", 1000 - 600 * F(3, 2))
p("Remark 3.2 lambda_R (p=1/3, g=1000, l=300, alpha=1/2)",
  f"{(1/3*math.sqrt(1000-(F(400,3))))/((2/3)*math.sqrt(300+F(400,3))):.6f}, sqrt(2)/2={math.sqrt(2)/2:.6f}")
p("M1 L06 lambda*", (F(1, 3) * 900) / (F(2, 3) * 300))
p("M1 L06 W at 2", F(1, 3) * 900 - F(2, 3) * 2 * 300)
p("M2 L06 W", F(1, 2) * 100 - F(1, 2) * 2 * 100)
p("R3 L06 v(1)+v(-1)*2 check", (2 + 2 * -1, 1))

print("== L07 ==")
def omega(pr, eta=0.5):
    return pr ** eta / (pr ** eta + (1 - pr) ** eta) ** (1 / eta)
w310, w35, w12 = omega(0.3), omega(0.6), omega(0.5)
p("omega(3/10)", f"{w310:.10f}")
p("omega(3/5)", f"{w35:.10f}")
p("omega(1/2)", f"{w12:.10f}  1/(2 sqrt2)={1/(2*math.sqrt(2)):.10f}")
ratio = w310 / w35
p("ratio omega(3/10)/omega(3/5)", f"{ratio:.10f}")
p("threshold alpha=1", 2 / 3)
p("threshold alpha=1/2", f"{1/(1+2**-0.5):.10f}")
p("Gamma(A) alpha=1", f"{w310*(50+100):.8f}")
p("Gamma(B) alpha=1", f"{w35*100:.8f}")
p("Gamma(A) alpha=1/2", f"{w310*(50**0.5+100**0.5):.6f}")
p("Gamma(B) alpha=1/2", f"{w35*100**0.5:.6f}")
p("difference alpha=1 (unrounded)", f"{w310*150 - w35*100:.8f}")
p("omega(1/4) closed", f"{omega(0.25):.10f}  2-sqrt3={2-math.sqrt(3):.10f}")
p("omega(0.01)*100+omega(0.99)*50", f"{omega(0.01)*100+omega(0.99)*50:.6f}; EV={0.01*100+0.99*50}")
p("omega(0.01), omega(0.99)", f"{omega(0.01):.8f} {omega(0.99):.8f}")
p("2*omega(3/10)", f"{2*w310:.8f}")
# grid observations
grid = [i / 1000 for i in range(1001)]
diffs = [omega(x) - x for x in grid[1:-1]]
changes = sum(1 for a, b in zip(diffs, diffs[1:]) if (a > 0) != (b > 0))
above = [x for x in grid[1:-1] if omega(x) > x]
p("grid sign changes (interior)", changes)
p("grid last omega>p", max(above))
p("grid first omega<p", min(x for x in grid[1:-1] if omega(x) < x))
closed_gap_eta1 = max(abs(x - math.sqrt(x) / (1 + 2 * math.sqrt(x * (1 - x)))) for x in grid if 0 < x < 1)
p("closed-form gap at eta=1 (grid)", f"{closed_gap_eta1:.4e}")
p("E2 L07 difference rounded", f"{w310*150 - w35*100:.4f}")
p("L07 wFull at 0.01/0.05", f"{omega(0.01):.4f} {omega(0.05):.4f}")

print("== L08 ==")
W1, WL, W0 = F(110000), F(95000), F(100000)
def ce_inv(pr):
    return pr / W1 + (1 - pr) / WL
p("EU CE = 4180000/41", float(1 / ce_inv(F(1, 2))))
p("EU CE exact", 1 / ce_inv(F(1, 2)))
p("maxmin CE (1/3)", float(1 / ce_inv(F(1, 3))))
p("maxmin CE exact", 1 / ce_inv(F(1, 3)))
p("CE at prior 2/3", float(1 / ce_inv(F(2, 3))))
p("M1 CE (1/4) exact", 1 / ce_inv(F(1, 4)), )
p("M1 CE float", float(1 / ce_inv(F(1, 4))))
p("M2 CE at 3/4", float(1 / ce_inv(F(3, 4))))
p("M3 tau=0 CE (3/4)", float(1 / ce_inv(F(3, 4))))
p("M1 inner sum exact", ce_inv(F(1, 4)))
p("EU premium exact", F(102500) - 1 / ce_inv(F(1, 2)))
p("EU premium float", float(F(102500) - 1 / ce_inv(F(1, 2))))
p("maxmin shortfall", float(W0 - 1 / ce_inv(F(1, 3))))
p("full set worst prior CE", float(1 / ce_inv(F(0))))
p("Example 2.5 known red CE", float(1 / (F(1, 3) / 110000 + F(2, 3) / 100000)))
p("Example 2.5 known black CE", float(1 / (F(2, 3) / 110000 + F(1, 3) / 100000)))
p("Example 2.5 ambiguous (full set) red CE", float(min(1 / (F(k, 90) / 110000 + (1 - F(k, 90)) / 100000) for k in range(91))))
p("Remark 2.3 maxmin vs average CE", (float(1 / ce_inv(F(1, 3))), float(1 / ce_inv(F(1, 2)))))
p("E1 L08 known - maxmin red", float(1 / (F(1, 3) / 110000 + F(2, 3) / 100000) - 100000))
# Prospect model
V = 0.5 * math.sqrt(100) + 0.5 * (-2 * math.sqrt(50))
p("prospect V", f"{V:.8f}")
inv = -((-V / 2) ** 2)
p("prospect CE of change (CU)", f"{inv:.8f}; cents {inv*100:.6f}; wealth {100000 + 100*inv:.6f}")
# Epstein-Zin CE by bisection: psi=1/2 beta=0.95 gamma=2 (should equal 101951.2195)
def ez_val(c0_, dist, psi, beta_):
    a = 1 - 1 / psi
    e = sum(pr * c ** (1 - 2.0) for c, pr in dist)
    return ((1 - beta_) * c0_ ** a + beta_ * e ** (a / (1 - 2.0))) ** (1 / a)
target = ez_val(100000.0, [(110000.0, 0.5), (95000.0, 0.5)], 0.5, 0.95)
lo, hi = 95000.0 - 1000, 110000.0 + 1000
for _ in range(200):
    mid = (lo + hi) / 2
    if ez_val(100000.0, [(mid, 1.0)], 0.5, 0.95) < target:
        lo = mid
    else:
        hi = mid
p("EZ CE by bisection (expect 101951.2195)", f"{(lo+hi)/2:.6f}")
