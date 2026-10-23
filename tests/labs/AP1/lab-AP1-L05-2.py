import numpy as np
from numpy.typing import NDArray

# Lab 1's SIMULATED market, rebuilt: 8 states, a riskless payoff and 3 risky payoffs priced by a positive SDF.
rng = np.random.default_rng(606)
probs = rng.dirichlet(np.full(8, 5.0))
m = np.exp(rng.normal(0.0, 0.3, 8))
m *= 0.98 / float(probs @ m)
risky = 1.0 + 0.25 * rng.standard_normal((8, 3))
X = np.column_stack([np.ones(8), risky])
p = X.T @ (probs * m)


def E(v: NDArray[np.float64]) -> float:  # noqa: N802  expectation under the state probabilities
    return float(probs @ v)


def cov(a: NDArray[np.float64], b: NDArray[np.float64]) -> float:
    return E(a * b) - E(a) * E(b)


x_star = X @ np.linalg.solve(X.T @ (probs[:, None] * X), p)
r_f = 1.0 / p[0]
R = risky / p[1:]
r_star = x_star / E(x_star**2)

# Theorem 5.1: E[R_i] - R_f = -R_f Cov(m, R_i) for ANY SDF m; and = beta_i (E[R*] - R_f) with beta on R*.
print("asset  E[R]-R_f   -R_f Cov(m,R)  -R_f Cov(x*,R)  beta_R*  beta_R*(E[R*]-R_f)")
for i in range(3):
    r = R[:, i]
    beta = cov(r, r_star) / cov(r_star, r_star)
    print(
        f"{i + 1:5d}  {E(r) - r_f:+.6f}  {-r_f * cov(m, r):+.6f}      {-r_f * cov(x_star, r):+.6f}       "
        f"{beta:+.4f}  {beta * (E(r_star) - r_f):+.6f}"
    )
# R* is on the lower (inefficient) part of the frontier: its mean is below R_f whenever x* is not constant.
print(f"E[R*] = {E(r_star):.6f} < R_f = {r_f:.6f}: {E(r_star) < r_f}")
