import math, random
BETA=0.9; ALPHA=0.3; GRID=[0.45+0.25*j for j in range(10)]; TOL=1e-10
print("grid last repr", repr(GRID[-1]), "grid", [round(g,4) for g in GRID])
def bellman(values):
    out=[]
    for k in GRID:
        r=k**ALPHA
        out.append(max(math.sqrt(r-kp)+BETA*values[j] for j,kp in enumerate(GRID) if kp<=r))
    return out
def sd(a,b): return max(abs(x-y) for x,y in zip(a,b))
gap=min(abs(kp-k**ALPHA) for k in GRID for kp in GRID)
print("gap %.12f"%gap)
values=[0.0]*10; sweeps=0; cert=math.inf; change=math.inf
while cert>TOL:
    new=bellman(values); change=sd(new,values); cert=BETA/(1-BETA)*change; values=new; sweeps+=1
print("sweeps",sweeps,"last change %.12e cert %.12e"%(change,cert))
U=math.sqrt(max(GRID)**ALPHA); n=0
while BETA**n*U/(1-BETA)>TOL: n+=1
print("apriori",n, "U", U)
res=sd(bellman(values),values)
print("residual %.12e  bound (1+b)cert %.12e  ok %s"%(res,(1+BETA)*cert,res<=(1+BETA)*cert))
rng=random.Random(7); worst=0.0
for _ in range(200):
    v=[rng.uniform(0.0,4.0) for _ in GRID]; w=[rng.uniform(0.0,4.0) for _ in GRID]
    worst=max(worst, sd(bellman(v),bellman(w))/sd(v,w))
print("worst %.15f  worst-beta %.3e  <= beta+1e-12: %s  <= beta exactly: %s"%(worst,worst-BETA,worst<=BETA+1e-12,worst<=BETA))
print("V", ["%.6f"%x for x in values])
print("last change*9/(...)", "%.6f"%(change*BETA/(1-BETA)))
# last change from certified: certified is 9*change ; relation
print("cert/change", cert/change)
