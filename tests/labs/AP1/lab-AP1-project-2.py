import numpy as np
from numpy.typing import NDArray


def recover(
    train: NDArray[np.float64], test: NDArray[np.float64], prices: NDArray[np.float64]
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """Sample x* weights from `train`, and its pricing errors E[m x] - p on `train` and on `test`."""
    second = train.T @ train / len(train)
    b = np.linalg.solve(second, prices)
    in_errors = train.T @ (train @ b) / len(train) - prices
    out_errors = test.T @ (test @ b) / len(test) - prices
    return np.asarray(b, dtype=np.float64), in_errors, out_errors


# SIMULATED: 4 payoffs (one riskless) priced by a lognormal SDF; 120 training and 120 test months.
rng = np.random.default_rng(2)
shock = rng.standard_normal(240)
m = np.exp(-0.01 - 0.5 * 0.2**2 - 0.2 * shock)
x = np.column_stack([np.ones(240), 1.0 + np.outer(shock, [0.03, 0.06, 0.09]) + 0.1 * rng.standard_normal((240, 3))])
prices = np.array([np.exp(-0.01), *(x[:, 1:].T @ m / 240)])  # prices of the risky payoffs: their sample E[m x]
b, in_errors, out_errors = recover(x[:120], x[120:], prices)
print("weights:", np.round(b, 4))
print("max |in-sample error|:", f"{np.abs(in_errors).max():.1e}")
print("out-of-sample errors:", np.round(out_errors, 5))
