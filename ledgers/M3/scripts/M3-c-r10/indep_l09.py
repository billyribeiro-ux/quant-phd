import numpy as np
np.set_printoptions(precision=6, suppress=True)
C0 = np.array([[1,0.9,0.9],[0.9,1,-0.9],[0.9,-0.9,1.0]])
print("C0 eig", np.linalg.eigvalsh(C0))
def clip(a):
    # PSD projection via SVD of a symmetric matrix (independent route)
    U,s,Vt = np.linalg.svd(a)
    w, V = np.linalg.eigh(a)
    return (V*np.maximum(w,0))@V.T
def rescale(b):
    d = 1/np.sqrt(np.diag(b)); return b*np.outer(d,d)
B = clip(C0); print("||C0-B||^2", np.sum((C0-B)**2), "sum neg eig^2", np.sum(np.minimum(np.linalg.eigvalsh(C0),0)**2))
R = rescale(B); print("R\n", R, "\nR eig", np.linalg.eigvalsh(R))
rng = np.random.default_rng(20261028)
mins=[]; closer=0; nonpsd=0; feas=0; first=None
def alt(a):
    x=a.copy()
    for _ in range(500):
        y=clip(x); np.fill_diagonal(y,1.0)
        if np.max(np.abs(y-x))<1e-12: return y
        x=y
    return y
for i in range(40):
    noise = rng.normal(0.0,0.35,size=(5,5)); noise=(noise+noise.T)/2
    a = 0.5+noise; np.fill_diagonal(a,1.0)
    mn = np.linalg.eigvalsh(a)[0]; mins.append(mn)
    if mn >= -1e-9: continue
    nonpsd+=1
    Rr = rescale(clip(a)); W = alt(a)
    dR = np.linalg.norm(a-Rr); dW = np.linalg.norm(a-W)
    if dW < dR: closer+=1
    ok = np.max(np.abs(W-W.T))<1e-12 and np.max(np.abs(np.diag(W)-1))<1e-12 and np.linalg.eigvalsh(W)[0]>=-1e-8
    feas+=ok
    if first is None: first=(i,dR,dW)
print("nonpsd",nonpsd,"feasible",feas,"closer",closer,"first",first)
m=np.sort(np.array(mins)); print("min eig sorted (closest to 0 from below and above):", m[:3], m[m>-1e-3][:5] if (m>-1e-3).any() else None)
print("PSD count from min eig >= -1e-9:", sum(1 for x in mins if x>=-1e-9))
print("min eigen values within (-1e-6, 1e-6):", [x for x in mins if abs(x)<1e-6])
