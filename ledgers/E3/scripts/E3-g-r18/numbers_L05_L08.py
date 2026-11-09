"""Round-18 verifier: independent recomputation of the numbers stated on pages L05-L08 and their cards.
Uses fractions.Fraction and decimal.Decimal (40 digits) and math; prints each claim with the recomputed value."""
import math
from decimal import Decimal, getcontext, ROUND_HALF_UP
from fractions import Fraction as F

getcontext().prec = 60
D = Decimal


def show(label, value):
    print(f"{label}: {value}")


print("== L05")
# exact tree gamma=2, psi=1/2, beta=9/10, c0=2, c1 in {1,4} w.p. 1/2
Om = 1 - 1 / F(1, 2)          # Omega = -1
beta, c0 = F(9, 10), F(2)
Ec1inv = F(1, 2) * 1 + F(1, 2) * F(1, 4)
CE1 = 1 / Ec1inv
show("L05 Omega at psi=1/2", Om)
show("L05 E c1^-1", Ec1inv)
show("L05 CE1 (gamma=2)", CE1)
V0 = ((1 - beta) * c0**Om + beta * CE1**Om) ** (1 / Om)
show("L05 V0 exact tree", V0)
u = lambda c: -1 / c
U = (1 - beta) * u(c0) + beta * (F(1, 2) * u(F(1)) + F(1, 2) * u(F(4)))
show("L05 U exact tree", U)
show("L05 (1-gamma)U == V0^(1-gamma)", (1 - 2) * U == V0 ** (1 - 2))
show("L05 mean c1", F(1, 2) * 1 + F(1, 2) * 4)
sure = ((1 - beta) * c0**Om + beta * F(8, 5) ** Om) ** (1 / Om)
show("L05 sure plan at 8/5 value", sure)
show("L05 M2: V0(c0=1,c1=3,beta=1/2,psi=1/2)", ((F(1, 2) * F(1) ** -1 + F(1, 2) * F(3) ** -1)) ** -1)
show("L05 Remark1.5 CE {2,3} at gamma=2", 1 / (F(1, 2) * F(1, 2) + F(1, 2) * F(1, 3)))
show("L05 Remark1.5 CE {1,4} at gamma=2", 1 / (F(1, 2) * 1 + F(1, 2) * F(1, 4)))
show("L05 M1 CE (1/4 at 1, 3/4 at 3)", 1 / (F(1, 4) * 1 + F(3, 4) * F(1, 3)))
show("L05 theta at gamma=2, psi=2", (1 - 2) / (1 - F(1, 2)))
risky = [(0.5, 1.0), (0.5, 4.0)]
for g in (0.5, 2.0, 3.0):
    m = sum(p * c ** (1 - g) for p, c in risky)
    show(f"L05 risky CE1 gamma={g}", f"{m ** (1 / (1 - g)):.6f}")
# Lab 1 pair at psi=2, gamma=2, beta=1/2
def ez(c0_, plan, b, g, psi):
    om = 1 - 1 / psi
    ce = (sum(p * c ** (1 - g) for p, c in plan)) ** (1 / (1 - g))
    return ((1 - b) * c0_**om + b * ce**om) ** (1 / om)
def crra_eu(c0_, plan, b, g):
    u_ = lambda c: c ** (1 - g) / (1 - g)
    return (1 - b) * u_(c0_) + b * sum(p * u_(c) for p, c in plan)
show("L05 U(4,4)", f"{crra_eu(4.0, [(1.0, 4.0)], 0.5, 2.0):.6f}")
show("L05 U(1,10)", f"{crra_eu(1.0, [(1.0, 10.0)], 0.5, 2.0):.6f}")
show("L05 V0(4,4)", f"{ez(4.0, [(1.0, 4.0)], 0.5, 2.0, 2.0):.6f}")
show("L05 V0(1,10)", f"{ez(1.0, [(1.0, 10.0)], 0.5, 2.0, 2.0):.6f}")
show("L05 EIS exact (analytic) for psi 0.5, 2, 0.25", "0.5, 2, 0.25 (EIS = psi by Prop 2.2)")
# MRS closed form at (2,4), beta 0.9, psi 0.5
show("L05 MRS closed form (2,4)", (0.1 / 0.9) * (4 / 2) ** 2)

print("== L06")
v = lambda x, lam, a, d: x**a if x >= 0 else -lam * (-x) ** d
lam_star = math.sqrt(5 / 3)
show("L06 sqrt(5/3)", f"{lam_star:.6f}")
show("L06 PV(2) alpha=delta=0.5", f"{0.5 * v(1000, 2, .5, .5) + 0.5 * v(-600, 2, .5, .5):.6f}")
show("L06 PV sign below/above lam*", (0.5 * v(1000, lam_star * (1 - 1e-6), .5, .5) + 0.5 * v(-600, lam_star * (1 - 1e-6), .5, .5) > 0,
     0.5 * v(1000, lam_star * (1 + 1e-6), .5, .5) + 0.5 * v(-600, lam_star * (1 + 1e-6), .5, .5) < 0))
show("L06 Ex2.3 PV at 1, 3/2, 2", [F(1, 2) * 1000 + F(1, 2) * (-600) * l for l in (F(1), F(3, 2), F(2))])
show("L06 combined at lam=2", F(1, 4) * 2000 + F(1, 2) * 400 - F(1, 4) * 2 * 1200)
show("L06 separate at lam=2", 2 * (F(1, 2) * 1000 + F(1, 2) * (-600) * 2))
show("L06 E2 lam* 1000/600 alpha=1/2", math.sqrt(1000 / 600))
show("L06 M1 lam*", (F(1, 3) * 900) / (F(2, 3) * 300))
show("L06 M1 PV(2)", F(1, 3) * 900 - F(2, 3) * 2 * 300)
show("L06 E3 combined at 3/2", F(1, 4) * 2000 + F(1, 2) * 400 - F(1, 4) * F(3, 2) * 1200)
show("L06 E3 separate at 3/2", 2 * (F(1, 2) * 1000 + F(1, 2) * (-600) * F(3, 2)))
show("L06 Remark3.2 lambda_R p=1/3 g=1000 l=300 alpha=1/2", (F(1, 3) * (1000 - F(400, 3)) ** 0.5) / (F(2, 3) * (300 + F(400, 3)) ** 0.5))
show("L06 sqrt(2)/2", math.sqrt(2) / 2)
show("L06 R3 v(x+y) v(x)+v(y) at x=2,y=-1,lam=2", (v(1, 2, 1, 1), v(2, 2, 1, 1) + v(-1, 2, 1, 1)))
show("L06 M2 EV/PV", (F(1, 2) * 100 - F(1, 2) * 100, F(1, 2) * 100 - F(1, 2) * 2 * 100))
show("L06 M3 v(16), v(-16), ratio", (v(16, 2, .5, .5), v(-16, 2, .5, .5), v(-16, 2, .5, .5) / v(16, 2, .5, .5)))
show("L06 Example 2.3 CE sign at lam=2 (PV<0)", F(1, 2) * 1000 - F(1, 2) * 2 * 600)

print("== L07")
def om(p, eta=0.5):
    return p**eta / (p**eta + (1 - p) ** eta) ** (1 / eta)
for p in (0.3, 0.6, 0.5, 0.01, 0.05, 0.95, 0.99, 0.4, 0.25):
    show(f"L07 omega({p})", f"{om(p):.10f}")
show("L07 omega(1/4) exact 1/(2+sqrt3)", f"{1 / (2 + math.sqrt(3)):.10f}; 2-sqrt3={2 - math.sqrt(3):.8f}")
show("L07 omega(3/10)/omega(3/5) unrounded", f"{om(0.3) / om(0.6):.10f}")
show("L07 quotient of eight-decimal values", f"{0.28579088 / 0.39125077:.10f}")
show("L07 thresholds", (1 / (1 + 2 ** -1.0), 1 / (1 + 2 ** -0.5)))
show("L07 Remark1.6 sum A", f"{om(0.4) + 2 * om(0.3):.10f}; 2omega(3/10)={2 * om(0.3):.10f}")
show("L07 Gamma(A) alpha=1 (dec)", f"{150 * D(om(0.3))}")
show("L07 Gamma(B) alpha=1 (dec)", f"{100 * D(om(0.6))}")
gA = 150 * om(0.3); gB = 100 * om(0.6)
show("L07 Gamma(A) alpha=1 float", f"{gA:.6f}, Gamma(B) {gB:.6f}, diff {gA - gB:.6f}")
show("L07 Gamma(A) alpha=.5 float", f"{om(0.3) * (50**0.5 + 100**0.5):.6f}; Gamma(B) {om(0.6) * 100**0.5:.6f}")
show("L07 misconception 3 weighted value", f"{om(0.01) * 100 + om(0.99) * 50:.6f}; EV 50.5")
show("L07 over/under", f"over {(om(0.01) - 0.01) * 100:.6f}; under {(0.99 - om(0.99)) * 50:.6f}; net {(om(0.01)-0.01)*100 - (0.99-om(0.99))*50:.6f}")
show("L07 M2 V_omega 100*omega(1/2)", f"{100 * om(0.5):.6f}")
show("L07 omega(0.862) vs p at eta=1 closed form", f"{math.sqrt(0.862) / (1 + 2 * math.sqrt(0.862 * 0.138)):.6f}")
grid = [i / 1000 for i in range(1001)]
gap1 = max(abs(p - math.sqrt(p) / (1 + 2 * math.sqrt(p * (1 - p)))) for p in grid)
show("L07 max gap closed form vs p (eta=1 is identity)", f"{gap1:.6f}")
show("L07 omega(0.278)>p and omega(0.279)<p", (om(0.278) > 0.278, om(0.279) < 0.279, om(0.278), om(0.279)))
show("L07 Tail checks", (1 - F(2, 5), F(3, 10), F(3, 5)))
show("L07 E1 crossing sign", "see above")

print("== L08")
RED_WIN, RED_LOSS = F(110000), F(95000)
ce = lambda p: 1 / (p / RED_WIN + (1 - p) / RED_LOSS)
show("L08 M1 EU CE p=1/2 exact", f"{ce(F(1, 2))} = {float(ce(F(1, 2))):.6f}")
show("L08 M1 closed 4180000/41", f"{F(4180000, 41)} = {float(F(4180000, 41)):.6f}")
show("L08 Model4 maxmin p=1/3", f"{ce(F(1, 3))} = {float(ce(F(1, 3))):.6f}")
show("L08 M1 (quarter prior) exact", f"{ce(F(1, 4))} = {float(ce(F(1, 4))):.8f}; 8360000/85={float(F(8360000, 85)):.8f}; 1672000/17={float(F(1672000, 17)):.8f}")
show("L08 M2 prior 3/4 CE", f"{float(ce(F(3, 4))):.6f}")
show("L08 Model 4 minus initial", f"{float(ce(F(1, 3))) - 100000:.4f}")
show("L08 Model 1 minus initial", f"{float(ce(F(1, 2))) - 100000:.4f}; expected wealth {0.5*110000+0.5*95000}; premium {102500 - float(ce(F(1,2))):.4f} exact {F(22500,41)} = {float(F(22500,41)):.4f}")
show("L08 E1 difference", 103125 - 100000)
show("L08 known urn red", 1 / (F(1, 3) / 110000 + F(2, 3) / 100000))
show("L08 known urn black", 1 / (F(2, 3) / 110000 + F(1, 3) / 100000))
show("L08 known red exact 1650000/16", F(1650000, 16))
show("L08 known black exact 3300000/31", f"{F(3300000, 31)} = {float(F(3300000,31)):.4f}")
# prospect Model 2
Vp = 0.5 * math.sqrt(100) + 0.5 * (-2 * math.sqrt(50))
Vp_exact = D(5) - D(50).sqrt()
inv = -((-Vp_exact / 2) ** 2)
show("L08 Model 2 Vp (dec)", f"{Vp_exact:.12f}")
show("L08 Model 2 inverse CU (dec)", f"{inv:.12f}")
show("L08 Model 2 wealth cents", f"{D(100000) + 100 * inv:.6f}")
show("L08 Model2 whole cents", int((D(100000) + 100 * inv).quantize(D(1), rounding=ROUND_HALF_UP)))
show("L08 Model 2 minus initial", f"{100 * inv:.6f}")
show("L08 Model1 whole", int(D(4180000) / D(41)).__str__())
show("L08 Model 4 whole", int(D(ce(F(1,3)).numerator) / D(ce(F(1,3)).denominator) + D("0.5")))
show("L08 Model 4 exact", str(ce(F(1, 3))))
show("L08 Remark 4.2 midpoint", (F(1, 3) + F(2, 3)) / 2)
# Model 3 by bisection (EZ) with psi=1/2, beta=.95, gamma=2
def ez_ce(psi, beta_):
    gamma = 2.0
    om_ = 1 - 1 / psi
    def value_plan(pl):
        ex = sum(p * c ** (1 - gamma) for c, p in pl)
        return ((1 - beta_) * 100000.0**om_ + beta_ * ex ** (om_ / (1 - gamma))) ** (1 / om_)
    tgt = value_plan([(110000.0, 0.5), (95000.0, 0.5)])
    lo, hi = 94000.0, 111000.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if ((1 - beta_) * 100000.0**om_ + beta_ * (mid ** (1 - gamma)) ** (om_ / (1 - gamma))) ** (1 / om_) < tgt:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2
show("L08 Model3 EZ CE psi=.5 beta=.95 (bisection)", f"{ez_ce(0.5, 0.95):.6f}")
show("L08 Part B EZ CE psi=3 beta=0.9", f"{ez_ce(3.0, 0.9):.6f}")
show("L08 Model 2 bisection not needed", "")
show("L08 lab 2 prospect value 99892.7670", f"{100000 + 100 * (-((2.0710678118654755/2) ** 2)):.4f}")
show("L08 E3 exact premium 22500/41", float(F(22500, 41)))
show("L08 Remark 2.3 maxmin vs average CE", f"{float(ce(F(1,3))):.4f} <= {float(ce(F(1,2))):.4f}")
show("L08 quiz: M2 maxmin (min of CE over {1/4,3/4})", float(min(ce(F(1, 4)), ce(F(3, 4)))))
show("L08 M3 tau=0 CE (max of CE)", float(max(ce(F(1, 4)), ce(F(3, 4)))))
