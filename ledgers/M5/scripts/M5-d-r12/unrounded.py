import math, random
BETA=0.9; ALPHA=0.5; GRID=[0.5,0.9,1.4]
def res(k): return k**ALPHA
def bell(vals):
    out=[]
    for k in GRID:
        out.append(max(math.sqrt(res(k)-GRID[j])+BETA*vals[j] for j in range(3) if GRID[j]<=res(k)))
    return out
def sd(a,b): return max(abs(x-y) for x,y in zip(a,b))
v0=[0.0]*3; v1=bell(v0)
print("sweep1 change", sd(v1,v0), "cert", BETA/(1-BETA)*sd(v1,v0))
vals=v0; n=0; cert=math.inf; ch=None
while cert>1e-6:
    n+=1; new=bell(vals); ch=sd(new,vals); cert=BETA/(1-BETA)*ch; vals=new
print("lab1 stop", n, "change", ch, "cert", cert)
ref=v0
for _ in range(100000):
    nxt=bell(ref); small = BETA/(1-BETA)*sd(nxt,ref)<=1e-12; ref=nxt
    if small: break
print("actual", sd(vals,ref))
# lab 2 values
v=[0.0]*3; w=[0.1,0.2,0.3]
print("lab2 ratio", sd(bell(v),bell(w))/sd(v,w))
vals=[0.0]*3; n=0; cert=math.inf
while cert>1e-6 and n<300:
    n+=1; new=bell(vals); ch=sd(new,vals); cert=BETA/(1-BETA)*ch; vals=new
print("lab2 sweeps", n, "cert", cert, "last change", ch)
# candidate ratio: check worst ratio of sup|BV-BW|/sup|V-W| for tie in lab 2 ratio
