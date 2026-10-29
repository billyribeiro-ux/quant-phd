import numpy as np
# L07 E2: A^T y for seeded response
rng = np.random.default_rng(7)
n = 12
x1 = rng.normal(size=n); x2 = rng.normal(size=n); noise = rng.normal(scale=0.3, size=n)
y = 1.5 + 0.8 * x1 - 0.4 * x2 + noise
a = np.column_stack([np.ones(n), x1, x2])
print("A^T y", np.round(a.T @ y, 4))
beta = np.linalg.solve(a.T @ a, a.T @ y)
print("beta", beta, "resid norm", np.linalg.norm(y - a @ beta))
# L07 M2 check
A = np.array([[1,0],[1,1],[1,2.]]); Y = np.array([1,2,2.])
b = np.linalg.solve(A.T@A, A.T@Y); print("M2", b, A@b, Y-A@b)
# L08 rederive
rng = np.random.default_rng(8)
def unit(v): return v/np.linalg.norm(v)
TEN = np.array([0.25,0.5,1,2,5,10.])
level=unit(np.ones(6)); slope=unit(TEN-TEN.mean()); q=TEN**2; q=q-q.mean(); q=q-(q@level)*level-(q@slope)*slope; curv=unit(q)
scores=np.column_stack([rng.normal(scale=8.0,size=750),rng.normal(scale=4.0,size=750),rng.normal(scale=2.0,size=750)])
panel=scores@np.column_stack([level,slope,curv]).T+rng.normal(scale=0.5,size=(750,6))
def pca(P):
    xc=P-P.mean(0); m=xc.T@xc/(P.shape[0]-1); w,v=np.linalg.eigh(m); o=np.argsort(w)[::-1]; return w[o],v[:,o],m
lam,v,m=pca(panel); sh=lam/lam.sum()
print("shares", 100*sh[:3])
print("rescaled first share", pca(np.column_stack([panel[:,0]*10,panel[:,1:]]))[0][0]/pca(np.column_stack([panel[:,0]*10,panel[:,1:]]))[0].sum())
M11=m[0,0]; S0=np.trace(m); print("M11",M11,"S0",S0,"bound",100*M11/(S0+99*M11))
# L09 rederive
C0=np.array([[1,.9,.9],[.9,1,-.9],[.9,-.9,1.]])
w,Q=np.linalg.eigh(C0); print("eig",w)
B=Q@np.diag(np.maximum(w,0))@Q.T; d=np.sqrt(np.diag(B)); R=B/np.outer(d,d); print("R",np.round(R,6))
print("||C0-R||", np.linalg.norm(C0-R), np.sqrt(0.96))
