"""Independent recomputation of the M2 L01-L06 displayed numbers (round 3, verifier M2-a)."""
from fractions import Fraction as F
import math

def row(name, value):
    print(f"{name}: {value}")

# L01: a_n = (2n+1)/(n+1), error 1/(n+1); least N for tolerance 1/1000
err = lambda n: F(1, n + 1)
row("L01 error n=999 exact", float(err(999)))
row("L01 error n=1000 exact", float(err(1000)))
row("L01 n=10 error", float(err(10)))
row("L01 E1 1/1001 six-digit mantissa", f"{1/1001:.6e}")
row("L01 least N for 0.001 (formula)", min(n for n in range(1, 5001) if all(err(m) < F(1, 1000) for m in range(n, 5001))))
# L02: closed forms
for n in (1, 10, 100, 1000, 10000):
    a = F(2*n+1, n+1); b = F(n+2, n)
    s = abs(a + b - 3); p = abs(a*b - 2); q = abs(a/b - 2)
    assert s == F(n+2, n*(n+1)) and p == F(3*n+2, n*(n+1)) and q == F(5*n+4, (n+1)*(n+2))
    row(f"L02 n={n} errors", f"{float(s):.6e} {float(p):.6e} {float(q):.6e}")
row("L02 E2 302/10100 digits", float(F(302, 10100)))
# L03: gap 1+4h-h^2 and f values
for k in range(1, 5):
    h = F(1, 10**k)
    left = (1 - h)**2; right = 2 + 2*h
    row(f"L03 h=1e-{k}", f"{float(left):.6f} {float(right):.6f} {float(right-left):.6f}")
row("L03 E2 1+4(0.01)-(0.01)^2", float(1 + F(4, 100) - F(1, 10000)))
# L04: Q(h) = 3+3h+h^2
for k in range(1, 7):
    h = F(1, 10**k); Q = 3 + 3*h + h*h
    row(f"L04 h=1e-{k}", f"{float(Q):.6f} {float(abs(Q-3)):.6e}")
row("L04 E2 error at h=1e-5 exact equals 3.00001e-5", F(3, 10**5) + F(1, 10**10) == F(300001, 10**10))
# L05: analytic derivatives and central-difference errors at x=1.5, h=1e-4
x = 1.5; h = 1e-4
p = lambda t: (t*t+1)*t**3
q = lambda t: (t*t+1)/(t+2)
c = lambda t: (t*t+1)**3
dp = 2*x*x**3 + (x*x+1)*3*x*x
dq = (x*x+4*x-1)/(x+2)**2
dc = 6*x*(x*x+1)**2
row("L05 analytic", f"{dp:.9f} {dq:.9f} {dc:.9f}")
row("L05 p'''(1.5)/6*h^2", 141/6*h*h)
row("L05 29/49 9dp", f"{29/49:.9f}")
row("L05 c'(1.5)", dc)
# L06: f=x^3-3x on grid of step 1/4 from -2 to 2
f = lambda t: t**3 - 3*t
pts = [F(-2) + F(i, 4) for i in range(17)]
inc = sum(1 for lo, hi in zip(pts, pts[1:]) if f(hi) > f(lo))
row("L06 increasing intervals", f"{inc} of 16")
row("L06 f(-1), f(1)", (f(F(-1)), f(F(1))))
row("L06 c=2/sqrt3", 2/math.sqrt(3))
row("L06 c=1/sqrt3", 1/math.sqrt(3))
