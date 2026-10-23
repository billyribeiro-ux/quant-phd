import numpy as np
from numpy.typing import NDArray
from scipy.optimize import linprog  # type: ignore[import-untyped]


def detect_arbitrage(payoffs: NDArray[np.float64], prices: NDArray[np.float64]) -> tuple[float, NDArray[np.float64]]:
    """Definition 2.1's linear program: max 1'X theta - p'theta s.t. X theta >= 0, p'theta <= 0,
    X theta <= 1, -p'theta <= 1. Returns (optimal value, optimal theta); the value is positive iff arbitrage."""
    n_states, n_assets = payoffs.shape
    a_ub = np.vstack([-payoffs, prices[None, :], payoffs, -prices[None, :]])
    b_ub = np.concatenate([np.zeros(n_states), [0.0], np.ones(n_states), [1.0]])
    c = -(payoffs.sum(axis=0) - prices)  # linprog minimizes
    res = linprog(c, A_ub=a_ub, b_ub=b_ub, bounds=[(None, None)] * n_assets, method="highs")
    return float(-res.fun), np.asarray(res.x)


def state_price_margin(payoffs: NDArray[np.float64], prices: NDArray[np.float64]) -> float:
    """Largest t <= 1 such that some psi >= t solves X'psi = p; positive iff strictly positive state prices exist."""
    n_states = payoffs.shape[0]
    c = np.zeros(n_states + 1)
    c[-1] = -1.0
    a_eq = np.hstack([payoffs.T, np.zeros((payoffs.shape[1], 1))])
    a_ub = np.hstack([-np.eye(n_states), np.ones((n_states, 1))])
    bounds = [(None, None)] * n_states + [(None, 1.0)]
    res = linprog(c, A_ub=a_ub, b_ub=np.zeros(n_states), A_eq=a_eq, b_eq=prices, bounds=bounds, method="highs")
    return float(res.x[-1]) if res.status == 0 else float("-inf")


# SIMULATED market: 12 states, 6 assets, priced by strictly positive state prices; then one price is shaded.
rng = np.random.default_rng(303)
X = 1.0 + 0.3 * rng.standard_normal((12, 6))
psi = rng.uniform(0.02, 0.14, 12)
fair = X.T @ psi
print("asset prices from psi >> 0:", np.round(fair, 4))

# The lowest arbitrage-free price of asset 4 given the other five: min psi'x_4 over psi >= 0 pricing the others.
others = [0, 1, 2, 4, 5]
res = linprog(X[:, 3], A_eq=X[:, others].T, b_eq=fair[others], bounds=[(0, None)] * 12, method="highs")
print(f"lowest arbitrage-free price of asset 4: {res.fun:.4f}, i.e. a shade of {fair[3] - res.fun:.4f}")

for shade in (0.0, 0.10, 0.20, 0.30):
    p = fair.copy()
    p[3] -= shade  # asset 4 quoted below its state-price value
    value, theta = detect_arbitrage(X, p)
    margin = state_price_margin(X, p)
    verdict = "arbitrage" if value > 1e-9 else "no arbitrage"
    print(f"shade {shade:.2f}: LP value {round(value, 6) + 0.0:.6f}, state-price margin {margin:+.6f} -> {verdict}")
