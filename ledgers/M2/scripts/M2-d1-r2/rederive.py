"""Independent re-derivation of the numbers and claims in M2 L19-L21 (verifier round 2, slice d1)."""
import math
import random
from fractions import Fraction as Fr

print("== L19 Example 1.2: f = x^3 + 2xy^2 - y at (1,2)")
x, y = 1.0, 2.0
print("fx", 3*x*x+2*y*y, "fy", 4*x*y-1, "fxx", 6*x, "fxy", 4*y, "fyy", 4*x)

print("== L19 Example 2.2: f = xy(x^2-y^2)/(x^2+y^2)")
def f(x, y):
    if x == 0 and y == 0:
        return 0.0
    return x*y*(x*x-y*y)/(x*x+y*y)
for y0 in (0.3, -0.7):
    h = 1e-7
    print("f_x(0,%s) numeric" % y0, (f(h, y0)-f(-h, y0))/(2*h), "claimed", -y0)
for x0 in (0.3, -0.7):
    h = 1e-7
    print("f_y(%s,0) numeric" % x0, (f(x0, h)-f(x0, -h))/(2*h), "claimed", x0)
def M(x, y): return x**4+4*x*x*y*y-y**4
def D(x, y): return (x*x+y*y)**2
t = 1e-3
print("diagonal fxy via formula (t,t):", M(t,t)/D(t,t) + t*(-1/t))
# fxy numeric along diagonal and axis via difference of fx
def fx(x, y, h=1e-6):
    return (f(x+h, y)-f(x-h, y))/(2*h)
def fxy(x, y, h=1e-4):
    return (fx(x, y+h)-fx(x, y-h))/(2*h)
for t in (1e-2, 1e-3):
    print("fxy numeric at (t,t) t=%g" % t, fxy(t, t), " at (t,0)", fxy(t, 0.0), " (t,1e-6)", fxy(t, 1e-6))
print("fxy(0,0) numeric", (fx(0.0, 1e-4)-fx(0.0, -1e-4))/(2e-4), "claimed -1")
print("fyx(0,0) numeric", ((f(1e-4, 0.0)-0.0)/1e-4) if False else "see below")
def fy(x, y, h=1e-6):
    return (f(x, y+h)-f(x, y-h))/(2*h)
print("fyx(0,0) numeric", (fy(1e-4, 0.0)-fy(-1e-4, 0.0))/(2e-4), "claimed 1")

print("== L19 Theorem 3.1 bound on a test function")
def g(x, y): return math.exp(x)*y + x*y*y
p = (0.5, 0.25)
def H(x, y): 
    e = math.exp(x); return ((e*y, e+2*y), (e+2*y, 2*x))
random.seed(0)
worst = 0.0
for _ in range(2000):
    hh = (random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2))
    r = math.hypot(*hh)
    lin = (math.exp(p[0])*p[1]+p[1]**2)*hh[0] + (math.exp(p[0])+2*p[0]*p[1])*hh[1]
    Hp = H(*p)
    quad = 0.5*(hh[0]*(Hp[0][0]*hh[0]+Hp[0][1]*hh[1]) + hh[1]*(Hp[1][0]*hh[0]+Hp[1][1]*hh[1]))
    R = g(p[0]+hh[0], p[1]+hh[1]) - g(*p) - lin - quad
    # omega(r) = sup over |q|<=r of max entry change; estimate by dense sampling
    om = 0.0
    for k in range(64):
        for j in range(64):
            ang = 2*math.pi*k/64; rad = r*j/63
            q = (rad*math.cos(ang), rad*math.sin(ang))
            Hq = H(p[0]+q[0], p[1]+q[1])
            om = max(om, max(abs(Hq[i][jj]-Hp[i][jj]) for i in range(2) for jj in range(2)))
    ratio = abs(R)/(2*r*r*om) if om > 0 else 0.0
    worst = max(worst, ratio)
print("Theorem 3.1 worst |R|/(2|h|^2 omega) over samples (must be <= 1):", round(worst, 6))

print("== L19 Prop 3.3 ratio: g(s)=s^3+s^4, E(s)=g(s)-g(0)-g'(0)s-g''(0)s^2/2")
def E(s): return s**3 + s**4
for s in (0.1, 0.01, 0.001):
    print("E(s)/E(s/2) at s=%g" % s, E(s)/E(s/2))

print("== L19 R2 inequality (sum|h_i|)^2 <= n |h|^2")
ok = True
for n in range(1, 8):
    for _ in range(2000):
        v = [random.uniform(-1, 1) for _ in range(n)]
        if (sum(abs(a) for a in v))**2 > n*sum(a*a for a in v)+1e-12: ok = False
print("holds:", ok)

print("== L20 Prop 2.4 exact for n=1..60 both orders (fractions)")
def mids(lo, hi, n):
    w = (hi-lo)/n
    return [lo + (i+Fr(1, 2))*w for i in range(n)]
def f20(x, y): return x*y + x*x
allok = True
for n in range(1, 61):
    xs = mids(Fr(0), Fr(1), n); ys = mids(Fr(0), Fr(2), n)
    dx = Fr(1, n); dy = Fr(2, n)
    sx = sum(sum(f20(x, y)*dy for y in ys)*dx for x in xs)
    sy = sum(sum(f20(x, y)*dx for x in xs)*dy for y in ys)
    pred = Fr(5, 3) - Fr(1, 6*n*n)
    if not (sx == pred and sy == pred): allok = False; print("FAIL", n)
print("Prop 2.4 holds for n=1..60 both orders:", allok)

print("== L20 Theorem 1.2: random tags and random partitions, mesh -> 0")
def rsum(n_x, n_y):
    xs = sorted([0.0, 1.0] + [random.random() for _ in range(n_x-1)])
    ys = sorted([0.0, 2.0] + [2*random.random() for _ in range(n_y-1)])
    S = 0.0
    for i in range(len(xs)-1):
        for j in range(len(ys)-1):
            a = random.uniform(xs[i], xs[i+1]); b = random.uniform(ys[j], ys[j+1])
            S += (a*b + a*a)*(xs[i+1]-xs[i])*(ys[j+1]-ys[j])
    mesh = max(max(xs[i+1]-xs[i] for i in range(len(xs)-1)), max(ys[j+1]-ys[j] for j in range(len(ys)-1)))
    return S, mesh
for N in (10, 100, 1000):
    S, mesh = rsum(N, N)
    print("N=%d mesh=%.4f |S-5/3|=%.5f" % (N, mesh, abs(S-5/3)))

print("== L20 Example 3.1 inner integrals and outer values")
def f31(x, y): return (x*x-y*y)/(x*x+y*y)**2
def integ(fn, a, b, n=20000):
    h = (b-a)/n
    return sum(fn(a+(i+0.5)*h) for i in range(n))*h
for x0 in (0.3, 0.7):
    print("int_0^1 f(x0,y)dy at x0=%g" % x0, integ(lambda yy: f31(x0, yy), 0.0, 1.0), "claim 1/(1+x^2)=", 1/(1+x0*x0))
for y0 in (0.3, 0.7):
    print("int_0^1 f(x,y0)dx at y0=%g" % y0, integ(lambda xx: f31(xx, y0), 0.0, 1.0), "claim -1/(1+y^2)=", -1/(1+y0*y0))
print("pi/4 =", math.pi/4)

print("== L21 Lab: Newton roots, slope formula, central difference")
def F(x, y): return y**3 + x*y - 1
def root(x):
    y = 1.0
    for _ in range(100):
        s = F(x, y)/(3*y*y+x); y -= s
        if abs(s) < 1e-15: return y
    raise RuntimeError
for x in (0.25, 0.5, 1.0, 2.0):
    yv = root(x)
    slope = -yv/(3*yv*yv+x)
    h = 1e-5
    cd = (root(x+h)-root(x-h))/(2*h)
    # uniqueness: F strictly increasing in y for x>0 (F_y = 3y^2+x > 0 on R)
    ys = [yy/1000 for yy in range(-5000, 5000)]
    sign_changes = sum(1 for a, b in zip(ys, ys[1:]) if F(x, a)*F(x, b) < 0)
    print("x=%g y=%.10f slope=%.10f cd=%.10f diff=%.1e sign_changes_on_grid=%d" % (x, yv, slope, cd, abs(slope-cd), sign_changes))

print("== L21 E2 truncation estimate (1/6)h^2 and rounding eps/h")
print("(1/6)h^2 at h=1e-5:", (1/6)*1e-10, " eps/h:", 2.220446e-16/1e-5)
print("== L21 example 2.2 slope at (0.6,0.8):", -0.6/0.8, " formula:", -2*0.6/(2*0.8))
print("== L21 misconception 2: F_y/F_x at (0.6,0.8):", (2*0.8)/(2*0.6))
print("== L21 R1: sign of 1/P'(y) for P'<0 is negative (sample P(y)=exp(-y))")
print("== L21 slope of x=sqrt(1-y^2) at y=0:", -0/math.sqrt(1-0))
