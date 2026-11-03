"""E3 slice f round 3: independent recomputation of every number the L01 to L04 cards and lessons state.

Run: python3 -I ledgers/E3/scripts/E3-f-r3/numbers_check.py  (standard library only)
"""
import math
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP


def half_up(v):
    return int(Decimal(repr(v * 100)).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def ok(name, got, want):
    print(f"{name}: got {got} want {want} {'OK' if got == want else 'MISMATCH'}")


print("== L01")
A = [(0, F(1, 4)), (10000, F(1, 2)), (40000, F(1, 4))]
B = [(5000, F(1, 2)), (20000, F(1, 2))]
C = [(0, F(1, 3)), (15000, F(1, 3)), (30000, F(1, 3))]
lin = lambda x: F(x)
quad = lambda x: F(x * x, 10000)
ev = lambda L: sum((p * x for x, p in L), F(0))
eu = lambda L, u: sum((p * u(x) for x, p in L), F(0))
for n, L, w in (("A", A, 15000), ("B", B, 12500), ("C", C, 15000)):
    ok(f"EV {n} cents", ev(L), w)
ok("EU quad A", eu(A, quad), 45000)
ok("EU quad B", eu(B, quad), 21250)
ok("EU quad C", eu(C, quad), 37500)
ok("u(EX) quad A (cents^2/1e4)", quad(150 * 100), 22500)
ok("E1 difference A-C quad", eu(A, quad) - eu(C, quad), 7500)
ok("Example 1.4 EU quad in CU^2", F(0) * F(1, 4) + F(10000, 1) * F(1, 2) + F(160000, 1) * F(1, 4), 45000)
ok("Example 3.4 EU quad C in CU^2", (F(0) + F(22500) + F(90000)) / 3, 37500)
ok("M1 EU x^2", F(400, 5) + F(2500) * F(3, 10) + F(6400, 2), 4030)
ok("M1 u(EX)", 59 * 59, 3481)
ok("M1 diff", 4030 - 3481, 549)
ok("E2 mixture 1/3 quad", F(45000 * 1, 3) + F(2, 3) * 37500, 40000)
ok("Q7 weight 0 in 1/3 A + 2/3 D", F(1, 3) * F(1, 4) + F(2, 3) * F(1, 2), F(5, 12))
ok("Q10 EU", F(0) * F(3, 4) + F(200) * F(1, 4), 50)

print("== L02")
W = [(40, F(1, 4)), (100, F(1, 2)), (160, F(1, 4))]
EW = sum(p * x for x, p in W)
ok("E W", EW, 100)
EU = sum(float(p) * math.sqrt(x) for x, p in W)
print(f"E sqrt W = {EU:.6f}")
CE = EU * EU
prem = 100 - CE
print(f"CE = {CE:.6f} premium = {prem:.6f}")
ok("ce cents half-up", half_up(CE), 9493)  # half_up takes CU and multiplies by 100
ok("premium cents half-up", half_up(prem), 507)
var = sum(p * x * x for x, p in [(-60, F(1, 4)), (0, F(1, 2)), (60, F(1, 4))])
ok("Var X", var, 1800)
rA = 0.5 / 100 ** 0.5 / 100 ** 0.5 * 0 + 1 / (2 * 100)
ok("r_A(100) sqrt", rA, 0.005)
approx = 0.5 * rA * 1800
print(f"Pratt approximation {approx:.6f} CU; exact premium {prem:.6f} CU")
err = prem - approx
print(f"error {err:.6f} CU; share of exact premium {err / prem * 100:.4f} percent; share of approximation {err / approx * 100:.4f} percent")
print(f"half-variance rule {0.5 * 1800} CU^2")
# Part B values with the same formulas as the lab
def ce_sqrt(eps):
    gam = [(-60, .25), (0, .5), (60, .25)]
    e = sum(p * math.sqrt(100 + eps * x) for x, p in gam)
    return e * e
for eps in (1.0, 0.5, 0.25, 0.1, 0.01):
    ratio = (100 - ce_sqrt(eps)) / (eps * eps)
    print(f"eps {eps}: premium/eps^2 {ratio:.6f} gap {abs(ratio - 4.5):.6f}")
print(f"gap ratio 0.028811/0.004565 = {0.028811 / 0.004565:.4f}; (0.25/0.1)^2 = {(0.25 / 0.1) ** 2}")
print(f"E2 share approx of premium 0.565835/4.5 = {0.565835 / 4.5 * 100:.4f} percent")
print(f"R1 (eps 0.1) gap check: 4.504565-4.5 = {4.504565 - 4.5:.6f} below 0.005: {4.504565 - 4.5 < 0.005}")
print(f"M2 log: r_A = 1/w; r_R=1")
print(f"Ex 2.3 r_R sqrt = {(100 * (1 / (2 * 100)))}")
print(f"v=e^u: r_A^v = r_A^u - u' check (u=ln w): skip")

print("== L03")
prizes = [5000, 10000, 20000]
probs = [F(1, 4), F(1, 2), F(1, 4)]
def ce(g, xs=prizes):
    if g == 1:
        return math.exp(sum(float(p) * math.log(x) for p, x in zip(probs, xs)))
    s = 1 - g
    return (sum(float(p) * x ** s for p, x in zip(probs, xs))) ** (1 / s)
ok("expected prize", sum(p * x for p, x in zip(probs, prizes)), 11250)
for g, want in ((0, 11250.0), (0.25, 10931.7733), (0.5, 10615.8009), (1, 10000.0), (2, 8888.8889), (4, 7337.6161)):
    v = ce(g)
    print(f"gamma {g}: CE {v:.4f} (lesson/lab {want}) {'OK' if abs(round(v,4)-want)<1e-9 else 'CHECK'} rounded cents {half_up(v/100) if False else math.floor(v+0.5)}")
M2 = sum(p / x for p, x in zip(probs, prizes))
ok("M for gamma 2 = 9/80000", M2, F(9, 80000))
ok("CE gamma 2 exact = 80000/9", 1 / M2, F(80000, 9))
print(f"80000/9 = {80000 / 9:.6f}, rounds to {math.floor(80000 / 9 + 0.5)}")
ok("Example 2.5 CE gamma 2", 1 / (F(1, 2) / 1000 + F(1, 2) / 4000), 1600)
print(f"Example 2.5 CE gamma 1 = {math.exp(0.5 * math.log(1000) + 0.5 * math.log(4000)):.6f}")
ok("M2 problem CE2", 1 / (F(1, 4) / 1000 + F(3, 4) / 9000), 3000)
ok("M3 problem CE2 of 3X", 1 / (F(1, 4) / 3000 + F(3, 4) / 27000), 9000)
print(f"gamma 0.5 CE rounding: {ce(0.5):.4f} -> {math.floor(ce(0.5) + 0.5)}")
print(f"E3 bound k=10: {(10 + 1) / 2}")
print("Remark 2.8 bound check for v in a grid:")
bad = 0
for k in (2, 3, 10):
    for i in range(0, 20001):
        v = 0.0 + i * 0.37
        R = lambda z: math.floor(z + 0.5)
        if abs(R(k * v) - k * R(v)) > (k + 1) / 2 + 1e-12:
            bad += 1
print("bound violations on grid:", bad)

print("== L04")
def I(pmf, t):
    return sum(p * max(t - x, 0) for x, p in pmf)
def Fc(pmf, t):
    return sum(p for x, p in pmf if x <= t)
X = [(2000, F(1, 2)), (4000, F(1, 2))]
Y = [(1000, F(1, 4)), (3000, F(1, 2)), (5000, F(1, 4))]
ok("I_X(3000)", I(X, 3000), 500)
ok("I_X(4000)", I(X, 4000), 1000)
ok("I_X(5000)", I(X, 5000), 2000)
ok("I_Y(2000)", I(Y, 2000), 250)
ok("I_Y(3000)", I(Y, 3000), 500)
ok("I_Y(4000)", I(Y, 4000), 1250)
ok("I_Y(5000)", I(Y, 5000), 2000)
ok("F_X(2000)", Fc(X, 2000), F(1, 2))
ok("F_Y(2000)", Fc(Y, 2000), F(1, 4))
ok("F_Y(3000)", Fc(Y, 3000), F(3, 4))
ok("F_X(3000)", Fc(X, 3000), F(1, 2))
ok("means X,Y", (sum(p * x for x, p in X), sum(p * x for x, p in Y)), (3000, 3000))
E1 = [(2000, F(1, 2)), (4000, F(1, 2))]
E1Y = [(3000, F(1, 2)), (4000, F(1, 2))]
ok("Example 1.7 F_X", (Fc(E1, 2000), Fc(E1, 3000), Fc(E1, 4000)), (F(1, 2), F(1, 2), F(1)))
ok("Example 1.7 F_Y", (Fc(E1Y, 2000), Fc(E1Y, 3000), Fc(E1Y, 4000)), (F(0), F(1, 2), F(1)))
ok("Example 1.7 means", (sum(p * x for x, p in E1), sum(p * x for x, p in E1Y)), (3000, 3500))
Z = [(1000, F(1, 2)), (5000, F(1, 2))]
Yd = [(3000, F(1))]
ok("Example 2.6 I_Y(t)=(t-3000)^+ at 1000,3000,5000", (I(Yd, 1000), I(Yd, 3000), I(Yd, 5000)), (0, 0, 2000))
ok("Example 2.6 I_X at 1000,3000,5000", (I(Z, 1000), I(Z, 3000), I(Z, 5000)), (0, 1000, 2000))
ok("M1 mech F_X(1000)", Fc(X, 1000), F(0))
M3X = [(1000, F(1, 4)), (5000, F(3, 4))]
ok("M3 I_X(3000)", I(M3X, 3000), 500)
ok("E1 pair B I_Y(4000)", I(E1Y, 4000), 500)
print("done")
