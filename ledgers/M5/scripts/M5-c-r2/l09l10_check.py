import math
from fractions import Fraction as Fr
b=0.9; d=math.sqrt(3)/2
for n in (146,147,150,151,152):
    print("apriori n",n, b**n/(1-b)*d)
print("apriori 10:", 0.9**10/0.1, "R3 0.9^n threshold", 1e-6*(1-b)/d)
print("9*step vs quotient", 0.0000085808/0.0000009534)
# L10 exact sums
def rs(n,tag):
    pts=[Fr(i,n) for i in range(n+1)]
    tags=pts[1:] if tag=='r' else pts[:-1]
    return sum(t*(pts[i+1]**2-pts[i]**2) for i,t in enumerate(tags))
for n in (4,10,100,1000):
    r=rs(n,'r'); l=rs(n,'l')
    print(n, float(r), float(l), r-Fr(2,3)==Fr(3*n-1,6*n*n), l-Fr(2,3)==-Fr(3*n+1,6*n*n), (n+1)*(4*n-1)==round(float(r)*6*n*n) or '')
print("E1 errors 29/600, -31/600:", Fr(29,600), Fr(-31,600), float(Fr(31,600)-Fr(29,600)))
print("1001*3999/6e6", 1001*3999/6e6)
# L10 Part B seeded
import random, itertools
rng=random.Random(20261028); worst=0.0; allw=True
for _ in range(200):
    m=rng.randint(1,30); interior=sorted(rng.random() for _ in range(m))
    bounds=[0.0,*interior,1.0]; tags=[lo+rng.random()*(hi-lo) for lo,hi in itertools.pairwise(bounds)]
    tot=sum(tg*(bounds[i]**2-bounds[i-1]**2) for i,tg in enumerate(tags,1))
    mesh=max(hi-lo for lo,hi in itertools.pairwise(bounds)); err=abs(tot-2/3)
    allw = allw and err<=2*mesh+1e-12; worst=max(worst,err/mesh)
print("B worst", worst, allw)
