import numpy as np
from numpy.typing import NDArray
from scipy.optimize import linprog  # type: ignore[import-untyped]

# The three-state market of Lesson 1: a bond paying 1 and a stock. Illustrative numbers.
X = np.array([[1.0, 1.4], [1.0, 1.1], [1.0, 0.6]])
bond_price = 0.96


def strictly_positive_state_prices(prices: NDArray[np.float64]) -> tuple[float, NDArray[np.float64]]:
    """Largest t such that some psi >= t (componentwise, t <= 1) solves X' psi = prices; returns (t, psi).

    Theorem 3.1: no arbitrage holds exactly when the optimum t is strictly positive.
    """
    n_states = X.shape[0]
    c = np.zeros(n_states + 1)
    c[-1] = -1.0  # maximize t
    a_eq = np.hstack([X.T, np.zeros((X.shape[1], 1))])
    a_ub = np.hstack([-np.eye(n_states), np.ones((n_states, 1))])  # t - psi_s <= 0
    bounds = [(None, None)] * n_states + [(None, 1.0)]
    res = linprog(c, A_ub=a_ub, b_ub=np.zeros(n_states), A_eq=a_eq, b_eq=prices, bounds=bounds, method="highs")
    return float(res.x[-1]), np.asarray(res.x[:-1])


print("stock price   max min-state-price   no arbitrage?")
for stock_price in (0.50, 0.576, 0.976, 1.344, 1.40):
    t, psi = strictly_positive_state_prices(np.array([bond_price, stock_price]))
    print(f"{stock_price:11.3f}   {t:+.6f}            {t > 1e-12}")
print(f"open interval of arbitrage-free stock prices: ({0.6 * bond_price:.3f}, {1.4 * bond_price:.3f})")
