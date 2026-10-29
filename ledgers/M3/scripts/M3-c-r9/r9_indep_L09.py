import numpy as np
C0 = np.array([[1,.9,.9],[.9,1,-.9],[.9,-.9,1.]])
print("char poly coeffs", np.round(np.poly(C0),6))
w, V = np.linalg.eig(C0)
print("eig", np.round(np.sort(w.real),6))
neg = [i for i in range(3) if w[i] < 0]
B = sum(max(w[i],0)*np.outer(V[:,i],V[:,i]) for i in range(3)).real
d = np.sqrt(np.diag(B)); R = B/np.outer(d,d)
print("R", np.round(R,4).tolist())
print("dist2 C0-B", round(float(np.sum((C0-B)**2)),10), "sum neg eig^2", round(float(sum(w[i]**2 for i in neg)),10))
print("x^T C0 x", float(np.array([1,-1,-1])@C0@np.array([1,-1,-1])))
print("||C0-R||", np.sqrt(np.sum((C0-R)**2)), round(np.sqrt(0.96),6))
# independent re-derivation of the 40-matrix experiment with an independent RNG call pattern check
rng = np.random.default_rng(20261028)
cnt_np=0; cnt_closer=0; cnt_feas=0; first=None
for idx in range(40):
    N = rng.normal(0,0.35,size=(5,5)); N=(N+N.T)/2
    A = 0.5+N; np.fill_diagonal(A,1.0)
    lam, Q = np.linalg.eigh(A)
    if lam[0] >= -1e-9: continue
    cnt_np+=1
    Bc = Q@np.diag(np.maximum(lam,0))@Q.T
    dd=np.sqrt(np.diag(Bc)); Rr = Bc/np.outer(dd,dd)
    X=A.copy()
    for _ in range(500):
        Y = np.linalg.eigh(X)
        Yc = Y[1]@np.diag(np.maximum(Y[0],0))@Y[1].T
        np.fill_diagonal(Yc,1.0)
        if np.max(np.abs(Yc-X))<1e-12: X=Yc; break
        X=Yc
    W=X
    ok = np.max(np.abs(W-W.T))<1e-12 and np.max(np.abs(np.diag(W)-1))<1e-12 and np.linalg.eigvalsh(W)[0]>=-1e-8
    cnt_feas+=bool(ok)
    dR=np.linalg.norm(A-Rr); dW=np.linalg.norm(A-W)
    cnt_closer+= bool(dW<dR)
    if first is None: first=(idx, round(dR,6), round(dW,6))
print("nonPSD",cnt_np,"feasible",cnt_feas,"closer",cnt_closer,"first",first)
