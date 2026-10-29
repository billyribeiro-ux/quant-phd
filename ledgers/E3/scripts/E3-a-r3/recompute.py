"""Independent recomputation of every number in the E3 slice-a pages (L01-L03, hub), from first principles."""
from fractions import Fraction as F
import math

out = []
def show(label, val):
    out.append(f"{label}: {val}")

# ---- L01 Example 1.4 and Example 3.4 (CU)
A = [(0, F(1, 4)), (100, F(1, 2)), (400, F(1, 4))]
C = [(0, F(1, 3)), (150, F(1, 3)), (300, F(1, 3))]
ev = lambda L: sum(p * x for x, p in L)
eu = lambda L, u: sum(p * u(x) for x, p in L)
show("L01 EX A", ev(A)); show("L01 EU A x^2", eu(A, lambda x: x * x))
show("L01 EX C", ev(C)); show("L01 EU C x^2", eu(C, lambda x: x * x))
show("L01 u(EX_A)^2", ev(A) ** 2)
# M1
M1 = [(20, F(1, 5)), (50, F(3, 10)), (80, F(1, 2))]
show("L01 M1 EX", ev(M1)); show("L01 M1 EU", eu(M1, lambda x: x * x)); show("L01 M1 u(EX)", ev(M1) ** 2)
show("L01 M1 gap", eu(M1, lambda x: x * x) - ev(M1) ** 2)
# M2
Lq = [(0, F(1, 2)), (100, F(1, 2))]; Mq = [(100, F(1, 4)), (200, F(3, 4))]
mix = [(0, F(1, 6)), (100, F(1, 3)), (200, F(1, 2))]
show("L01 M2 mixture EU", eu(mix, lambda x: x)); show("L01 M2 rhs", F(1, 3) * eu(Lq, lambda x: x) + F(2, 3) * eu(Mq, lambda x: x))
# M3
X3 = [(10, F(1, 2)), (30, F(1, 2))]; Y3 = [(0, F(1, 4)), (40, F(3, 4))]
show("L01 M3 EU_u X,Y", (eu(X3, lambda x: x), eu(Y3, lambda x: x)))
show("L01 M3 EU_v X,Y", (eu(X3, lambda x: 5 + 3 * x), eu(Y3, lambda x: 5 + 3 * x)))
# E1 and E2 of L01
show("L01 E2 check", F(1, 3) * 45000 + F(2, 3) * 37500)
show("L01 quiz 5/12", F(1, 3) * F(1, 4) + F(2, 3) * F(1, 2))
# R3
show("L01 R3 X EU", (F(1, 2) * (100 ** 2) + F(1, 2) * (200 ** 2)) / 1)  # printed as sum/2
show("L01 R3 Y EU", F(150) ** 2)

# ---- L02 (floats)
W = 100.0
G = [(-60, 0.25), (0, 0.5), (60, 0.25)]
var = sum(p * x * x for x, p in G)
show("L02 var", var)
def ce(eps, val, inv):
    e = sum(p * val(W + eps * x) for x, p in G)
    return inv(e)
sv = lambda w: math.sqrt(w); si = lambda y: y * y
ce1 = ce(1.0, sv, si)
show("L02 CE sqrt eps=1", ce1); show("L02 premium", W - ce1)
show("L02 cents CE", round(ce1 * 100, 4)); show("L02 premium cents", round((W - ce1) * 100, 4))
rA = 1 / (2 * W)
show("L02 pratt premium", 0.5 * rA * var); show("L02 error", (W - ce1) - 0.5 * rA * var)
show("L02 error share of exact", ((W - ce1) - 0.5 * rA * var) / (W - ce1))
show("L02 error share of approx", ((W - ce1) - 0.5 * rA * var) / (0.5 * rA * var))
gaps = []
for eps in (1.0, 0.5, 0.25, 0.1, 0.01):
    prem = W - ce(eps, sv, si)
    gaps.append(abs(prem / eps ** 2 - 0.5 * rA * var))
    show(f"L02 eps {eps} ratio, gap", (prem / eps ** 2, gaps[-1]))
show("L02 gap ratio 0.25/0.1", gaps[2] / gaps[3])
show("L02 eps^2 ratio 0.25/0.1", 0.25 ** 2 / 0.1 ** 2)
show("L02 half-var", var / 2); show("L02 half-var / premium", (var / 2) / (W - ce1))
show("L02 Example1.5 EU", 0.25 * math.sqrt(40) + 0.5 * 10 + 0.25 * math.sqrt(160))
show("L02 M1 CE (4,16 wealth)", 9.0)
show("L02 E1-check: 1/(2w)", 1 / (2 * 100))

# ---- L03
PR = [5000, 10000, 20000]; PB = [F(1, 4), F(1, 2), F(1, 4)]
show("L03 mean", sum(p * x for p, x in zip(PB, PR)))
def ce_g(prizes, g):
    if g == 1:
        return math.exp(sum(float(p) * math.log(x) for p, x in zip(PB, prizes)))
    s = 1 - g
    return (sum(float(p) * x ** s for p, x in zip(PB, prizes))) ** (1 / s)
for g in (0, 0.25, 0.5, 1, 2, 4):
    show(f"L03 CE gamma {g}", round(ce_g(PR, g), 4))
show("L03 gamma2 exact", 1 / sum(p / x for p, x in zip(PB, PR)))
show("L03 M for E2", F(1, 4) * F(1, 5000) + F(1, 2) * F(1, 10000) + F(1, 4) * F(1, 20000))
show("L03 M2 CE", 1 / (F(1, 4) * F(1, 1000) + F(3, 4) * F(1, 9000)))
show("L03 M3 CE", 1 / (F(1, 4) * F(1, 3000) + F(3, 4) * F(1, 27000)))
show("L03 Ex2.5 CE2", 1 / (F(1, 2) * F(1, 1000) + F(1, 2) * F(1, 4000)))
show("L03 Ex2.5 CE1", math.sqrt(1000 * 4000))
show("L03 E3 bound", (10 + 1) / 2)
show("L03 R1 check: gamma2 M", 1 / (F(1,4)*F(1,5000)+F(1,2)*F(1,10000)+F(1,4)*F(1,20000)))
show("L03 M1 r_A(4) gamma 1/2", (0.5 / 4))
show("L03 geometric mean", math.exp(sum(float(p) * math.log(x) for p, x in zip(PB, PR))))
show("L03 gamma 1 proof: CE gamma 1 +-1e-6 rel err", abs(ce_g(PR, 1 + 1e-6) - ce_g(PR, 1)))
print("\n".join(out))
