import math, random
B=0.9; A=0.5; G=[0.5,0.9,1.4]
def res(k): return k**A
def bell(v):
    out=[]
    for k in G:
        out.append(max(math.sqrt(res(k)-G[j])+B*v[j] for j in range(3) if G[j]<=res(k)))
    return out
def sd(a,b): return max(abs(x-y) for x,y in zip(a,b))
v0=[0.0]*3; v1=bell(v0)
print("V1 unrounded", v1)
print("change sweep1 unrounded", sd(v1,v0), "cert", 9*sd(v1,v0))
print("ratio lab1 lhs/rhs", sd(bell(v0),bell(v1)), B*sd(v0,v1))
# rung2 completion ratio
w=[0.1,0.2,0.3]
print("rung2 ratio", sd(bell(v0),bell(w))/sd(v0,w))
vals=[0.0]*3; n=0; cert=math.inf
while cert>1e-6 and n<300:
    n+=1; new=bell(vals); ch=sd(new,vals); cert=9*ch; vals=new
print("rung2 n",n,"cert",cert,"change",ch)
# lab1 stop
vals=[0.0]*3; n=0; cert=math.inf
while cert>1e-6:
    n+=1; new=bell(vals); ch=sd(new,vals); cert=9*ch; vals=new
print("lab1 n",n,"change",ch,"cert",cert)
# lab 3
G3=[0.45+0.25*j for j in range(10)]
A3=0.3
def bell3(v):
    out=[]
    for k in G3:
        r=k**A3
        out.append(max(math.sqrt(r-kp)+0.9*v[j] for j,kp in enumerate(G3) if kp<=r))
    return out
vals=[0.0]*10; s=0; cert=math.inf; ch=math.inf
while cert>1e-10:
    new=bell3(vals); ch=sd(new,vals); cert=9*ch; vals=new; s+=1
print("lab3 sweeps",s,"change",ch,"cert",cert, "cert/ch", cert/ch)
print("rounded change 1.025e-11 *9 =", 9*1.025e-11, " unrounded*9 =", cert)
ref=vals
res_=sd(bell3(vals),vals); print("residual", res_, "1.9*cert", 1.9*cert)
gap=min(abs(kp-k**A3) for k in G3 for kp in G3); print("gap",gap)
U=math.sqrt(max(G3)**A3); na=0
while 0.9**na*U/0.1>1e-10: na+=1
print("apriori",na, "U",U)
rng=random.Random(7); worst=0.0
for _ in range(200):
    v=[rng.uniform(0.0,4.0) for _ in G3]; w=[rng.uniform(0.0,4.0) for _ in G3]
    worst=max(worst, sd(bell3(v),bell3(w))/sd(v,w))
print("worst ratio", repr(worst), worst<=0.9+1e-12)
