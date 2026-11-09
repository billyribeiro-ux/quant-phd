"""Probe: does numpy eigvalsh return a negative tiny value for an exactly rank-deficient Gram matrix? (evidence for card M3-c100)"""
import numpy as np
rng = np.random.default_rng(2604)
neg = 0
tot = 0
smallest_vals = []
for _ in range(2000):
    b = rng.standard_normal((4, 2)) @ rng.standard_normal((2, 3))  # rank 2, 4x3
    g = b.T @ b
    v = np.linalg.eigvalsh(g)[0]
    smallest_vals.append(v)
    tot += 1
    neg += v < 0
print("rank-2 4x3 factor products tested:", tot, "smallest eigenvalue negative:", neg)
print("most negative smallest eigenvalue:", min(smallest_vals))
b = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 1.0]])
print("Remark 3.2 G eigvalsh:", np.linalg.eigvalsh(b.T @ b).tolist())
