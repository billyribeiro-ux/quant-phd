import numpy as np
from numpy.typing import NDArray
from scipy.optimize import linprog  # type: ignore[import-untyped]

# Problem E2: Lab 1's SIMULATED market at shades near the exact boundary of asset 4's arbitrage-free prices.
rng = np.random.default_rng(303)
X = 1.0 + 0.3 * rng.standard_normal((12, 6))
psi = rng.uniform(0.02, 0.14, 12)
fair = X.T @ psi


def detect(prices: NDArray[np.float64]) -> tuple[float, NDArray[np.float64]]:
    """Lesson 3's detection program: (optimal value, optimal theta)."""
    a_ub = np.vstack([-X, prices[None, :], X, -prices[None, :]])
    b_ub = np.concatenate([np.zeros(12), [0.0], np.ones(12), [1.0]])
    res = linprog(-(X.sum(axis=0) - prices), A_ub=a_ub, b_ub=b_ub, bounds=[(None, None)] * 6, method="highs")
    return float(-res.fun), np.asarray(res.x)


def margin(prices: NDArray[np.float64]) -> float:
    """Lesson 3's state-price margin t*."""
    c = np.zeros(13)
    c[-1] = -1.0
    a_ub = np.hstack([-np.eye(12), np.ones((12, 1))])
    a_eq = np.hstack([X.T, np.zeros((6, 1))])
    bounds = [(None, None)] * 12 + [(None, 1.0)]
    res = linprog(c, A_ub=a_ub, b_ub=np.zeros(12), A_eq=a_eq, b_eq=prices, bounds=bounds, method="highs")
    return float(res.x[-1])


others = [0, 1, 2, 4, 5]
lowest = linprog(X[:, 3], A_eq=X[:, others].T, b_eq=fair[others], bounds=[(0, None)] * 12, method="highs").fun
gap = float(fair[3] - lowest)
print(f"exact gap: {gap:.7f}")
for label, shade in (("0.2078", 0.2078), ("gap - 1e-12", gap - 1e-12), ("exact gap", gap)):
    p = fair.copy()
    p[3] -= shade
    value, theta = detect(p)
    flows = np.concatenate([[-p @ theta], X @ theta])
    print(
        f"shade {label}: margin {margin(p) + 0.0:+.3e}, detection value {round(value, 6) + 0.0:.6f}, "
        f"cash flows of the returned theta from {flows.min() + 0.0:+.1e} to {flows.max() + 0.0:.1e}"
    )
