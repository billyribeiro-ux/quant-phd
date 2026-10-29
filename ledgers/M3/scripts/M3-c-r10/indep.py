import numpy as np
np.set_printoptions(precision=6, suppress=True)
print("== L07 independent")
rng = np.random.default_rng(7)
n = 12
x1 = rng.normal(size=n); x2 = rng.normal(size=n); noise = rng.normal(scale=0.3, size=n)
y = 1.5 + 0.8*x1 - 0.4*x2 + noise
A = np.column_stack([np.ones(n), x1, x2])
print("A^T y =", A.T @ y)
beta = np.linalg.lstsq(A, y, rcond=None)[0]
r = y - A @ beta
print("beta", beta, "resid norm", np.linalg.norm(r), "A^T r", A.T @ r)
# independent via QR
Q, R = np.linalg.qr(A)
print("beta QR", np.linalg.solve(R, Q.T @ y), "resid QR", np.linalg.norm(y - Q @ (Q.T @ y)))
print("rank A^T A dup:", np.linalg.matrix_rank(np.column_stack([A[:,0],A[:,1],A[:,1]]).T @ np.column_stack([A[:,0],A[:,1],A[:,1]])))

print("== L08 independent")
rng = np.random.default_rng(8)
T = 750
tenors = np.array([0.25,0.5,1,2,5,10.0])
level = np.ones(6)/np.sqrt(6)
s = tenors - tenors.mean(); slope = s/np.linalg.norm(s)
q = tenors**2 - (tenors**2).mean()
q = q - (q@level)*level - (q@slope)*slope
curv = q/np.linalg.norm(q)
sc = np.column_stack([rng.normal(scale=8.0,size=T), rng.normal(scale=4.0,size=T), rng.normal(scale=2.0,size=T)])
panel = sc @ np.column_stack([level,slope,curv]).T + rng.normal(scale=0.5,size=(T,6))
X = panel - panel.mean(0)
U,S,Vt = np.linalg.svd(X, full_matrices=False)
ev = S**2/(T-1)
print("svd eig", ev)
M = X.T@X/(T-1)
w,V = np.linalg.eigh(M); w=w[::-1]; V=V[:,::-1]
print("eigh eig", w, "max|diff|", np.max(np.abs(w-ev)))
sh = w/w.sum()
print("shares %", 100*sh[:3])
for k,sv in zip(["level","slope","curv"],[level,slope,curv]):
    c = np.abs(V.T@sv); print(k, np.argmax(c)+1, c.max())
M11 = M[0,0]; tr = np.trace(M)
print("M11", M11, "trace", tr, "bound", 100*M11/(tr+99*M11))
P = panel.copy(); P[:,0]*=10; Xr = P-P.mean(0); Mr = Xr.T@Xr/(T-1)
wr = np.linalg.eigvalsh(Mr)[::-1]; print("rescaled first share", wr[0]/wr.sum())
print("sum of the three printed shares", 75.9+18.1+5.2)
