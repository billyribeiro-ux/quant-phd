import numpy as np
from scipy.optimize import linprog  # type: ignore[import-untyped]

# Problem E1: Lab 1's SIMULATED market; for each asset, its arbitrage-free price range given the other five.
rng = np.random.default_rng(303)
X = 1.0 + 0.3 * rng.standard_normal((12, 6))
psi = rng.uniform(0.02, 0.14, 12)
fair = X.T @ psi
print("asset  fair     lowest   highest  width   residual s.d. on the others")
for n in range(6):
    others = [k for k in range(6) if k != n]
    a_eq, b_eq = X[:, others].T, fair[others]
    lo = linprog(X[:, n], A_eq=a_eq, b_eq=b_eq, bounds=[(0, None)] * 12, method="highs").fun
    hi = -linprog(-X[:, n], A_eq=a_eq, b_eq=b_eq, bounds=[(0, None)] * 12, method="highs").fun
    coef, *_ = np.linalg.lstsq(X[:, others], X[:, n], rcond=None)
    resid = X[:, n] - X[:, others] @ coef
    print(f"{n + 1:5d}  {fair[n]:.4f}  {lo:.4f}   {hi:.4f}   {hi - lo:.4f}  {resid.std():.4f}")
