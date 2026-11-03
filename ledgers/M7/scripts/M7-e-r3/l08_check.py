from fractions import Fraction as F
PROFIT={0:F(6),1:F(4),2:F(1)}; REPAIR=F(-4); beta=F(9,10); H=6
def acts(s): return {'run':(PROFIT[s], min(s+1,2)), 'repair':(REPAIR,0)}
V={H:{s:F(0) for s in range(3)}}
pol={}
ties=0
for t in range(H-1,-1,-1):
    V[t]={}
    for s in range(3):
        vals={a:r+beta*V[t+1][n] for a,(r,n) in acts(s).items()}
        m=max(vals.values()); V[t][s]=m
        best=[a for a in vals if vals[a]==m]
        pol[(t,s)]=best
        if t<=5 and len(best)>1: ties+=1
for t in range(H+1):
    print("t",t,[ "%.6f"%float(V[t][s]) for s in range(3)], "exact", [str(V[t][s]) for s in range(3)])
for t in range(H):
    print("policy t",t,{s:pol[(t,s)] for s in range(3)})
print("ties",ties)
# value iteration from U0=0, sup-norm change
U=[F(0)]*3; prev=None
for n in range(6):
    Un=[max(r+beta*U[nx] for (r,nx) in acts(s).values()) for s in range(3)]
    ch=max(abs(Un[s]-U[s]) for s in range(3))
    print("n",n,"change",float(ch))
    U=Un
    # iterate equals n+1 period recursion check
# brute force: count sequences
cnt=0
for t in range(H):
    cnt+=3*2**(H-t)
print("plans enumerated",cnt)
# check negative-discount example
import itertools
print("ratios", float(F(274,100)/F(36,10)), float(F(2466,1000)/F(274,100)), float(F(22194,10000)/F(2466,1000)), float(F(199746,100000)/F(22194,10000)))
