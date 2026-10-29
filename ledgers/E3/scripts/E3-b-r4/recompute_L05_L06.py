"""Independent recomputation of the L05 and L06 numbers quoted in prose, tables, cards and quiz (E3-b round 4)."""
import math
from fractions import Fraction as F

def ce(tree, g):
    m = sum(p * c ** (1 - g) for p, c in tree)
    return m ** (1 / (1 - g))

def v0(c0, tree, beta, g, psi):
    a = 1 - 1 / psi
    ce1 = ce(tree, g)
    return ((1 - beta) * c0 ** a + beta * ce1 ** a) ** (1 / a)

def u_crra(c, g):
    return c ** (1 - g) / (1 - g)

def eu(c0, tree, beta, g):
    return (1 - beta) * u_crra(c0, g) + beta * sum(p * u_crra(c, g) for p, c in tree)

# L05 exact tree (Fractions)
beta, g, psi, c0 = F(9, 10), F(2), F(1, 2), F(2)
tree = [(F(1, 2), F(1)), (F(1, 2), F(4))]
inv = sum(p * c ** -1 for p, c in tree)
ce1 = 1 / inv
a = 1 - 1 / psi
br = (1 - beta) * c0 ** int(a) + beta * ce1 ** int(a)
V0 = br ** (1 / int(a))
U = eu(c0, tree, beta, g)
print("L05 CE1", ce1, "mean", sum(p * c for p, c in tree), "V0", V0, "U", U, "(1-g)U", (1 - g) * U, "V0^(1-g)", V0 ** int(1 - g))
print("L05 sure at CE1 value", (1 - beta) * c0 ** int(a) + beta * ce1 ** int(a), "->", ((1 - beta) * c0 ** int(a) + beta * ce1 ** int(a)) ** (1 / int(a)))
# E2 variant (prose)
t2 = [(F(1, 4), F(1)), (F(3, 4), F(4))]
inv2 = sum(p * c ** -1 for p, c in t2)
ce2 = 1 / inv2
V2 = (F(1, 20) + F(9, 10) * inv2) ** -1
print("E2 CE", ce2, "V0", V2, float(V2), "80/49", F(80, 49), float(F(80, 49)))
# risky float CE at gamma 0.5, 2, 3 (floats)
for g_ in (0.5, 2.0, 3.0):
    print("L05 CE1 gamma", g_, "%.6f" % ce([(0.5, 1.0), (0.5, 4.0)], g_))
# psi=1/gamma identity for float plan
worst = 0.0
for g_ in (0.5, 2.0, 3.0):
    fp = [(0.3, 0.5), (0.7, 3.0)]
    vf = v0(1.5, fp, 0.95, g_, 1 / g_)
    uf = eu(1.5, fp, 0.95, g_)
    worst = max(worst, abs((1 - g_) * uf - vf ** (1 - g_)) / abs(vf ** (1 - g_)))
print("L05 psi=1/gamma worst rel gap", worst)
# (4,4) and (1,10) at psi=2, gamma=2, beta=1/2
print("L05 U(4,4) %.4f U(1,10) %.4f" % (eu(4.0, [(1.0, 4.0)], 0.5, 2.0), eu(1.0, [(1.0, 10.0)], 0.5, 2.0)))
print("L05 V0(4,4) %.4f V0(1,10) %.4f" % (v0(4.0, [(1.0, 4.0)], 0.5, 2.0, 2.0), v0(1.0, [(1.0, 10.0)], 0.5, 2.0, 2.0)))
# EIS analytic and MRS closed form at (c0,c1)=(2,4), psi=1/2, beta=0.9 vs finite difference
def mrs(c0_, c1_, beta_, psi_):
    h = 1e-6
    dv0 = (v0(c0_ * (1 + h), [(1.0, c1_)], beta_, 2.0, psi_) - v0(c0_ * (1 - h), [(1.0, c1_)], beta_, 2.0, psi_)) / (2 * c0_ * h)
    dv1 = (v0(c0_, [(1.0, c1_ * (1 + h))], beta_, 2.0, psi_) - v0(c0_, [(1.0, c1_ * (1 - h))], beta_, 2.0, psi_)) / (2 * c1_ * h)
    return dv0 / dv1
for ps in (0.5, 2.0, 0.25):
    lo, hi = 0.999 * 4.0, 1.001 * 4.0
    eis = (math.log(hi / 2) - math.log(lo / 2)) / (math.log(mrs(2.0, hi, 0.9, ps)) - math.log(mrs(2.0, lo, 0.9, ps)))
    print("L05 EIS psi=%g estimate %.6f" % (ps, eis))
print("L05 closed-form MRS (2,4) psi=1/2:", (0.1 / 0.9) * 2 ** 2, "numeric", mrs(2.0, 4.0, 0.9, 0.5))
# L06
p, gg, ll = F(1, 2), F(1000), F(600)
EV = p * gg - (1 - p) * ll
print("L06 EV", EV, "lam*", p * gg / ((1 - p) * ll))
for lam in (F(1), F(3, 2), F(2)):
    print("L06 W at", lam, "=", p * gg - (1 - p) * lam * ll)
print("L06 combined at 2:", F(1, 4) * 2000 + F(1, 2) * 400 - F(1, 4) * 2 * 1200, "separate 2W:", 2 * (p * gg - (1 - p) * 2 * ll))
print("L06 combined at 3/2:", F(1, 4) * 2000 + F(1, 2) * 400 - F(1, 4) * F(3, 2) * 1200, "separate:", 2 * (p * gg - (1 - p) * F(3, 2) * ll))
print("L06 sqrt(5/3)", math.sqrt(5 / 3), "W(2) alpha=delta=1/2", 0.5 * 1000 ** 0.5 - 0.5 * 2 * 600 ** 0.5)
print("L06 lam* power", 0.5 * 1000 ** 0.5 / (0.5 * 600 ** 0.5))
# Remark 3.2 cases
EVb = F(1, 3) * 1000 - F(2, 3) * 300
print("R3.2 p=1/3 EV", EVb, "g-EV", 1000 - EVb, "l+EV", 300 + EVb, "ratio", (1000 - EVb) / (300 + EVb), "lam_R", math.sqrt(2) / 2, "=", 0.5 * math.sqrt(2))
print("R3.2 example 2.3 g-EV", 1000 - EV, "l+EV", 600 + EV)
# L06 P1-type numbers
print("L06 M1 lam*", F(1, 3) * 900 / (F(2, 3) * 300), "W(2)", F(1, 3) * 900 - F(2, 3) * 2 * 300)
print("L06 R3 v(1)", 2 + 2 * -1, "v(x+y)", 1)
# Remark 1.5 existence check: two lotteries with mean 5/2 and different CE1 at gamma = 2
from fractions import Fraction as _F
def _ce2(tree):
    return 1 / sum(p * c ** -1 for p, c in tree)
_A = [(_F(1, 2), _F(1)), (_F(1, 2), _F(4))]
_B = [(_F(1, 2), _F(2)), (_F(1, 2), _F(3))]
print("Remark 1.5 pair: means", sum(p * c for p, c in _A), sum(p * c for p, c in _B), "CE1", _ce2(_A), _ce2(_B))
