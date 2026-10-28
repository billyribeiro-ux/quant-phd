# Independent recomputation of numbers quoted in L07-L09 prose and problems.
import numpy as np
np.set_printoptions(precision=10)
# L07 Lab 1 data, re-generated from the same seed
rng = np.random.default_rng(7); n = 12
x1 = rng.normal(size=n); x2 = rng.normal(size=n); noise = rng.normal(scale=0.3, size=n)
y = 1.5 + 0.8*x1 - 0.4*x2 + noise
a = np.column_stack([np.ones(n), x1, x2])
print("L07 A^T y =", a.T @ y)
g = a.T @ a; beta = np.linalg.solve(g, a.T @ y); r = y - a @ beta
print("L07 beta unrounded =", beta, "residual norm =", np.linalg.norm(r))
# L07 E2 claim: check prints False when entries of A^T y >= 1e-9 (sure), and A^T y ~ (18.38, 3.10, -17.60)
# L07 M2 exact
A = np.array([[1,0],[1,1],[1,2.]]); yy = np.array([1,2,2.])
print("L07 M2 beta", np.linalg.solve(A.T@A, A.T@yy), "fitted", A@np.linalg.solve(A.T@A, A.T@yy))

# L08
exec(open("/tmp/verifyB1-M3-c/tests/labs/M3/lab-M3-L08-1.py").read().split("def main()")[0].replace("from __future__ import annotations",""))
rng = np.random.default_rng(8); panel = simulate_panel(rng)
lam, v = pca(panel)
sh = lam/lam.sum()
print("L08 unrounded shares", sh[:3]*100, "sum top3", sh[:3].sum()*100, "sum of printed", round(sh[0]*100,1)+round(sh[1]*100,1)+round(sh[2]*100,1))
xc = panel - panel.mean(axis=0); m = xc.T@xc/(T_DAYS-1)
print("L08 M11 (0.25y) =", m[0,0], "trace", np.trace(m), "M11/trace", m[0,0]/np.trace(m))
rescaled = panel.copy(); rescaled[:,0]*=10
m3 = (rescaled - rescaled.mean(axis=0)); m3 = m3.T@m3/(T_DAYS-1)
print("L08 rescaled first-share", np.linalg.eigvalsh(m3)[-1]/np.trace(m3), "rescaled M11 =", m3[0,0], "lower bound share", m3[0,0]/np.trace(m3))
# does the lower bound lambda1>=M11' alone imply share rises? lower bound on share:
M11=m[0,0]; T0=np.trace(m)
print("L08 lower bound on new share 100*M11/(T0+99*M11) =", 100*M11/(T0+99*M11), "vs old share", lam[0]/T0)
# causal claim: does ordering follow planted scales? vary scales
import itertools
for sc in [(8,4,2),(2,4,8),(4,8,2)]:
    def sim(rng):
        level, slope, curv = planted_shapes()
        scores = np.column_stack([rng.normal(scale=sc[0],size=T_DAYS), rng.normal(scale=sc[1],size=T_DAYS), rng.normal(scale=sc[2],size=T_DAYS)])
        return scores @ np.column_stack([level,slope,curv]).T + rng.normal(scale=0.5,size=(T_DAYS,6))
    l2, v2 = pca(sim(np.random.default_rng(8)))
    lev = np.argmax(np.abs(v2[:,:3].T@planted_shapes()[0]))
    print("scales", sc, "level best PC index", lev, "eigs", np.round(l2[:3],2))
