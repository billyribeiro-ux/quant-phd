"""Lab FC3-project-3: Project Rung 3 reference verification check on Seed 0.

SIMULATED 40-fund universe with T=60 months generated from Seed 0.
Compares naive chance counting against bootstrap maximum-t skill recovery.
"""

from __future__ import annotations

import math
import random


def make_instance(seed: int) -> dict[str, object]:
    """Generate simulated fund returns and market factor."""
    rng = random.Random(seed)
    n_funds = 40
    n_months = 60
    mu_f = 0.007
    sigma_f = 0.045
    factor = [rng.gauss(mu_f, sigma_f) for _ in range(n_months)]
    mean_f = sum(factor) / n_months
    s_ff = sum((ft - mean_f) ** 2 for ft in factor)
    sigma_eps = 0.020
    expected_se = sigma_eps * math.sqrt(1.0 / n_months + (mean_f**2) / s_ff)
    num_skilled = rng.randint(3, 5)
    planted_skill = sorted(rng.sample(range(n_funds), num_skilled))
    planted_alpha = [0.0] * n_funds
    for idx in planted_skill:
        planted_alpha[idx] = expected_se * (6.5 + 1.2 * rng.random())
    returns: list[list[float]] = []
    for i in range(n_funds):
        beta = 0.8 + 0.4 * rng.random()
        alpha = planted_alpha[i]
        r_i = [alpha + beta * factor[t] + rng.gauss(0.0, sigma_eps) for t in range(n_months)]
        returns.append(r_i)
    return {
        "returns": returns,
        "factor": factor,
        "planted_skill": planted_skill,
        "planted_alpha": planted_alpha,
    }


def alpha_and_t(returns: list[float], factor: list[float]) -> tuple[float, float]:
    """Compute OLS alpha and t-statistic."""
    n_months = len(returns)
    mean_f = sum(factor) / n_months
    mean_r = sum(returns) / n_months
    s_ff = sum((f - mean_f) ** 2 for f in factor)
    s_fr = sum((factor[t] - mean_f) * (returns[t] - mean_r) for t in range(n_months))
    beta = s_fr / s_ff
    alpha = mean_r - beta * mean_f
    rss = sum((returns[t] - (alpha + beta * factor[t])) ** 2 for t in range(n_months))
    s2 = rss / (n_months - 2)
    var_a = s2 * (1.0 / n_months + (mean_f**2) / s_ff)
    se_a = math.sqrt(var_a)
    t_stat = alpha / se_a
    return alpha, t_stat


def bootstrap_skilled_set(
    returns: list[list[float]],
    factor: list[float],
    level: float,
    n_boot: int,
    seed: int,
) -> list[int]:
    """Identify skilled funds via bootstrap maximum-t threshold."""
    n_funds = len(returns)
    n_months = len(factor)
    mean_f = sum(factor) / n_months
    s_ff = sum((f - mean_f) ** 2 for f in factor)
    slopes: list[float] = [0.0] * n_funds
    residuals: list[list[float]] = []
    observed_t: list[float] = [0.0] * n_funds
    for i in range(n_funds):
        alpha_i, t_i = alpha_and_t(returns[i], factor)
        mean_r_i = sum(returns[i]) / n_months
        s_fr_i = sum((factor[t] - mean_f) * (returns[i][t] - mean_r_i) for t in range(n_months))
        beta_i = s_fr_i / s_ff
        e_i = [returns[i][t] - (alpha_i + beta_i * factor[t]) for t in range(n_months)]
        slopes[i] = beta_i
        residuals.append(e_i)
        observed_t[i] = t_i
    rng = random.Random(seed)
    max_t_boot: list[float] = [0.0] * n_boot
    for k in range(n_boot):
        tau = [rng.randrange(n_months) for _ in range(n_months)]
        m_k = -1e9
        for i in range(n_funds):
            r_null = [slopes[i] * factor[t] + residuals[i][tau[t]] for t in range(n_months)]
            _, t_boot = alpha_and_t(r_null, factor)
            if t_boot > m_k:
                m_k = t_boot
        max_t_boot[k] = m_k
    max_t_boot.sort()
    idx = math.ceil((1.0 - level) * n_boot) - 1
    idx = max(0, min(n_boot - 1, idx))
    threshold = max_t_boot[idx]
    return [i for i in range(n_funds) if observed_t[i] > threshold]


def main() -> None:
    """Run Seed 0 instance analysis and display results."""
    inst = make_instance(0)
    returns = inst["returns"]
    assert isinstance(returns, list)
    factor = inst["factor"]
    assert isinstance(factor, list)
    planted = inst["planted_skill"]
    assert isinstance(planted, list)

    n_funds = len(returns)
    t_stats = [alpha_and_t(returns[i], factor)[1] for i in range(n_funds)]

    crit = 1.644854
    naive = [i for i, t in enumerate(t_stats) if t > crit]
    boot = bootstrap_skilled_set(returns, factor, level=0.05, n_boot=200, seed=1000)

    print("Universe: N=40 funds, T=60 months (SIMULATED Seed 0)")
    print(f"Planted skilled funds ({len(planted)}): {planted}")
    print(f"Naive significant funds at 5% ({len(naive)}): {naive}")
    print(f"Expected false positives under null: {n_funds * 0.05:.1f}")
    false_pos_naive = sorted(set(naive) - set(planted))
    print(f"Naive false discoveries (zero-skill funds): {false_pos_naive}")
    print(f"Bootstrap recovered skilled funds ({len(boot)}): {boot}")
    false_pos_boot = sorted(set(boot) - set(planted))
    false_neg_boot = sorted(set(planted) - set(boot))
    print(f"Bootstrap false discoveries: {false_pos_boot}")
    print(f"Bootstrap false negatives: {false_neg_boot}")
    print(f"Exact recovery achieved: {boot == planted}")


main()
