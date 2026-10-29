import math, random
B=0.9
def run(alpha, grid, tol, bellman_fn=None):
    pass
def make(alpha, grid, beta=0.9):
    def res(k): return k**alpha
    def bell(vals):
        out=[]
        for k in grid:
            r=res(k)
            out.append(max(math.sqrt(r-kp)+beta*vals[j] for j,kp in enumerate(grid) if kp<=r))
        return out
    return bell
def sd(a,b): return max(abs(x-y) for x,y in zip(a,b))
# Lab 1 unrounded
G1=[0.5,0.9,1.4]; bell1=make(0.5,G1)
v0=[0.0]*3; v1=bell1(v0)
print("V1 unrounded", v1)
print("sweep1 cert unrounded", 9*sd(v1,v0))
vals=v0; n=0; cert=math.inf
while cert>1e-6:
    n+=1; new=bell1(vals); ch=sd(new,vals); cert=9*ch; vals=new
    if n==146: print("lab1 sweep146 change", ch, "cert", cert)
print("lab1 stop", n, ch, cert)
# Lab 2 ratio for V=0, W=(0.1,.2,.3), unrounded
w=[0.1,0.2,0.3]
print("lab2 ratio", sd(bell1(v0), bell1(w))/sd(v0,w))
# Lab 3
G3=[0.45+0.25*j for j in range(10)]; B3=0.9
bell3=make(0.3,G3,B3)
vals=[0.0]*10; s=0; cert=math.inf
while cert>1e-10:
    new=bell3(vals); ch=sd(new,vals); cert=9*ch; vals=new; s+=1
print("lab3 sweeps",s,"change",ch,"cert",cert)
print("exemplarB 9*change check: 9*ch=",9*ch)
res=sd(bell3(vals),vals); print("residual",res,"(1+b)*cert",1.9*cert, res<=1.9*cert)
um=math.sqrt(max(G3)**0.3); n=0
while 0.9**n*um/0.1>1e-10: n+=1
print("apriori",n, "sweeps<=n+1", s<=n+1)
rng=random.Random(7); worst=0.0
for _ in range(200):
    v=[rng.uniform(0,4) for _ in G3]; w_=[rng.uniform(0,4) for _ in G3]
    worst=max(worst, sd(bell3(v),bell3(w_))/sd(v,w_))
print("worst ratio unrounded", repr(worst))
gap=min(abs(kp-k**0.3) for k in G3 for kp in G3); print("gap", gap)
print("constant shift ratio", sd(bell3([0.0]*10), bell3([1.0]*10))/1.0)
for k,x in zip(G3,vals): print(k, repr(x))
