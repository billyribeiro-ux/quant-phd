from fractions import Fraction as F
from itertools import product
Q=[[F(4),F(1),F(0)],[F(1),F(3),F(1)],[F(0),F(1),F(2)]]
c=[F(-1),F(0),F(2)]
A=[[F(1),F(1),F(1)],[F(0),F(1),F(-1)]]
b=[F(1),F(0)]
n=3;m=2
K=[Q[i]+[A[k][i] for k in range(m)] for i in range(n)]+[A[k]+[F(0)]*m for k in range(m)]
rhs=[-x for x in c]+b
def solve(M,r):
    N=len(r); M=[row[:]+[r[i]] for i,row in enumerate(M)]
    for col in range(N):
        p=next(i for i in range(col,N) if M[i][col]!=0)
        M[col],M[p]=M[p],M[col]
        for i in range(N):
            if i!=col and M[i][col]!=0:
                f=M[i][col]/M[col][col]; M[i]=[a-f*bb for a,bb in zip(M[i],M[col])]
    return [M[i][N]/M[i][i] for i in range(N)]
sol=solve(K,rhs)
x=sol[:3]; lam=sol[3:]
print("x",x,"lam",lam)
# determinant
def det(M):
    M=[r[:] for r in M]; N=len(M); d=F(1)
    for col in range(N):
        p=next((i for i in range(col,N) if M[i][col]!=0),None)
        if p is None: return F(0)
        if p!=col: M[col],M[p]=M[p],M[col]; d=-d
        d*=M[col][col]
        for i in range(col+1,N):
            f=M[i][col]/M[col][col]; M[i]=[a-f*bb for a,bb in zip(M[i],M[col])]
    return d
print("det K",det(K))
Qx=[sum(Q[i][j]*x[j] for j in range(n)) for i in range(n)]
print("stationarity", [Qx[i]+c[i]+sum(A[k][i]*lam[k] for k in range(m)) for i in range(n)])
print("constraint", [sum(A[k][i]*x[i] for i in range(n))-b[k] for k in range(m)])
obj=F(1,2)*sum(x[i]*Qx[i] for i in range(n))+sum(c[i]*x[i] for i in range(n))
print("objective",obj,float(obj))
print("x'Qx",sum(x[i]*Qx[i] for i in range(n)))
v=[F(-2),F(1),F(1)]
print("Av",[sum(A[k][i]*v[i] for i in range(n)) for k in range(m)])
Qv=[sum(Q[i][j]*v[j] for j in range(n)) for i in range(n)]
print("v'Qv",sum(v[i]*Qv[i] for i in range(n)), "Qv",Qv)
# null-line check
x0=x
ok=True
for k in range(-8,9):
    t=F(k,4)
    xt=[x0[i]+t*v[i] for i in range(n)]
    ft=F(1,2)*sum(xt[i]*sum(Q[i][j]*xt[j] for j in range(n)) for i in range(n))+sum(c[i]*xt[i] for i in range(n))
    f0=F(1,2)*sum(x0[i]*Qx[i] for i in range(n))+sum(c[i]*x0[i] for i in range(n))
    ok &= (ft-f0==F(1,2)*t*t*sum(v[i]*Qv[i] for i in range(n)))
print("null line identity all 17 t:",ok)
# Part B
QB=[[F(2),F(1)],[F(1),F(2)]]; cB=[F(-3),F(1)]
def fB(x): 
    return F(1,2)*sum(x[i]*QB[i][j]*x[j] for i in range(2) for j in range(2))+sum(cB[i]*x[i] for i in range(2))
cands=[]
for S in [(),(0,),(1,),(0,1)]:
    free=[i for i in range(2) if i not in S]
    xs=[F(0),F(0)]
    if free:
        # solve Q_FF x_F = -c_F
        Mx=[[QB[i][j] for j in free] for i in free]
        rr=[-cB[i] for i in free]
        sv=solve(Mx,rr) if len(free)==1 else solve(Mx,rr)
        for idx,i in enumerate(free): xs[i]=sv[idx]
    Qxs=[sum(QB[i][j]*xs[j] for j in range(2)) for i in range(2)]
    mu=[Qxs[i]+cB[i] for i in range(2)]
    primal=all(v>=0 for v in xs)
    dual=all(mu[i]>=0 for i in S)
    print("S",S,"x",xs,"mu",mu,"primal",primal,"dual",dual)
    if primal and dual: cands.append((xs,fB(xs)))
print("passing",len(cands),cands)
xh=cands[0][0]; vh=cands[0][1]
grid=[F(k,16) for k in range(33)]
below=sum(1 for a in grid for bb in grid if fB([a,bb])<vh)
least=min(fB([a,bb]) for a in grid for bb in grid)
print("grid pts",len(grid)**2,"below",below,"min equals cand",least==vh)
print("obj of E1 check", float(F(551,722)))
print("kkt Q pos leading minors", F(4), F(4*3-1), det(Q))
