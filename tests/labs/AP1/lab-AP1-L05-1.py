import numpy as np
from numpy.typing import NDArray

# SIMULATED market: 8 states, a riskless payoff and 3 risky payoffs, priced by a strictly positive SDF m.
rng = np.random.default_rng(606)
probs = rng.dirichlet(np.full(8, 5.0))
m = np.exp(rng.normal(0.0, 0.3, 8))
m *= 0.98 / float(probs @ m)  # scale so that E[m] = 0.98: a riskless rate of about 2% for the period
risky = 1.0 + 0.25 * rng.standard_normal((8, 3))
X = np.column_stack([np.ones(8), risky])
p = X.T @ (probs * m)


def E(v: NDArray[np.float64]) -> float:  # noqa: N802  expectation under the state probabilities
    return float(probs @ v)


x_star = X @ np.linalg.solve(X.T @ (probs[:, None] * X), p)
r_f = 1.0 / p[0]
R = risky / p[1:]  # gross returns of the risky assets
Re = R - r_f  # excess returns
print(f"R_f = {r_f:.6f}, E[x*] = {E(x_star):.6f} = 1/R_f: {np.isclose(E(x_star), 1 / r_f)}")

# R* = x*/p(x*) with p(x*) = E[x*^2]; it is the gross return with the smallest second moment (Theorem 3.2).
r_star = x_star / E(x_star**2)
print(f"E[R*^2] = {E(r_star**2):.6f}; 1/E[x*^2] = {1 / E(x_star**2):.6f}; E[R*] = {E(r_star):.6f} <= R_f")
for w in rng.dirichlet(np.ones(3), size=3):
    other = R @ w
    print(f"  another return: E[R^2] = {E(other**2):.6f} >= E[R*^2]: {E(other**2) >= E(r_star**2)}")

# R^e* = projection of 1 on the excess returns; mean-variance frontier = {R* + w R^e*} (Theorem 3.5).
g = np.linalg.solve(Re.T @ (probs[:, None] * Re), Re.T @ probs)
re_star = Re @ g
mu = Re.T @ probs
cov = Re.T @ (probs[:, None] * Re) - np.outer(mu, mu)
max_sr = float(np.sqrt(mu @ np.linalg.solve(cov, mu)))
print(f"E[R^e*] = {E(re_star):.6f} = E[R^e*^2] = {E(re_star**2):.6f}")
print(f"maximum Sharpe ratio of the excess returns: {max_sr:.6f}")
for w in (-2.0, 0.0, 2.0):
    frontier = r_star + w * re_star
    sd = float(np.sqrt(E(frontier**2) - E(frontier) ** 2))
    print(f"  w = {w:+.1f}: E[R] = {E(frontier):.6f}, s.d. {sd:.6f}, |SR| = {abs(E(frontier) - r_f) / sd:.6f}")

# The variance bound (Theorem 4.4): sigma(m) / E(m) >= max Sharpe ratio, with equality for x* (in span{1, x}).
for name, sdf in (("true m", m), ("x*", x_star)):
    print(f"{name}: sigma/E = {np.sqrt(E(sdf**2) - E(sdf) ** 2) / E(sdf):.6f}")
