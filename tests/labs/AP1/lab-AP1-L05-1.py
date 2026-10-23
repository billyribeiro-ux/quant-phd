import numpy as np
from numpy.typing import NDArray

# SIMULATED market without a riskless payoff: 10 states, 4 risky payoffs priced by a strictly positive SDF.
rng = np.random.default_rng(653)
probs = rng.dirichlet(np.full(10, 5.0))
m_true = np.exp(rng.normal(0.0, 0.35, 10))
m_true *= 0.97 / float(probs @ m_true)
X = 1.0 + 0.3 * rng.standard_normal((10, 4))
p = X.T @ (probs * m_true)
mu = X.T @ probs  # E[x]
cov = X.T @ (probs[:, None] * X) - np.outer(mu, mu)  # Cov(x)


def sigma_min(v: float) -> float:
    """Smallest standard deviation of an SDF with mean v that prices x (Theorem 2.1)."""
    g = p - v * mu
    return float(np.sqrt(g @ np.linalg.solve(cov, g)))


def max_sharpe(v: float) -> float:
    """Largest Sharpe ratio of a zero-price payoff x'theta - (p'theta / v) * 1, if a riskless asset cost v."""
    best = 0.0
    for theta in np.vstack([np.linalg.solve(cov, p - v * mu), rng.standard_normal((2000, 4))]):
        y = X @ theta - (p @ theta) / v
        sd = float(np.sqrt(probs @ (y - probs @ y) ** 2))
        best = max(best, abs(float(probs @ y)) / sd)
    return best


def sd(z: NDArray[np.float64]) -> float:
    return float(np.sqrt(probs @ (z - probs @ z) ** 2))


print("  v      sigma_min(v)  sigma_min(v)/v  max Sharpe at R_f = 1/v")
for v in (0.90, 0.95, 0.97, 1.00, 1.05):
    print(f"{v:5.2f}   {sigma_min(v):.6f}      {sigma_min(v) / v:.6f}        {max_sharpe(v):.6f}")
print(f"true SDF: mean {probs @ m_true:.6f}, s.d. {sd(m_true):.6f} >= sigma_min at its mean {sigma_min(0.97):.6f}")
v_star = float(mu @ np.linalg.solve(cov, p) / (mu @ np.linalg.solve(cov, mu)))
print(f"the mean with the smallest bound: v = {v_star:.6f}, sigma_min = {sigma_min(v_star):.6f}")
