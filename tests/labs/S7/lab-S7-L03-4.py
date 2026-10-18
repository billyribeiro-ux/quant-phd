import math

import numpy as np
from numpy.typing import NDArray

# SIMULATED universes of N strategies, each with T daily returns of unit volatility. For iid normal returns the
# sample mean and variance are independent (normal, and chi-square over T - 1), so each Sharpe ratio is drawn
# exactly from those two instead of from T returns.
rng = np.random.default_rng(306)
N, T, P, q = 500, 1260, 252, 0.10
se = 1.0 / math.sqrt(T)  # per-period standard error of a Sharpe ratio near zero
annual = math.sqrt(P)
Vec = NDArray[np.float64]


def draw_truth(design: str) -> Vec:
    """True per-period Sharpe ratios: annualized N(0, 0.5^2), or 450 zeros and 50 skilled at N(1.0, 0.25^2)."""
    if design == "normal":
        return rng.normal(0.0, 0.5, N) / annual
    theta = np.zeros(N)
    theta[:50] = rng.normal(1.0, 0.25, 50) / annual
    return theta


def sample_sharpe(theta: Vec) -> Vec:
    mean = theta + rng.standard_normal(N) * se
    var = rng.chisquare(T - 1, N) / (T - 1)
    return np.asarray(mean / np.sqrt(var), dtype=np.float64)


def normal_pdf(x: Vec) -> Vec:
    return np.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def upper_tail(x: float) -> float:
    return 0.5 * math.erfc(x / math.sqrt(2.0))


def analyse(x: Vec) -> dict[str, Vec]:
    """Empirical Bayes in one universe: estimated lfdr, normal-prior (linear) shrinkage and Tweedie's formula."""
    z = x / se
    pi0_hat = min(1.0, float(np.mean(z < 0.0)) / 0.5)  # Storey's estimator at lambda = 0.5: p > 0.5 iff z < 0
    h = 1.06 * float(z.std(ddof=1)) * N**-0.2  # Gaussian kernel density estimate of f, Silverman's bandwidth
    u = (z[:, None] - z[None, :]) / h
    f = normal_pdf(u).mean(axis=1) / h
    f_prime = (-u * normal_pdf(u)).mean(axis=1) / h**2
    mu, tau2 = float(x.mean()), max(0.0, float(x.var(ddof=1)) - se**2)
    b = tau2 / (tau2 + se**2)
    return {
        "lfdr": np.minimum(1.0, pi0_hat * normal_pdf(z) / f),
        "linear": mu + b * (x - mu),
        "tweedie": (z + f_prime / f) * se,
        "pi0, B": np.array([pi0_hat, b]),
    }


# The two-group design's true z-densities: nulls N(0, 1), skilled N(m1, 1 + v1), with z = SR_hat / se.
m1, v1 = math.sqrt(T / P) * 1.0, (T / P) * 0.25**2


def true_lfdr(z: Vec) -> Vec:
    f1 = normal_pdf((z - m1) / math.sqrt(1.0 + v1)) / math.sqrt(1.0 + v1)
    return 0.9 * normal_pdf(z) / (0.9 * normal_pdf(z) + 0.1 * f1)


theta = draw_truth("two-group")
x = sample_sharpe(theta)
est = analyse(x)
lfdr_true = true_lfdr(x / se)
order = np.argsort(-x)
p = np.array([upper_tail(v) for v in x[order] / se])
k_bh = int(np.max(np.nonzero(p <= q * np.arange(1, N + 1) / N)[0], initial=-1)) + 1
last = order[k_bh - 1]
print(f"one universe: pi0_hat {est['pi0, B'][0]:.3f} (true 0.900), shrinkage factor B {est['pi0, B'][1]:.3f}")
print(f"BH at q = {q:.2f}: {k_bh} rejections, {int(np.sum(theta[order[:k_bh]] == 0.0))} of them null")
print(f"last BH rejection: z {x[last] / se:.3f}  lfdr_hat {est['lfdr'][last]:.3f}  lfdr_true {lfdr_true[last]:.3f}")
print("rank  raw_SR  linear_SR  tweedie_SR  true_SR  lfdr_hat  lfdr_true  (annualized Sharpe ratios)")
for rank, n in enumerate(order[:3], start=1):
    sharpes = " ".join(f"{v * annual:.3f}" for v in (x[n], est["linear"][n], est["tweedie"][n], theta[n]))
    print(rank, sharpes, f"{est['lfdr'][n]:.3f} {lfdr_true[n]:.3f}")

# 200 universes per design: the top-ranked strategy's bias, and (two-group) the pooled tails behind Proposition 7.3.
n_reps = 200
bias: dict[str, list[float]] = {}
pooled_z, pooled_null = [], []
for design in ("normal", "two-group"):
    for _ in range(n_reps):
        theta = draw_truth(design)
        x = sample_sharpe(theta)
        est = analyse(x)
        top = int(np.argmax(x))
        for name, value in (("raw", x[top]), ("linear", est["linear"][top]), ("tweedie", est["tweedie"][top])):
            bias.setdefault(f"{design} {name}", []).append(float(value - theta[top]) * annual)
        if design == "two-group":
            pooled_z.append(x / se)
            pooled_null.append(theta == 0.0)
z_all, null_all = np.concatenate(pooled_z), np.concatenate(pooled_null)
print("c  Fdr(c)  mean_true_lfdr_on_tail  null_share_of_tail")
for c in (2.0, 3.0):
    s0, s1 = upper_tail(c), upper_tail((c - m1) / math.sqrt(1.0 + v1))
    fdr, tail = 0.9 * s0 / (0.9 * s0 + 0.1 * s1), z_all >= c
    print(f"{c:.1f} {fdr:.4f} {true_lfdr(z_all[tail]).mean():.4f} {null_all[tail].mean():.4f}")
print("design  bias_raw  bias_linear  bias_tweedie  (top-ranked strategy, annualized; mean over 200 universes, with")
print("        its Monte Carlo standard error in brackets)")
for design in ("normal", "two-group"):
    cells = [np.array(bias[f"{design} {name}"]) for name in ("raw", "linear", "tweedie")]
    print(design, " ".join(f"{b.mean():.3f} ({b.std(ddof=1) / math.sqrt(n_reps):.3f})" for b in cells))
