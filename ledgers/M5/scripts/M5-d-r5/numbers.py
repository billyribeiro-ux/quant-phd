import math, random
BETA=0.9; ALPHA=0.5; GRID=[0.5,0.9,1.4]
def res(k): return float(k**ALPHA)
def bellman(values, beta=BETA, alpha=ALPHA, grid=GRID):
    out=[]
    for k in grid:
        r=k**alpha
        out.append(max(math.sqrt(r-kp)+beta*values[j] for j,kp in enumerate(grid) if kp<=r))
    return out
def sd(a,b): return max(abs(x-y) for x,y in zip(a,b))
# Lab 1 iteration
v=[0.0]*3; n=0; cert=math.inf; change=math.inf; first=[]
while cert>1e-6:
    n+=1; new=bellman(v); change=sd(new,v); cert=BETA/(1-BETA)*change; v=new
    if n<=3: first.append((change,cert))
print("lab1 stop sweep",n,"change %.12e cert %.12e"%(change,cert))
print("first sweeps", ["%.10f/%.10f"%x for x in first])
print("first sweep change*9", "%.10f"%(9*first[0][0]))
# Lab 2 values
w=[0.1,0.2,0.3]; zero=[0.0]*3
ratio=sd(bellman(zero),bellman(w))/sd(zero,w)
print("lab2 ratio %.12f"%ratio)
v=[0.0]*3; n=0; cert=math.inf
while cert>1e-6 and n<300:
    n+=1; new=bellman(v); change=sd(new,v); cert=BETA/(1-BETA)*change; v=new
print("lab2 sweeps",n,"cert %.10e change %.10e"%(cert,change))
# Lab 1 reference error
ref=[0.0]*3
for _ in range(100000):
    nxt=bellman(ref); small=BETA/(1-BETA)*sd(nxt,ref)<=1e-12; ref=nxt
    if small: break
# actual err
print("lab1 actual err %.12e"%sd(v,ref))
