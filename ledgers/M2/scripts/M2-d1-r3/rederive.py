"""Independent re-derivation of the numbers printed or stated on L19-L21 (not the twins' code).

Usage: python -I rederive.py. Uses only fractions, decimal and math.
"""
import math
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 50

print("== L19 Example 1.2: f = x^3 + 2xy^2 - y at (1,2)")
# f_x = 3x^2+2y^2, f_y = 4xy-1, f_xx=6x, f_xy=4y, f_yy=4x
x, y = 1, 2
print("f_x", 3 * x * x + 2 * y * y, "f_y", 4 * x * y - 1, "H", [[6 * x, 4 * y], [4 * y, 4 * x]])

print("== L19 Example 2.2 numeric: f(x,y)=xy(x^2-y^2)/(x^2+y^2)")
def f22(a, b):
    if a == 0 and b == 0:
        return 0.0
    return a * b * (a * a - b * b) / (a * a + b * b)
for t in (1e-3, 1e-5):
    fx0 = (f22(t, 0.0) - f22(0.0, 0.0)) / t
    fxy_origin = ((f22(0.0, t) - f22(0.0, 0.0)) / t)  # f_y(0,t)... not used directly
    print(f"h={t:g}: [f(h,0)-f(0,0)]/h={fx0:.3e}")
# f_x(0,y) = -y, f_y(x,0)=x exactly: check difference quotients at y=0.3, x=0.7
for yv in (0.3, -0.5):
    q = (f22(1e-7, yv) - f22(0.0, yv)) / 1e-7
    print(f"f_x(0,{yv}) ~ {q:.6f} (claimed {-yv})")
for xv in (0.7, -0.4):
    q = (f22(xv, 1e-7) - f22(xv, 0.0)) / 1e-7
    print(f"f_y({xv},0) ~ {q:.6f} (claimed {xv})")
# diagonal and axis values of f_xy from the closed form M/D + y d_y(M/D)
def fxy_closed(a, b):
    M = a**4 + 4*a*a*b*b - b**4
    D = (a*a + b*b) ** 2
    dMdy = 8*a*a*b - 4*b**3
    dDdy = 4*b*(a*a + b*b)
    return M / D + b * (dMdy * D - M * dDdy) / (D * D)
for t in (0.1, -0.2):
    print(f"f_xy({t},{t}) closed = {fxy_closed(t, t):.12f} (claimed 0); f_xy({t},0) = {fxy_closed(t, 0.0):.12f} (claimed 1)")

print("== L19 lab: closed-form values at base point (0.5, 0.25)")
X, Y = Decimal("0.5"), Decimal("0.25")
ex = X.exp()
fxx = ex * Y
fxy = ex + 2 * Y
fyy = 2 * X
print(f"f_xx={float(fxx):.6f} f_xy={float(fxy):.6f} f_yy={float(fyy):.6f}")
print(f"fxx predicted e^0.5/4 = {float(ex/4):.5f}; fxy predicted e^0.5+0.5 = {float(ex+Decimal('0.5')):.5f}")
print(f"grad f_x={float(ex*Y+Y*Y):.6f} f_y={float(ex+2*X*Y):.6f}")

def f_lab(p):
    x_, y_ = p
    return math.exp(x_) * y_ + x_ * y_ * y_

# direction d and d^T H d, g'''(0) computed from the closed third partials
d1, d2 = 0.6, -0.8
dHd = d1 * d1 * float(fxx) + 2 * d1 * d2 * float(fxy) + d2 * d2 * float(fyy)
print(f"d^T H d = {dHd:.6f} (E2 claims about -1.274)")
# third partials of f = e^x y + x y^2 : f_xxx = e^x y, f_xxy = e^x, f_xyy = 2, f_yyy = 0
e = math.exp(0.5)
g3 = e * 0.25 * d1**3 + 3 * e * d1 * d1 * d2 + 3 * 2.0 * d1 * d2 * d2 + 0.0
print(f"g'''(0) = {g3:.6f} (E3 claims about 0.969)")
# cross-check g''' by finite differences of g(s)=f(p+s d) with high-precision style steps
def g(s):
    return f_lab((0.5 + s * d1, 0.25 + s * d2))
h = 1e-2
g3_fd = (g(2*h) - 2*g(h) + 2*g(-h) - g(-2*h)) / (2 * h**3)
print(f"g'''(0) finite-difference check (h=1e-2): {g3_fd:.4f}")

# the printed step ratios: first-order and second-order errors along d at base point
p = (0.5, 0.25)
gx = (math.exp(p[0]) * p[1] + p[1]**2, math.exp(p[0]) + 2*p[0]*p[1])
hess = ((math.exp(p[0])*p[1], math.exp(p[0]) + 2*p[1]), (math.exp(p[0]) + 2*p[1], 2*p[0]))
quad = d1 * (hess[0][0]*d1 + hess[0][1]*d2) + d2 * (hess[1][0]*d1 + hess[1][1]*d2)
def e1(s):
    return f_lab((p[0]+s*d1, p[1]+s*d2)) - (f_lab(p) + s*(gx[0]*d1 + gx[1]*d2))
def e2(s):
    return e1(s) - 0.5*s*s*quad
prev = None
for s in (0.1, 0.05, 0.025, 0.0125):
    a, b = e1(s), e2(s)
    line = f"s={s:<7g} e1={a:.6e} e2={b:.6e}"
    if prev:
        line += f" ratios {prev[0]/a:.4f} {prev[1]/b:.4f}"
    print(line)
    prev = (a, b)

print("== L19 central difference of the closed gradient at step 1e-5 (Hessian entries)")
def grad(p_):
    x_, y_ = p_
    return (math.exp(x_)*y_ + y_*y_, math.exp(x_) + 2*x_*y_)
hh = 1e-5
def cd(i, j):
    up = [p[0], p[1]]; dn = [p[0], p[1]]
    up[j] += hh; dn[j] -= hh
    return (grad(up)[i] - grad(dn)[i]) / (2*hh)
M = [[cd(0,0), cd(0,1)], [cd(1,0), cd(1,1)]]
ref = [[float(fxx), float(fxy)], [float(fxy), float(fyy)]]
print("max err", max(abs(M[i][j] - ref[i][j]) for i in range(2) for j in range(2)), "asym", abs(M[0][1]-M[1][0]))

print("== L20 exact checks")
def midpoints(lo, hi, n):
    w = (hi - lo) / n
    return [lo + (i + Fraction(1, 2)) * w for i in range(n)]
def f20(x_, y_):
    return x_ * y_ + x_ * x_
for n in (1, 2, 4, 8, 16, 32, 64):
    xs = midpoints(Fraction(0), Fraction(1), n)
    ys = midpoints(Fraction(0), Fraction(2), n)
    dx, dy = Fraction(1, n), Fraction(2, n)
    sx = sum(f20(a, b) * dx * dy for a in xs for b in ys)
    sy = sum(f20(a, b) * dx * dy for b in ys for a in xs)
    pred = Fraction(5, 3) - Fraction(1, 6 * n * n)
    assert sx == pred and sy == pred, n
print("Prop 2.4 midpoint sums equal 5/3 - 1/(6n^2) exactly in both orders for n = 1,2,4,...,64: True")
for n in range(1, 200):
    assert sum(Fraction(2*i+1)**2 for i in range(n)) == Fraction(n*(4*n*n-1), 3)
print("odd-square identity for n<200: True")
# Example 3.1 numeric: inner integrals
def fe(a, b):
    return (a*a - b*b) / (a*a + b*b) ** 2
def simpson(fn, lo, hi, m=20000):
    hstep = (hi - lo) / m
    s = fn(lo) + fn(hi)
    for k in range(1, m):
        s += (4 if k % 2 else 2) * fn(lo + k*hstep)
    return s * hstep / 3
for xv in (0.3, 0.8):
    val = simpson(lambda yv: fe(xv, yv), 1e-6, 1.0)
    print(f"Example 3.1 inner int_0^1 f(x={xv},y)dy ~ {val:.6f}, closed 1/(1+x^2) = {1/(1+xv*xv):.6f}")
print("pi/4 =", math.pi/4)
print("f(t,y) near y->0 at t=0.5:", fe(0.5, 1e-9), "1/t^2 =", 1/0.25)
