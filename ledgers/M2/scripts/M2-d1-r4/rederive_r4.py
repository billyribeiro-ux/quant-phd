"""Independent re-derivation for M2 slice d1 (L19, L20, L21), round 4. Standard library only. Run with python3 -I."""
from fractions import Fraction as Fr
import math
import random

def f(x, y): return math.exp(x) * y + x * y * y
def grad(x, y): return (math.exp(x) * y + y * y, math.exp(x) + 2 * x * y)
p = (0.5, 0.25); d = (0.6, -0.8)
e = math.exp(0.5)
H = ((e * 0.25, e + 0.5), (e + 0.5, 1.0))
print("L19 closed form: f_xx=%.6f f_xy=%.6f f_yy=%.6f" % (H[0][0], H[0][1], H[1][1]))
print("L19 e^0.5/4 = %.5f, e^0.5+0.5 = %.5f" % (e / 4, e + 0.5))
a, b = d
dHd = a * a * H[0][0] + 2 * a * b * H[0][1] + b * b * H[1][1]
print("L19 d^T H d = %.5f  (page E2: about -1.274)" % dHd)
g3 = e * (a**3 * 0.25 + 3 * a * a * b) + 6 * a * b * b
g = lambda s: f(p[0] + s * a, p[1] + s * b)
hh = 1e-2
g3num = (g(2*hh) - 2*g(hh) + 2*g(-hh) - g(-2*hh)) / (2 * hh**3)
print("L19 g'''(0) analytic = %.5f, numeric = %.5f  (page E3: about 0.969)" % (g3, g3num))
def fdH(x, y, h):
    rows = []
    for i in range(2):
        row = []
        for j in range(2):
            up = [x, y]; dn = [x, y]; up[j] += h; dn[j] -= h
            row.append((grad(*up)[i] - grad(*dn)[i]) / (2 * h))
        rows.append(row)
    return rows
F = fdH(0.5, 0.25, 1e-5)
worst = max(abs(F[i][j] - H[i][j]) for i in range(2) for j in range(2))
print("L19 central-difference worst error %.3e, asymmetry %.3e" % (worst, abs(F[0][1] - F[1][0])))
def q(s): return f(0.5 + s * a, 0.25 + s * b)
g0 = grad(0.5, 0.25)
def first(s): return q(s) - (f(0.5, 0.25) + s * (g0[0] * a + g0[1] * b))
def second(s): return q(s) - (f(0.5, 0.25) + s * (g0[0] * a + g0[1] * b) + 0.5 * s * s * dHd)
prev = None
for s in (0.1, 0.05, 0.025, 0.0125):
    e1, e2 = first(s), second(s)
    if prev: print("L19 s=%g first %.6e second %.6e ratios %.4f %.4f" % (s, e1, e2, prev[0] / e1, prev[1] / e2))
    else: print("L19 s=%g first %.6e second %.6e" % (s, e1, e2))
    prev = (e1, e2)
def ex22(x, y):
    if x == 0 and y == 0: return 0.0
    return x * y * (x * x - y * y) / (x * x + y * y)
def fx(x, y, t=1e-7): return (ex22(x + t, y) - ex22(x - t, y)) / (2 * t)
for tt in (1e-2, 1e-3):
    print("L19 Ex2.2 f_xy(t,t) at t=%g ~ %.4f ; f_xy(t,0) ~ %.4f" % (tt, (fx(tt, tt+1e-9) - fx(tt, tt-1e-9)) / 2e-9, (fx(tt, 1e-9) - fx(tt, -1e-9)) / 2e-9))
print("L19 Ex2.2 f_x(0,y) at y=0.3: %.6f (page: -y = -0.3); f_y(x,0) at x=0.4: %.6f (page: x = 0.4)" % (
    (ex22(1e-6, 0.3) - ex22(-1e-6, 0.3)) / 2e-6, (ex22(0.4, 1e-6) - ex22(0.4, -1e-6)) / 2e-6))
def mids(lo, hi, n):
    w = (hi - lo) / n
    return [lo + (i + Fr(1, 2)) * w for i in range(n)]
ok = True
for n in (1, 2, 3, 4, 5, 8, 16, 32, 64):
    xs = mids(Fr(0), Fr(1), n); ys = mids(Fr(0), Fr(2), n)
    dx = Fr(1, n); dy = Fr(2, n)
    sx = sum((x * y + x * x) * dx * dy for x in xs for y in ys)
    sy = sum((x * y + x * x) * dx * dy for y in ys for x in xs)
    pred = Fr(5, 3) - Fr(1, 6 * n * n)
    ok = ok and (sx == pred and sy == pred)
print("L20 exact both orders equal 5/3-1/(6n^2) for n in 1,2,3,4,5,8,16,32,64:", ok)
print("L20 odd-square identity n<=200:", all(3*sum((2*i+1)**2 for i in range(n)) == n*(4*n*n-1) for n in range(1, 201)))
print("L20 P1 algebra identity n<500:", all(4*n**3+12*n**2+11*n+3 == (n+1)*(4*(n+1)**2-1) for n in range(0, 500)))
random.seed(0)
bad = 0
for _ in range(2000):
    x = random.uniform(0.01, 1); y = random.uniform(0.01, 1); t = 1e-6
    fint = (x*x - y*y) / (x*x + y*y)**2
    dy_ = ((y+t)/(x*x+(y+t)**2) - (y-t)/(x*x+(y-t)**2)) / (2*t)
    dx_ = ((-(x+t))/((x+t)**2+y*y) - (-(x-t))/((x-t)**2+y*y)) / (2*t)
    if abs(dy_ - fint) > 1e-4 * max(1, abs(fint)) or abs(dx_ - fint) > 1e-4 * max(1, abs(fint)): bad += 1
print("L20 Ex3.1 antiderivative derivative checks failures:", bad)
def Fr_(x, y): return y**3 + x*y - 1
def root_bisect(x):
    lo, hi = 0.0, 2.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if Fr_(x, mid) > 0: hi = mid
        else: lo = mid
    return (lo + hi) / 2
for x in (0.25, 0.5, 1.0, 2.0):
    y = root_bisect(x)
    formula = -y / (3*y*y + x)
    h = 1e-5
    cd = (root_bisect(x+h) - root_bisect(x-h)) / (2*h)
    print("L21 x=%g y=%.10f F_y=%.6f formula=%.10f central=%.10f diff=%.2e" % (x, y, 3*y*y+x, formula, cd, abs(formula-cd)))
print("L21 circle slope -0.6/sqrt(1-0.36) =", -0.6/math.sqrt(1-0.36), " -F_x/F_y =", -1.2/1.6)
