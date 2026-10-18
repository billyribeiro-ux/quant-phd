import math
from statistics import NormalDist

import numpy as np
from numpy.typing import NDArray

# SIMULATED daily excess returns throughout; each row is one independent sample.
rng = np.random.default_rng(4707)
phi, n_reps = NormalDist(), 4000


def centred(r: NDArray[np.float64]) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Per-row Sharpe ratio (ddof=1) and the deviations from the row mean, per period."""
    c = r - r.mean(axis=1, keepdims=True)
    return r.mean(axis=1) / np.sqrt((c**2).sum(axis=1) / (r.shape[1] - 1)), c


# Part 1. Theorem 5.1 against simulation. Two strategies share a crash shock:
# u_i = sqrt(p) e_0 + sqrt(1 - p) e_i, each e a mirrored standardized exponential
# (skewness -2, kurtosis 9), so corr(u_1, u_2) = p. True daily Sharpe ratios 0.1 and 0.05.
p, sr1, sr2, n_obs = 0.5, 0.1, 0.05, 1000
skew, kurt = -2.0 * (p**1.5 + (1 - p) ** 1.5), 9.0 * (p**2 + (1 - p) ** 2) + 6.0 * p * (1 - p)
k12, k22 = -2.0 * p**1.5, 1.0 + 8.0 * p**2  # E[u1 u2^2] = E[u1^2 u2], and E[u1^2 u2^2]
v1, v2 = (1.0 - skew * s + (kurt - 1.0) / 4.0 * s**2 for s in (sr1, sr2))
general = v1 + v2 - 2.0 * p + sr1 * k12 + sr2 * k12 - sr1 * sr2 * (k22 - 1.0) / 2.0
normal = 2.0 * (1.0 - p) + (sr1**2 + sr2**2) / 2.0 - sr1 * sr2 * p**2
e = -(rng.exponential(1.0, (3, n_reps, n_obs)) - 1.0)
diff = centred(sr1 + math.sqrt(p) * e[0] + math.sqrt(1 - p) * e[1])[0]
diff -= centred(sr2 + math.sqrt(p) * e[0] + math.sqrt(1 - p) * e[2])[0]
print("T*Var(SR1 - SR2): formula_(4)  formula_(5)  naive_V1+V2  simulated")
print(f"{general:.4f} {normal:.4f} {v1 + v2:.4f} {n_obs * diff.var(ddof=1):.4f}")

# Part 2. Size of the paired test (5) and of the naive test that treats the strategies as
# independent ((5) with rho = 0). Jointly normal returns, both true Sharpe ratios 0.05,
# three years of daily data; two-sided tests at 5%.
n_obs, crit = 756, phi.inv_cdf(0.975)
print("rho  rejection_rate_paired  rejection_rate_naive")
for rho in (-0.5, 0.0, 0.5, 0.9):
    x = rng.standard_normal((2, n_reps, n_obs))
    (s1, c1), (s2, c2) = centred(0.05 + x[0]), centred(0.05 + rho * x[0] + math.sqrt(1 - rho**2) * x[1])
    rho_hat = (c1 * c2).sum(axis=1) / np.sqrt((c1**2).sum(axis=1) * (c2**2).sum(axis=1))
    common = (s1**2 + s2**2) / 2.0
    paired = 2.0 * (1.0 - rho_hat) + common - s1 * s2 * rho_hat**2
    naive = 2.0 + common
    z_paired, z_naive = (np.abs(s1 - s2) * math.sqrt(n_obs - 1) / np.sqrt(v) for v in (paired, naive))
    print(f"{rho:.1f} {np.mean(z_paired > crit):.4f} {np.mean(z_naive > crit):.4f}")

# Part 3. MinTRL in repeated samples. True daily Sharpe ratio 0.09 with the crash shock of
# Part 1 (skewness -2, kurtosis 9), benchmark 0, alpha = 0.05. MinTRL from the true moments,
# and the length that gives the PSR test 80% power.
sr, z_a, z_b = 0.09, phi.inv_cdf(0.95), phi.inv_cdf(0.80)
bracket = 1.0 + 2.0 * sr + 2.0 * sr**2
print("length  T  median_PSR(0)  share_PSR(0)>=0.95")
for name, z in (("MinTRL", z_a), ("80%_power", z_a + z_b)):
    n_obs = math.ceil(1.0 + bracket * (z / sr) ** 2)
    s, c = centred(sr - (rng.exponential(1.0, (n_reps, n_obs)) - 1.0))
    m2, m3, m4 = (np.mean(c**k, axis=1) for k in (2, 3, 4))
    se = np.sqrt((1.0 - m3 / m2**1.5 * s + (m4 / m2**2 - 1.0) / 4.0 * s**2) / (n_obs - 1))
    psr = np.array([phi.cdf(v) for v in s / se])
    print(f"{name} {n_obs} {np.median(psr):.4f} {np.mean(psr >= 0.95):.4f}")
