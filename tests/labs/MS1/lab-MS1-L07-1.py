"""Lab MS1-L07-1: Probability of informed trading (PIN) and mixture likelihood.

SIMULATED: generates daily trade arrival counts from the Easley et al. (1996) mixture model.
Verifies that the mixture likelihood sums to unity over a truncated support,
and performs grid maximum-likelihood estimation of the event probability and informed arrival rate.
"""

from __future__ import annotations

import math
import random


def poisson_pmf(k: int, lam: float) -> float:
    """Compute Poisson probability mass function at k with arrival rate lam."""
    if k < 0:
        return 0.0
    return math.exp(-lam + k * math.log(lam) - math.lgamma(k + 1))


def pin_day_pmf(b: int, s: int, alpha: float, delta: float, mu: float, eps_b: float, eps_s: float) -> float:
    """Evaluate mixture joint probability mass function of (B, S) arrivals on one trading day."""
    p_no_event = (1.0 - alpha) * poisson_pmf(b, eps_b) * poisson_pmf(s, eps_s)
    p_good_news = alpha * (1.0 - delta) * poisson_pmf(b, eps_b + mu) * poisson_pmf(s, eps_s)
    p_bad_news = alpha * delta * poisson_pmf(b, eps_b) * poisson_pmf(s, eps_s + mu)
    return p_no_event + p_good_news + p_bad_news


def check_truncated_sum(
    alpha: float, delta: float, mu: float, eps_b: float, eps_s: float, max_count: int = 60
) -> float:
    """Verify that the discrete joint probability sums to 1 over truncated support."""
    total = 0.0
    for b in range(max_count):
        for s in range(max_count):
            total += pin_day_pmf(b, s, alpha, delta, mu, eps_b, eps_s)
    return total


def simulate_pin_days(
    n_days: int,
    alpha: float,
    delta: float,
    mu: float,
    eps_b: float,
    eps_s: float,
    seed: int = 42,
) -> list[tuple[int, int]]:
    """Simulate daily buy and sell counts under the PIN arrival structure."""
    rng = random.Random(seed)

    def sample_poisson(lam: float) -> int:
        l_val = math.exp(-lam)
        k = 0
        p = 1.0
        while p > l_val:
            k += 1
            p *= rng.random()
        return k - 1

    days: list[tuple[int, int]] = []
    for _ in range(n_days):
        has_event = rng.random() < alpha
        if not has_event:
            rate_b = eps_b
            rate_s = eps_s
        else:
            is_bad = rng.random() < delta
            if is_bad:
                rate_b = eps_b
                rate_s = eps_s + mu
            else:
                rate_b = eps_b + mu
                rate_s = eps_s
        days.append((sample_poisson(rate_b), sample_poisson(rate_s)))
    return days


def grid_search_pin(
    days: list[tuple[int, int]],
    delta_known: float,
    eps_b_known: float,
    eps_s_known: float,
) -> tuple[float, float, float]:
    """Perform grid search over (alpha, mu) to maximize log-likelihood."""
    best_ll = -1e18
    best_alpha = 0.0
    best_mu = 0.0

    # Grid specifications: alpha in [0.10, 0.50] step 0.02; mu in [8.0, 22.0] step 1.0
    for a_idx in range(21):
        a = 0.10 + a_idx * 0.02
        for m_idx in range(15):
            m = 8.0 + m_idx * 1.0
            ll = 0.0
            for b, s in days:
                prob = pin_day_pmf(b, s, a, delta_known, m, eps_b_known, eps_s_known)
                ll += math.log(max(prob, 1e-30))
            if ll > best_ll:
                best_ll = ll
                best_alpha = a
                best_mu = m

    pin_est = (best_alpha * best_mu) / (best_alpha * best_mu + eps_b_known + eps_s_known)
    return best_alpha, best_mu, pin_est


def main() -> None:
    alpha_true = 0.30
    delta_true = 0.40
    mu_true = 15.0
    eps_b_true = 10.0
    eps_s_true = 10.0
    pin_true = (alpha_true * mu_true) / (alpha_true * mu_true + eps_b_true + eps_s_true)

    # 1. Truncated support check
    max_k = 60
    trunc_sum = check_truncated_sum(alpha_true, delta_true, mu_true, eps_b_true, eps_s_true, max_k)
    print(f"Truncated support sum [0, {max_k - 1}] x [0, {max_k - 1}]: {trunc_sum:.8f}")
    print(f"Truncation deficit from 1.0: {abs(1.0 - trunc_sum):.2e}")

    # 2. Simulate 200 days of trade counts
    n_days = 200
    days = simulate_pin_days(n_days, alpha_true, delta_true, mu_true, eps_b_true, eps_s_true, seed=42)

    # 3. Grid search
    best_alpha, best_mu, pin_est = grid_search_pin(days, delta_true, eps_b_true, eps_s_true)

    print(f"Sample size: {n_days} trading days")
    print(f"True parameters:      alpha = {alpha_true:.2f}, mu = {mu_true:.1f}, PIN = {pin_true:.4f}")
    print(f"Grid search estimate: alpha = {best_alpha:.2f}, mu = {best_mu:.1f}, PIN = {pin_est:.4f}")
    print(f"PIN estimation error: {abs(pin_est - pin_true):.4f}")


main()
