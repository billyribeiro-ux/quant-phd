import numpy as np

# SIMULATED one-period market: 6 states, 3 traded payoffs, priced by a strictly positive SDF m.
rng = np.random.default_rng(505)
probs = rng.dirichlet(np.full(6, 4.0))
m = np.exp(rng.normal(-0.03, 0.25, 6))  # the SDF that generated the prices (unknown to the analyst)
X = np.column_stack([np.ones(6), 1.0 + 0.2 * rng.standard_normal(6), 1.0 + 0.5 * rng.standard_normal(6)])
p = X.T @ (probs * m)  # p = E[m x], one price per payoff
print("state probabilities:", np.round(probs, 4))
print("prices p = E[m x]:  ", np.round(p, 6))

# x* = x' b with E[x x'] b = p: the unique SDF in the payoff space (Theorem 3.2).
second = X.T @ (probs[:, None] * X)  # E[x x'] under the state probabilities
b = np.linalg.solve(second, p)
x_star = X @ b
print("x* by state:        ", np.round(x_star, 6))
print("E[x* x] - p:        ", np.round(X.T @ (probs * x_star) - p, 12) + 0.0)

# m - x* is orthogonal to every payoff, so x* is the projection of m on the payoff space (Theorem 4.1).
eps = m - x_star
print("E[(m - x*) x]:      ", np.round(X.T @ (probs * eps), 12) + 0.0)
print(f"E[m^2] = {probs @ m**2:.6f} = E[x*^2] + E[eps^2] = {probs @ x_star**2:.6f} + {probs @ eps**2:.6f}")

# Any other SDF is x* plus a noise orthogonal to the payoffs; build one from a random vector.
z = rng.standard_normal(6)
coef = np.linalg.solve(second, X.T @ (probs * z))
other = x_star + (z - X @ coef)
print(
    "another SDF prices the payoffs:",
    bool(np.allclose(X.T @ (probs * other), p)),
    "| min value:",
    round(float(other.min()), 4),
)
