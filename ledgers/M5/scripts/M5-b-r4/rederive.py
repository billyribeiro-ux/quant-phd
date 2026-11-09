"""Independent re-derivation of the numbers printed in prose on L05-L07 (round 4, M5 slice b)."""
import math
from fractions import Fraction as F

print("== L05 Empirical 3 / quiz: 0.99^100 and ln route")
print("0.99**100 =", 0.99**100, " to 10dp", f"{float(F(99,100)**100):.10f}")
print("0.99**10 =", f"{float(F(99,100)**10):.10f}", " 0.99**1000 =", f"{float(F(99,100)**1000):.10f}")
print("ln 0.99 =", math.log(0.99), " 100 ln =", 100*math.log(0.99), " exp =", math.exp(100*math.log(0.99)))
print("(1/2)^9 =", F(1,2)**9, float(F(1,2)**9), " (1/2)^10 =", F(1,2)**10, float(F(1,2)**10))
print("2^50 =", 2**50, " 1/2^50 =", F(1, 2**50))

print("== L06 Empirical 2: 1/4 - 12/49")
print("gap =", F(1,4) - F(12,49), float(F(1,4)-F(12,49)))
print("grid sevenths max:", max((F(k,7)*(1-F(k,7)), F(k,7)) for k in range(8)))
print("grid tenths max:", max((F(k,10)*(1-F(k,10)), F(k,10)) for k in range(11)))
print("C(10,2) =", math.comb(10,2))

print("== L07 Part A recomputation")
beta = math.sin(1.0)
x = 0.0
for _ in range(2000):
    x = math.cos(x)
xbar = x
print("beta =", beta, " xbar =", xbar, " cos(xbar)-xbar =", math.cos(xbar)-xbar)
d01 = 1.0
x = 0.0
rows = []
for n in range(31):
    err = abs(x - xbar)
    bound = beta**n * d01 / (1 - beta)
    rows.append((n, x, err, bound))
    x = math.cos(x)
for n, xn, err, bound in rows:
    if n in (0,1,2,5,10,20,30):
        print(f"n={n:2d} x_n={xn:.6f} err={err:.6e} bound={bound:.6e} ok={err<=bound+1e-12}")
print("bound/err at n=5:", rows[5][3]/rows[5][2], " sin1^5/(1-sin1) =", beta**5/(1-beta))
print("all n 0..30 err<=bound:", all(err <= bound + 1e-12 for _, _, err, bound in rows))
print("M2 bound n=13,14 (x/3+2 from 0):", 3/3**13, 3/3**14)
print("R2 threshold: ln(1/(eps(1-beta)))/ln(1/beta) =", math.log(1/(1e-6*(1-beta)))/math.log(1/beta))
for n in (90, 91):
    print("n", n, "beta^n/(1-beta) =", beta**n/(1-beta), " <= 1e-6:", beta**n/(1-beta) <= 1e-6)
print("R1 check: bound(beta,n)=beta^n for x0=1:", all(abs(b**n*(1-b)/(1-b) - b**n) < 1e-15 for b in [0.3,0.5,0.9] for n in range(20)))
print("E1 ratio 2.661258/0.05439523 =", 2.661258/0.05439523)
print("L07 E3 quotient (cos 0.995 - cos 1)/0.005 =", (math.cos(0.995)-math.cos(1.0))/0.005)
print("sin1 - that =", beta - (math.cos(0.995)-math.cos(1.0))/0.005)
print("sin1 =", beta, " sin1 digits:", f"{beta:.10f}")
print("E2 f'(5)=", 5/math.sqrt(26), " f'(50)=", 50/math.sqrt(2501))
print("cos(1)=", math.cos(1.0), " cos(0.5)=", math.cos(0.5))
print("cos(0)-cos(1) =", 1-math.cos(1.0))
print("Ex2.3 bound: (1/3)^n*2/(2/3) == 3*3^-n for n in 0..20:", all(abs((1/3)**n*2/(2/3) - 3*3**-n) < 1e-12 for n in range(21)))

print("== L07 Part B grid sampled max (k/200 grid of 201 points)")
GRID = 200
xs = [i/GRID for i in range(GRID+1)]
best = 0.0; arg=None
for i,x in enumerate(xs):
    for y in xs[i+1:]:
        q = abs(math.cos(x)-math.cos(y))/(y-x)
        if q > best: best, arg = q, (x,y)
print("max quotient =", best, "at", arg)

print("== L07 Part C recomputation")
def f(x): return math.sqrt(x*x+1.0)
for half in (5.0, 50.0):
    xs = [-half + 2.0*half*i/GRID for i in range(GRID+1)]
    best = 0.0; arg=None
    for i,x in enumerate(xs):
        for y in xs[i+1:]:
            q = abs(f(x)-f(y))/(y-x)
            if q > best: best, arg = q, (x,y)
    gap = min(f(x)-x for x in xs)
    print(f"window {half}: max quotient {best:.6f} at {arg}, min f(x)-x {gap:.6f}")

print("== L07 Lab Part B: is the lab's grid sample for sin1 bound ok; 1-h quotient check")
for h in (0.1, 0.01, 0.001):
    print("h", h, (math.cos(1-h)-math.cos(1))/h)

print("== L07 canon item 2 check: |phi x - phi y|/|x-y| near y=1e6, x=y+1")
phi = lambda t: math.sqrt(t*t+1)
for y in (10.0, 1e3, 1e6):
    x = y+1
    print(y, abs(phi(x)-phi(y))/abs(x-y))
