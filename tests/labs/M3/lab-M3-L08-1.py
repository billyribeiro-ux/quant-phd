"""M3 L08 lab 1: principal component analysis of a SIMULATED six-tenor yield-change panel.

SIMULATED: the panel is generated here from a seeded generator (seed 8) with three planted factors, a level, a
slope and a curvature shape, and independent noise. No Treasury, Federal Reserve or other market data are read or
represented. The planted shapes and factor sizes are the generator's choices; nothing here estimates a real curve.
Units: daily changes in basis points (bp), one row per day, one column per tenor (0.25, 0.5, 1, 2, 5, 10 years).

The lab forms the centred data matrix Xc, the matrix M = Xc^T Xc / (T - 1), and its eigendecomposition with
numpy.linalg.eigh. It checks, to the tolerances printed: M is positive semidefinite, M V = V Lambda, the scores
Z = Xc V satisfy Z^T Z / (T - 1) = Lambda, and the eigenvalues sum to trace(M). The explained shares are computed from
unrounded eigenvalues and printed to one decimal place of a percent. Each planted shape is matched to the principal
component with the largest absolute cosine. Two scale checks show what a rescaling does to the shares. Standard
library and NumPy only. No randomness outside the seeded generator, and no network access.
"""

from __future__ import annotations

import numpy as np

TOL = 1e-9
TENORS = np.array([0.25, 0.5, 1.0, 2.0, 5.0, 10.0])
T_DAYS = 750


def unit(v: np.ndarray) -> np.ndarray:
    """Return v scaled to Euclidean norm 1."""
    scaled: np.ndarray = v / np.linalg.norm(v)
    return scaled


def planted_shapes() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return orthonormal level, slope and curvature shapes over the six tenors (unitless)."""
    level = unit(np.ones_like(TENORS))
    slope = unit(TENORS - TENORS.mean())
    quad = TENORS**2
    quad = quad - quad.mean()
    quad = quad - (quad @ level) * level - (quad @ slope) * slope  # remove the level and slope parts
    return level, slope, unit(quad)


def simulate_panel(rng: np.random.Generator) -> np.ndarray:
    """Return a T x 6 SIMULATED panel of daily yield changes in bp: planted factors plus noise."""
    level, slope, curv = planted_shapes()
    scores = np.column_stack(
        [
            rng.normal(scale=8.0, size=T_DAYS),  # level factor, bp per day
            rng.normal(scale=4.0, size=T_DAYS),  # slope factor, bp per day
            rng.normal(scale=2.0, size=T_DAYS),  # curvature factor, bp per day
        ]
    )
    shapes = np.column_stack([level, slope, curv])
    noise = rng.normal(scale=0.5, size=(T_DAYS, len(TENORS)))
    panel: np.ndarray = scores @ shapes.T + noise
    return panel


def pca(panel: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return (eigenvalues descending, eigenvectors as columns) of M = Xc^T Xc / (T - 1)."""
    xc = panel - panel.mean(axis=0)
    m = xc.T @ xc / (panel.shape[0] - 1)
    values, vectors = np.linalg.eigh(m)
    order = np.argsort(values)[::-1]
    return values[order], vectors[:, order]


def main() -> None:
    rng = np.random.default_rng(8)
    panel = simulate_panel(rng)
    t_count = panel.shape[0]
    xc = panel - panel.mean(axis=0)
    m = xc.T @ xc / (t_count - 1)
    lam, v = pca(panel)

    print(f"panel: T = {t_count} days, {len(TENORS)} tenors, SIMULATED, in bp")
    print(f"M positive semidefinite (smallest eigenvalue >= -{TOL:g}): {bool(lam[-1] >= -TOL)}")
    print(f"M V = V Lambda to {TOL:g}: {bool(np.max(np.abs(m @ v - v * lam)) < TOL)}")
    scores = xc @ v
    print(
        f"scores satisfy Z^T Z / (T - 1) = Lambda to {TOL:g}: "
        f"{bool(np.max(np.abs(scores.T @ scores / (t_count - 1) - np.diag(lam))) < TOL)}"
    )
    trace_ok = abs(float(np.sum(lam)) - float(np.trace(m))) < TOL
    print(f"eigenvalues sum to trace(M) to {TOL:g}: {trace_ok}")

    shares = lam / np.sum(lam)
    print(
        "explained share of PC1, PC2, PC3 (from unrounded eigenvalues), percent to one decimal: "
        f"{100 * shares[0]:.1f} {100 * shares[1]:.1f} {100 * shares[2]:.1f}"
    )
    print(f"explained shares of all six components sum to 1 to {TOL:g}: {bool(abs(float(np.sum(shares)) - 1) < TOL)}")

    level, slope, curv = planted_shapes()
    names = ("level", "slope", "curvature")
    matches = []
    for name, shape in zip(names, (level, slope, curv), strict=True):
        cosines = np.abs(v[:, :3].T @ shape)
        best = int(np.argmax(cosines))
        matches.append(best)
        print(f"planted {name}: best-matching component PC{best + 1}, |cosine| {cosines[best]:.4f}")
    print(f"the three planted shapes match three different components: {len(set(matches)) == 3}")

    doubled = panel * 2.0
    lam2, _ = pca(doubled)
    print(
        f"doubling every entry leaves the shares unchanged to {TOL:g}: "
        f"{bool(np.max(np.abs(lam2 / np.sum(lam2) - shares)) < TOL)}"
    )
    rescaled = panel.copy()
    rescaled[:, 0] *= 10.0
    lam3, _ = pca(rescaled)
    print(
        f"first share before rescaling the 0.25-year column by 10: {shares[0]:.4f}; after: {lam3[0] / np.sum(lam3):.4f}"
    )


main()
