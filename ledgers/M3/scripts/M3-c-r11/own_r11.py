import numpy as np
# L08 independent re-derivation
rng = np.random.default_rng(8)
T=750; tau=np.array([0.25,0.5,1.0,2.0,5.0,10.0])
def unit(v): return v/np.linalg.norm(v)
lev=unit(np.ones(6)); sl=unit(tau-tau.mean()); q=tau**2; q=q-q.mean(); q=q-(q@lev)*lev-(q@sl)*sl; cv=unit(q)
sc=np.column_stack([rng.normal(scale=8,size=T),rng.normal(scale=4,size=T),rng.normal(scale=2,size=T)])
panel=sc@np.column_stack([lev,sl,cv]).T+rng.normal(scale=0.5,size=(T,6))
xc=panel-panel.mean(0); M=xc.T@xc/(T-1)
lam,V=np.linalg.eigh(M); o=np.argsort(lam)[::-1]; lam=lam[o]; V=V[:,o]
sh=lam/lam.sum(); print('shares %', np.round(100*sh[:3],4))
print('cos', [round(abs(V[:,:3].T@s).max(),6) for s in (lev,sl,cv)], [int(np.argmax(np.abs(V[:,:3].T@s))) for s in (lev,sl,cv)])
p2=panel.copy(); p2[:,0]*=10; Mp=(p2-p2.mean(0)).T@(p2-p2.mean(0))/(T-1); lp=np.sort(np.linalg.eigvalsh(Mp))[::-1]
print('rescaled first share', lp[0]/lp.sum())
M11=M[0,0]; tr=np.trace(M); print('bound', 100*M11/(tr+99*M11), M11, tr)
# Remark 2.4: rescale column j of X by c; check M' vs kappa*M
X=rng.normal(size=(30,4)); Xc=X-X.mean(0); Mx=Xc.T@Xc/29
for c in (0.5,2.0,-3.0):
    Y=X.copy(); Y[:,1]*=c; Yc=Y-Y.mean(0); My=Yc.T@Yc/29
    k=(My[0,1]/Mx[0,1]) if abs(Mx[0,1])>1e-12 else None
    print('c',c,'is multiple:', np.allclose(My, k*Mx), 'k',k, 'diag ratio', My[1,1]/Mx[1,1], 'off ratio', My[0,1]/Mx[0,1])
# counterexample to 'nonzero off-diagonal' hypothesis being sufficient: row with zero off-diag but nonzero elsewhere
Z=np.zeros((30,3)); Z[:,0]=rng.normal(size=30); Z[:,1]=rng.normal(size=30); Z[:,2]=rng.normal(size=30)
Mz=np.cov(Z.T); print('M_jj zero case not needed; diag positive', np.diag(Mz))
# L09 independent re-derivation
rng=np.random.default_rng(20261028)
C0=np.array([[1,.9,.9],[.9,1,-.9],[.9,-.9,1.]])
w,U=np.linalg.eigh(C0); print('C0 eig', np.round(w,6))
B=U@np.diag(np.maximum(w,0))@U.T; print('dist2', np.sum((C0-B)**2), np.sum(np.minimum(w,0)**2), 'diag B', np.diag(B))
d=1/np.sqrt(np.diag(B)); R=B*np.outer(d,d); print('R', np.round(R,4).tolist())
def clip(a): l,q=np.linalg.eigh(a); return (q*np.maximum(l,0))@q.T
def alt(a):
    x=a.copy()
    for _ in range(500):
        y=clip(x); np.fill_diagonal(y,1.0)
        if np.max(np.abs(y-x))<1e-12: break
        x=y
    return y
cnt=0; feas=0; closer=0; first=None
for i in range(40):
    n=rng.normal(0,0.35,size=(5,5)); n=(n+n.T)/2; a=0.5+n; np.fill_diagonal(a,1.0)
    if np.linalg.eigvalsh(a)[0]>=-1e-9: continue
    cnt+=1
    dd=np.diag(clip(a)); Rr=clip(a)*np.outer(1/np.sqrt(dd),1/np.sqrt(dd))
    W=alt(a)
    ok = np.max(np.abs(W-W.T))<1e-12 and np.max(np.abs(np.diag(W)-1))<1e-12 and np.linalg.eigvalsh(W)[0]>=-1e-8
    feas+=ok
    dR=np.linalg.norm(a-Rr); dW=np.linalg.norm(a-W)
    closer+= dW<dR
    if first is None: first=(i,dR,dW)
print('nonpsd',cnt,'feasible',feas,'closer',closer,'first',first)
