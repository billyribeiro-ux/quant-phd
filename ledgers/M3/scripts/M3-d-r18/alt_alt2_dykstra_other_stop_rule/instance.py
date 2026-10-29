"""Per-learner instances for the M3 autograder: the covariance-matrix doctor. All values are SIMULATED.

``make_instance(seed)`` is deterministic and uses only the standard library. From the seed alone it draws:

* a dimension k in {3, 4, 5} and k volatilities in [0.05, 0.40], rounded to four decimals;
* ``corr``, a pairwise-estimated matrix: unit diagonal, off-diagonal entries in [-0.95, 0.95] rounded to four
  decimals. A draw is redrawn until its smallest eigenvalue is below -0.02, so every ``corr`` is not positive
  semidefinite by a margin of 0.02;
* ``psd_corr``, a positive definite matrix with unit diagonal: the normalised Gram matrix of a random factor;
* ``spectrum``, k planted eigenvalues in [-0.6, 1.4], and ``psd_spectrum``, k planted eigenvalues in [0, 2] whose
  first entry is exactly 0 (a rank-deficient positive semidefinite case);
* ``eigenvectors``, k orthonormal vectors (Gram-Schmidt of seeded Gaussian draws) that the planted spectra are built on.

Every instance is valid under the contract in project.html. Nothing here is a real covariance matrix, a real
volatility or market data.
"""

from __future__ import annotations

import math
import random
from typing import Any

_MARGIN = 0.02


def _min_eigenvalue(matrix: list[list[float]]) -> float:
    """Smallest eigenvalue of a symmetric matrix, by cyclic Jacobi rotations (used only to certify an instance)."""
    n = len(matrix)
    a = [row[:] for row in matrix]
    for _ in range(60):
        off = math.sqrt(sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j))
        if off < 1e-14:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if a[p][q] == 0.0:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p] = c * akp - s * akq
                    a[k][q] = s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k] = c * apk - s * aqk
                    a[q][k] = s * apk + c * aqk
    return min(a[i][i] for i in range(n))


def _unit_symmetric(rng: random.Random, k: int) -> list[list[float]]:
    """A symmetric matrix with unit diagonal and off-diagonal entries in [-0.95, 0.95], rounded to four decimals."""
    m = [[1.0 if i == j else 0.0 for j in range(k)] for i in range(k)]
    for i in range(k):
        for j in range(i + 1, k):
            value = round(rng.uniform(-0.95, 0.95), 4)
            m[i][j] = value
            m[j][i] = value
    return m


def _positive_definite(rng: random.Random, k: int) -> list[list[float]]:
    """A unit-diagonal positive definite matrix: the normalised Gram matrix of a random k x (k + 2) factor."""
    factor = [[rng.gauss(0.0, 1.0) for _ in range(k + 2)] for _ in range(k)]
    gram = [[sum(factor[i][m] * factor[j][m] for m in range(k + 2)) for j in range(k)] for i in range(k)]
    return [[gram[i][j] / math.sqrt(gram[i][i] * gram[j][j]) for j in range(k)] for i in range(k)]


def _orthonormal(rng: random.Random, k: int) -> list[list[float]]:
    """k orthonormal vectors in R^k, by Gram-Schmidt on seeded Gaussian draws."""
    basis: list[list[float]] = []
    while len(basis) < k:
        v = [rng.gauss(0.0, 1.0) for _ in range(k)]
        for u in basis:
            d = sum(a * b for a, b in zip(v, u, strict=True))
            v = [a - d * b for a, b in zip(v, u, strict=True)]
        norm = math.sqrt(sum(a * a for a in v))
        if norm > 1e-3:
            basis.append([round(a / norm, 12) for a in v])
    return basis


def make_instance(seed: int) -> dict[str, Any]:
    """A deterministic SIMULATED instance for ``seed``. Every instance is valid under the contract."""
    for attempt in range(10_000):
        rng = random.Random(1_000_003 * int(seed) + 7_919 * attempt + 17)
        k = rng.choice((3, 4, 5))
        vols = [round(rng.uniform(0.05, 0.40), 4) for _ in range(k)]
        corr = _unit_symmetric(rng, k)
        if _min_eigenvalue(corr) >= -_MARGIN:
            continue
        psd_corr = _positive_definite(rng, k)
        spectrum = [round(rng.uniform(-0.6, 1.4), 4) for _ in range(k)]
        psd_spectrum = [0.0] + [round(rng.uniform(0.1, 2.0), 4) for _ in range(k - 1)]
        eigenvectors = _orthonormal(rng, k)
        return {
            "seed": int(seed),
            "label": "SIMULATED",
            "k": k,
            "vols": vols,
            "corr": corr,
            "psd_corr": psd_corr,
            "spectrum": spectrum,
            "psd_spectrum": psd_spectrum,
            "eigenvectors": eigenvectors,
        }
    raise RuntimeError("no non-PSD instance found in 10 000 draws")  # a guard against an endless loop
