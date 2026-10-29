import random, math
from fractions import Fraction
N=2000; SEED=90
def stream(o):
    rng=random.Random(SEED); return [o+rng.random() for _ in range(N)]
xs=stream(1e9)
vals=[Fraction(x) for x in xs]; n=len(vals)
mean=sum(vals,Fraction(0))/n
ex=sum(((x-mean)**2 for x in vals),Fraction(0))/(n-1)
print('exact unrounded', float(ex), float(ex)*1999)
tot=0.0; tsq=0.0
for x in xs:
    tot+=x; tsq+=x*x
print('naive total_sq', repr(tsq), 'exact sumsq', float(sum((v*v for v in vals),Fraction(0))))
print('ulp', math.ulp(2e21), math.ulp(tsq))
xs0=stream(0.0); v0=[Fraction(x) for x in xs0]; m0=sum(v0,Fraction(0))/n
e0=sum(((x-m0)**2 for x in v0),Fraction(0))/(n-1); print('exact0', float(e0))
