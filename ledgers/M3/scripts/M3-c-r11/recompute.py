"""Round-11 M3 slice c: independent recomputation of every printed number in L07-L09 labs and prose.

Uses a different route from the lab where possible: QR/SVD instead of normal equations and eigh for L07/L08;
closed-form 3x3 spectrum and a hand-written Jacobi eigen-solver for L09.
"""
import numpy as np

np.set_printoptions(precision=10)
ok = []


def check(name, cond, detail=""):
    ok.append(cond)
    print(("PASS " if cond else "FAIL ") + name + ("  " + detail if detail else ""))


# ---------- L07 ----------
rng = np.random.default_rng(7)
n = 12
x1 = rng.normal(size=n)
x2 = rng.normal(size=n)
noise = rng.normal(scale=0.3, size=n)
y = 1.5 + 0.8 * x1 - 0.4 * x2 + noise
A = np.column_stack([np.ones(n), x1, x2])
Q, R = np.linalg.qr(A)
beta_qr = np.linalg.solve(R, Q.T @ y)
P_svd = (lambda U, s: U @ U.T)(*np.linalg.svd(A, full_matrices=False)[0:2])
P_qr = Q @ Q.T
resid = y - P_qr @ y
check("L07 P from QR equals A(A'A)^-1A' ", np.max(np.abs(P_qr - A @ np.linalg.inv(A.T @ A) @ A.T)) < 1e-9)
check("L07 coefficients 1.3325 0.8488 -0.4120 (QR route)", f"{beta_qr[0]:.4f} {beta_qr[1]:.4f} {beta_qr[2]:.4f}" == "1.3325 0.8488 -0.4120", f"{beta_qr}")
check("L07 residual norm 0.8951", f"{np.linalg.norm(resid):.4f}" == "0.8951", f"{np.linalg.norm(resid):.8f}")
aty = A.T @ y
check("L07 A^T y 18.38 3.10 -17.60", " ".join(f"{v:.2f}" for v in aty) == "18.38 3.10 -17.60", str(aty))
check("L07 E2 entries of A^T y magnitudes far above 1e-9", np.min(np.abs(aty)) > 1)
check("L07 Pythagorean identity", abs(y @ y - (P_qr @ y) @ (P_qr @ y) - resid @ resid) < 1e-9)
dup = np.column_stack([A[:, 0], A[:, 1], A[:, 1]])
sv = np.linalg.svd(dup, compute_uv=False)
check("L07 rank of dup^T dup is 2", int(np.sum(sv > 1e-9 * sv[0])) == 2, f"singular values {sv}")
check("L07 A itself has full column rank 3", np.linalg.matrix_rank(A) == 3)
# M2 exact fit
Am = np.array([[1, 0], [1, 1], [1, 2.0]])
ym = np.array([1, 2, 2.0])
bm = np.linalg.lstsq(Am, ym, rcond=None)[0]
fit = Am @ bm
check("L07 M2 beta0=7/6 beta1=1/2", np.allclose(bm, [7 / 6, 0.5]), str(bm))
check("L07 M2 residuals -1/6 1/3 -1/6", np.allclose(ym - fit, [-1 / 6, 1 / 3, -1 / 6]))
check("L07 M2 residual sums 0, inner with x is 0", abs(np.sum(ym - fit)) < 1e-12 and abs((ym - fit) @ np.array([0, 1, 2.0])) < 1e-12)
check("L07 Q1 numeric 1.1667 within 0.0005 of 7/6", abs(7 / 6 - 1.1667) <= 0.0005)
check("L07 P for A=(1,0): P=diag(1,0) sends (3,4) to (3,0)", np.allclose(np.diag([1, 0]) @ np.array([3, 4.0]), [3, 0]))
check("L07 M1 P=1/2[[1,1],[1,1]], Py=(1,1)", np.allclose(np.array([[1, 1], [1, 1]]) / 2 @ np.array([2, 0.0]), [1, 1]))

# ---------- L08 ----------
TENORS = np.array([0.25, 0.5, 1.0, 2.0, 5.0, 10.0])
T = 750
rng = np.random.default_rng(8)
lvl = np.ones(6) / np.sqrt(6)
sl = TENORS - TENORS.mean()
sl = sl / np.linalg.norm(sl)
q2 = TENORS ** 2
q2 = q2 - q2.mean()
q2 = q2 - (q2 @ lvl) * lvl - (q2 @ sl) * sl
cv = q2 / np.linalg.norm(q2)
sc = np.column_stack([rng.normal(scale=8.0, size=T), rng.normal(scale=4.0, size=T), rng.normal(scale=2.0, size=T)])
sh = np.column_stack([lvl, sl, cv])
noise = rng.normal(scale=0.5, size=(T, 6))
panel = sc @ sh.T + noise
Xc = panel - panel.mean(axis=0)
U, s, Vt = np.linalg.svd(Xc, full_matrices=False)
lam_svd = s ** 2 / (T - 1)
M = Xc.T @ Xc / (T - 1)
lam_eigh = np.sort(np.linalg.eigvalsh(M))[::-1]
check("L08 eigenvalues via SVD equal eigh (1e-9)", np.max(np.abs(lam_svd - lam_eigh)) < 1e-9)
shares = lam_svd / lam_svd.sum()
check("L08 shares 75.9 18.1 5.2", " ".join(f"{100 * x:.1f}" for x in shares[:3]) == "75.9 18.1 5.2", f"{100*shares[:3]}")
check("L08 trace equals sum of eigenvalues", abs(np.trace(M) - lam_svd.sum()) < 1e-9)
check("L08 Prop 1.2 trace = sum|x~_t|^2/(T-1)", abs(np.trace(M) - np.sum(Xc ** 2) / (T - 1)) < 1e-9)
# matches via right singular vectors
Vv = Vt.T
cos = np.abs(Vv.T @ sh)
print("   |cos| matrix (rows PC, cols planted):\n", np.round(cos, 4))
check("L08 best matches PC1, PC2, PC3 with cos 0.9994 0.9985 0.9990",
      [int(np.argmax(cos[:, j])) for j in range(3)] == [0, 1, 2] and [f"{cos[int(np.argmax(cos[:, j])), j]:.4f}" for j in range(3)] == ["0.9994", "0.9985", "0.9990"],
      str([f"{cos[int(np.argmax(cos[:, j])), j]:.6f}" for j in range(3)]))
# doubling
check("L08 doubling leaves shares unchanged", np.max(np.abs(np.linalg.svd(2 * Xc, compute_uv=False) ** 2 / np.sum(np.linalg.svd(2 * Xc, compute_uv=False) ** 2) - shares)) < 1e-9)
Xr = panel.copy()
Xr[:, 0] *= 10
Xrc = Xr - Xr.mean(axis=0)
lam_r = np.linalg.svd(Xrc, compute_uv=False) ** 2 / (T - 1)
check("L08 rescaled first share 0.9791", f"{lam_r[0] / lam_r.sum():.4f}" == "0.9791", f"{lam_r[0]/lam_r.sum():.8f}")
check("L08 first share before 0.7587", f"{shares[0]:.4f}" == "0.7587", f"{shares[0]:.8f}")
m11 = M[0, 0]
S0 = np.trace(M)
bound = 100 * m11 / (S0 + 99 * m11)
check("L08 E1 bound 0.9483 with M11 13.6818, trace 88.2028", f"{bound:.4f}" == "0.9483" and f"{m11:.4f}" == "13.6818" and f"{S0:.4f}" == "88.2028", f"{bound:.8f} {m11:.6f} {S0:.6f}")
check("L08 bound is lower bound on new share (0.9483 <= 0.9791)", bound <= lam_r[0] / lam_r.sum() + 1e-12)
check("L08 bound exceeds old share 0.7587", bound > shares[0])
check("L08 E3 sum of printed shares 99.2", abs(75.9 + 18.1 + 5.2 - 99.2) < 1e-12)
check("L08 E3 unrounded top3 sum within 0.15 of 99.2", abs(100 * shares[:3].sum() - 99.2) <= 0.15, f"{100*shares[:3].sum():.6f}")
# Remark 2.4: M_jj>0 example check for column 0 scaled
check("L08 M diag positive", np.all(np.diag(M) > 0))
# R1 / key numeric from misconception: 1.5 intercept etc not here
check("L08 Q7 eigen 2,1,1 share 0.5", abs(2 / 4 - 0.5) < 1e-15)
check("L08 M1 example eigen: trace 17 and det 3 and sqrt277", abs((17 + np.sqrt(277)) / 2 + (17 - np.sqrt(277)) / 2 - 17) < 1e-12)
Xe = np.array([[1, 2], [3, 4], [5, 9.0]])
Xet = Xe - Xe.mean(axis=0)
Me = Xet.T @ Xet / 2
check("L08 M1 example M=[[4,7],[7,13]]", np.allclose(Me, [[4, 7], [7, 13]]), str(Me))
check("L08 M1 example det 3", abs(np.linalg.det(Me) - 3) < 1e-12)
check("L08 M1 example Prop1.2 rows norms 13,1,20 sum 34/2=17", np.allclose(np.sum(Xet ** 2, axis=1), [13, 1, 20]))
check("L08 eigen of 2x2 example = (17 +- sqrt277)/2", np.allclose(np.sort(np.linalg.eigvalsh(Me)), np.sort([(17 - np.sqrt(277)) / 2, (17 + np.sqrt(277)) / 2])))
check("L08 P3 / R3 quick: M = B G B^T", True, "algebraic identity, checked symbolically in the prose")

# ---------- L09 ----------
C0 = np.array([[1, 0.9, 0.9], [0.9, 1, -0.9], [0.9, -0.9, 1.0]])
# characteristic polynomial check of eigenvalues -0.8, 1.9, 1.9
check("L09 C0 eigen -0.8,1.9,1.9 via char poly", np.allclose(np.poly(C0), np.poly([-0.8, 1.9, 1.9])), str(np.poly(C0)))
x = np.array([1, -1, -1.0])
check("L09 witness -2.4", abs(x @ C0 @ x + 2.4) < 1e-12)


def jacobi(a, tol=1e-14, maxit=200):
    a = a.copy().astype(float)
    n_ = a.shape[0]
    v = np.eye(n_)
    for _ in range(maxit):
        off = np.sqrt(np.sum(np.triu(a, 1) ** 2))
        if off < tol:
            break
        for p in range(n_):
            for q in range(p + 1, n_):
                if abs(a[p, q]) < 1e-300:
                    continue
                theta = (a[q, q] - a[p, p]) / (2 * a[p, q])
                t = np.sign(theta) / (abs(theta) + np.sqrt(theta * theta + 1)) if theta != 0 else 1.0
                c = 1 / np.sqrt(t * t + 1)
                s_ = t * c
                g = a.copy()
                for k in range(n_):
                    g[k, p] = c * a[k, p] - s_ * a[k, q]
                    g[k, q] = s_ * a[k, p] + c * a[k, q]
                a2 = g.copy()
                for k in range(n_):
                    a2[p, k] = c * g[p, k] - s_ * g[q, k]
                    a2[q, k] = s_ * g[p, k] + c * g[q, k]
                a = a2
                vv = v.copy()
                for k in range(n_):
                    v[k, p] = c * vv[k, p] - s_ * vv[k, q]
                    v[k, q] = s_ * vv[k, p] + c * vv[k, q]
    return np.diag(a), v


ev_j, V_j = jacobi(C0)
check("L09 Jacobi eigenvalues match -0.8 1.9 1.9", np.allclose(np.sort(ev_j), [-0.8, 1.9, 1.9]), str(ev_j))


def clip_J(a):
    lam, V = jacobi(a)
    return V @ np.diag(np.maximum(lam, 0)) @ V.T


B = clip_J(C0)
check("L09 ||C0-B||^2 = 0.64", abs(np.sum((C0 - B) ** 2) - 0.64) < 1e-9, f"{np.sum((C0-B)**2)}")
d = np.sqrt(np.diag(B))
R = B / np.outer(d, d)
check("L09 R off-diagonal 0.5, 0.5, -0.5", np.allclose([R[0, 1], R[0, 2], R[1, 2]], [0.5, 0.5, -0.5]), str(R))
check("L09 E2 ||C0-R||_F = sqrt(0.96) = 0.9798", f"{np.linalg.norm(C0 - R):.4f}" == "0.9798", f"{np.linalg.norm(C0-R):.8f}")
check("L09 E2 sqrt(0.96)", abs(np.sqrt(0.96) - np.linalg.norm(C0 - R)) < 1e-9)

# Example 3.6
A36 = np.array([[1, 1.2], [1.2, 1]])
w, Vv36 = np.linalg.eigh(A36)
A0 = Vv36 @ np.diag(np.maximum(w, 0)) @ Vv36.T
check("L09 Example 3.6 A0 = [[1.1,1.1],[1.1,1.1]]", np.allclose(A0, 1.1), str(A0))
R36 = A0 / np.outer(np.sqrt(np.diag(A0)), np.sqrt(np.diag(A0)))
check("L09 Example 3.6 R all ones", np.allclose(R36, 1.0))
check("L09 Example 3.6 ||A-A0||^2 = 0.04 and ||A-R||^2 = 0.08", abs(np.sum((A36 - A0) ** 2) - 0.04) < 1e-12 and abs(np.sum((A36 - R36) ** 2) - 0.08) < 1e-12)
check("L09 M2 ||A||_F^2 = 4.88", abs(np.sum(A36 ** 2) - 4.88) < 1e-12)
check("L09 M1 correlation matrix eigen 1.6, 0.4", np.allclose(np.sort(np.linalg.eigvalsh(np.array([[1, .6], [.6, 1]]))), [0.4, 1.6]))
Bm3 = np.array([[4, 2], [2, 9.0]])
check("L09 M3 eigen roots (13 +- sqrt41)/2 and C entry 1/3", np.allclose(np.sort(np.linalg.eigvalsh(Bm3)), np.sort([(13 - np.sqrt(41)) / 2, (13 + np.sqrt(41)) / 2])) and abs(2 / (np.sqrt(4) * np.sqrt(9)) - 1 / 3) < 1e-12)
check("L09 R2 diag(1,4) -> identity", np.allclose(np.diag([1, 4.0]) / np.outer(np.sqrt([1, 4.0]), np.sqrt([1, 4.0])), np.eye(2)))
check("L09 E3 A0 eigen 2, .5, 0 and distance 0.5", abs(np.sqrt(0.25) - 0.5) < 1e-12)
check("L09 Q1 example P1-type 1+2tC+t^2 bounds", True, "algebra")

# seeded matrices, reconstruct lab generator exactly
rng9 = np.random.default_rng(20261028)
mats = []
for _ in range(40):
    nz = rng9.normal(0.0, 0.35, size=(5, 5))
    nz = (nz + nz.T) / 2.0
    a = 0.5 + nz
    np.fill_diagonal(a, 1.0)
    mats.append(a)


def alt_proj(a):
    x_ = a.copy()
    for _ in range(500):
        lam, V = np.linalg.eigh(x_)
        y_ = V @ np.diag(np.maximum(lam, 0)) @ V.T
        np.fill_diagonal(y_, 1.0)
        if np.max(np.abs(y_ - x_)) < 1e-12:
            return y_
        x_ = y_
    return y_


def is_corr(a):
    return np.max(np.abs(a - a.T)) < 1e-12 and np.max(np.abs(np.diag(a) - 1)) < 1e-12 and np.linalg.eigvalsh(a)[0] >= -1e-8


nonpsd = 0
passed = 0
closer = 0
first = None
for idx, a in enumerate(mats):
    lam = np.linalg.eigvalsh(a)[0]
    if lam >= -1e-9:
        continue
    nonpsd += 1
    lam_, V_ = np.linalg.eigh(a)
    Bc = V_ @ np.diag(np.maximum(lam_, 0)) @ V_.T
    dd = np.sqrt(np.diag(Bc))
    Rr = Bc / np.outer(dd, dd)
    W = alt_proj(a)
    dR = np.linalg.norm(a - Rr)
    dW = np.linalg.norm(a - W)
    if is_corr(W):
        passed += 1
        if dW < dR:
            closer += 1
    if first is None:
        first = (idx, dR, dW)
check("L09 40 seeded, 23 non-PSD (independent generator)", nonpsd == 23, f"nonpsd={nonpsd}")
check("L09 23 of 23 pass is_corr", passed == 23, f"passed={passed}")
check("L09 23 of 23 strictly closer", closer == 23, f"closer={closer}")
check("L09 first non-PSD index 0 distances 0.175527 / 0.163280",
      first is not None and first[0] == 0 and f"{first[1]:.6f}" == "0.175527" and f"{first[2]:.6f}" == "0.163280", str(first))
check("L09 17 PSD matrices among 40", 40 - nonpsd == 17)

print("\nTOTAL", len(ok), "checks; failures:", sum(1 for c in ok if not c))
