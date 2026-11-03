"""Starter for the M3 project: covariance_doctor.py, the covariance-matrix doctor.

Implement every function to the contract in project.html, section "Rung 3 · Specification", then run the
autograder there, or locally with the browser's flags:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Use the standard library and NumPy only. Every function must validate the conditions the specification names and raise
ValueError for them. No function may print or warn.
"""

from __future__ import annotations


def min_eigenvalue(matrix: list[list[float]]) -> float:
    """The smallest eigenvalue of the symmetric matrix."""
    raise NotImplementedError("min_eigenvalue is not written yet")


def is_psd(matrix: list[list[float]], tol: float = 1e-10) -> bool:
    """True when every eigenvalue of the symmetric matrix is at least -tol."""
    raise NotImplementedError("is_psd is not written yet")


def clip_repair(matrix: list[list[float]], floor: float = 0.0) -> list[list[float]]:
    """Eigenvalues below floor set to floor, the matrix rebuilt from them, then rescaled to unit diagonal."""
    raise NotImplementedError("clip_repair is not written yet")


def projection_repair(matrix: list[list[float]], tol: float = 1e-10, max_iter: int = 500) -> list[list[float]]:
    """An approximation of the Frobenius-nearest symmetric positive semidefinite matrix with unit diagonal."""
    raise NotImplementedError("projection_repair is not written yet")


def comparison_weights(corr: list[list[float]], vols: list[float]) -> list[float]:
    """Weights proportional to the inverse covariance matrix times the ones vector, normalised to sum to 1."""
    raise NotImplementedError("comparison_weights is not written yet")
