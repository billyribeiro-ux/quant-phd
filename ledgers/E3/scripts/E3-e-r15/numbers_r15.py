"""Independent recomputation of prose numbers in E3 slice e, lessons L01-L08 (verifier round 15).

Uses decimal (50 significant digits) and fractions only; no lesson code is imported.
Run as: python -I ledgers/E3/scripts/E3-e-r15/numbers_r15.py
"""
from decimal import Decimal, getcontext
from fractions import Fraction
import math

getcontext().prec = 60
D = Decimal


def dsqrt(x):
    return D(x).sqrt()


def omega(p):
    # closed form for eta = 1/2: sqrt(p) / (1 + 2 sqrt(p(1-p)))
    p = D(p)
    return dsqrt(p) / (1 + 2 * dsqrt(p * (1 - p)))


def show(label, value, digits=12):
    print(f"{label} = {value:.{digits}f}")


print("== L02 Example 1.5 (u = sqrt, W pays 40,100,160 w.p. 1/4,1/2,1/4)")
eu = D(1) / 4 * dsqrt(40) + D(1) / 2 * dsqrt(100) + D(1) / 4 * dsqrt(160)
show("E sqrt(W) (unrounded)", eu, 10)
show("CE = (E sqrt W)^2", eu * eu, 6)
show("squared printed 9.743416", D("9.743416") ** 2, 6)
show("premium = 100 - CE", D(100) - eu * eu, 6)
print("premium cents (rounded once, half up):", math.floor(float((D(100) - eu * eu) * 100) + 0.5))
print("CE cents (rounded once, half up):", math.floor(float(eu * eu * 100) + 0.5))

print("== L02 Lab 1 Part A/B quantities (gamble -60,0,60 w.p. 1/4,1/2,1/4 at w=100)")
var = D(1800)
rA = D("0.005")
show("approx premium 0.5*rA*Var", D("0.5") * rA * var, 6)
for eps in (D(1), D("0.5"), D("0.25"), D("0.1"), D("0.01")):
    ce = (D(1) / 4) * dsqrt(100 - 60 * eps) + (D(1) / 2) * dsqrt(100) + (D(1) / 4) * dsqrt(100 + 60 * eps)
    ce = ce * ce
    prem = D(100) - ce
    ratio = prem / (eps * eps)
    print(f"eps {eps}: premium_over_eps2 {float(ratio):.6f} gap {float(abs(ratio - D('4.5'))):.6f}")
show("error share of exact premium at eps=1", (D("5.065835") - D("4.5")) / D("5.065835") * 100, 4)

print("== L03 CRRA CE at prizes 5000,10000,20000 w.p. 1/4,1/2,1/4")
prizes = [D(5000), D(10000), D(20000)]
probs = [D(1) / 4, D(1) / 2, D(1) / 4]
for g in (D("0.25"), D("0.5"), D(4)):
    s = 1 - g
    m = sum(p * x ** s for p, x in zip(probs, prizes))
    ce = m ** (1 / s)
    show(f"CE at gamma {g}", ce, 4)

print("== L07 weights (eta = 1/2)")
for p in ("0.01", "0.05", "0.3", "0.5", "0.6", "0.95", "0.99", "0.279", "0.278", "2/5", "3/5", "1/4"):
    pp = D(Fraction(p).numerator) / D(Fraction(p).denominator)
    w = omega(pp)
    print(f"omega({p}) = {w:.12f} ; omega(p) - p = {float(w - pp):+.6e}")
w310 = omega(D(3) / 10)
w35 = omega(D(3) / 5)
w25 = omega(D(2) / 5)
w12 = omega(D(1) / 2)
print(f"omega(3/10) 10dp = {w310:.10f}, omega(3/5) 10dp = {w35:.10f}, omega(1/2) 10dp = {w12:.10f}")
ratio = w310 / w35
print(f"ratio omega(3/10)/omega(3/5) = {ratio:.12f}")
print("8-decimal quotient 0.28579088/0.39125077 =", f"{D('0.28579088') / D('0.39125077'):.12f}")
print("threshold alpha=1: 2/3 =", f"{D(2) / 3:.12f}", "; alpha=1/2:", f"{1 / (1 + D(2) ** D('-0.5')):.12f}")
print(f"Remark 1.6 sum A weights: w(2/5)+2w(3/10) = {w25 + 2 * w310:.12f}; 2w(3/10) = {2 * w310:.12f}")
print(f"Gamma(A) alpha=1 = 150*w(3/10) = {150 * w310:.12f}; Gamma(B) = 100*w(3/5) = {100 * w35:.12f}")
print(f"difference of unrounded values = {150 * w310 - 100 * w35:.12f}")
print(f"Gamma(A) alpha=1/2 = w(3/10)*(sqrt50+10) = {w310 * (D(50).sqrt() + 10):.10f}; Gamma(B) = 10*w(3/5) = {10 * w35:.10f}")
print(f"misconception: 0.01*w-weight 100 + w(0.99)*50 = {100 * omega(D('0.01')) + 50 * omega(D('0.99')):.10f}; EV = 50.5")
print(f"overweight adds (w(0.01)-0.01)*100 = {(omega(D('0.01')) - D('0.01')) * 100:.6f}; underweight subtracts (0.99-w(0.99))*50 = {(D('0.99') - omega(D('0.99'))) * 50:.6f}")
print("eta=1 closed-form gap at p=0.862:", f"{abs(omega(D('0.862')) - D('0.862')):.6f}")
best = (D(0), D(0))
for i in range(1001):
    p = D(i) / 1000
    if p == 0 or p == 1:
        continue
    gap = abs(omega(p) - p)
    if False:
        pass
# eta = 1 "closed form" for the same test: compare sqrt(p)/(1+2sqrt(p(1-p))) with p (identity weighting)
worst = D(0)
worst_p = None
for i in range(1, 1001):
    p = D(i) / 1000
    g = abs(omega(p) - p)
    if g > worst:
        worst, worst_p = g, p
print(f"largest |closed form - p| over the grid (not eta=1 weighting itself) = {worst:.6f} at p = {worst_p}")

print("== L08 gamble (final wealth 110000 red / 95000 otherwise, u = -1/w)")


def ce_of_p(p):
    return 1 / (p / D(110000) + (1 - p) / D(95000))


print("EU CE (P(red)=1/2) =", f"{ce_of_p(D(1) / 2):.10f}", "; 4180000/41 =", f"{D(4180000) / 41:.10f}")
print("maxmin CE (p=1/3) =", f"{ce_of_p(D(1) / 3):.10f}", "; p=3/4 CE =", f"{ce_of_p(D(3) / 4):.10f}", "; p=1/4 CE =", f"{ce_of_p(D(1) / 4):.10f}")
print("M1 CE at P(red)=1/4 =", f"{ce_of_p(D(1) / 4):.10f}", "; 1672000/17 =", f"{D(1672000) / 17:.10f}")
print("risk premium 102500 - EU CE =", f"{D(102500) - ce_of_p(D(1) / 2):.10f}", "; 22500/41 =", f"{D(22500) / 41:.10f}")
prospect = D("0.5") * dsqrt(100) - D("0.5") * 2 * dsqrt(50)
inv = (-prospect / 2) ** 2
print("prospect V_p (CU^1/2) =", f"{prospect:.10f}", "; CE change (CU) =", f"{-inv:.10f}", "; wealth CE cents =", f"{D(100000) - 100 * inv:.10f}")
print("known urn red CE (30/90) =", f"{1 / (D(1) / 3 / 110000 + D(2) / 3 / 100000):.6f}", "; black CE (60/90) =", f"{1 / (D(2) / 3 / 110000 + D(1) / 3 / 100000):.6f}")
print("Example 2.5 known black CE =", f"{1 / (D(2) / 3 / 110000 + D(1) / 3 / 100000):.6f}")
print("bet CE at P(red)=1/3 with 110000/100000 wealth =", f"{1 / (D(1) / 3 / 110000 + D(2) / 3 / 100000):.6f}")
print("one-quarter identity 85/8360000 =", f"{D(85) / 8360000:.12f}", "; 1/440000+3/380000 =", f"{D(1) / 440000 + D(3) / 380000:.12f}")

print("== L05 EZ values")
beta = Fraction(9, 10)
# psi = 1/2 -> a = -1 ; gamma = 2; tree c1 = 1 or 4 w.p. 1/2; c0 = 2
ce1 = 1 / (Fraction(1, 2) * 1 + Fraction(1, 2) * Fraction(1, 4))
v0 = 1 / ((1 - beta) / Fraction(2) + beta / ce1)
print("L05 CE1 =", ce1, "; V0 =", v0, "; mean =", Fraction(5, 2))
print("L05 Remark 1.5 CEs at gamma 2:", 1 / (Fraction(1, 2) * 1 + Fraction(1, 2) * Fraction(1, 4)), 1 / (Fraction(1, 2) * Fraction(1, 2) + Fraction(1, 2) * Fraction(1, 3)))
print("L05 E2 V0 with P(1)=1/4, P(4)=3/4:", 1 / ((1 - beta) / Fraction(2) + beta * (Fraction(1, 4) * 1 + Fraction(3, 4) * Fraction(1, 4))))
# psi = 2, beta = 1/2, plans (1,10) and (4,4), gamma = 2
v_a = (D("0.5") * D(4) ** D("0.5") + D("0.5") * D(4) ** D("0.5")) ** 2
v_b = (D("0.5") * D(1) ** D("0.5") + D("0.5") * D(10) ** D("0.5")) ** 2
print(f"L05 V0(4,4) psi=2 beta=1/2 = {v_a:.6f}; V0(1,10) = {v_b:.6f}")
print("L05 U(4,4) =", -Fraction(1, 2) * Fraction(1, 4) - Fraction(1, 2) * Fraction(1, 4), "; U(1,10) =", -Fraction(1, 2) - Fraction(1, 2) * Fraction(1, 10))
print("L05 M3 theta(gamma=2,psi=2) =", (1 - 2) / (1 - Fraction(1, 2)))

print("== L06 power-form numbers (alpha = delta = 1/2, lambda = 2, p = 1/2, g = 1000, l = 600)")
thr = (D("0.5") * D(1000).sqrt()) / (D("0.5") * D(600).sqrt())
print(f"threshold = {thr:.10f}; sqrt(5/3) = {(D(5) / 3).sqrt():.10f}")
print(f"W at lambda 2 = {D('0.5') * D(1000).sqrt() - D('0.5') * 2 * D(600).sqrt():.10f}")
print(f"lambda_R (reference point = EV, p=1/3, g=1000, l=300, alpha=1/2) = {(D(1) / 3 * (D(1000) - D(400) / 3).sqrt()) / (D(2) / 3 * (D(300) + D(400) / 3).sqrt()):.10f}")
print("EV for p=1/3, g=1000, l=300 =", Fraction(1, 3) * 1000 - Fraction(2, 3) * 300)

print("== L04 Example 2.5 integrated CDFs")
X = [(2000, Fraction(1, 2)), (4000, Fraction(1, 2))]
Y = [(1000, Fraction(1, 4)), (3000, Fraction(1, 2)), (5000, Fraction(1, 4))]
for t in (1000, 2000, 3000, 4000, 5000):
    ix = sum(p * max(t - x, 0) for x, p in X)
    iy = sum(p * max(t - x, 0) for x, p in Y)
    print(f"t={t}: I_X={ix} I_Y={iy}")
print("means:", sum(p * x for x, p in X), sum(p * x for x, p in Y))

print("== L01 exact (Fractions)")
F = Fraction


def ev(lot):
    return sum((p * x for x, p in lot), F(0))


def eu(lot, u):
    return sum((p * u(x) for x, p in lot), F(0))


A1 = [(0, F(1, 4)), (100, F(1, 2)), (400, F(1, 4))]
sq = lambda x: F(x) ** 2
print("Ex1.4 EV A =", ev(A1), "; EU quad (CU^2) =", eu(A1, sq))
C = [(0, F(1, 3)), (150, F(1, 3)), (300, F(1, 3))]
print("Ex3.4 EU quad C =", eu(C, sq), "; (0+22500+90000)/3 =", F(0 + 22500 + 90000, 3))
M1 = [(20, F(1, 5)), (50, F(3, 10)), (80, F(1, 2))]
print("M1 E X =", ev(M1), "; E u =", eu(M1, sq), "; u(EX) =", ev(M1) ** 2, "; gap =", eu(M1, sq) - ev(M1) ** 2)
L_ = [(0, F(1, 2)), (100, F(1, 2))]
M_ = [(100, F(1, 4)), (200, F(3, 4))]
mix = [(0, F(1, 6)), (100, F(1, 3)), (200, F(1, 2))]
print("M2 mixture weights sum =", sum(p for _, p in mix), "; E mix =", ev(mix), "; rhs =", F(1, 3) * ev(L_) + F(2, 3) * ev(M_), "; E L =", ev(L_), "; E M =", ev(M_))
X3 = [(10, F(1, 2)), (30, F(1, 2))]
Y3 = [(0, F(1, 4)), (40, F(3, 4))]
print("M3 E X =", ev(X3), "; E Y =", ev(Y3), "; tilde-u E X =", 5 + 3 * ev(X3), "; E Y =", 5 + 3 * ev(Y3))
mixE = [(0, F(2, 5)), (50, F(3, 10)), (100, F(3, 10))]
print("E1 quad A =", eu(A1, sq), "; C =", eu(C, sq))
print("E2 rho=1/3 check: 1/3*45000 + 2/3*37500 =", F(1, 3) * 45000 + F(2, 3) * 37500)
print("E3 sums: 1/2+1/3 =", F(1, 2) + F(1, 3), "; (5/6)")
print("L01 Q7: 1/3*1/4 + 2/3*1/2 =", F(1, 3) * F(1, 4) + F(2, 3) * F(1, 2))
print("L01 R3: E u(X) =", eu([(100, F(1, 2)), (200, F(1, 2))], sq), "; E u(Y) =", eu([(150, F(1))], sq))
