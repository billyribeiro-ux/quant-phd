import math, random
ALPHA=0.3; H=40; SEED=2026
rng=random.Random(SEED)
a=[1.0]; k=[100.0]; l=[50.0]
for _ in range(H):
    a.append(a[-1]*math.exp(rng.uniform(0.005,0.02)))
    k.append(k[-1]*math.exp(rng.uniform(0.02,0.05)))
    l.append(l[-1]*math.exp(rng.uniform(0.0,0.015)))
y=[ai*ki**ALPHA*li**(1-ALPHA) for ai,ki,li in zip(a,k,l)]
def lg(x): return [math.log(x[t])-math.log(x[t-1]) for t in range(1,len(x))]
dk=lg(k); dy=lg(y); dl=lg(l); da=lg(a)
mk=sum(dk)/len(dk); my=sum(dy)/len(dy); ml=sum(dl)/len(dl)
print('mean_dlnK', repr(mk))
print('alpha*mean_dlnK', 0.3*mk, 'round6', round(0.3*mk,6))
print('0.4*mean_dlnK', 0.4*mk, 'round6', round(0.4*mk,6))
print('0.4*0.035557', 0.4*0.035557, '0.4*0.0355562', 0.4*0.0355562)
print('mean_dlnK round6', round(mk,6))
print('printed 0.010667/0.3', 0.010667/0.3)
print('0.4*0.0355562 round6', round(0.4*0.0355562,6))
