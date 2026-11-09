"""Independent re-derivation of every printed number and worked example in M3 L04-L06 (round 2).

Run as: .venv/bin/python -I ledgers/M3/scripts/M3-b-r2/recheck_numbers_r2.py
Each check prints a line 'PASS <id> ...' or 'FAIL <id> ...'. Independent of the page code: it uses
closed forms where possible, and a second algorithm (characteristic polynomial roots, Cholesky,
sqrt of eigenvalues of A^T A) where a solver is needed.
"""

from __future__ import annotations

import math

import numpy as np

results: list[tuple[str, bool, str]] = []


def check(cid: str, ok: bool, detail: str) -> None:
    results.append((cid, bool(ok), detail))
    print(("PASS " if ok else "FAIL ") + cid + " " + detail)


r2 = math.sqrt(2.0)

# ---------------- L04 ----------------
A = np.array([[2.0, 1.0], [1.0, 2.0]])
Q = np.array([[1.0, 1.0], [1.0, -1.0]]) / r2
Lam = np.diag([3.0, 1.0])
check("L04-ex26-factor", np.allclose(Q @ Lam @ Q.T, A) and np.allclose(Q.T @ Q, np.eye(2)), f"QLQ^T={np.round(Q @ Lam @ Q.T, 12).tolist()}")
y = Q.T @ np.array([1.0, 0.0])
check("L04-ex26-corollary", abs(3 * y[0] ** 2 + 1 * y[1] ** 2 - 2.0) < 1e-12, f"y^2={np.round(y**2, 6).tolist()} sum={3*y[0]**2+y[1]**2:.12f}")

Nm = np.array([[1.0, 2.0], [0.0, 3.0]])
check("L04-rem27-eig", np.allclose(sorted(np.linalg.eigvals(Nm).real), [1.0, 3.0]), "eig(N)={1,3}")
ip = abs(np.array([1.0, 0.0]) @ (np.array([1.0, 1.0]) / r2))
check("L04-rem27-ip", f"{ip:.4f}" == "0.7071" and abs(ip - 1 / r2) < 1e-15, f"|<(1,0),(1,1)/sqrt2>|={ip:.10f}")
check("L04-E3-digits", abs(1 / r2 - 0.70710678) < 1e-8, f"1/sqrt2={1/r2:.10f}")

R = np.array([[0.0, -1.0], [1.0, 0.0]])
ev = np.linalg.eigvals(R)
check("L04-rem16", np.allclose(sorted(np.abs(ev.imag)), [1.0, 1.0]) and np.allclose(ev.real, 0.0), f"eig(R)={np.round(ev, 12).tolist()}")

B41 = np.array([[4.0, 1.0], [1.0, 3.0]])
ev41 = sorted(np.linalg.eigvalsh(B41))
check("L04-ex15-target", np.allclose(ev41, sorted([(7 - math.sqrt(5)) / 2, (7 + math.sqrt(5)) / 2])), "eig = (7 -/+ sqrt5)/2")

# M1: v, w orthogonal eigenvectors of [[4,1],[1,3]]
v = np.array([1.0, (-1 + math.sqrt(5)) / 2])
w = np.array([1.0, (-1 - math.sqrt(5)) / 2])
Ab = B41
check("L04-M1", abs(v @ w) < 1e-12 and np.allclose(Ab @ v, ((7 + math.sqrt(5)) / 2) * v) and np.allclose(Ab @ w, ((7 - math.sqrt(5)) / 2) * w), f"<v,w>={v @ w:.2e}")

# M2: Q Lambda Q^T for Q=(1/sqrt2)[[1,1],[1,-1]], Lambda=diag(5,-1)
Q2 = np.array([[1.0, 1.0], [1.0, -1.0]]) / r2
check("L04-M2", np.allclose(Q2 @ np.diag([5.0, -1.0]) @ Q2.T, [[2.0, 3.0], [3.0, 2.0]]), "QLQ^T=[[2,3],[3,2]]")

# M3: x^T A x for A=[[2,1],[1,2]], x=(1,-2)
x = np.array([1.0, -2.0])
direct = x @ A @ x
y3 = Q.T @ x
check("L04-M3", abs(direct - 6) < 1e-12 and abs(3 * y3[0] ** 2 + y3[1] ** 2 - 6) < 1e-12, f"direct={direct} corollary={3*y3[0]**2+y3[1]**2:.12f}")

# R1: z=(1,-i) eigenvector of R with eigenvalue i; z*Rz = 2i
z = np.array([1.0, -1.0j])
check("L04-R1", np.allclose(R @ z, 1j * z) and np.isclose(np.conj(z) @ R @ z, 2j), f"z*Rz={np.conj(z) @ R @ z}")

check("L04-E2-pairs", 200 * math.comb(4, 2) == 1200 and math.comb(4, 2) == 6, "C(4,2)=6, 200*6=1200")
check("L04-quiz-x", abs(np.array([1.0, 0.0]) @ A @ np.array([1.0, 0.0]) - 2.0) < 1e-12, "x^TAx=2 for x=(1,0)")

# Lab 1 of L04 (independent second algorithm on the same seeded sample, for the counts)
rng = np.random.default_rng(2604)
c_orth = c_rec = c_res = c_real = 0
pairs = pairs_orth = 0
for _ in range(200):
    g = rng.standard_normal((4, 4))
    s = (g + g.T) / 2.0
    w_, V_ = np.linalg.eigh(s)
    c_orth += np.max(np.abs(V_.T @ V_ - np.eye(4))) < 1e-10
    c_rec += np.max(np.abs(V_ @ np.diag(w_) @ V_.T - s)) < 1e-10
    c_res += all(np.max(np.abs(s @ V_[:, j] - w_[j] * V_[:, j])) < 1e-10 for j in range(4))
    # general solver: characteristic polynomial roots as a second algorithm
    coeffs = np.poly(s)
    roots = np.roots(coeffs)
    c_real += np.max(np.abs(roots.imag)) < 1e-6
    for i in range(4):
        for j in range(i + 1, 4):
            if abs(w_[i] - w_[j]) > 1e-6:
                pairs += 1
                pairs_orth += abs(V_[:, i] @ V_[:, j]) < 1e-10
check("L04-lab-counts", (c_orth, c_rec, c_res, pairs, pairs_orth) == (200, 200, 200, 1200, 1200), f"orth={c_orth} rec={c_rec} res={c_res} real(roots,1e-6)={c_real} pairs={pairs} orth_pairs={pairs_orth}")

# ---------------- L05 ----------------
C = np.array([[1.0, 2.0], [2.0, 1.0]])
xq = np.array([1.0, -1.0])
check("L05-ex17", xq @ C @ xq == -2.0 and np.allclose(sorted(np.linalg.eigvalsh(C)), [-1.0, 3.0]), "form=-2, eig={-1,3}")
check("L05-ex26-vec", np.allclose(C @ np.array([1.0, -1.0]), [-1.0, 1.0]), "A(1,-1)=(-1,1)")

Mrem = np.array([[1.0, 1.0], [-1.0, 1.0]])
rng2 = np.random.default_rng(1)
xs = rng2.standard_normal((1000, 2))
forms = np.einsum("ij,jk,ik->i", xs, Mrem, xs)
check("L05-rem18-form", np.allclose(forms, (xs ** 2).sum(1)), "x^TMx=x1^2+x2^2 (1000 random x)")
ev_m = np.linalg.eigvals(Mrem)
check("L05-rem18-eig", np.allclose(sorted(ev_m, key=lambda z: z.imag), sorted([1 - 1j, 1 + 1j], key=lambda z: z.imag)), f"eig={np.round(ev_m, 12).tolist()}")

Bf = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 1.0]])
G = Bf.T @ Bf
check("L05-rem32-G", np.allclose(G, [[1, 0, 1], [0, 1, 1], [1, 1, 2]]), "G matches")
tt = np.linspace(-3, 3, 7)
det_ok = all(abs(np.linalg.det(G - lam * np.eye(3)) - (1 - lam) * lam * (lam - 3)) < 1e-9 for lam in tt)
check("L05-rem32-det", det_ok, "det(G-lamI)=(1-lam)lam(lam-3) at 7 points")
check("L05-rem32-eig", np.allclose(sorted(np.linalg.eigvalsh(G)), [0, 1, 3], atol=1e-12), f"eig(G)={np.round(sorted(np.linalg.eigvalsh(G)), 15).tolist()}")
check("L05-rem32-null", np.allclose(Bf @ np.array([1.0, 1.0, -1.0]), 0) and np.allclose(G @ np.array([1.0, 1.0, -1.0]), 0), "(1,1,-1) in null space")

# Example 2.5: B = Lambda^{1/2} Q^T
Qe = np.array([[1.0, 1.0], [1.0, -1.0]]) / r2
Be = np.diag([math.sqrt(3), 1.0]) @ Qe.T
check("L05-ex25", np.allclose(Be, np.array([[math.sqrt(3), math.sqrt(3)], [1, -1]]) / r2) and np.allclose(Be.T @ Be, [[2, 1], [1, 2]]), f"B^TB={np.round(Be.T @ Be, 12).tolist()}")

# Part B: grid count on [[1,2],[2,1]] over 360 angles
ks = np.arange(360)
t = 2 * math.pi * ks / 360
cs, sn = np.cos(t), np.sin(t)
vals = cs * cs + 4 * cs * sn + sn * sn
neg = int(np.sum(vals < -1e-10))
zer = int(np.sum(np.abs(vals) <= 1e-10))
check("L05-partB", neg == 118 and zer == 4 and abs(vals.min() + 1.0) < 1e-12, f"negative={neg} zero={zer} min={vals.min():.12f}")
closed = 1 + 2 * np.sin(2 * t)
check("L05-partB-closed", np.allclose(vals, closed, atol=1e-12), "form = 1 + 2 sin 2t on the grid")
check("L05-E2", abs(118 / 360 - 0.3278) < 5e-5 and 59 + 59 == 118 and 164 - 106 + 1 == 59 and 344 - 286 + 1 == 59, f"118/360={118/360:.6f}")
ends = [105, 165, 285, 345]
check("L05-E2-endpoints", all(abs(1 + 2 * math.sin(2 * math.radians(e))) < 1e-12 for e in ends), "form is 0 at 105,165,285,345 degrees")

# Part C: independent second algorithm (min Rayleigh quotient by Cholesky-free general solver)
rng3 = np.random.default_rng(2604)
eig_ok = form_ok = 0
forms_total = 0
min_eig_seen = []
min_ratio_seen = []
for _ in range(500):
    b = rng3.standard_normal((4, 3))
    a = b.T @ b
    lo = float(np.min(np.linalg.eigvals(a).real))
    min_eig_seen.append(lo)
    eig_ok += lo >= -1e-10
    xv = rng3.standard_normal((200, 3))
    fm = np.sum((xv @ a) * xv, axis=1)
    nrm = np.sum(xv * xv, axis=1)
    min_ratio_seen.append(float(np.min(fm / nrm)))
    form_ok += int(np.sum(fm >= -1e-10 * nrm))
    forms_total += 200
check("L05-partC", eig_ok == 500 and form_ok == 100000 and forms_total == 100000, f"eig_pass={eig_ok}/500 form_pass={form_ok}/{forms_total} min_eig_over_500={min(min_eig_seen):.3e}")

# Part D
Gd = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 1.0]])
Gd = Gd.T @ Gd
vd = np.sort(np.linalg.eigvalsh(Gd))
check("L05-partD", abs(vd[0]) <= 1e-10 and abs(vd[1] - 1) < 1e-12 and abs(vd[2] - 3) < 1e-12 and int(np.sum(np.abs(vd) <= 1e-10)) == 1, f"sorted={vd.tolist()}")

# M2 and M3 of L05
M2m = np.array([[1.0, 2.0], [2.0, 4.0]])
check("L05-M2", np.allclose(sorted(np.linalg.eigvalsh(M2m)), [0, 5], atol=1e-12) and np.array([2.0, -1.0]) @ M2m @ np.array([2.0, -1.0]) == 0.0, "eig {0,5}; x=(2,-1) gives 0")
M3m = np.array([[3.0, -1.0], [-1.0, 3.0]])
check("L05-M3", np.allclose(sorted(np.linalg.eigvalsh(M3m)), [2, 4]) and np.array([1.0, 1.0]) @ M3m @ np.array([1.0, 1.0]) == 4.0, "eig {2,4}; form at (1,1) = 4")

# R1 (L05): factor -B and O_pi = -I
check("L05-R1", np.allclose(np.array([[-1.0, 0.0], [0.0, -1.0]]) @ Be, -Be) and np.allclose(Be.T @ Be, [[2, 1], [1, 2]]), "O_pi B = -B and B^TB = Example 2.5 matrix")

# ---------------- L06 ----------------
a_seed0 = np.random.default_rng(0).normal(size=(4, 3))
g0 = a_seed0.T @ a_seed0
sv_eig = np.sqrt(np.sort(np.linalg.eigvalsh(g0))[::-1])
sv_svd = np.linalg.svd(a_seed0, compute_uv=False)
ok_sv = np.allclose(sv_eig, sv_svd, atol=1e-12)
rounded = [f"{v:.4f}" for v in sv_svd]
check("L06-seed0-sv", ok_sv and rounded == ["2.2335", "0.9250", "0.3348"], f"sv={sv_svd.tolist()} rounded={rounded}")
margin = min(abs(v * 1e4 - math.floor(v * 1e4) - 0.5) for v in sv_svd)
check("L06-seed0-rounding-margin", margin > 1e-3, f"distance of 4th decimal from a rounding tie: {margin:.4f} (in units of 1e-4)")

planted = np.random.default_rng(7).normal(size=(4, 2)) @ np.random.default_rng(8).normal(size=(2, 3))
spl = np.linalg.svd(planted, compute_uv=False)
check("L06-planted-rank", int(np.sum(spl > 1e-10 * spl[0])) == 2 and np.linalg.matrix_rank(planted) == 2, f"sv={spl.tolist()}")

check("L06-M1", np.allclose(np.linalg.svd(np.diag([3.0, 4.0]), compute_uv=False), [4, 3]) and np.allclose(np.array([[0, 1], [1, 0]]) @ np.diag([4.0, 3.0]) @ np.array([[0, 1], [1, 0]]), np.diag([3.0, 4.0])), "sv {4,3}; swap U diag(4,3) V^T = diag(3,4)")
check("L06-M2", np.allclose(np.linalg.svd(np.array([[1.0, 1.0], [0.0, 0.0]]), compute_uv=False), [r2, 0.0], atol=1e-12) and abs(np.sum(np.array([[1.0, 1.0], [0.0, 0.0]]) ** 2) - 2) < 1e-12, "sv {sqrt2,0}; ||A||_F^2=2")
M3ident = np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]])
check("L06-M3", np.allclose(np.linalg.svd(M3ident, compute_uv=False), [1, 1]), "sv {1,1} for the 3x2 matrix")
check("L06-E3", np.allclose(np.linalg.svd(np.array([[3.0, 4.0]]), compute_uv=False), [5.0]) and 9 + 16 == 25, "sv 5 for (3 4)")
check("L06-quiz-frob", np.sum(np.array([[1.0, 2.0], [3.0, 4.0]]) ** 2) == 30, "||A||_F^2=30")
check("L06-quiz-2I", np.sum((2 * np.eye(2)) ** 2) == 8 and np.allclose(np.linalg.svd(2 * np.eye(2), compute_uv=False), [2, 2]), "||2I||_F^2=8")
N01 = np.array([[0.0, 1.0], [0.0, 0.0]])
check("L06-misc-sv", np.allclose(np.linalg.svd(N01, compute_uv=False), [1, 0], atol=1e-12) and np.allclose(sorted(np.linalg.eigvals(N01).real), [0, 0]) and np.allclose(N01.T @ N01, [[0, 0], [0, 1]]), "sv {1,0}; eig(A)={0,0}; A^TA=diag(0,1)")
I2swap = np.array([[0.0, 1.0], [1.0, 0.0]])
check("L06-rem25", np.allclose(I2swap @ np.eye(2) @ I2swap.T, np.eye(2)) and not np.allclose(I2swap, np.eye(2)), "P I_2 P^T = I_2 with P swap")
rng6 = np.random.default_rng(11)
spot_ok = True
for _ in range(3):
    Mx = rng6.normal(size=(4, 3))
    s_a = np.linalg.svd(Mx, compute_uv=False)
    s_t = np.linalg.svd(Mx.T, compute_uv=False)
    spot_ok = spot_ok and np.allclose(s_a, s_t)
check("L06-R1-spot", spot_ok, "singular values of A and A^T agree on 3 random 4x3 matrices")

n_pass = sum(1 for _, ok, _ in results if ok)
print(f"SUMMARY {n_pass} of {len(results)} checks PASS")
