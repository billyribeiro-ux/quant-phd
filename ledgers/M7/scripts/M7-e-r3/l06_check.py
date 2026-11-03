from fractions import Fraction as F
from itertools import product
SEED=2026; N=4
class Lcg:
    def __init__(s,seed): s.state=seed
    def draw(s,m):
        s.state=(1103515245*s.state+12345)%2**31
        return s.state%m
g=Lcg(SEED)
M=[[F(g.draw(7)-3) for _ in range(N)] for _ in range(N)]
mu=[F(g.draw(13)+2,100) for _ in range(N)]
S=[[sum(M[k][i]*M[k][j] for k in range(N))/F(16)+(F(1,10) if i==j else 0) for j in range(N)] for i in range(N)]
print("M",[[int(x) for x in r] for r in M]); print("mu",[str(x) for x in mu]); print("Sigma diag",[str(S[i][i]) for i in range(N)])
print("sym", all(S[i][j]==S[j][i] for i in range(N) for j in range(N)))
def solve(A,b):
    n=len(b); Mx=[row[:]+[b[i]] for i,row in enumerate(A)]
    for c in range(n):
        p=next(i for i in range(c,n) if Mx[i][c]!=0)
        Mx[c],Mx[p]=Mx[p],Mx[c]
        for i in range(n):
            if i!=c and Mx[i][c]!=0:
                f=Mx[i][c]/Mx[c][c]; Mx[i]=[a-f*bb for a,bb in zip(Mx[i],Mx[c])]
    return [Mx[i][n]/Mx[i][i] for i in range(n)]
def mv(A,x): return [sum(A[i][j]*x[j] for j in range(len(x))) for i in range(len(A))]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def risk(w): return dot(w,mv(S,w))
def ret(w): return dot(mu,w)
def obj(gam,w): return gam*risk(w)/2-ret(w)
def eq_w(gam,idx=None):
    idx=list(range(N)) if idx is None else idx
    Sub=[[gam*S[i][j] for j in idx] for i in idx]
    K=[Sub[i]+[F(1)] for i in range(len(idx))]+[[F(1)]*len(idx)+[F(0)]]
    rhs=[mu[i] for i in idx]+[F(1)]
    sol=solve(K,rhs)
    w=[F(0)]*N
    for p,i in enumerate(idx): w[i]=sol[p]
    return w, sol[-1]
gammas=[F(1),F(2),F(4),F(8),F(16)]
Sinv=None
# closed form check
y=solve(S,mu); z=solve(S,[F(1)]*N)
print("1'z",sum(z),">0", sum(z)>0)
for gam in gammas:
    w,lam=eq_w(gam)
    lam_cf=(sum(y)-gam)/sum(z)
    wcf=[(y[i]-lam_cf*z[i])/gam for i in range(N)]
    print("gamma",gam,"budget exact",sum(w)==1,"kkt==closed form",w==wcf,"lam",lam,lam_cf==lam)
    print("   w",[float(x) for x in w],"risk",float(risk(w)),"ret",float(ret(w)),"obj",float(obj(gam,w)), "exact risk",risk(w),"exact obj",obj(gam,w))
    print("   printed-style 6dp:", ["%.6f"%float(x) for x in w], "risk %.6f ret %.6f obj %.6f"%(float(risk(w)),float(ret(w)),float(obj(gam,w))))

print("---- Part B (w>=0) ----")
res={}
for gam in gammas:
    cands=[]
    for mask in product((0,1),repeat=N):
        zeros=[i for i in range(N) if mask[i]]; free=[i for i in range(N) if not mask[i]]
        if not free: continue
        w,lam=eq_w(gam,free)
        nu=[gam*mv(S,w)[i]-mu[i]+lam for i in range(N)]
        if all(x>=0 for x in w) and all(nu[i]>=0 for i in zeros):
            cands.append((tuple(zeros),w))
    print("gamma",gam,"passing",[ (c[0]) for c in cands], "count", len(cands))
    zs,wbest=min(cands,key=lambda c: obj(gam,c[1]))
    eq_obj=obj(gam,eq_w(gam)[0])
    res[gam]=(zs,wbest)
    print("  zero set",zs,"weights",[float(x) for x in wbest],"risk",float(risk(wbest)),"ret",float(ret(wbest)),"obj",float(obj(gam,wbest)),"eq obj",float(eq_obj),"constrained>=eq",obj(gam,wbest)>=eq_obj)
    print("  6dp weights",["%.6f"%float(x) for x in wbest],"risk %.6f ret %.6f obj %.6f"%(float(risk(wbest)),float(ret(wbest)),float(obj(gam,wbest))))
    # all 15 candidates pass count and zero sets for each candidate
# E2
w16=eq_w(F(16))[0]; c16=res[F(16)][1]
d=obj(F(16),c16)-obj(F(16),w16)
print("E2 gamma16 difference unrounded", float(d), "=", d)
# E3 turnover gamma=4
w4=res[F(4)][1]; w0=[F(1,4)]*N
turn=sum(abs(w4[i]-w0[i]) for i in range(N))
print("E3 turnover unrounded", float(turn), "printed-weights turnover", sum(abs(F(round(float(w4[i])*10**6),10**6)-w0[i]) for i in range(N)) if False else "")
pr=[F("0.389219"),F("0.220570"),F("0.390211"),F(0)]
print("E3 printed weights turnover", float(sum(abs(pr[i]-w0[i]) for i in range(N))), "lab-prints %.6f"%float(turn))
print("unrounded weights gamma4 (float)", [float(x) for x in w4])
