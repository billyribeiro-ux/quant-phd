import random, math
def simple(f):
    tot=float(f[0]); 
    if tot>=0: return None
    for t in range(1,len(f)):
        prev=tot; tot+=f[t]
        if tot>=0: return t, (t-1)+(-prev)/f[t]
    return None
def disc(f,r): return [x/(1+r)**t for t,x in enumerate(f)]
rng=random.Random(1); bad=0; n=0; both=0
for _ in range(200000):
    N=rng.randint(1,8); f=[-rng.randint(1,1000)]+[rng.randint(0,800) if rng.random()<0.8 else 0 for _ in range(N)]
    r=rng.choice([0,0.01,0.05,0.1,0.3,1.5])
    s=simple(f); d=simple(disc(f,r))
    if s and d:
        both+=1
        if d[0] < s[0]: bad+=1
print("Prop2.2 counterexamples", bad, "of cases with both paybacks", both)
# Prop 3.1 PV of years 4-6 for A vs B
A=[-1e6,3e5,4e5,4e5,3e5,2e5,1e5]; B=[-1e6,3e5,4e5,4e5,0,0,0]
gap=sum((a-b)/1.1**t for t,(a,b) in enumerate(zip(A,B)))
print("gap cents", round(gap,2), "ratio to A NPV", round(gap/289367.40*100,2))
print("gap pv 4-6 direct", round(sum(x/1.1**t for t,x in [(4,3e5),(5,2e5),(6,1e5)]),2))
print("B npv", round(sum(x/1.1**t for t,x in enumerate(B)),2))
print("E1 range", 693692.91-121251.71)
print("M2 check", 400/1.1+400/1.21+400/1.331, 400/1.4641, -1000+400/1.1+400/1.21+400/1.331, 3+5.26/273.21)
print("witness1", -1000+1/1.1**4+1/1.1**5, "witness2", -1000+1000/1.1**4, 1000/1.1**4)
print("PB witness2", simple([-1000,0,0,0,1000,0]))
print("D2.2 example: A-B ratio", 385535.69/289367.40, 385535.69/96168.29)
print("E2 A-B", 289367.40+96168.29)
