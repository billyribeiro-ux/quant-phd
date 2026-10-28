"""Independent NumPy recomputation of Lab 1 and Lab 2 (project.html rungs 1 and 2) for the printed numbers."""

import numpy as np

for name, C in [
    ("Lab1", np.array([[1.0, 0.8, -0.5], [0.8, 1.0, 0.6], [-0.5, 0.6, 1.0]])),
    ("Lab2", np.array([[1.0, 0.6, 0.5], [0.6, 1.0, -0.7], [0.5, -0.7, 1.0]])),
]:
    w, U = np.linalg.eigh(C)
    X = U @ np.diag(np.maximum(w, 0)) @ U.T
    d = np.sqrt(np.diag(X))
    R = X / np.outer(d, d)
    print(name, "eig", np.round(w, 6), "min", f"{w.min():.6f}", "diag X", np.round(np.diag(X), 6))
    print(name, "R rows", [list(np.round(r, 6)) for r in R], "max dev", f"{np.max(np.abs(np.diag(R)-1)):.2e}", "min eig R", f"{np.linalg.eigvalsh(R).min():.2e}")
