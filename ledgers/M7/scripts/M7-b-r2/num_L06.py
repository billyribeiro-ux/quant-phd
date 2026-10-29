# independent L06 recomputation with numpy float and Fraction-based solve
from fractions import Fraction as F
import numpy as np
# recreate inputs from the lab's stated recurrence (independent implementation)
state=2026
def draw(mod):
    global state
    state=(1103515245*state+12345)%2**31
    return state%mod
M=[[F(draw(7)-3) for _ in range(4)] for _ in range(4)]
mu=[F(draw(13)+2,100) for _ in range(4)]
S=[[sum(M[k][i]*M[k][j] for k in range(4))/16 + (F(1,10) if i==j else 0) for j in range(4)] for i in range(4)]
print("mu",[str(x) for x in mu]); print("diag",[str(S[i][i]) for i in range(4)])
Sn=np.array([[float(x) for x in r] for r in S]); mun=np.array([float(x) for x in mu])
def eq(gam, free):
    idx=free; k=len(idx)
    K=np.zeros((k+1,k+1)); K[:k,:k]=gam*Sn[np.ix_(idx,idx)]; K[:k,k]=1; K[k,:k]=1
    rhs=np.concatenate([mun[idx],[1.0]])
    sol=np.linalg.solve(K,rhs)
    w=np.zeros(4); w[idx]=sol[:k]; return w, sol[k]
def obj(gam,w): return gam/2*w@Sn@w - mun@w
for gam in [1,2,4,8,16]:
    w,l=eq(gam,[0,1,2,3])
    print("eq gamma",gam,"ret %.9f var %.9f obj %.9f"%(mun@w, w@Sn@w, obj(gam,w)), "w",np.round(w,9), "sum", w.sum())
# E2: difference at gamma 16
w16,_=eq(16,[0,1,2,3]); print("E2 eq obj16 unrounded",obj(16,w16))
import itertools
def best_nonneg(gam):
    cands=[]
    for r in range(1,5):
        for free in itertools.combinations(range(4),r):
            w,l=eq(gam,list(free))
            if (w>=-1e-12).all():
                sw=Sn@w; nu=gam*sw-mun+l
                zeros=[i for i in range(4) if i not in free]
                if all(nu[i]>=-1e-12 for i in zeros): cands.append((tuple(zeros),w))
    return cands
for gam in [1,2,4,8,16]:
    c=best_nonneg(gam)
    best=min(c,key=lambda t: obj(gam,t[1]))
    print("nonneg gamma",gam,"n_cands",len(c),"zeros",best[0],"w",np.round(best[1],9),"ret %.9f var %.9f obj %.9f"%(mun@best[1],best[1]@Sn@best[1],obj(gam,best[1])))
    if gam==16: print("E2 nonneg obj16 unrounded", obj(gam,best[1]), "diff", obj(gam,best[1])-obj(16,w16))
    if gam==4:
        w4=best[1]; d=w4-0.25; print("E3 turnover unrounded", np.abs(d).sum(), "printed-digits sum", sum(abs(round(x,6)-0.25) for x in w4))
