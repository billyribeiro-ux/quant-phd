import numpy as np
from numpy.typing import NDArray

# SIMULATED null loss differentials: AR(1) with unit-variance shocks and mean zero. Four two-sided 5% tests of
# equal predictive accuracy, each on the same series.
rng = np.random.default_rng(4041)
T, n_reps, n_flips, lag, mean_block, z_crit = 500, 2000, 499, 7, 20.0, 1.959964
Vec = NDArray[np.float64]


def ar1(phi: float) -> Vec:
    e = rng.standard_normal(T + 200)
    x = np.empty_like(e)
    x[0] = e[0]
    for t in range(1, e.size):
        x[t] = phi * x[t - 1] + e[t]
    return x[200:]  # drop the burn-in so the path starts near stationarity


def newey_west(d: Vec) -> float:
    """Bartlett-weighted long-run variance: gamma(0) + 2 sum_j (1 - j/(lag + 1)) gamma(j), divisor T."""
    u = d - d.mean()
    gamma = [float(u[j:] @ u[: T - j]) / T for j in range(lag + 1)]
    return gamma[0] + 2.0 * sum((1.0 - j / (lag + 1)) * gamma[j] for j in range(1, lag + 1))


def stationary_bootstrap_var(d: Vec) -> float:
    """Theorem 3.3: the exact stationary-bootstrap variance of the mean, from circular autocovariances."""
    u = d - d.mean()
    c = np.fft.irfft(np.abs(np.fft.rfft(u)) ** 2, n=T) / T  # c[h] = (1/T) sum_i u_i u_{(i+h) mod T}
    h = np.arange(1, T)
    return float(c[0] + 2.0 * np.sum((1.0 - h / T) * (1.0 - 1.0 / mean_block) ** h * c[1:])) / T


print("phi  naive_t  sign_flip  diebold_mariano_nw  stationary_bootstrap_var  (rejection rates at 5%)")
for phi in (0.0, 0.5):
    rejections = np.zeros(4)
    for _ in range(n_reps):
        d = ar1(phi)
        total = abs(float(d.sum()))
        signs = rng.choice(np.array([-1.0, 1.0]), size=(n_flips, T))
        p_flip = (1 + int(np.sum(np.abs(signs @ d) >= total))) / (n_flips + 1)
        rejections += [
            abs(d.mean()) / (d.std(ddof=1) / np.sqrt(T)) > z_crit,
            p_flip <= 0.05,
            abs(d.mean()) / np.sqrt(newey_west(d) / T) > z_crit,
            abs(d.mean()) / np.sqrt(stationary_bootstrap_var(d)) > z_crit,
        ]
    print(f"{phi:.1f} " + " ".join(f"{r / n_reps:.3f}" for r in rejections))
