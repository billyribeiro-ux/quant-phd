"""Independent exact re-derivation of the numbers on the L05-L08 cards (Fractions where rational, floats otherwise).

Run: python -I ledgers/E3/scripts/E3-g-r3/verify_numbers.py
"""
import math
from fractions import Fraction as F

out = []


def show(name, value, shown):
    out.append(f"{name}: {shown}")


# ---- L05: two-period Epstein-Zin, exact tree gamma=2, psi=1/2, beta=9/10, c0=2, c1 in {1,4} w.p. 1/2
g, psi, beta, c0 = F(2), F(1, 2), F(9, 10), F(2)
a = 1 - 1 / psi
ce1 = (F(1, 2) * F(1) ** (1 - g) + F(1, 2) * F(4) ** (1 - g)) ** (1 / (1 - g))
show("L05 CE1 (gamma=2, tree {1,4})", ce1, str(ce1))
V0 = ((1 - beta) * c0**a + beta * ce1**a) ** (1 / a)
show("L05 V0 (psi=1/2)", V0, f"{V0} = {float(V0):.6f}")
U = (1 - beta) * (c0 ** (1 - g) / (1 - g)) + beta * (F(1, 2) * (F(1) ** (1 - g) / (1 - g)) + F(1, 2) * (F(4) ** (1 - g) / (1 - g)))
show("L05 U", U, str(U))
show("L05 (1-g)U == V0^(1-g)", None, str((1 - g) * U == V0 ** (1 - g)))
# E2 variant: P(c1=1)=1/4, P(c1=4)=3/4
ce1b = (F(1, 4) * F(1) ** (1 - g) + F(3, 4) * F(4) ** (1 - g)) ** (1 / (1 - g))
V0b = ((1 - beta) * c0**a + beta * ce1b**a) ** (1 / a)
show("L05 E2 CE1", ce1b, str(ce1b))
show("L05 E2 V0", V0b, str(V0b))
# Remark 1.5 CE for {1,4} and {2,3} at gamma=2
ce_23 = (F(1, 2) * F(2) ** (1 - g) + F(1, 2) * F(3) ** (1 - g)) ** (1 / (1 - g))
show("L05 Remark 1.5 CE {2,3}", ce_23, str(ce_23))
# risky tree CE at gamma 0.5, 2, 3 (floats)
for gg in (0.5, 2.0, 3.0):
    ce = ((0.5 * 1.0 ** (1 - gg) + 0.5 * 4.0 ** (1 - gg))) ** (1 / (1 - gg))
    show(f"L05 risky CE1 gamma={gg}", ce, f"{ce:.6f}")
# psi=2, beta=1/2 plans
def ez(c0_, plan, b, psi_):
    aa = 1 - 1 / psi_
    ce = sum(p * c for p, c in plan)  # placeholder not used
    return None
# deterministic: V0 = [(1-b) c0^a + b c1^a]^(1/a), a = 1 - 1/psi
for (c0_, c1_), label in (((4.0, 4.0), "(4,4)"), ((1.0, 10.0), "(1,10)")):
    aa = 1 - 1 / 2.0
    V = ((1 - 0.5) * c0_**aa + 0.5 * c1_**aa) ** (1 / aa)
    uu = 0.5 * (-1 / c0_) + 0.5 * (-1 / c1_)
    show(f"L05 plan {label} V0 (psi=2,beta=1/2)", V, f"{V:.6f}")
    show(f"L05 plan {label} U (gamma=2)", uu, f"{uu:.6f}")
# E1 check: V0^{-1} = (1-b)/c0 + b E c1^{-1}
show("L05 E1 V0^-1 = 49/80", None, str(F(1, 20) + F(9, 10) * F(5, 8)))

# ---- L06
p, g_, l_ = F(1, 2), F(1000), F(600)
EV = p * g_ - (1 - p) * l_
lam_star = p * g_ / ((1 - p) * l_)
show("L06 EV", EV, str(EV))
show("L06 lam*", lam_star, str(lam_star))
for lam in (F(1), F(3, 2), F(2)):
    show(f"L06 W(lam={lam})", None, str(p * g_ - (1 - p) * lam * l_))
show("L06 combined 700-300*2", None, str(F(700) - 300 * 2))
show("L06 separate 2*(500-300*2)", None, str(2 * (500 - 300 * 2)))
show("L06 combined at 3/2", None, str(F(700) - 300 * F(3, 2)))
show("L06 separate at 3/2", None, str(1000 - 600 * F(3, 2)))
lam_pow = math.sqrt(1000) / math.sqrt(600)
show("L06 power threshold (alpha=delta=1/2)", lam_pow, f"{lam_pow:.6f} vs sqrt(5/3)={math.sqrt(5/3):.6f}")
W_pow = 0.5 * math.sqrt(1000) - 0.5 * 2 * math.sqrt(600)
show("L06 W at lam=2 (alpha=delta=1/2)", W_pow, f"{W_pow:.6f}")
# Remark 3.2 lambda_R for p=1/3, g=1000, l=300, alpha=delta=1/2
pp = F(1, 3)
EVr = pp * 1000 + (1 - pp) * (-300)
lamR = math.sqrt(float(pp * (1000 - EVr) ** 0.5 / ((1 - pp) * (300 + EVr) ** 0.5))) if False else float((pp * (1000 - EVr)) ** F(1, 2) / ((1 - pp) * (300 + EVr)) ** F(1, 2)) if False else None
gap = F(1000) - EVr
loss_mag = F(300) + EVr
ratio_root = math.sqrt(float(gap / loss_mag))
lamR = float(pp / (1 - pp)) * ratio_root
show("L06 EV(p=1/3)", EVr, str(EVr))
show("L06 lambda_R (p=1/3, alpha=delta=1/2)", lamR, f"{lamR:.6f} = sqrt2/2={math.sqrt(2)/2:.6f}")
# Remark 3.2 (alpha=1): gain/loss around EV for the Example 2.3 gamble
show("L06 Remark 3.2 gamble EV", EV, f"g-EV={g_-EV}, l+EV={l_+EV}")

# ---- L08
W1, WL, W0 = F(110000), F(95000), F(100000)
ce_eu = 1 / (F(1, 2) / W1 + F(1, 2) / WL)
show("L08 EU CE", ce_eu, f"{ce_eu} = {float(ce_eu):.4f}")
show("L08 premium 102500 - CE", None, f"{F(102500) - ce_eu} = {float(F(102500) - ce_eu):.4f}")
show("L08 maxmin CE (p=1/3)", None, f"{1 / (F(1,3)/W1 + F(2,3)/WL)} = {float(1 / (F(1,3)/W1 + F(2,3)/WL)):.4f}")
show("L08 p=1/4 EU CE (M1)", None, f"{float(1 / (F(1,4)/W1 + F(3,4)/WL)):.8f}")
show("L08 p=3/4 EU CE (M2/M3)", None, f"{float(1 / (F(3,4)/W1 + F(1,4)/WL)):.8f}")
show("L08 known urn red CE", None, f"{1 / (F(1,3)/F(110000) + F(2,3)/F(100000))}")
show("L08 known urn black CE", None, f"{float(1 / (F(2,3)/F(110000) + F(1,3)/F(100000))):.4f}")
show("L08 3300000/31", None, f"{float(F(3300000, 31)):.4f}")
pv = 0.5 * 100 ** 0.5 + 0.5 * (-2 * 50 ** 0.5)
inv = -((-pv / 2) ** 2)
show("L08 prospect V", pv, f"{pv:.6f}")
show("L08 prospect CE wealth", 100000 + 100 * inv, f"{100000 + 100 * inv:.4f} (CU change {inv:.6f})")
show("L08 prospect 5-sqrt50", 5 - math.sqrt(50), f"{5 - math.sqrt(50):.6f}")
show("L08 expected final wealth (P=1/2)", None, str(F(1, 2) * W1 + F(1, 2) * WL))
show("L08 22500/41", None, f"{float(F(22500, 41)):.4f}")
show("L08 Remark 2.3 maxmin CE 99523.8095 below EU CE 101951.2195", None, str(float(1/(F(1,3)/W1+F(2,3)/WL)) < float(ce_eu)))

# Example 2.5 (known urn CE for red at 110000/100000)
out.append(f"L08 Example 2.5 known urn (red) = {float(1/(F(1,3)/F(110000)+F(2,3)/F(100000))):.4f}")

for line in out:
    print(line)
