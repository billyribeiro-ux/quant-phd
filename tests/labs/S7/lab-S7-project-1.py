import numpy as np
from numpy.typing import NDArray


def benjamini_hochberg(pvalues: NDArray[np.float64], q: float) -> NDArray[np.bool_]:
    """Benjamini-Hochberg step-up at FDR level q; returns a mask in the input order."""
    if not 0.0 < q < 1.0:
        raise ValueError("q must lie strictly between 0 and 1")  # a level of 0 or 1 is not a test
    p = np.asarray(pvalues, dtype=np.float64)
    if p.ndim != 1 or np.any(~np.isfinite(p)) or np.any((p < 0.0) | (p > 1.0)):
        raise ValueError("pvalues must be a 1-D array in [0, 1]")
    m = p.size
    if m == 0:
        return np.zeros(0, dtype=bool)  # no hypotheses, no rejections
    order = np.argsort(p)  # any sort order gives the same mask: ties never straddle k*
    lines = q * np.arange(1, m + 1) / m  # the BH line k*q/m for k = 1..m
    below = np.nonzero(p[order] <= lines)[0]  # every k whose ordered p-value is under its line
    reject = np.zeros(m, dtype=bool)
    if below.size:
        k_star = below[-1] + 1  # step-UP: the LARGEST passing k, not the first failure
        reject[order[:k_star]] = True  # reject the k* smallest p-values, including any above their own line
    return reject


# Eight p-values from a hypothetical strategy grid (illustrative inputs, not data).
p = np.array([0.041, 0.001, 0.300, 0.012, 0.024, 0.700, 0.020, 0.049])
mask = benjamini_hochberg(p, 0.05)
print("rejected (input order):", "".join("R" if r else "." for r in mask))
print("number rejected:", int(mask.sum()))
print("largest rejected p-value:", f"{p[mask].max():.3f}")
third = float(np.sort(p)[2])
print(
    "third-smallest p-value:",
    f"{third:.3f}",
    "| its own line:",
    f"{3 * 0.05 / p.size:.4f}",
    "| rejected:",
    bool(third <= p[mask].max()),
)
