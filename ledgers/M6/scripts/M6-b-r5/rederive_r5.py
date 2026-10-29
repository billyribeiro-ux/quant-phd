from fractions import Fraction as F
import math, itertools
# L07 independent recomputation
p=[F(n,16) for n in (1,2,1,3,2,3,2,2)]; x=[F(v) for v in (2,-1,4,0,3,-2,1,5)]
cells=[(0,1,2),(3,4),(5,6,7)]
assert sum(p)==1
Y=[None]*8
for c in cells:
    pb=sum(p[w] for w in c); ex=sum(p[w]*x[w] for w in c)
    for w in c: Y[w]=ex/pb
print("L07 cell avgs", sorted({str(Y[c[0]]) for c in cells}))
mse=sum(p[w]*(x[w]-Y[w])**2 for w in range(8)); print("L07 mse", mse, float(mse))
# 125 candidates min check
best=min(sum(p[w]*(x[w]-(v[i])) ** 2 for w in range(8)) for v in [None] for i in [0]) if False else None
cnt=0; minok=True
for t in itertools.product((-2,-1,0,1,2),repeat=3):
    yy=[F(0)]*8
    for c,v in zip(cells,t):
        for w in c: yy[w]=F(v)
    e=sum(p[w]*(x[w]-yy[w])**2 for w in range(8))
    if e<=mse: minok=False
    if e==mse: cnt+=1
print("L07 candidates min ok", minok, "ties", cnt)
# L07 Part D
H=[(0,1,2,3,4),(5,6,7)]
for c in H:
    pb=sum(p[w] for w in c); print("H cell", c, sum(p[w]*Y[w] for w in c)/pb, sum(p[w]*x[w] for w in c)/pb)
# L08 counts
print("L08 cells levels0-9", sum(2**k for k in range(10)), "paths", 2**10, "level-total mismatches biased", 10*1024)
# L08 E[S_2] biased p=1/3 N=2 and N(2p-1) for N=10
q=lambda s,pp: pp if s==1 else 1-pp
pp=F(1,3); es=sum(q(a,pp)*q(b,pp)*(a+b) for a in (1,-1) for b in (1,-1)); print("E[S2] biased", es)
print("N=10 expected", 10*(2*pp-1))
# L05 numeric: block integral and quadrature error
f=lambda a,b:(a*a-b*b)/(a*a+b*b)**2
def simpson(g,a,b,n=2000):
    h=(b-a)/n; s=g(a)+g(b)
    for i in range(1,n): s+= (4 if i%2 else 2)*g(a+i*h)
    return s*h/3
print("arctan2-pi/4", math.atan(2)-math.pi/4)
c0=simpson(lambda x: simpson(lambda y: f(x,y),0.0,1.0,400),1.0,2.0,400)
print("block0 quadrature", c0, c0-(math.atan(2)-math.pi/4))
# L05 y-first over square: integral over x of (int over y) with x>0: 1/(1+x^2)
print("pi/4", math.pi/4, "int_0^1 1/(1+x^2)", math.atan(1))
