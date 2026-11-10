"""E-index mutant: counts unequal_voting instead of supermajority_merger in core provisions."""

from __future__ import annotations

import math
from collections.abc import Sequence
from statistics import NormalDist
from typing import Any

CORE_ENTRENCHMENT_KEYS = (
    "staggered_board",
    "poison_pill",
    "golden_parachute",
    "limit_bylaw_amendment",
    "limit_charter_amendment",
    "unequal_voting",  # MUTATION: wrong provision key
)


def compute_e_index(provisions: dict[str, int]) -> int:
    total = 0
    for key in CORE_ENTRENCHMENT_KEYS:
        if key not in provisions:
            raise ValueError(f"Missing required entrenchment provision: {key}")
        val = provisions[key]
        if val not in (0, 1):
            raise ValueError(f"Provision {key} must be binary 0 or 1, got {val}")
        total += val
    return total


def compute_g_index(provisions: dict[str, int]) -> int:
    if not provisions:
        raise ValueError("Provisions dictionary cannot be empty")
    total = 0
    for key, val in provisions.items():
        if val not in (0, 1):
            raise ValueError(f"Provision {key} must be binary 0 or 1, got {val}")
        total += val
    return total


def compute_tobins_q(
    assets_cents: int,
    debt_cents: int,
    market_equity_cents: int,
    book_equity_cents: int,
) -> float:
    if assets_cents <= 0:
        raise ValueError("Total assets must be strictly positive")
    if market_equity_cents <= 0:
        raise ValueError("Market value of equity must be strictly positive")
    if debt_cents < 0:
        raise ValueError("Debt cannot be negative")
    if book_equity_cents < 0:
        raise ValueError("Book value of equity cannot be negative")
    numerator = assets_cents - book_equity_cents + market_equity_cents
    return numerator / assets_cents


def cross_sectional_ols(x: Sequence[float], y: Sequence[float]) -> dict[str, float]:
    n = len(x)
    if n != len(y):
        raise ValueError(f"Length mismatch: x has {n} observations, y has {len(y)}")
    if n < 3:
        raise ValueError(f"At least 3 observations required for bivariate OLS with n - 2 df, got {n}")
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    s_xx = sum((xi - mean_x) ** 2 for xi in x)
    if s_xx <= 1e-12:
        raise ValueError("Zero sample variance in explanatory variable x")
    s_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y, strict=True))
    s_yy = sum((yi - mean_y) ** 2 for yi in y)
    beta = s_xy / s_xx
    alpha = mean_y - beta * mean_x
    rss = sum((yi - (alpha + beta * xi)) ** 2 for xi, yi in zip(x, y, strict=True))
    df = n - 2
    s_squared = rss / df
    se_beta = math.sqrt(s_squared / s_xx)
    se_alpha = math.sqrt(s_squared * (1.0 / n + (mean_x**2) / s_xx))
    t_stat = beta / se_beta if se_beta > 1e-15 else 0.0
    r_squared = 1.0 - (rss / s_yy) if s_yy > 1e-12 else 0.0
    return {
        "alpha": alpha,
        "beta": beta,
        "se_alpha": se_alpha,
        "se_beta": se_beta,
        "t_stat": t_stat,
        "r_squared": max(0.0, min(1.0, r_squared)),
        "n": float(n),
        "rss": rss,
        "s_squared": s_squared,
    }


def statistical_power_t_test(
    n: int,
    true_slope: float,
    se_slope: float,
    alpha_sig: float = 0.05,
) -> float:
    if n < 3:
        raise ValueError(f"Sample size n must be >= 3, got {n}")
    if se_slope <= 0:
        raise ValueError(f"Standard error of slope must be strictly positive, got {se_slope}")
    if not (0.0 < alpha_sig < 1.0):
        raise ValueError(f"Significance level alpha_sig must be in (0, 1), got {alpha_sig}")
    dist = NormalDist()
    z_crit = dist.inv_cdf(1.0 - alpha_sig / 2.0)
    delta = abs(true_slope) / se_slope
    power = (1.0 - dist.cdf(z_crit - delta)) + dist.cdf(-z_crit - delta)
    return max(0.0, min(1.0, power))


def score_firm_panel(firms: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    scored: list[dict[str, Any]] = []
    for f in firms:
        e_idx = compute_e_index(f["provisions"])
        g_idx = compute_g_index(f["provisions"])
        q_val = compute_tobins_q(
            f["assets_cents"],
            f["debt_cents"],
            f["market_equity_cents"],
            f["book_equity_cents"],
        )
        scored_record = dict(f)
        scored_record["e_index"] = e_idx
        scored_record["g_index"] = g_idx
        scored_record["tobins_q"] = q_val
        scored.append(scored_record)
    return scored


def governance_regression(
    firms: Sequence[dict[str, Any]],
    index_key: str = "e_index",
) -> dict[str, float]:
    if not firms:
        raise ValueError("Firm list cannot be empty")
    x = [float(f[index_key]) for f in firms]
    y = [float(f["tobins_q"]) for f in firms]
    ols_res = cross_sectional_ols(x, y)
    power = statistical_power_t_test(
        len(firms),
        ols_res["beta"],
        ols_res["se_beta"],
        alpha_sig=0.05,
    )
    result = dict(ols_res)
    result["power"] = power
    return result
