"""Independent recomputation (numpy, not the lab's Jacobi code) of every printed number in project Labs 1-3.

Run with: .venv/bin/python -I ledgers/M3/scripts/M3-d-r1/recompute_lab_numbers.py
"""

from __future__ import annotations

import numpy as np


def clip(c: np.ndarray) -> np.ndarray:
    w, v = np.linalg.eigh(c)
    x = v @ np.diag(np.maximum(w, 0.0)) @ v.T
    d = np.sqrt(np.diag(x))
    return x / np.outer(d, d)


def dykstra(c: np.ndarray, iters: int = 20000) -> np.ndarray:
    """Higham's alternating projections (plain, not Dykstra) as an independent nearest-correlation estimate."""
    y = c.copy()
    for _ in range(iters):
        w, v = np.linalg.eigh(y)
        p = v @ np.diag(np.maximum(w, 0.0)) @ v.T
        y_new = p.copy()
        np.fill_diagonal(y_new, 1.0)
        if np.max(np.abs(y_new - y)) < 1e-14:
            y = y_new
            break
        y = y_new
    return y


def weights(c: np.ndarray, vols: np.ndarray) -> np.ndarray:
    sigma = np.diag(vols) @ c @ np.diag(vols)
    x = np.linalg.solve(sigma, np.ones(len(vols)))
    return x / x.sum()


def main() -> None:
    lab1 = np.array([[1.0, 0.8, -0.5], [0.8, 1.0, 0.6], [-0.5, 0.6, 1.0]])
    lab2 = np.array([[1.0, 0.6, 0.5], [0.6, 1.0, -0.7], [0.5, -0.7, 1.0]])
    lab3 = np.array([[1.0, 0.7, 0.3, -0.6], [0.7, 1.0, 0.5, 0.4], [0.3, 0.5, 1.0, 0.2], [-0.6, 0.4, 0.2, 1.0]])
    vols = np.array([0.10, 0.20, 0.15, 0.30])
    print("lab1 eig:", " ".join(f"{x:.6f}" for x in np.linalg.eigvalsh(lab1)))
    c1 = clip(lab1)
    print("lab1 rebuilt diagonal (pre-rescale):", np.round(np.diag(np.linalg.eigh(lab1)[1] @ np.diag(np.maximum(np.linalg.eigh(lab1)[0], 0)) @ np.linalg.eigh(lab1)[1].T), 6))
    print("lab1 repaired:", np.round(c1, 6).tolist())
    print("lab2 eig:", " ".join(f"{x:.6f}" for x in np.linalg.eigvalsh(lab2)))
    print("lab2 repaired:", np.round(clip(lab2), 6).tolist())
    pr = dykstra(lab3)
    cl = clip(lab3)
    print("lab3 smallest eig:", f"{np.linalg.eigvalsh(lab3)[0]:.6f}")
    dc = np.linalg.norm(cl - lab3)
    dp = np.linalg.norm(pr - lab3)
    print("dist clip", f"{dc:.6f}", "dist proj", f"{dp:.6f}", "saved", f"{dc - dp:.6f}")
    print("max entry diff proj-clip", f"{np.max(np.abs(pr - cl)):.6f}")
    print("max diag dev clip", f"{np.max(np.abs(np.diag(cl) - 1)):.6e}", "proj", f"{np.max(np.abs(np.diag(pr) - 1)):.6e}")
    print("min eig proj", f"{np.linalg.eigvalsh(pr)[0]:.3e}")
    wc = weights(cl, vols)
    wp = weights(pr, vols)
    print("w clip", np.round(wc, 6).tolist(), "sum", f"{wc.sum():.6f}")
    print("w proj", np.round(wp, 6).tolist(), "sum", f"{wp.sum():.6f}")
    print("max weight diff", f"{np.max(np.abs(wp - wc)):.6f}", "at index", int(np.argmax(np.abs(wp - wc))))
    print("dist clip-proj as printed gap", f"{dc:.6f} - {dp:.6f}")


if __name__ == "__main__":
    main()
