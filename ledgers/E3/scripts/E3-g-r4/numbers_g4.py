"""Recompute every number on the L05-L08 cards of E3 with exact fractions and 40-digit decimals (stdlib only).

Usage: python -I numbers_g4.py
"""
from decimal import Decimal, getcontext
from fractions import Fraction as F

getcontext().prec = 40
D = Decimal


def om(p: Decimal) -> Decimal:
    """omega_{1/2}(p) = sqrt(p) / (1 + 2 sqrt(p(1-p)))."""
    return p.sqrt() / (1 + 2 * (p * (1 - p)).sqrt())


def show(name: str, value: Decimal, digits: int = 8) -> None:
    print(f"{name} = {value:.{digits}f}  (40-digit: {value})")


print("== L07 weights ==")
w310, w35, w12, w25 = om(D(3) / 10), om(D(3) / 5), om(D(1) / 2), om(D(2) / 5)
show("omega(3/10)", w310)
show("omega(3/5)", w35)
show("omega(1/2)", w12)
show("omega(2/5)", w25)
show("2*omega(3/10)", 2 * w310)
show("omega(2/5)+2*omega(3/10)", w25 + 2 * w310)
print("eq 1/(2 sqrt2) =", D(1) / (2 * D(2).sqrt()))
print("ratio omega(3/10)/omega(3/5) =", w310 / w35, "| 8-digit quotient of printed values:", D("0.28579088") / D("0.39125077"))
print("thresholds: alpha=1 ->", D(1) / (1 + D("0.5")), " alpha=1/2 ->", D(1) / (1 + D(2) ** D("-0.5")))
G_A1 = 150 * w310
G_B1 = 100 * w35
G_A05 = 17 * 0 + w310 * (D(50).sqrt() + D(100).sqrt())
G_B05 = w35 * D(100).sqrt()
show("Gamma(A) alpha=1", G_A1)
show("Gamma(B) alpha=1", G_B1)
show("Gamma(A) alpha=1/2", G_A05)
show("Gamma(B) alpha=1/2", G_B05)
show("Gamma(A)-Gamma(B) alpha=1", G_A1 - G_B1, 8)
print("8-decimal rounded values:", f"{G_A1:.8f}", f"{G_B1:.8f}", "difference of those:", D(f"{G_A1:.8f}") - D(f"{G_B1:.8f}"))
print("expected value of L (100 w.p. .01, 50 w.p. .99) =", D("0.01") * 100 + D("0.99") * 50)
wl1, wl99 = om(D("0.01")), om(D("0.99"))
print("omega(0.01)=", wl1, " omega(0.99)=", wl99)
v_L = wl1 * 100 + wl99 * 50
print("weighted value at alpha=1 =", v_L, " (card: 49.8328)")
print("overweight add", (wl1 - D("0.01")) * 100, " underweight sub", (D("0.99") - wl99) * 50, " net", (wl1 - D("0.01")) * 100 - (D("0.99") - wl99) * 50)
print("omega(1/4) =", om(D(1) / 4), " 2-sqrt3 =", 2 - D(3).sqrt())
print("omega(0.99)<0.99", wl99 < D("0.99"), " omega(0.01)>0.01", wl1 > D("0.01"))
print("weight of 2 positive outcomes of A (identity would be 0.6) =", 2 * w310)

print("\n== L07 distribution / dominance ==")
print("F_A(50)=", F(2, 5) + F(3, 10), " F_B(50)=", F(2, 5), " tail_A(50)=", F(3, 5), " tail_B(50)=", F(3, 5), " tail_A(100)=", F(3, 10), " tail_B(100)=", F(3, 5))

print("\n== L06 ==")
p = D("0.5")
print("threshold sqrt(5/3) =", (D(5) / 3).sqrt(), " lam*(alpha=delta=.5, p=1/2, g=1000, l=600) =", (p * D(1000).sqrt()) / ((1 - p) * D(600).sqrt()))
W_pow = p * D(1000).sqrt() - (1 - p) * 2 * D(600).sqrt()
print("W at lam=2 powers 0.5 =", W_pow)
print("R3 lam_R (p=1/3,g=1000,l=300, EV=400/3, alpha=1/2) =", (D(1) / 3 * (1000 - D(400) / 3).sqrt()) / ((D(2) / 3) * (300 + D(400) / 3).sqrt()), " sqrt2/2=", D(2).sqrt() / 2)
print("combined value 700-300*2 =", F(1, 4) * 2000 + F(1, 2) * 400 - F(1, 4) * 2 * 1200, " separate 2*(500-600)=", 2 * (500 - 300 * 2))
print("M1 lam* (p=1/3,g=900,l=300) =", F(1, 3) * 900 / (F(2, 3) * 300), " W(2)=", F(1, 3) * 900 - F(2, 3) * 2 * 300)
print("Remark 3.2 value check: 0.5*800^a(1-lam) with a=1 at lam=1 ->", F(1, 2) * 800 * (1 - 1))
print("R2 check exact: 1000-600*lam=0 at lam=5/3:", 1000 - 600 * F(5, 3), " 700-300*7/3=", 700 - 300 * F(7, 3))
print("L06 M2: EV=0 W=", F(1, 2) * 100 - F(1, 2) * 2 * 100, " lam*=", (F(1, 2) * 100) / (F(1, 2) * 100))

print("\n== L08 certainty equivalents (u = -1/w, gamma = 2) ==")
W1, WL, W0 = F(110000), F(95000), F(100000)


def ce(pr: F) -> F:
    return 1 / (pr / W1 + (1 - pr) / WL)


print("EU CE p=1/2 =", ce(F(1, 2)), "=", float(ce(F(1, 2))), "(card 101951.2195)")
print("maxmin CE p=1/3 =", float(ce(F(1, 3))), "(card 99523.8095)")
print("CE p=1/4 =", float(ce(F(1, 4))), "(card 98352.94; exact 1672000/17 =", F(1672000, 17), ")")
print("CE p=3/4 =", float(ce(F(3, 4))), "(card 105822.78)")
print("risk premium 102500 - CE =", float(102500 - ce(F(1, 2))), "exact 22500/41 =", float(F(22500, 41)), " in CU =", float((102500 - ce(F(1, 2))) / 100))
print("maxmin wealth-initial =", float(ce(F(1, 3)) - W0), "EU - initial =", float(ce(F(1, 2)) - W0))
known_r = 1 / (F(1, 3) / 110000 + F(2, 3) / 100000)
known_b = 1 / (F(2, 3) / 110000 + F(1, 3) / 100000)
print("known urn red CE =", float(known_r), " black CE =", float(known_b), " diff CU =", float((known_r - 100000) / 100))
print("CE with worst prior p=0 (red bet) =", float(1 / (F(0) / W1 + F(1) / WL)), " with P0 gives wealth 95000 (not 100000 for lottery of Ex 2.5?)")
print("Example 2.5 (prize 10000, loss 0): P0 -> wealth 100000:", float(1 / (F(0) / 110000 + F(1) / 100000)))
print("Example 2.5 known red CE and black CE:", float(1 / (F(1, 3) / 110000 + F(2, 3) / 100000)), float(1 / (F(2, 3) / 110000 + F(1, 3) / 100000)))
print("Example 2.5 exact black (known urn: 60 black of 90 => P(black)=2/3 win):", float(1 / (F(2, 3) / 110000 + F(1, 3) / 100000)))

print("\n== L08 prospect model (alpha=delta=1/2, lambda=2, changes in CU) ==")
V = D("0.5") * D(100).sqrt() - D("0.5") * 2 * D(50).sqrt()
print("V_p =", V, " card 5 - sqrt50 =", 5 - D(50).sqrt())
inv = -((-V / 2) ** 2)
print("v^-1(V) =", inv, " card -1.072330; wealth eq =", 100000 + 100 * inv, " card 99892.7670")

print("\n== L05 ==")
print("CE1 lottery (1,4) gamma=2 =", 1 / (F(1, 2) * 1 + F(1, 2) * F(1, 4)), " CE1 lottery (2,3)=", 1 / (F(1, 2) * F(1, 2) + F(1, 2) * F(1, 3)), " means 5/2")
print("CE1 gamma .5 (1,4 each 1/2) =", ((F(1, 2) * 1 ** F(1, 2) + F(1, 2) * 4 ** F(1, 2)) ** 2))
print("CE1 gamma 3 =", float((D("0.5") + D("0.5") * D(4) ** D(-2)) ** D("-0.5")))
V0 = 1 / (F(1, 10) / 2 + F(9, 10) * F(5, 8))
print("V0 exact tree =", V0, " U =", -(F(1, 10) * F(1, 2) + F(9, 10) * F(5, 8)))
print("E2 V0 with p(c1=1)=1/4 =", 1 / (F(1, 10) / 2 + F(9, 10) * F(7, 16)), " CE1=16/7:", 1 / F(7, 16))
print("M1 CE =", 1 / (F(1, 4) * 1 + F(3, 4) * F(1, 3)), " mean =", F(1, 4) + F(9, 4))
print("M2 V0 =", 1 / (F(1, 2) * 1 + F(1, 2) * F(1, 3)))
print("sure plan c1=8/5 value =", 1 / (F(1, 10) / 2 + F(9, 10) * F(5, 8)))
print("(4,4) vs (1,10) at psi=2 gamma=2 beta=1/2: U(4,4)=", F(1, 2) * (-F(1, 4)) + F(1, 2) * (-F(1, 4)), " U(1,10)=", F(1, 2) * (-1) + F(1, 2) * F(-1, 10))
print("V0(1,10) psi=2 =", float((D("0.5") * D(1) ** D("0.5") + D("0.5") * D(10).sqrt()) ** 2), " V0(4,4) =", float((D("0.5") * 2 + D("0.5") * 2) ** 2))
print("theta(gamma=2,psi=2) =", (1 - 2) / (1 - F(1, 2)))
print("prob 1/4 CE1 mean check; theta(1) check", (1 - 2) / (1 - F(1, 2)))
