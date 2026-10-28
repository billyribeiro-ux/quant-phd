# Verifier round 2 (slice M2-d): independent recomputation of the numbers in the changed prose of L19-L24.
# Standard library only. Run as: python -I recheck_r2.py
import math
from fractions import Fraction
from decimal import Decimal, getcontext

getcontext().prec = 60

# L19: f = e^x y + x y^2 at (0.5, 0.25), d = (0.6, -0.8)
def f19(x, y):
    return math.exp(x) * y + x * y * y
p = (0.5, 0.25); d = (0.6, -0.8)
e = math.exp(0.5)
fx = e * 0.25 + 0.0625; fy = e + 2 * 0.5 * 0.25
gp = fx * d[0] + fy * d[1]
H = (e * 0.25, e + 0.5, 1.0)  # f_xx, f_xy, f_yy
gpp = d[0] ** 2 * H[0] + 2 * d[0] * d[1] * H[1] + d[1] ** 2 * H[2]
print("L19 f_xy =", round(H[1], 6), " cross-term magnitude at s=0.1:", abs(H[1] * d[0] * d[1] * 0.01))
e1 = [f19(p[0] + s * d[0], p[1] + s * d[1]) - f19(*p) - s * gp for s in (0.1, 0.05, 0.025, 0.0125)]
e2 = [E - 0.5 * s * s * gpp for E, s in zip(e1, (0.1, 0.05, 0.025, 0.0125))]
print("L19 first-order ratios", [round(e1[i - 1] / e1[i], 4) for i in (1, 2, 3)])
print("L19 second-order ratios", [round(e2[i - 1] / e2[i], 4) for i in (1, 2, 3)])
print("L19 second-order error at s=0.1:", f"{e2[0]:.6e}")

# L20: exact midpoint sums, both orders
def mids(lo, hi, n):
    w = Fraction(hi - lo, n)
    return [lo + (i + Fraction(1, 2)) * w for i in range(n)]
ok = True
for n in (1, 2, 3, 4, 8, 16, 32):
    xs, ys = mids(Fraction(0), Fraction(1), n), mids(Fraction(0), Fraction(2), n)
    dx, dy = Fraction(1, n), Fraction(2, n)
    sx = sum((x * y + x * x) * dx * dy for x in xs for y in ys)
    sy = sum((x * y + x * x) * dx * dy for y in ys for x in xs)
    ok &= (sx == sy == Fraction(5, 3) - Fraction(1, 6 * n * n))
print("L20 both orders equal 5/3 - 1/(6 n^2) for n in 1,2,3,4,8,16,32:", ok)

# L20 Example 3.1 iterated integrals (midpoint-free): check antiderivatives numerically at x=0.5
def g(x, y):
    return (x * x - y * y) / (x * x + y * y) ** 2
def integ(fun, a, b, N=200000):
    h = (b - a) / N
    return sum(fun(a + (i + 0.5) * h) for i in range(N)) * h
x0 = 0.5
print("L20 Ex3.1 inner dy at x=0.5:", round(integ(lambda y: g(x0, y), 0.0, 1.0), 6), "vs 1/(1+x^2) =", round(1 / (1 + x0 * x0), 6))
y0 = 0.5
print("L20 Ex3.1 inner dx at y=0.5:", round(integ(lambda x: g(x, y0), 0.0, 1.0), 6), "vs -1/(1+y^2) =", round(-1 / (1 + y0 * y0), 6))

# L21: roots, F_y range, dy/dx formula at x=0.25..2
def root(x):
    y = 1.0
    for _ in range(200):
        y -= (y ** 3 + x * y - 1) / (3 * y * y + x)
    return y
for x in (0.25, 0.5, 1.0, 2.0):
    y = root(x)
    print("L21 x", x, "y", f"{y:.10f}", "F_y", f"{3 * y * y + x:.6f}", "dy/dx", f"{-y / (3 * y * y + x):.10f}")
# F_y over the grid lies between 2.39 and 2.78 (page: about 2.4 to 2.8)
# F_y=0 example for Theorem 2.1 counterexample: F=y^3-x, (x0,y0)=(1,1), I=(-0.1,1.1), J=(-0.5,1.5)
F_y = lambda y: 3 * y * y
print("L21 counterexample: F(1,1)=", 1 - 1, " F_y(0,0)=", F_y(0.0), " g(x)=cbrt(x) in J on I:",
      all(-0.5 < math.copysign(abs(x) ** (1 / 3), x) < 1.5 for x in (-0.1, 0.0, 1.1)))
print("L21 cbrt(-0.1)=", round(math.copysign(abs(-0.1) ** (1 / 3), -0.1), 4), " cbrt(1.1)=", round(1.1 ** (1 / 3), 4))

# L22: V(a) = a ln a - (a-1), V'(a) = ln a; Part B V = a^2/4 ; f_xx at x*=a-1 for a=1.5
for a in (1.5, 2.0, 3.0, 4.0):
    h = 1e-4
    V = lambda t: t * math.log(t) - (t - 1)
    print("L22 a", a, "V' cd", f"{(V(a + h) - V(a - h)) / (2 * h):.8f}", "ln a", f"{math.log(a):.8f}")
a = 1.5
fxx = -a / (1 + (a - 1)) ** 2
print("L22 f_xx(x*,a) at a=1.5:", fxx, " objective change for 1e-8 location error:", 0.5 * abs(fxx) * 1e-16)

# L23: bond
cf = {t: 5000 + (100000 if t == 10 else 0) for t in range(1, 11)}
def P(y): return sum(cf[t] / (1 + y) ** t for t in cf)
def P1(y): return -sum(t * cf[t] / (1 + y) ** (t + 1) for t in cf)
def P2(y): return sum(t * (t + 1) * cf[t] / (1 + y) ** (t + 2) for t in cf)
def P3(y): return -sum(t * (t + 1) * (t + 2) * cf[t] / (1 + y) ** (t + 3) for t in cf)
y0 = 0.04
print("L23 P(0.04) =", f"{P(y0):.6f}", " P'=", f"{P1(y0):.6f}", " P''=", f"{P2(y0):.6f}", " P'''=", f"{P3(y0):.3f}")
print("L23 P(0.05) =", f"{P(0.05):.9f}")
print("L23 -P'/P =", f"{-P1(y0) / P(y0):.6f}", " P''/P =", f"{P2(y0) / P(y0):.6f}")
T1 = lambda dy: P(y0) + P1(y0) * dy
T2 = lambda dy: T1(dy) + 0.5 * P2(y0) * dy * dy
for dy in (0.01, -0.01):
    print("L23 shift", dy, "exact", f"{P(y0 + dy):.6f}", "T2", f"{T2(dy):.6f}", "exact-T2", f"{P(y0 + dy) - T2(dy):.6f}")
E1 = [P(y0 + dy) - T1(dy) for dy in (0.01, 0.005, 0.0025)]
E2 = [P(y0 + dy) - T2(dy) for dy in (0.01, 0.005, 0.0025)]
print("L23 first-order ratios", [round(E1[i - 1] / E1[i], 4) for i in (1, 2)], "second-order ratios", [round(E2[i - 1] / E2[i], 4) for i in (1, 2)])
# Prop 2.2 check: bond with yield equal to coupon rate prices at face, N=10, F=100000 coupon 5000
print("L23 par check (yield 0.05, coupon 5000, face 100000):", f"{sum(5000 / 1.05 ** t for t in range(1, 11)) + 100000 / 1.05 ** 10:.6f}")
# Counterexample to 'essential' hypothesis: c_1 = -1, c_2 = 1000 gives P' < 0 at y = 0.04
Pn = lambda y: -1 / (1 + y) + 1000 / (1 + y) ** 2
dPn = lambda y: 1 / (1 + y) ** 2 - 2000 / (1 + y) ** 3
print("L23 mixed-sign example: P'(0.04) =", f"{dPn(0.04):.4f}", "(negative, so 'every cash flow positive' is not necessary)")

# L24: errors and Lemma numbers
delta = 2.22e-16
print("L24 2 sqrt(delta/e) =", f"{2 * math.sqrt(delta / math.e):.4e}", " (3 delta/e)^(1/3) =", f"{(3 * delta / math.e) ** (1 / 3):.4e}")
for k in (1, 5, 8, 9, 11, 15):
    h = 10.0 ** -k
    fwd = abs((math.exp(1 + h) - math.e) / h - math.e)
    cen = abs((math.exp(1 + h) - math.exp(1 - h)) / (2 * h) - math.e)
    print("L24 k", k, f"fwd {fwd:.3e} cen {cen:.3e}")
print("L24 half e h at 1e-5 =", f"{0.5 * math.e * 1e-5:.4e}")
print("L24 Prop4.2 check: min of A h + B/h at h=sqrt(B/A) is 2 sqrt(AB) (A=M2/2,B=2delta) with M2=e:",
      round((e_ := math.e) / 2 * math.sqrt(4 * delta / e_) + 2 * delta / math.sqrt(4 * delta / e_), 12), round(2 * math.sqrt(e_ * delta), 12))
print("L24 M3 problem: 2.1^3-2^3 over 0.1 =", round((2.1 ** 3 - 8) / 0.1, 6))
