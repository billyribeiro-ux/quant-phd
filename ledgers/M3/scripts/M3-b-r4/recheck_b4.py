"""M3-b round 4 independent recomputation of L04-L06 numbers (no lab code reused)."""
import math
import numpy as np
from fractions import Fraction

# L06: singular values of seed-0 4x3 matrix, independent path: eig of A^T A
a0 = np.random.default_rng(0).normal(size=(4, 3))
ev = np.sort(np.linalg.eigvalsh(a0.T @ a0))[::-1]
print("L06 seed0 sigma (sqrt eig A^TA):", [f"{math.sqrt(x):.4f}" for x in ev], [repr(math.sqrt(x)) for x in ev])

# L06 planted rank count via matrix_rank with the page's threshold
planted = np.random.default_rng(7).normal(size=(4, 2)) @ np.random.default_rng(8).normal(size=(2, 3))
s = np.linalg.svd(planted, compute_uv=False)
print("L06 planted sigmas:", s, "count >1e-10 rel:", int(np.sum(s > 1e-10 * s[0])), "matrix_rank:", np.linalg.matrix_rank(planted))

# L05 Part B: exact integer-degree grid of 360 angles; form = 1 + 2 sin(2t) exactly
neg = zer = 0
mins = []
for k in range(360):
    t = math.radians(k)
    c, s_ = math.cos(t), math.sin(t)
    v = c * c + 4 * c * s_ + s_ * s_
    mins.append(v)
    if v < -1e-10:
        neg += 1
    if abs(v) <= 1e-10:
        zer += 1
print("L05 grid negative:", neg, "zero:", zer, "min:", round(min(mins), 4), "118/360 =", round(118 / 360, 4))
exact_neg = [k for k in range(360) if 1 + 2 * math.sin(math.radians(2 * k)) < 0]
exact_zero = [k for k in range(360) if abs(1 + 2 * math.sin(math.radians(2 * k))) < 1e-12]
print("exact-integer-degree negative count:", len(exact_neg), "zeros at:", exact_zero)
print("interval endpoints check 2t=210,330 ->", 1 + 2*math.sin(math.radians(210)), 1 + 2*math.sin(math.radians(330)))

# L04 contrast value
N = np.array([[1.0, 2.0], [0.0, 3.0]])
v1 = np.array([1.0, 0.0]); v2 = np.array([1.0, 1.0]) / math.sqrt(2)
print("L04 |<v1,v2>| exact:", 1 / math.sqrt(2), "4dp:", f"{abs(v1 @ v2):.4f}", "eig check:", np.linalg.eig(N)[1][:, 0] @ np.linalg.eig(N)[1][:, 1])

# L05 Remark 3.2 / Part D spectrum
G = np.array([[1, 0, 1], [0, 1, 1], [1, 1, 2]], dtype=float)
print("L05 G eig:", np.round(np.sort(np.linalg.eigvalsh(G)), 12))

# L05 Example 2.5 factor product exact
B = np.array([[math.sqrt(3), math.sqrt(3)], [1, -1]]) / math.sqrt(2)
print("L05 Ex2.5 B^T B:", np.round(B.T @ B, 12).tolist())

# L06 Problem E3 and M1 checks
print("E3 sigma:", np.linalg.svd(np.array([[3.0, 4.0]]), compute_uv=False))
print("M1 sigma:", np.linalg.svd(np.diag([3.0, 4.0]), compute_uv=False))

# L05 E2 fraction 118/360 and one-third
print("1/3 =", Fraction(1, 3), "118/360 reduced:", Fraction(118, 360), float(Fraction(118, 360)))
