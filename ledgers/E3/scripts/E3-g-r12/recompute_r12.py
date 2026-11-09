# Independent recomputation of the numbers on the E3 L05-L08 lessons and their cards (no imports from the course).
from fractions import Fraction as F
from decimal import Decimal, getcontext
import math

getcontext().prec = 60

print("== L05 exact tree ==")
beta, gamma, psi, c0 = F(9, 10), F(2), F(1, 2), F(2)
tree = [(F(1, 2), F(1)), (F(1, 2), F(4))]
a = 1 - 1 / psi
ce1 = (sum(p * c ** (1 - gamma) for p, c in tree)) ** (1 / (1 - gamma))  # float-ish
Einv = sum(p * c ** -1 for p, c in tree)
ce1_exact = 1 / Einv
print("CE1 exact (gamma=2) =", ce1_exact, " mean =", sum(p * c for p, c in tree))
bracket = (1 - beta) * c0 ** (-1) + beta * ce1_exact ** (-1)
V0 = 1 / bracket
U = (1 - beta) * (-1 / c0) + beta * sum(p * (-1 / c) for p, c in tree)
print("V0 =", V0, " U =", U, " (1-g)U == V0^(1-g):", (1 - gamma) * U == V0 ** (1 - gamma))
print("E2 variant: CE1 =", 1 / (F(1, 4) * 1 + F(3, 4) * F(1, 4)), " V0 =", 1 / (F(1, 20) + F(9, 10) * F(7, 16)))
print("M1: CE1 =", 1 / (F(1, 4) * 1 + F(3, 4) * F(1, 3)), "mean =", F(1, 4) * 1 + F(3, 4) * 3)
print("M2: V0 =", 1 / (F(1, 2) * 1 + F(1, 2) * F(1, 3)))
print("CE1 for gamma 0.5, 2, 3 (c=1,4 w.p. 1/2):")
for g in (0.5, 2.0, 3.0):
    m = 0.5 * 1.0 ** (1 - g) + 0.5 * 4.0 ** (1 - g)
    print("  gamma", g, "CE1 = %.6f" % (m ** (1 / (1 - g))))
print("EIS-free check: deterministic V0 for psi=1/2, c0=2, c1=4, beta=0.9:", (0.1 * 2 ** (-1) + 0.9 * 4 ** (-1)) ** -1)
# ratio of MRS at (2,4), psi=1/2, beta=0.9
print("closed-form MRS (1-b)/b (c1/c0)^(1/psi) =", (0.1 / 0.9) * (4 / 2) ** 2)
print("(4,4) and (1,10) at psi=2, beta=1/2, gamma=2:")
def ez_sure(c0_, c1_, beta_, psi_):
    a_ = 1 - 1 / psi_
    return ((1 - beta_) * c0_ ** a_ + beta_ * c1_ ** a_) ** (1 / a_)
print("  V0(4,4) = %.4f  V0(1,10) = %.4f" % (ez_sure(4.0, 4.0, 0.5, 2.0), ez_sure(1.0, 10.0, 0.5, 2.0)))
print("  U(4,4) = %.4f  U(1,10) = %.4f" % (-(1 / 4), 0.5 * (-1) + 0.5 * (-0.1)))

print("== L06 ==")
print("Example 2.3 W at lam=1,1.5,2:", [0.5 * 1000 - 0.5 * lam * 600 for lam in (1, 1.5, 2)], " lam*=", 500 / 300)
print("power threshold sqrt(5/3) =", math.sqrt(5 / 3), " W(lam=2,a=d=.5) =", 0.5 * math.sqrt(1000) - 0.5 * 2 * math.sqrt(600))
print("Remark 2.5: combined 700-300*2 =", 700 - 600, " separate 1000-600*2 =", 1000 - 1200)
print("Remark 3.2 p=1/3 g=1000 l=300 a=d=1/2: EV =", F(1000, 3) - F(600, 3), " lambda_R =", (1 / 3) ** 0.5 / (2 / 3) ** 0.5 * 0 + (1 / 3) * math.sqrt(1000 - 400 / 3) / ((2 / 3) * math.sqrt(300 + 400 / 3)))
print("M1 L06: lam*=", (1 / 3 * 900) / (2 / 3 * 300), " W(2)=", 300 - 2 / 3 * 2 * 300)
print("M2 L06: EV=", 50 - 50, " W(2)=", 50 - 100)
print("E3 L06 framing at 3/2: combined", 700 - 300 * 1.5, " separate", 1000 - 600 * 1.5)

print("== L07 ==")
def omega(p, eta=0.5):
    return p ** eta / (p ** eta + (1 - p) ** eta) ** (1 / eta)
def omega_closed(p):
    return math.sqrt(p) / (1 + 2 * math.sqrt(p * (1 - p)))
for p in (0.3, 0.6, 0.5, 0.4, 0.01, 0.99, 0.05, 0.95, 0.25, 0.75, 0.01):
    print("  omega(%s) = %.12f  closed=%.12f" % (p, omega_closed(p), omega_closed(p)))
# 40-digit decimal values
def om_dec(p):
    p = Decimal(p) if not isinstance(p, Decimal) else p
    s = p.sqrt()
    q = (p * (1 - p)).sqrt()
    return s / (1 + 2 * q)
w310 = om_dec(Decimal(3) / Decimal(10))
w35 = om_dec(Decimal(3) / Decimal(5))
w12 = om_dec(Decimal(1) / Decimal(2))
print("40-digit omega(3/10) =", w310)
print("40-digit omega(3/5)  =", w35)
print("omega(1/2) =", w12, " 1/(2 sqrt2) =", 1 / (2 * math.sqrt(2)))
print("Gamma(A) at alpha=1 (150 w310) =", 150 * w310, " Gamma(B) (100 w35) =", 100 * w35)
dA = 150 * w310 - 100 * w35
print("40-digit difference =", dA, " 4dp =", round(dA, 4))
gA8, gB8 = Decimal("42.86863274"), Decimal("39.12507700")
print("8-decimal difference =", gA8 - gB8)
print("Gamma A/B float:", 150 * omega_closed(0.3), 100 * omega_closed(0.6))
print("2*omega(3/10)+omega(2/5) =", omega_closed(0.4) + 2 * omega_closed(0.3), " omega(2/5)=", omega_closed(0.4))
print("2*omega(3/10) =", 2 * omega_closed(0.3))
print("8-dec 0.28579088/0.39125077 =", 0.28579088 / 0.39125077, " exact ratio:", w310 / w35)
print("threshold alpha=1/2:", 1 / (1 + 2 ** -0.5))
print("E3 L07 counterexample:", omega_closed(0.01) * 100 + omega_closed(0.99) * 50, " EV=", 0.01 * 100 + 0.99 * 50)
print("  overweight part", (omega_closed(0.01) - 0.01) * 100, " underweight part", (0.99 - omega_closed(0.99)) * 50)
print("  unrounded omega(0.01), omega(0.99):", omega_closed(0.01), omega_closed(0.99))
print("ω(1/4)=", omega_closed(0.25), " 2-sqrt3=", 2 - math.sqrt(3))
print("alpha=0.5 Gamma A/B:", math.sqrt(50) * omega_closed(0.3) + 10 * omega_closed(0.3), 10 * omega_closed(0.6))
print("alpha=1 Gamma A/B floats:", 150 * omega_closed(0.3), 100 * omega_closed(0.6))
# closed form vs omega at eta=1: gap
grid = [i / 1000 for i in range(1001)]
gap_eta1 = max(abs(p - omega_closed(p)) for p in grid)
argmax = max(grid, key=lambda p: abs(p - omega_closed(p)))
print("eta=1 closed-form gap =", gap_eta1, "at p =", argmax)
gap_eta_half = max(abs(omega(p) - omega_closed(p)) for p in grid)
print("eta=1/2 general vs closed gap =", gap_eta_half)
above = [omega_closed(p) > p for p in grid[1:-1]]
ch = sum(1 for a_, b_ in zip(above, above[1:]) if a_ != b_)
pts = [p for p in grid[1:-1] if omega_closed(p) > p]
print("sign changes", ch, "last omega>p point", max(pts))
print("derivative formula check at p=0.3:")
p = 0.3
h = 1e-6
num_d = (omega_closed(p + h) - omega_closed(p - h)) / (2 * h)
q = math.sqrt(p * (1 - p))
print("  numeric", num_d, " formula", (q + 2 * p * p) / (2 * math.sqrt(p) * q * (1 + 2 * q) ** 2))
p = 0.7
num_d = (omega_closed(p + h) - omega_closed(p - h)) / (2 * h)
q = math.sqrt(p * (1 - p))
print("  numeric p=0.7", num_d, " formula", (q + 2 * p * p) / (2 * math.sqrt(p) * q * (1 + 2 * q) ** 2))

print("== L08 ==")
W1, WL = 110000, 95000
print("EU CE p=1/2:", 1 / (0.5 / W1 + 0.5 / WL), " exact", F(4180000, 41), float(F(4180000, 41)))
print("EU CE p=1/4:", 1 / (F(1, 4) / 110000 + F(3, 4) / 95000), float(1 / (F(1, 4) / 110000 + F(3, 4) / 95000)))
print("EU CE p=3/4:", 1 / (F(3, 4) / 110000 + F(1, 4) / 95000), float(1 / (F(3, 4) / 110000 + F(1, 4) / 95000)))
print("maxmin p=1/3:", float(1 / (F(1, 3) / 110000 + F(2, 3) / 95000)))
print("known red 1/3:", float(1 / (F(1, 3) / 110000 + F(2, 3) / 100000)), " known black 2/3:", float(1 / (F(2, 3) / 110000 + F(1, 3) / 100000)))
print("risk premium exact 22500/41 =", float(F(22500, 41)))
print("prospect: V=", 0.5 * 10 + 0.5 * (-2 * math.sqrt(50)), " CE change CU:", -((-(0.5 * 10 - math.sqrt(50))) / 2) ** 2, " wealth:", 100000 + 100 * -((-(0.5 * 10 - math.sqrt(50))) / 2) ** 2)
print("prospect 5-sqrt50 =", 5 - math.sqrt(50))
print("EZ at lam: nothing else")
