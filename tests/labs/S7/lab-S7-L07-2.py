import math
from statistics import NormalDist

import numpy as np
from numpy.typing import NDArray

# SIMULATED: one proposed strategy (true daily Sharpe ratio 0.06, skewness -2) chosen
# from N trials; the other N - 1 trials are skill-free. Five years of daily data.
rng = np.random.default_rng(2707)
phi, gamma_e, n_obs = NormalDist(), 0.5772156649015329, 1260


def moments(r: NDArray[np.float64]) -> tuple[float, float, float]:
    """Sharpe ratio (ddof=1), skewness and kurtosis (moment estimators), per period."""
    c = r - r.mean()
    m2, m3, m4 = (float(np.mean(c**k)) for k in (2, 3, 4))
    return float(r.mean() / r.std(ddof=1)), m3 / m2**1.5, m4 / m2**2


def psr(r: NDArray[np.float64], benchmark: float) -> float:
    """Probability that the true Sharpe ratio exceeds `benchmark` (per-period units)."""
    sr, g3, g4 = moments(r)
    se = math.sqrt((1.0 - g3 * sr + (g4 - 1.0) / 4.0 * sr**2) / (r.size - 1))
    return phi.cdf((sr - benchmark) / se)


def expected_max_z(n: int) -> float:
    return (1 - gamma_e) * phi.inv_cdf(1 - 1 / n) + gamma_e * phi.inv_cdf(1 - 1 / (n * math.e))


selected = 0.01 * (0.06 - (rng.exponential(1.0, n_obs) - 1.0))
sr, g3, g4 = moments(selected)
print(f"selected: annualized SR {sr * math.sqrt(252):.3f}, skewness {g3:.3f}, kurtosis {g4:.3f}")
print(f"PSR against zero: {psr(selected, 0.0):.4f}")
print("N  SR0_annualized  DSR")
for n in (2, 10, 100, 1000):
    nulls = rng.standard_normal((n_obs, n - 1))
    trial_sr = np.append(nulls.mean(axis=0) / nulls.std(axis=0, ddof=1), sr)
    sr0 = math.sqrt(float(np.var(trial_sr, ddof=1))) * expected_max_z(n)
    print(f"{n} {sr0 * math.sqrt(252):.3f} {psr(selected, sr0):.4f}")
