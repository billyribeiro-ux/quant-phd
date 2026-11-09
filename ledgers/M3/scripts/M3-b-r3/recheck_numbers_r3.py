"""Round-3 slice b: independent re-derivation of every printed number in the L04-L06 labs and prose.

Each block recomputes a quantity with code written for this round (not copied from the twins), and prints the
unrounded value with the margin to the tolerance used on the page. Run from the checkout root.
"""
import math
from fractions import Fraction

import numpy as np

print("## L04 lab 1 margins (seed 2604, 200 symmetric 4x4)")
rng = np.random.default_rng(2604)
worst = {"orth": 0.0, "recon": 0.0, "resid": 0.0, "imag": 0.0, "pair_orth": 0.0}
n_pairs = 0
for _ in range(200):
    g = rng.standard_normal((4, 4))
    a = (g + g.T) / 2
    w, q = np.linalg.eigh(a)
    worst["orth"] = max(worst["orth"], float(np.max(np.abs(q.T @ q - np.eye(4)))))
    worst["recon"] = max(worst["recon"], float(np.max(np.abs(q @ np.diag(w) @ q.T - a))))
    worst["resid"] = max(worst["resid"], max(float(np.max(np.abs(a @ q[:, j] - w[j] * q[:, j]))) for j in range(4)))
    worst["imag"] = max(worst["imag"], float(np.max(np.abs(np.linalg.eigvals(a).imag))))
    for i in range(4):
        for j in range(i + 1, 4):
            if abs(w[i] - w[j]) > 1e-6:
                n_pairs += 1
                worst["pair_orth"] = max(worst["pair_orth"], abs(float(q[:, i] @ q[:, j])))
for k, v in worst.items():
    print(f"  {k}: max = {v:.3e}  (tolerance 1e-10; margin factor {1e-10 / max(v, 1e-300):.3e})")
print(f"  pairs with eigenvalue gap > 1e-6: {n_pairs} (expected 1200)")
print(f"  |<(1,0),(1,1)/sqrt2>| exact = {1 / math.sqrt(2):.10f} rounds to {1 / math.sqrt(2):.4f}")
N = np.array([[1.0, 2.0], [0.0, 3.0]])
wN, vN = np.linalg.eig(N)
print(f"  eig of N: {sorted(wN)} ; |inner| of normalised eigenvectors = {abs(float(vN[:, 0] @ vN[:, 1])):.10f}")

print("## L05 Part B: 1 + 2 sin(2t) on 360 grid angles t_k = 2 pi k / 360")
vals = [1 + 2 * math.sin(2 * t) for t in (2 * math.pi * k / 360 for k in range(360))]
neg = [k for k, v in enumerate(vals) if v < -1e-10]
zer = [k for k, v in enumerate(vals) if abs(v) <= 1e-10]
print(f"  negative (< -1e-10): {len(neg)} ; first/last index {neg[0]}..{neg[-1]} ; zero: {zer}")
print(f"  min on grid = {min(vals):.12f}  (exact -1 at 135 and 315 degrees)")
print(f"  negative-arc measure fraction = {120 / 360:.6f}; grid count fraction = {len(neg) / 360:.6f}")

print("## L05 Part C: 500 Gram matrices, 200 vectors each (independent recomputation, seed 2604)")
rng = np.random.default_rng(2604)
min_eig = math.inf
min_ratio = math.inf
ok_eig = 0
ok_forms = 0
for _ in range(500):
    b = rng.standard_normal((4, 3))
    g = b.T @ b
    e = float(np.linalg.eigvalsh(g)[0])
    min_eig = min(min_eig, e)
    ok_eig += e >= -1e-10
    x = rng.standard_normal((200, 3))
    for row in x:
        f = float(row @ g @ row)
        nrm = float(row @ row)
        min_ratio = min(min_ratio, f / nrm)
        ok_forms += f >= -1e-10 * nrm
print(f"  Gram with smallest eigenvalue >= -1e-10: {ok_eig} of 500 (min smallest eigenvalue {min_eig:.3e})")
print(f"  sampled forms >= -1e-10|x|^2: {ok_forms} of 100000 (min form/|x|^2 = {min_ratio:.3e})")

print("## L05 Part D: G = B^T B, B = [[1,0,1],[0,1,1]], exact characteristic polynomial")
B = [[1, 0, 1], [0, 1, 1]]
G = [[sum(B[k][i] * B[k][j] for k in range(2)) for j in range(3)] for i in range(3)]
print(f"  G = {G}")
# det(G - t I) at t = 0, 1, 3 and exact expansion check with Fractions
def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
for t in (0, 1, 3, 2):
    m = [[G[i][j] - (t if i == j else 0) for j in range(3)] for i in range(3)]
    print(f"  det(G - {t} I) = {det3(m)}")
print("  (1-l)*l*(l-3) at l=2 is", (1 - 2) * 2 * (2 - 3))
print("  B(1,1,-1) =", [sum(B[i][j] * v for j, v in enumerate([1, 1, -1])) for i in range(2)])

print("## L06 lab 1 (seed-0 4x3 singular values; planted rank-2 count)")
a0 = np.random.default_rng(0).normal(size=(4, 3))
s_svd = np.linalg.svd(a0, compute_uv=False)
s_eig = np.sqrt(np.linalg.eigvalsh(a0.T @ a0)[::-1])
print(f"  svd: {s_svd[0]:.10f} {s_svd[1]:.10f} {s_svd[2]:.10f}")
print(f"  sqrt eig of A^T A: {s_eig[0]:.10f} {s_eig[1]:.10f} {s_eig[2]:.10f}")
print(f"  rounded 4 dp: {s_svd[0]:.4f} {s_svd[1]:.4f} {s_svd[2]:.4f}")
p = np.random.default_rng(7).normal(size=(4, 2)) @ np.random.default_rng(8).normal(size=(2, 3))
sp = np.linalg.svd(p, compute_uv=False)
print(f"  planted singular values: {sp}")
print(f"  relative: {sp / sp[0]}")
print(f"  count above 1e-10*s1: {int(np.sum(sp > 1e-10 * sp[0]))}; min relative of kept = {sp[1] / sp[0]:.3e}, third = {sp[2] / sp[0]:.3e}")
print(f"  rank (numpy matrix_rank) = {np.linalg.matrix_rank(p)}")
for seed in range(5):
    for shape, s in (((4, 3), seed), ((3, 4), 100 + seed)):
        m = np.random.default_rng(s).normal(size=shape)
        u, sv, vt = np.linalg.svd(m)
        k = min(shape)
        sig = np.zeros(shape)
        sig[:k, :k] = np.diag(sv)
        print(f"  seed {s} {shape}: |UtU-I|={np.max(np.abs(u.T@u-np.eye(shape[0]))):.2e} "
              f"|VtV-I|={np.max(np.abs(vt@vt.T-np.eye(shape[1]))):.2e} "
              f"recon={np.max(np.abs(u@sig@vt-m)):.2e} "
              f"eig={np.max(np.abs(sv**2-np.sort(np.linalg.eigvalsh(m.T@m))[::-1][:k])):.2e} "
              f"frob={abs(np.sum(sv**2)-np.sum(m*m)):.2e}")

print("## Exact checks by Fraction (L05 Example 2.5 entries; L06 Problem E3, M1, M2)")
f = Fraction
print("  Example 1.7 form at (1,-1):", f(1) * 1 + 2 * 2 * 1 * (-1) + f(1) * 1)
print("  L04 Example 2.6 form at (1,0) via eigen: 3*(1/2)+1*(1/2) =", f(3, 2) + f(1, 2))
print("  L04 mech-3 x=(1,-2): direct", 2 * 1 + 2 * 1 * (-2) + 2 * 4, "eig-form", 3 * f(1, 2) + 1 * f(9, 2))
print("  L05 Example 2.5 B^TB entries:", (3 + 1) / 2, (3 - 1) / 2, (3 + 1) / 2)
