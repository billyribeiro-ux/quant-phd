import math
from statistics import NormalDist

import numpy as np
from numpy.typing import NDArray


def probabilistic_sharpe_ratio(returns: NDArray[np.float64], sr_benchmark: float) -> float:
    """PSR of per-period excess returns against a per-period benchmark Sharpe ratio."""
    n = returns.size
    centred = returns - returns.mean()
    m2, m3, m4 = (float(np.mean(centred**k)) for k in (2, 3, 4))
    sr = float(returns.mean() / returns.std(ddof=1))
    skew, kurt = m3 / m2**1.5, m4 / m2**2
    bracket = 1 - skew * sr + (kurt - 1) / 4 * sr**2
    se = math.sqrt(bracket / (n - 1))
    return NormalDist().cdf((sr - sr_benchmark) / se)


rng = np.random.default_rng(3)
# SIMULATED daily excess returns with a negative-skew jump component.
crashes = (rng.random(1000) < 0.02) * rng.exponential(0.03, 1000)
r = rng.normal(0.0012, 0.01, 1000) - crashes
for bench in (0.0, 0.02, 0.05):
    print(f"PSR against {bench:.2f}: {probabilistic_sharpe_ratio(r, bench):.4f}")
