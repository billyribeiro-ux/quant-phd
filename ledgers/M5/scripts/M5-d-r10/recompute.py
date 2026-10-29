import math
B=0.9; A=0.5; G=[0.5,0.9,1.4]
def res(k): return k**A
def sweep(V):
    out=[]
    for k in G:
        out.append(max(math.sqrt(res(k)-kp)+B*V[j] for j,kp in enumerate(G) if kp<=res(k)))
    return out
def sd(a,b): return max(abs(x-y) for x,y in zip(a,b))
v0=[0.0]*3; v1=sweep(v0)
print("V1 unrounded", v1)
print("change1", sd(v1,v0), "cert1", B/(1-B)*sd(v1,v0))
vals=v0; n=0; cert=math.inf
while cert>1e-6:
    n+=1; new=sweep(vals); ch=sd(new,vals); cert=B/(1-B)*ch; vals=new
print("stop", n, "change", ch, "cert", cert)
ref=v0
for _ in range(100000):
    nxt=sweep(ref); small=B/(1-B)*sd(nxt,ref)<=1e-12; ref=nxt
    if small: break
print("actual", sd(vals,ref))
# lab 2 ratio
w=[0.1,0.2,0.3]; print("ratio", sd(sweep([0.0]*3),sweep(w))/sd([0.0]*3,w))
# lab3 instance
B3=0.9; A3=0.3; G3=[round(0.45+0.25*i,10) for i in range(10)]
print("grid3", G3)
km=G3[-1]; tol=1e-10
n=0
while B3**n*math.sqrt(km**A3)/(1-B3)>tol: n+=1
print("a priori count", n)
