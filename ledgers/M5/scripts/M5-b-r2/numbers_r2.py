import math
from fractions import Fraction as F
print("== L05 ==")
print("0.99^10", 0.99**10, "0.99^100", 0.99**100, "0.99^1000", 0.99**1000)
print("ln0.99*100", 100*math.log(0.99), "exp", math.exp(100*math.log(0.99)))
print("(1/2)^9", F(1,2)**9, float(F(1,2)**9), "(1/2)^10", float(F(1,2)**10), "1/2^50", F(1,2**50))
print("1/2^50 as float", 1/2**50)
# sup of x^n on grid k/200 up to 1/2
print("sup x^3 on [0,1/2]", max((F(k,200)**3) for k in range(101)))
# least n with (1/2)^n < 1/1000
n=1
while F(1,2)**n >= F(1,1000): n+=1
print("least n", n)
print("== L06 ==")
print("12/49 vs 1/4 gap", F(1,4)-F(12,49), float(F(1,4)-F(12,49)))
print("max of x(1-x) on k/7", max((F(k,7)*(1-F(k,7)), F(k,7)) for k in range(8)))
print("pairs", 10*9//2)
print("== L07 ==")
beta = math.sin(1.0)
print("sin1", beta, "1-sin1", 1-beta)
xs=0.0
x=0.0
fp=0.0
for _ in range(300): fp=math.cos(fp)
print("xbar", fp)
x=0.0
d01=abs(0.0-math.cos(0.0))
for n in range(31):
    err=abs(x-fp); bound=beta**n*d01/(1-beta)
    if n in (0,1,2,5,10,20,30):
        print(f"n={n} x_n={x:.6f} err={err:.6e} bound={bound:.6e}")
    assert err <= bound+1e-12
    x=math.cos(x)
print("x2=cos1", math.cos(1.0))
print("E1 ratio 2.661258/0.05439523 =", 2.661258/0.05439523, "bound formula sin1^5/(1-sin1)=", beta**5/(1-beta))
print("mis3 ratio 2.661258/0.05439523", 2.661258/0.05439523)
# Part B
GRID=200
g=[i/GRID for i in range(GRID+1)]
best=0.0; arg=None
for i,x in enumerate(g):
    for y in g[i+1:]:
        q=abs(math.cos(x)-math.cos(y))/(y-x)
        if q>best: best=q; arg=(x,y)
print("partB best", best, arg, "sin1 - best", beta-best)
q=(math.cos(0.995)-math.cos(1.0))/(1-0.995)
print("E3 quotient (0.995,1)", q, "sin1-q", beta-q)
# Part C
def f(x): return math.sqrt(x*x+1)
for half in (5.0,50.0):
    xs=[-half+2*half*i/GRID for i in range(GRID+1)]
    best=0.0
    for i,x in enumerate(xs):
        for y in xs[i+1:]:
            best=max(best, abs(f(x)-f(y))/(y-x))
    gap=min(f(x)-x for x in xs)
    print("partC", half, best, gap)
print("f'(5)", 5/math.sqrt(26), "f'(50)", 50/math.sqrt(2501))
# R2
eps=1e-6
print("R2 n bound", math.log(1/(eps*(1-beta)))/math.log(1/beta))
print("R2 n=30 bound", beta**30/(1-beta), "err", abs(0.0)+0)
# M2 / Example 2.3
print("M2 n13", 3/3**13, "n14", 3/3**14)
print("Ex2.3 x_n check", [ (3-3*3**-n) for n in range(4)])
print("E2 ratio 0.980390 vs f'(5)", 0.980390 < 5/math.sqrt(26), 0.999798 < 50/math.sqrt(2501))
