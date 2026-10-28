"""Independent recomputation of the printed numbers in M3 L04-L06 (run with python -I)."""
import math

import numpy as np

a0 = np.random.default_rng(0).normal(size=(4, 3))
s = np.linalg.svd(a0, compute_uv=False)
print("L06 seed-0 singular values unrounded:", s.tolist(), "rounded:", [f"{x:.4f}" for x in s])
J = np.array([[0.0, 1.0], [-1.0, 0.0]])
print("L06 counterexample J=[[0,1],[-1,0]] singular values:", np.linalg.svd(J, compute_uv=False).tolist(),
      "abs eigenvalues:", np.abs(np.linalg.eigvals(J)).tolist())
G = np.array([[1, 0, 1], [0, 1, 1], [1, 1, 2]], float)
print("L05 Remark 3.2 eigenvalues:", np.linalg.eigvalsh(G).tolist())
vals = [1 + 2 * math.sin(2 * math.pi * k / 360 * 2) for k in range(360)]
print("L05 Part B negative:", sum(v < -1e-10 for v in vals), "zero:", sum(abs(v) <= 1e-10 for v in vals), "min:", min(vals))
print("L05 E2 118/360 =", 118 / 360, "rounded", round(118 / 360, 4))
print("L04 E3 1/sqrt2 =", 1 / math.sqrt(2))
t = (-1 + math.sqrt(5)) / 2
A = np.array([[4.0, 1.0], [1.0, 3.0]])
v = np.array([1.0, t]); w = np.array([1.0, (-1 - math.sqrt(5)) / 2])
print("L04 M1 residual:", (A @ v - (4 + t) * v).tolist(), "inner product:", float(v @ w))
