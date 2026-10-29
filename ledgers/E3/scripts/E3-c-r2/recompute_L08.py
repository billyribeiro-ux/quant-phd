"""Independent recomputation of L08 numbers (E3-c round 2). Exact fractions where possible, floats at full precision."""
import math
from fractions import Fraction as F

W0, W1, WL = 100000, 110000, 95000   # initial wealth, red outcome, loss outcome (cents)

def ce_crra2(p):  # u(W) = -1/W, CE = 1/E[1/W], p = P(red)  (exact)
    return 1 / (F(p) / W1 + (1 - F(p)) / WL)

print("EU CE p=1/2 exact", ce_crra2(F(1, 2)), float(ce_crra2(F(1, 2))))
print("4180000/41", F(4180000, 41), float(F(4180000, 41)))
print("CE p=1/4 exact", ce_crra2(F(1, 4)), float(ce_crra2(F(1, 4))))
print("8360000/85", F(8360000, 85), float(F(8360000, 85)), "1672000/17", float(F(1672000, 17)))
print("inner sum 1/440000+3/380000", F(1, 440000) + F(3, 380000), "=85/8360000?", F(1, 440000) + F(3, 380000) == F(85, 8360000))
print("expected final wealth p=1/4", F(1, 4) * W1 + F(3, 4) * WL, " p=1/2", F(1, 2) * W1 + F(1, 2) * WL)
print("premium p=1/2 exact", F(102500) - F(4180000, 41), float(F(102500) - F(4180000, 41)), "= 22500/41?", F(102500) - F(4180000, 41) == F(22500, 41))
print("premium CU", float((F(102500) - F(4180000, 41)) / 100))
print("maxmin p=1/3", ce_crra2(F(1, 3)), float(ce_crra2(F(1, 3))))
print("CE p=3/4", float(ce_crra2(F(3, 4))), "CE p=1/4", float(ce_crra2(F(1, 4))))
print("M3 alpha=0 CE over {1/4,3/4} = 1/min g: ", float(1 / min(F(1,4)/W1+F(3,4)/WL, F(3,4)/W1+F(1,4)/WL)))
print("full-set maxmin p=0 CE", float(ce_crra2(F(0))))
print("known urn red", float(ce_crra2(F(1, 3))), "known black (q=2/3 black)", float(1/(F(2,3)/W1 + F(1,3)/W0)))
print("ambiguous black worst (black prob 0)", float(1/(F(0)/W1 + F(1)/W0)))
print("known red Ex2.5", float(1/(F(1,3)/W1 + F(2,3)/W0)))
# alpha-MEU alpha=1/2 over 30..60
g = lambda p: p / W1 + (1 - p) / WL
pr = [F(k, 90) for k in range(30, 61)]
mean_p = sum(pr, F(0)) / len(pr)
print("P-bar", mean_p, "mean of k/90 over 30..60", mean_p == F(1, 2))
print("alpha-MEU 1/2 exact", 1 / (F(1, 2) * max(g(p) for p in pr) + F(1, 2) * min(g(p) for p in pr)))
print("maxmin exact", 1 / max(g(p) for p in pr), float(1 / max(g(p) for p in pr)))
# prospect model
v = lambda x: x ** 0.5 if x >= 0 else -2 * (-x) ** 0.5
Vp = 0.5 * v(100) + 0.5 * v(-50)
print("prospect V", Vp, "5 - sqrt50", 5 - math.sqrt(50))
inv = -((-Vp / 2) ** 2)
print("prospect CU CE of change", inv, "wealth", W0 + 100 * inv)
# Epstein-Zin closed check at psi=1/2 beta=.95
rho = 1 - 1 / 0.5
print("rho psi=1/2", rho)
# Model 4 / Remark 4.2
print("g(1/3),g(2/3),g(1/2)", float(g(F(1,3))), float(g(F(2,3))), float(g(F(1,2))))
print("mid identity", float(g(F(1,3)) + g(F(2,3))) / 2 == float(g(F(1,2))))
print("max g at p_min?", g(F(1,3)) > g(F(2,3)))
# Remark: maxmin 'worst prior gives CE' vs average ambiguous
print("Maxmin 99523.8095 <= 101951.2195", float(1/max(g(p) for p in pr)) <= float(F(4180000,41)))
# Example 2.5 with CRRA: sanity check that 103125 and 106451.6129 use u=-1/W
print("ex2.5 black exact", float(1/(F(2,3)/W1 + F(1,3)/W0)), float(F(106451.6129)) if False else "")
print("ex2.5 black exact 200000/31", F(200000, 31) + 100000, float(F(200000,31)+100000))
# prospect value with mid: EU with u=sqrt? (check Example 2.5 is not sqrt)
print("ex2.5 with u=W (linear) would be EV: ", float(F(1,3)*W1+F(2,3)*W0), float(F(2,3)*W1+F(1,3)*W0))
# Model 2 Prospect rounding etc
print("whole cents prospect", round(W0 + 100*inv, 4))
print("exact alpha-MEU equals EU (fraction)", 1/(F(1,2)*max(g(p) for p in [F(1,3),F(2,3)]) + F(1,2)*min(g(p) for p in [F(1,3),F(2,3)])) == F(4180000,41))
