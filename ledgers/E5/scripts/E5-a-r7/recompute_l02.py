import math, random
from fractions import Fraction
ALPHA=0.3; H=40; SEED=2026
rng=random.Random(SEED)
A,K,L=[1.0],[100.0],[50.0]
for _ in range(H):
    A.append(A[-1]*math.exp(rng.uniform(0.005,0.02)))
    K.append(K[-1]*math.exp(rng.uniform(0.02,0.05)))
    L.append(L[-1]*math.exp(rng.uniform(0.0,0.015)))
Y=[a*k**ALPHA*l**(1-ALPHA) for a,k,l in zip(A,K,L)]
dk=[math.log(K[t])-math.log(K[t-1]) for t in range(1,len(K))]
mk=sum(dk)/len(dk)
print("mean dlnK", repr(mk))
print("alpha0.3 capital term", ALPHA*mk, "round6", round(ALPHA*mk,6))
print("alpha0.4 capital term", 0.4*mk, round(0.4*mk,6))
print("rounded-intermediate route", round(0.4*0.035557,6), round(0.010667/0.3,6), 0.4*round(0.010667/0.3,6))
