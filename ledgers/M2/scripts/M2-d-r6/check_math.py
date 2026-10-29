# Independent re-derivation for M2 slice d (L19-L24), round 6. Standard library + sympy if present.
from fractions import Fraction as Fr
import math, sys
try:
    import sympy as sp
except ImportError:
    sp = None
print("sympy available:", sp is not None)

# L19 Example 2.2: f = xy(x^2-y^2)/(x^2+y^2), f(0,0)=0
def f(x, y):
    if x == 0 and y == 0:
        return 0.0
    return x * y * (x * x - y * y) / (x * x + y * y)
def fx(x, y, h=1e-7):
    return (f(x + h, y) - f(x - h, y)) / (2 * h)
# analytic f_x(0,y) = -y  (limit of difference quotient at origin)
for y in (0.5, -0.3):
    print("L19 f_x(0,%g) quotient at h=1e-6:" % y, (f(1e-6, y) - f(0, y)) / 1e-6, "expected", -y)
for x in (0.5, -0.3):
    print("L19 f_y(%g,0) quotient at k=1e-6:" % x, (f(x, 1e-6) - f(x, 0)) / 1e-6, "expected", x)
# f_xy(0,0) = d/dy f_x at (0,0): f_x(0,y)=-y -> -1 ; f_yx(0,0): f_y(x,0)=x -> 1
print("L19 f_xy(0,0) = d/dy [f_x(0,y)] =", (-(1e-6) - (-(-1e-6))) / 2e-6)
if sp is not None:
    x, y = sp.symbols("x y", real=True)
    F = x * y * (x**2 - y**2) / (x**2 + y**2)
    Fxy = sp.simplify(sp.diff(F, x, y))  # d/dy(d/dx F)
    print("L19 symbolic f_xy off origin:", sp.factor(Fxy))
    # approach along y=x and along x=0 to see f_xy limit behaviour near origin
    t = sp.symbols("t", positive=True)
    print("L19 f_xy along y=x:", sp.limit(Fxy.subs({x: t, y: t}), t, 0, "+"))
    print("L19 f_xy along y=0 direction (x=t,y=0):", sp.limit(Fxy.subs({x: t, y: 0}), t, 0, "+"))
    print("L19 f_xy along x=0 (y=t):", sp.limit(Fxy.subs({x: 0, y: t}), t, 0, "+"))

# L19 Theorem 3.1 bound check: |R| <= 2|h|^2 omega for f(x,y)=e^x y + x y^2 at p=(0.5,0.25)
# (not needed beyond the lab; skip)

# L19 E1 rounding estimate
print("L19 E1 eps/h =", 2.220446049250313e-16 / 1e-5)

# L20 Prop 2.4: exact midpoint sums, both orders, Fractions, n=1..8
def mid(lo, hi, n):
    w = (hi - lo) / n
    return [lo + (i + Fr(1, 2)) * w for i in range(n)]
for n in (1, 2, 3, 5, 8):
    s = Fr(0)
    for x in mid(Fr(0), Fr(1), n):
        for y in mid(Fr(0), Fr(2), n):
            s += (x * y + x * x) * (Fr(1, n)) * (Fr(2, n))
    print("L20 n=%d midpoint sum %s, predicted 5/3-1/(6n^2)=%s, ok=%s" % (n, s, Fr(5, 3) - Fr(1, 6 * n * n), s == Fr(5, 3) - Fr(1, 6 * n * n)))
# L20 Example 3.1 numeric check of inner integrals
def g_inner_y(x, n=200000):
    # integral over y in (0,1] of f(x,y) dy, midpoint rule
    tot = 0.0
    for i in range(n):
        y = (i + 0.5) / n
        tot += (x * x - y * y) / (x * x + y * y) ** 2 / n
    return tot
for x in (0.5, 1.0):
    print("L20 Ex3.1 inner dy at x=%g numeric %.6f, claim 1/(1+x^2)=%.6f" % (x, g_inner_y(x), 1 / (1 + x * x)))
print("L20 pi/4 =", math.pi / 4)

# L21: implicit slope check for y^3+xy-1 at several x, using bisection (independent of lab Newton)
def root_bisect(x):
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid_ = (lo + hi) / 2
        if mid_ ** 3 + x * mid_ - 1 > 0:
            hi = mid_
        else:
            lo = mid_
    return (lo + hi) / 2
for x in (0.25, 0.5, 1.0, 2.0):
    y = root_bisect(x)
    slope_formula = -y / (3 * y * y + x)
    h = 1e-4
    slope_fd = (root_bisect(x + h) - root_bisect(x - h)) / (2 * h)
    print("L21 x=%g y=%.10f formula %.8f fd %.8f" % (x, y, slope_formula, slope_fd))

# L21 R3 / Example 2.2: circle slope
print("L21 circle slope at (0.6,0.8):", -2 * 0.6 / (2 * 0.8))

# L22 Part B and Ex 2.3 and M3
for a in (1.0, 2.0, 3.0):
    print("L22 partB V(a)=a^2/4 derivative a/2 =", a / 2)
print("L22 M3 check V(a)=a^2/8 at a=1 ->", 1 / 8, "V'(1)=", 1 / 4)

# L23: Prop 2.1 closed forms, numeric checks, cash-flow bond
FACE, CPN, YRS = 100000, 5000, 10
cf = [CPN + (FACE if t == YRS else 0) for t in range(1, YRS + 1)]
def P(y): return sum(c / (1 + y) ** t for t, c in zip(range(1, YRS + 1), cf))
def P1(y): return -sum(t * c / (1 + y) ** (t + 1) for t, c in zip(range(1, YRS + 1), cf))
def P2(y): return sum(t * (t + 1) * c / (1 + y) ** (t + 2) for t, c in zip(range(1, YRS + 1), cf))
y0 = 0.04
print("L23 P(y0)=%.6f P'=%.6f P''=%.6f" % (P(y0), P1(y0), P2(y0)))
print("L23 P(0.05)=%.6f" % P(0.05))
print("L23 -P'/P=%.6f P''/P=%.6f" % (-P1(y0) / P(y0), P2(y0) / P(y0)))
P1_0 = P1(y0); P_0 = P(y0)
for d in (0.01, -0.01):
    e2 = P(y0 + d) - (P_0 + P1_0 * d + 0.5 * P2(y0) * d * d)
    print("L23 shift %+.2f remainder %.4f (sign of -d expected)" % (d, e2))
# quiz L23q8 two-cash-flow example c1=-1, c2=1000, N=2, y=0.04
y = 0.04
print("L23 quiz two-cash-flow P'(y) =", -(1 * (-1) / (1 + y) ** 2 + 2 * 1000 / (1 + y) ** 3))
# L23 Prop 2.2: face value check at yield=coupon rate for 2-year bond
print("L23 M1 2-year bond at 0.05:", 50 / 1.05 + 1050 / 1.05 ** 2)

# L24 numbers
print("L24 e/2*1e-5 =", math.e / 2 * 1e-5)
print("L24 2*delta/h at 1e-15 =", 2 * 2.22e-16 / 1e-15)
print("L24 h* forward (M2=e, delta=2.22e-16) =", 2 * math.sqrt(2.22e-16 / math.e))
print("L24 h* central (M3=e) =", (3 * 2.22e-16 / math.e) ** (1 / 3))
print("L24 quiz h* =", 2 * math.sqrt(0.5 / 2))
print("L24 M3 cubic check: D+ at 2 with h=0.1 =", (2.1 ** 3 - 2 ** 3) / 0.1, "bound", 0.5 * 12.6 * 0.1)
print("L24 Lab delta: half ulp near e =", 2.0 ** -52, "ulp in [2,4) is 2^-51 =", 2.0 ** -51)
