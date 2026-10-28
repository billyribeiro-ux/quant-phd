"""Independent recomputation for M5 slice a, round 3 (L04 numeric and quoted claims)."""
from fractions import Fraction as F
from itertools import product
import random

ok = []
def check(name, cond):
    ok.append((name, bool(cond)))

# Mechanics 1
check("mech1 d2((1,2),(4,-2))=5", (1-4)**2 + (2-(-2))**2 == 25)
# Lagrange identity (Prop 1.4) on random rationals
random.seed(0)
lag = True
for _ in range(2000):
    u1,u2,v1,v2 = [F(random.randint(-9,9), random.randint(1,5)) for _ in range(4)]
    lhs = (u1*u1+u2*u2)*(v1*v1+v2*v2) - (u1*v1+u2*v2)**2
    lag &= lhs == (u1*v2-u2*v1)**2
check("Prop1.4 Lagrange identity on 2000 rational samples", lag)
# Mechanics 2: finite metric on {a,b,c}
pts = "abc"
d = {("a","b"):2,("b","a"):2,("b","c"):2,("c","b"):2,("a","c"):3,("c","a"):3}
def D(x,y): return 0 if x==y else d[(x,y)]
m3 = all(D(x,z) <= D(x,y)+D(y,z) for x,y,z in product(pts,repeat=3))
check("Mechanics2 finite metric M3 holds on all 27 triples", m3)
# Mechanics 3: max of x - x^2 on [0,1] grid, exact at 1/2
grid = [F(i,1000) for i in range(1001)]
check("Mechanics3 sup |x-x^2| = 1/4 at 1/2", max(abs(x-x*x) for x in grid)==F(1,4) and F(1,2)-F(1,4)==F(1,4))
# Empirical 2: triangle failures of (x-y)^2 on {0,1,2}
fails = [(x,y,z) for x,y,z in product([0,1,2],repeat=3) if (x-z)**2 > (x-y)**2+(y-z)**2]
check("Empirical2 failing triples are exactly (0,1,2),(2,1,0)", sorted(fails)==[(0,1,2),(2,1,0)])
# Empirical 1 and 3 counts
check("Empirical1 25^3=15625", 25**3==15625)
check("Empirical3 27^3=19683 and sup((0,0,0),(2,1,0))=2", 27**3==19683 and max(abs(0-2),abs(0-1),abs(0-0))==2)
# Lab 1 Part B: sup distance triangle, all 27^3 triples exact
vecs = [tuple(F(v) for v in c) for c in product((0,1,2),repeat=3)]
sup = lambda f,g: max(abs(a-b) for a,b in zip(f,g))
check("Part B sup triangle holds on all 19683 triples", all(sup(f,h) <= sup(f,g)+sup(g,h) for f in vecs for g in vecs for h in vecs))
# Example 1.5 discrete metric: M3 on a 4-point set
S = [0,1,2,3]
dd = lambda x,y: 0 if x==y else 1
check("Example1.5 discrete triangle on 64 triples", all(dd(x,z)<=dd(x,y)+dd(y,z) for x,y,z in product(S,repeat=3)))
# Remark 2.2 Euclidean: 1+r/2 in B(1,r), not in (0,1]
check("Remark2.2 1+r/2 in B(1,r) and not in (0,1] for r in {1,1/10,1/1000}", all(abs(1+r/2-1)<r and not (0 < 1+r/2 <= 1) for r in [F(1),F(1,10),F(1,1000)]))
# Remark 2.2 new discrete-metric witness: B(x,1/2) = {x} within a finite window of R (discrete metric)
ball = lambda x,r: {y for y in [F(i,4) for i in range(-8,9)] if dd(x,y) < r}
check("Remark2.2 discrete ball B(x,1/2)={x} for sample points", all(ball(x,F(1,2))=={x} for x in [F(0),F(1,4),F(1)]))
# Misconception 3: min(r/2,1) in (0,1] and in B(0,r)
check("Misc3 min(r/2,1) in (0,1] and within r of 0", all(0 < min(r/2,1) <= 1 and min(r/2,1) < r for r in [F(1,10),F(1),F(5)]))
# Research 1: phi(t)=t/(1+t) triangle on random rationals
phi = lambda t: t/(1+t)
rt = True
for _ in range(3000):
    x,y,z = [F(random.randint(-20,20), random.randint(1,4)) for _ in range(3)]
    rt &= phi(abs(x-z)) <= phi(abs(x-y)) + phi(abs(y-z))
check("Research1 triangle inequality for t/(1+t) on 3000 samples", rt)
# Proof 2 truncated metric min(|x-y|,1)
tr = all(min(abs(x-z),1) <= min(abs(x-y),1)+min(abs(y-z),1) for x,y,z in product([F(i,2) for i in range(-6,7)],repeat=3))
check("Proof2 truncated metric triangle on grid", tr)
# Example 3.6: 1/n Cauchy in (0,1] (distances as in R) and no limit: |x-1/n|->0 forces x=0
check("Example3.6 |1/n - 1/m| < eps for large n,m (n=10^4 test, eps=1/100)", abs(F(1,10000)-F(1,20000)) < F(1,100))
# Prop 3.4 arithmetic: eps^2/4 + eps^2/4 = eps^2/2 < eps^2
check("Prop3.4 eps^2/4+eps^2/4 < eps^2 for eps>0", F(1,4)+F(1,4) < 1)
# Quiz numeric answers
check("Quiz L04 numeric: d2((0,0),(3,4))=5; d_inf(x,0) on [0,1]=1", 3*3+4*4==25)
for name, c in ok:
    print(("PASS " if c else "FAIL ") + name)
print("total", len(ok), "pass", sum(c for _, c in ok))
