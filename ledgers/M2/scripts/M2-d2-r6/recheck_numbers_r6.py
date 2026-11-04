"""Independent re-derivation of the numbers printed or stated on L22-L24 (round 6). Standard library only.
Run as: python3 -I ledgers/M2/scripts/M2-d2-r6/recheck_numbers_r6.py"""
import math
from fractions import Fraction
import struct

print("== L22 Part A: V'(a) = ln a, central difference at h=1e-4 of V computed by the lab's own V(a)")
GOLD = (math.sqrt(5) - 1) / 2

def gmax(f, lo, hi, tol=1e-12):
    a, b = lo, hi
    c = b - GOLD * (b - a); d = a + GOLD * (b - a)
    fc, fd = f(c), f(d)
    while b - a > tol:
        if fc > fd:
            b, d, fd = d, c, fc; c = b - GOLD * (b - a); fc = f(c)
        else:
            a, c, fc = c, d, fd; d = a + GOLD * (b - a); fd = f(d)
    return (a + b) / 2

for a in (1.5, 2.0, 3.0, 4.0):
    f = lambda x, a=a: a * math.log(1 + x) - x
    xs = gmax(f, 0.0, 10.0)
    V = lambda t: f(gmax(lambda x: t * math.log(1 + x) - x, 0.0, 10.0), t)
    h = 1e-4
    fd = (V(a + h) - V(a - h)) / (2 * h)
    print(f"a={a} x_hat={xs:.10f} x_hat-(a-1)={xs-(a-1):+.3e} fd={fd:.10f} ln a={math.log(a):.10f} diff={fd-math.log(a):+.3e} f_a(x_hat)={math.log(1+xs):.10f} diff={math.log(1+xs)-math.log(a):+.3e}")

print("== L22 remark: f_xx at a=1.5, x_hat=0.5; objective change for 1e-8 location error")
a = 1.5; xh = 0.5
fxx = -a / (1 + xh) ** 2
print("f_xx =", fxx, " 0.5*|f_xx|*1e-16 =", 0.5 * abs(fxx) * 1e-16, " 0.5*0.666667*1e-16 =", 0.5 * 0.666667 * 1e-16)
print("sqrt(eps) =", math.sqrt(2.220446049250313e-16))

print("== L22 Example 1.5 / Example 2.2 / Example 2.3 numbers")
print("V(1.5) check: a ln a - (a-1) =", 1.5 * math.log(1.5) - 0.5)
print("Q2: a^2/2 with a^2=5 ->", 5 / 2)
print("Q3: V'(1) of Ex 2.2 = 1/2 ->", 1 / 2)
print("M3 (L22): V'(1) = 1/4 ->", 1 / 4)
print("Ex 2.2 check: F_x at a/2 zero, V=a^2/4 at a=2 ->", 2 * 2 / 4)

print("== L23 numbers")
FACE = 100000; COUP = 5000; N = 10; y0 = 0.04
def c(t): return COUP + (FACE if t == N else 0)
def P_exact(y):
    v = 1 + Fraction(y)
    return sum((Fraction(c(t)) / v**t for t in range(1, N + 1)), Fraction(0))
def P1(y):
    v = 1 + Fraction(y)
    return -sum((Fraction(t * c(t)) / v**(t + 1) for t in range(1, N + 1)), Fraction(0))
def P2(y):
    v = 1 + Fraction(y)
    return sum((Fraction(t * (t + 1) * c(t)) / v**(t + 2) for t in range(1, N + 1)), Fraction(0))
p0 = float(P_exact(y0)); d1 = float(P1(y0)); d2 = float(P2(y0))
print("P(y0) =", p0, " P'(y0) =", d1, " P''(y0) =", d2)
print("-P'/P =", -d1 / p0, " P''/P =", d2 / p0)
print("integer price cents:", round(P_exact(y0)), " half-even check: frac part", float(P_exact(y0)) - math.floor(float(P_exact(y0))))
prev1 = prev2 = None
for dy in (0.01, 0.005, 0.0025):
    e1 = P_exact(y0 + dy) - (P_exact(y0) + Fraction(d1) * Fraction(dy))
    e2 = e1 - Fraction(1, 2) * Fraction(d2) * Fraction(dy) ** 2
    e2 = P_exact(y0 + dy) - (P_exact(y0) + Fraction(d1) * Fraction(dy) + Fraction(1, 2) * Fraction(d2) * Fraction(dy) ** 2)
    line = f"dy={dy}: e1={float(e1):.6e} e2={float(e2):.6e}"
    if prev1 is not None:
        line += f" ratios {float(prev1 / e1):.4f} {float(prev2 / e2):.4f}"
    print(line)
    prev1, prev2 = e1, e2
for dy in (0.01, -0.01):
    ex = round(P_exact(y0 + dy)); ap = round(P_exact(y0) + Fraction(d1) * Fraction(dy) + Fraction(1, 2) * Fraction(d2) * Fraction(dy) ** 2)
    unr = float(P_exact(y0 + dy) - (P_exact(y0) + Fraction(d1) * Fraction(dy) + Fraction(1, 2) * Fraction(d2) * Fraction(dy) ** 2))
    print(f"shift {dy:+}: exact {ex} expansion {ap} rounded diff {ex-ap}; unrounded error {unr:.4f} cents; sign check (should be sign of -dy): {'ok' if (unr<0)==(dy>0) else 'BAD'}")
off = 0.04 + 0.01 - 0.05
print("float 0.04+0.01 - 0.05 =", off, " exact rational offset:", float(Fraction(0.04) + Fraction(0.01) - Fraction(0.05)))
print("P'(0.05) =", float(P1(0.05)), " P'(0.05)*offset(exact) =", float(P1(0.05)) * float(Fraction(0.04) + Fraction(0.01) - Fraction(0.05)))
print("P(0.05) unrounded =", float(P_exact(0.05)), " rounded:", round(P_exact(0.05)))
print("CHECK: P'' central offset etc. not printed by page")
# Q8 numeric: cash flows -1 at t=1, 1000 at t=2, y=0.04
v = 1.04
Pp = -((1 * -1) / v ** 2 + (2 * 1000) / v ** 3)
print("Q8 P'(0.04) with c1=-1, c2=1000 =", Pp)
print("M1 (L23): 50/1.05 =", 50 / 1.05, " 1050/1.05^2 =", 1050 / 1.05**2, " sum =", 50 / 1.05 + 1050 / 1.05**2)
print("M3 (L23): P'(0.04)=-200/1.04^3 =", -200 / 1.04**3)
print("Q3 (L23) numeric 1000 ok; Q6 P'(0) = -200 ->", -200 * 1 ** -3)
print("E2 ratio check (L23): 3.9279 vs 4, 7.8807 vs 8 (printed)")
print("== L24 numbers")
e = math.e
print("2 sqrt(delta/e) =", 2 * math.sqrt(2.22e-16 / e), " (3 delta/e)^(1/3) =", (3 * 2.22e-16 / e) ** (1 / 3))
ulp_e = math.ulp(e)
print("ulp(e) =", ulp_e, " half ulp(e) =", ulp_e / 2, " ulp(e)/2 vs 2.22e-16 ->", ulp_e / 2)
print("1/2 e h at h=1e-5:", 0.5 * e * 1e-5, " at h=1e-6:", 0.5 * e * 1e-6)
print("Prop 4.2 check h*=2 sqrt(delta/M2) at delta=0.5, M2=2:", 2 * math.sqrt(0.5 / 2))
print("R1 numeric: h*/10 ratio, 2 delta/h* = sqrt(M2 delta)?", 2 * 0.3 / (2 * math.sqrt(0.3 / 2)), math.sqrt(2 * 0.3))
print("E2 round-off bound 2*delta/h at h=1e-15:", 2 * 2.22e-16 / 1e-15)
print("M3 (L24): D+ = (2.1^3-8)/0.1 =", (2.1**3 - 8) / 0.1, " error", (2.1**3 - 8) / 0.1 - 12, " M2 bound 0.5*12.6*0.1 =", 0.5 * 12.6 * 0.1)
print("M1 (L24) D+ at x=1:", ((1 + 0.3) ** 2 - 1) / 0.3, " D0:", ((1.3) ** 2 - 0.7 ** 2) / 0.6)
print("L24 Q7: h* with delta=0.5, M2=2 ->", 2 * math.sqrt(0.5 / 2))
print("Prop 4.3 h*: (3*delta/M3)^(1/3) check at delta=1,M3=3 ->", (3 * 1 / 3) ** (1 / 3))
