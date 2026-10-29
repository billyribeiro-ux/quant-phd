from fractions import Fraction as F
from itertools import product
import math
# L07 independent recomputation
P=[F(n,16) for n in (1,2,1,3,2,3,2,2)]; X=[2,-1,4,0,3,-2,1,5]
C=[(0,1,2),(3,4),(5,6,7)]
avg=[None]*8
for c in C:
    pc=sum(P[w] for w in c); ec=sum(P[w]*X[w] for w in c)
    for w in c: avg[w]=ec/pc
print('avg', [str(a) for a in avg])
mse=lambda y: sum(P[w]*(X[w]-y[w])**2 for w in range(8))
m0=mse(avg); print('mse', m0, float(m0))
best=None; ties=0; cnt=0; below=0
for t in product(range(-2,3),repeat=3):
    y=[0]*8
    for c,v in zip(C,t):
        for w in c: y[w]=v
    e=mse(y); cnt+=1
    if e<m0: below+=1
    if e==m0: ties+=1
print('cands',cnt,'below',below,'ties',ties)
# tower
H=[(0,1,2,3,4),(5,6,7)]
for c in H:
    pc=sum(P[w] for w in c); print('H',c, sum(P[w]*avg[w] for w in c)/pc, sum(P[w]*X[w] for w in c)/pc)
print('total', sum(P[w]*avg[w] for w in range(8)), sum(P[w]*X[w] for w in range(8)))
# L05 numbers
print('block arctan2-pi/4', math.atan(2)-math.pi/4, 'nine', 9*(math.atan(2)-math.pi/4), 'ten', 10*(math.atan(2)-math.pi/4))
print('pi/4', math.pi/4, 'quad err', 0.7853982936-math.pi/4)
# L06 candidate misses
mu=[F(1,4)]*4+[F(0)]; nu=[F(1,4),F(1,4),F(1,4),F(1,8),F(1,8)]
def meas(w,a): return sum((w[i] for i in range(5) if a>>i&1),F(0))
cand=[nu[i]/mu[i] if mu[i]>0 else F(0) for i in range(5)]
miss=[a for a in range(32) if sum((cand[i]*mu[i] for i in range(5) if a>>i&1),F(0))!=meas(nu,a)]
print('L06 misses',len(miss), 'contain pt5', sum(1 for a in range(32) if a>>4&1), 'equal', sorted(miss)==[a for a in range(32) if a>>4&1])
# L08
N=10
def level(p,k):
    import itertools
    paths=list(itertools.product((1,-1),repeat=N))
    cells={}
    for q in paths: cells.setdefault(q[:k],[]).append(q)
    ok=0
    for pre,mem in cells.items():
        pr=lambda q: __import__('functools').reduce(lambda a,s: a*(p if s==1 else 1-p),q,F(1))
        m=sum(pr(q) for q in mem)
        av=sum(pr(q)*sum(q[:k+1]) for q in mem)/m
        if all(av==sum(pre) for _ in [0]): ok+=1
    return ok, len(cells)
for p in (F(1,2),F(1,3)):
    print('p',p,[level(p,k) for k in (0,1,2)])
