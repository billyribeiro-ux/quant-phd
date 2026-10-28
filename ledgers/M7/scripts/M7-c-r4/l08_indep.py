from fractions import Fraction as F
from itertools import product
H=6; b=F(9,10)
prof={0:6,1:4,2:1}
def step(s,a):
    if a=='run': return F(prof[s]), min(s+1,2)
    return F(-4), 0
V={H:{s:F(0) for s in (0,1,2)}}
for t in range(H-1,-1,-1):
    V[t]={}
    for s in (0,1,2):
        cands=[]
        for a in ('run','repair'):
            r,ns=step(s,a); cands.append(r+b*V[t+1][ns])
        V[t][s]=max(cands)
        if cands[0]==cands[1]: print("TIE",t,s)
for t in range(H+1):
    print(t, [f"{float(V[t][s]):.6f}" for s in (0,1,2)], [str(V[t][s]) for s in (0,1,2)][:1])
# brute force
cnt=0; ok=True
for t in range(H):
    for s in (0,1,2):
        best=None
        for plan in product(('run','repair'),repeat=H-t):
            cnt+=1; st=s; tot=F(0); w=F(1)
            for a in plan:
                r,ns=step(st,a); tot+=w*r; w*=b; st=ns
            best=tot if best is None or tot>best else best
        ok = ok and best==V[t][s]
print("plans",cnt,"match",ok)
# value iteration
U={0:F(0),1:F(0),2:F(0)}; its=[U]
for n in range(6):
    new={}
    for s in (0,1,2):
        new[s]=max(step(s,a)[0]+b*U[step(s,a)[1]] for a in ('run','repair'))
    its.append(new); U=new
for n in range(6):
    print("n",n,"change",float(max(abs(its[n+1][s]-its[n][s]) for s in (0,1,2))))
print("iter==recursion", all(its[n][s]==V[H-n][s] for n in range(7) for s in (0,1,2)))
