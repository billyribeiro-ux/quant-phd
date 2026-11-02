# Independent recomputation of L08 numbers (python -I). Shapes built by explicit Gram-Schmidt, not by the lab code.
import numpy as np
tenors = np.array([0.25, 0.5, 1.0, 2.0, 5.0, 10.0])
def gs(vecs):
    out = []
    for v in vecs:
        w = v.copy()
        for q in out:
            w = w - (q @ v) * q
        out.append(w / np.linalg.norm(w))
    return out
iota = np.ones(6)
f1, f2, f3 = gs([iota, tenors - tenors.mean(), tenors**2 - (tenors**2).mean()])
print("orthonormal check:", np.max(np.abs(np.array([[a@b for b in (f1,f2,f3)] for a in (f1,f2,f3)]) - np.eye(3))))
rng = np.random.default_rng(8)
T = 750
S_ = np.column_stack([rng.normal(scale=8, size=T), rng.normal(scale=4, size=T), rng.normal(scale=2, size=T)])
B = np.column_stack([f1, f2, f3])
X = S_ @ B.T + rng.normal(scale=0.5, size=(T, 6))
Xc = X - X.mean(axis=0)
M = Xc.T @ Xc / (T - 1)
lam, V = np.linalg.eigh(M)
lam = lam[::-1]; V = V[:, ::-1]
sh = lam / lam.sum()
print("shares (4 dp unrounded):", np.round(sh, 6))
print("shares x100 1dp:", [f"{100*s:.1f}" for s in sh[:3]], "sum of rounded printed:", round(sum(round(100*s,1) for s in sh[:3]),1))
print("sum of unrounded top3 x100:", 100*sh[:3].sum())
print("cosines planted vs top3 abs:", np.round(np.abs(V[:, :3].T @ f1),4), np.round(np.abs(V[:, :3].T @ f2),4), np.round(np.abs(V[:, :3].T @ f3),4))
# rescale check
R = X.copy(); R[:, 0] *= 10
Rc = R - R.mean(axis=0); MR = Rc.T @ Rc / (T - 1); lr = np.linalg.eigvalsh(MR)[::-1]
print("first share after rescale:", lr[0] / lr.sum())
M11 = M[0, 0]; tr = np.trace(M)
print("M11, trace:", M11, tr, "E1 bound:", 100*M11/(tr + 99*M11))
print("bound from printed inputs 13.6818, 88.2028:", 100*13.6818/(88.2028 + 99*13.6818))
print("lambda1' >= 100 M11 check:", lr[0] >= 100*M11 - 1e-9, "trace(MR) == tr + 99 M11:", np.isclose(np.trace(MR), tr + 99*M11))
# Problem M1
X1 = np.array([[1,2],[3,4],[5,9]], float); Xc1 = X1 - X1.mean(axis=0); M1 = Xc1.T@Xc1/2
print("M1:", M1, "trace", np.trace(M1), "det", np.linalg.det(M1), "eig", np.linalg.eigvalsh(M1), "(17+-sqrt277)/2", (17+np.sqrt(277))/2, (17-np.sqrt(277))/2)
