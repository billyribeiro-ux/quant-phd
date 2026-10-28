# Round 2, slice M3-a: the L03 R1 solution says the lab's residual is "small but not zero". Measure it.
# Run as: <checkout>/.venv/bin/python -I ledgers/M3/scripts/M3-a-r2/residual_check.py
import numpy as np

a = np.array([[2, 1, 0], [0, 3, 1], [0, 0, 5]], dtype=float)
values, vectors = np.linalg.eig(a)
res = [float(np.max(np.abs(a @ vectors[:, j] - values[j] * vectors[:, j]))) for j in range(3)]
print("L03 lab matrix A residuals (numpy eig):", res, "all exactly zero:", all(r == 0.0 for r in res))
