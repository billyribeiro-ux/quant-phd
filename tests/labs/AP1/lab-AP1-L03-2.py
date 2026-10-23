import numpy as np
from scipy.optimize import linprog  # type: ignore[import-untyped]

# Arbitrage bounds on a new payoff z: the primal (cheapest super-replication, dearest sub-replication) and the
# dual (extreme state-price values psi'z over psi >= 0 with X'psi = p) give the same numbers (Theorem 4.1).
X = np.array([[1.0, 1.4], [1.0, 1.1], [1.0, 0.6]])  # bond and stock, Lesson 1's three states
p = np.array([0.96, 0.976])
z = np.maximum(X[:, 1] - 1.0, 0.0)  # a call on the stock struck at 1
print("call payoff by state:", z)

free = [(None, None)] * 2
upper = linprog(p, A_ub=-X, b_ub=-z, bounds=free, method="highs")  # min p'theta s.t. X theta >= z
lower = linprog(-p, A_ub=X, b_ub=z, bounds=free, method="highs")  # max p'theta s.t. X theta <= z
print(f"super-replication: cost {upper.fun:.4f}, portfolio {np.round(upper.x, 4)}")
print(f"sub-replication:   value {-lower.fun:.4f}, portfolio {np.round(lower.x, 4)}")

nonneg = [(0, None)] * 3
dual_hi = linprog(-z, A_eq=X.T, b_eq=p, bounds=nonneg, method="highs")
dual_lo = linprog(z, A_eq=X.T, b_eq=p, bounds=nonneg, method="highs")
print(f"max psi'z over psi >= 0 pricing X: {-dual_hi.fun:.4f} at psi = {np.round(dual_hi.x, 4)}")
print(f"min psi'z over psi >= 0 pricing X: {dual_lo.fun:.4f} at psi = {np.round(dual_lo.x, 4)}")

# Any price strictly inside the interval admits strictly positive state prices; a price at an end does not.
for quote in (0.08, 0.14, 0.20):
    a_eq = np.vstack([X.T, z])
    b_eq = np.append(p, quote)
    c = np.zeros(4)
    c[-1] = -1.0
    a_ub = np.hstack([-np.eye(3), np.ones((3, 1))])
    res = linprog(
        c,
        A_ub=a_ub,
        b_ub=np.zeros(3),
        A_eq=np.hstack([a_eq, np.zeros((3, 1))]),
        b_eq=b_eq,
        bounds=[(None, None)] * 3 + [(None, 1.0)],
        method="highs",
    )
    print(f"call quoted at {quote:.2f}: largest smallest-state-price {round(float(res.x[-1]), 6) + 0.0:+.6f}")
