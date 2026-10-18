import math
from statistics import NormalDist

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


def means(phi: float) -> dict[str, float]:
    """Means, in units of gamma(0), of T Var(mean) and of both long-run variance estimates.

    Each estimate is a quadratic form u'Ku / T in the demeaned series u = Mx, so its exact mean is
    sum_ij K_ij (M R M)_ij / T, with R the AR(1) autocorrelation matrix and M = I - 11'/T. The
    "plain" means are the page's first approximations: every sample autocovariance replaced by gamma(h).
    """
    gap = np.abs(np.subtract.outer(np.arange(T), np.arange(T)))
    r = phi**gap
    m = np.eye(T) - 1.0 / T
    mrm = m @ r @ m
    k_nw = np.where(gap <= lag, 1.0 - gap / (lag + 1), 0.0)  # Bartlett weights on both sides of the diagonal
    lead = np.subtract.outer(np.arange(T), np.arange(T)) % T  # circular lag (j - i) mod T, as k and T - k
    h = np.arange(1, T)
    w = np.concatenate([[0.5], (1.0 - h / T) * (1.0 - 1.0 / mean_block) ** h])
    k_sb = w[lead] + w[(T - lead) % T]  # 1 on the diagonal, w_k + w_{T-k} off it
    j = np.arange(1, lag + 1)
    return {
        "target": float(r.sum()) / T,
        "nw weights": float(k_nw[0].sum() + k_nw[0, 1:].sum()),
        "sb weights": float(k_sb[0].sum()),
        "nw plain": 1.0 + 2.0 * float(np.sum((1.0 - j / (lag + 1)) * phi**j)),
        "sb plain": 1.0 + 2.0 * float(np.sum(w[1:] * phi**h)),
        "nw exact": float(np.sum(k_nw * mrm)) / T,
        "sb exact": float(np.sum(k_sb * mrm)) / T,
    }


def bias_only_size(mean_ratio: float) -> float:
    """Two-sided size of a normal test whose variance estimate equals mean_ratio times the true variance."""
    return 2.0 * (1.0 - NormalDist().cdf(z_crit * math.sqrt(mean_ratio)))


null_se = math.sqrt(0.05 * 0.95 / n_reps)
print("phi  naive_t  sign_flip  diebold_mariano_nw  stationary_bootstrap_var  (rejection rates at 5%)")
rates: dict[float, Vec] = {}
simulated: dict[float, tuple[float, float]] = {}
for phi in (0.0, 0.5):
    rejections, nw_total, sb_total = np.zeros(4), 0.0, 0.0
    for _ in range(n_reps):
        d = ar1(phi)
        total = abs(float(d.sum()))
        signs = rng.choice(np.array([-1.0, 1.0]), size=(n_flips, T))
        p_flip = (1 + int(np.sum(np.abs(signs @ d) >= total))) / (n_flips + 1)
        nw, sb = newey_west(d), stationary_bootstrap_var(d)
        nw_total, sb_total = nw_total + nw, sb_total + T * sb
        rejections += [
            abs(d.mean()) / (d.std(ddof=1) / np.sqrt(T)) > z_crit,
            p_flip <= 0.05,
            abs(d.mean()) / np.sqrt(nw / T) > z_crit,
            abs(d.mean()) / np.sqrt(sb) > z_crit,
        ]
    rates[phi] = rejections / n_reps
    gamma0 = 1.0 / (1.0 - phi**2)
    simulated[phi] = (nw_total / n_reps / gamma0, sb_total / n_reps / gamma0)
    print(f"{phi:.1f} " + " ".join(f"{r:.3f}" for r in rates[phi]))

print(f"rates in standard errors from 5% (standard error of a 5% rate over {n_reps} series: {null_se:.5f})")
for phi in (0.0, 0.5):
    print(f"{phi:.1f} " + " ".join(f"{(r - 0.05) / null_se:.2f}" for r in rates[phi]))
print("phi  estimate  weight_sum  T_var_mean  mean_ignoring_demeaning  exact_mean  simulated_mean")
print("     size_ignoring_demeaning  size_at_exact_mean  (variances in units of gamma(0))")
for phi in (0.0, 0.5):
    mean = means(phi)
    for name, sim in zip(("nw", "sb"), simulated[phi], strict=True):
        plain, exact = mean[f"{name} plain"], mean[f"{name} exact"]
        cells = (mean[f"{name} weights"], mean["target"], plain, exact, sim)
        sizes = (bias_only_size(plain / mean["target"]), bias_only_size(exact / mean["target"]))
        print(f"{phi:.1f} {name} " + " ".join(f"{v:.3f}" for v in cells) + "  " + " ".join(f"{v:.3f}" for v in sizes))
