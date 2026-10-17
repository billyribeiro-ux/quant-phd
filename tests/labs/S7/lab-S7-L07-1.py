import numpy as np

# SIMULATED returns r = mu + sigma * Z with Z standardized exponential (skewness 2,
# kurtosis 9) or its mirror image (skewness -2, kurtosis 9), daily Sharpe ratio 0.1.
rng = np.random.default_rng(707)
n_obs, n_reps, sr = 1000, 10000, 0.1


def simulated_scaled_variance(sign: float) -> float:
    """Monte Carlo estimate of T * Var(estimated Sharpe ratio), per-period units."""
    z = sign * (rng.exponential(1.0, (n_reps, n_obs)) - 1.0)
    r = sr + z  # mu / sigma = sr with sigma = 1; the Sharpe ratio is scale-free
    estimates = r.mean(axis=1) / r.std(axis=1, ddof=1)
    return float(n_obs * estimates.var(ddof=1))


print("skewness  kurtosis  normal_formula  nonnormal_formula  simulated")
for skew, sign in ((2.0, 1.0), (-2.0, -1.0)):
    kurt = 9.0
    normal = 1.0 + sr**2 / 2.0
    nonnormal = 1.0 - skew * sr + (kurt - 1.0) / 4.0 * sr**2
    print(f"{skew:.0f} {kurt:.0f} {normal:.4f} {nonnormal:.4f} {simulated_scaled_variance(sign):.4f}")
