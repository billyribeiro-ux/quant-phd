"""Round-4 verifier: independent numpy recomputation of the Lab 1 and Lab 2 printed numbers (clipping repair, rescale).

Usage (from the checkout root): .venv/bin/python -I ledgers/M3/scripts/M3-d-r4/lab12_numbers_independent_r4.py
"""

import numpy as np

for name, C in [
    ("Lab 1", np.array([[1.0, 0.8, -0.5], [0.8, 1.0, 0.6], [-0.5, 0.6, 1.0]])),
    ("Lab 2", np.array([[1.0, 0.6, 0.5], [0.6, 1.0, -0.7], [0.5, -0.7, 1.0]])),
]:
    w, U = np.linalg.eigh(C)
    X = (U * np.maximum(w, 0.0)) @ U.T
    d = np.diag(X)
    Y = X / np.outer(np.sqrt(d), np.sqrt(d))
    print(name, "eigenvalues sorted:", " ".join(f"{x:.6f}" for x in np.sort(w)))
    print(name, "smallest eigenvalue:", f"{w.min():.6f}", "| psd at 1e-10:", w.min() >= -1e-10)
    print(name, "rebuilt diagonal:", " ".join(f"{x:.6f}" for x in d))
    for row in Y:
        print(name, "repaired row:", " ".join(f"{x:.6f}" for x in row))
    print(name, "largest deviation of the diagonal from 1:", f"{np.max(np.abs(np.diag(Y) - 1)):.6f}")
    print(name, "psd at 1e-9 after repair:", np.linalg.eigvalsh(Y).min() >= -1e-9)
