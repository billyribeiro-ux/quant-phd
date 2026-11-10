"""Linear impact mutant: scales market impact linearly with trade size (Q/ADV) instead of square-root (sqrt(Q/ADV))."""

from __future__ import annotations

import math
from typing import Any

from integrity import validate_vectors


def compute_trade_lists(
    w_initial: list[float],
    w_target: list[float],
    aum: float,
    prices: list[float],
) -> dict[str, Any]:
    if aum <= 0:
        raise ValueError(f"aum must be positive; got {aum}")
    validate_vectors(w_initial, w_target, [1.0] * len(w_initial), [0.02] * len(w_initial), prices)

    n = len(w_initial)
    dollar_trades: list[float] = [0.0] * n
    share_trades: list[float] = [0.0] * n

    for i in range(n):
        delta_w = w_target[i] - w_initial[i]
        d_trade = aum * delta_w
        dollar_trades[i] = d_trade
        share_trades[i] = d_trade / prices[i]

    turnover_dollars = 0.5 * sum(abs(d) for d in dollar_trades)
    turnover_fraction = turnover_dollars / aum

    return {
        "dollar_trades": dollar_trades,
        "share_trades": share_trades,
        "turnover_dollars": turnover_dollars,
        "turnover_fraction": turnover_fraction,
    }


def estimate_impact_costs(
    dollar_trades: list[float],
    adv: list[float],
    sigma: list[float],
    prefactor_y: float = 0.5,
) -> dict[str, float]:
    n = len(dollar_trades)
    if len(adv) != n or len(sigma) != n:
        raise ValueError(f"mismatched dimensions: trades {n}, adv {len(adv)}, sigma {len(sigma)}")
    if prefactor_y <= 0:
        raise ValueError(f"prefactor_y must be positive; got {prefactor_y}")

    total_cost = 0.0
    total_traded = 0.0

    for i in range(n):
        if adv[i] <= 0 or sigma[i] <= 0:
            raise ValueError(f"adv and sigma must be positive; asset {i}")
        abs_d = abs(dollar_trades[i])
        total_traded += abs_d
        if abs_d > 1e-9:
            # Linear impact error: abs_d / adv[i] instead of sqrt(abs_d / adv[i])
            impact = prefactor_y * sigma[i] * (abs_d / adv[i])
            cost_i = abs_d * impact
            total_cost += cost_i

    eff_bps = (total_cost / total_traded) * 10000.0 if total_traded > 1e-9 else 0.0

    return {
        "total_cost_dollars": round(total_cost, 4),
        "effective_spread_bps": round(eff_bps, 4),
    }


def simulate_capacity_curve(
    aum_grid: list[float],
    w_initial: list[float],
    w_target: list[float],
    adv: list[float],
    sigma: list[float],
    gross_alpha: float,
    prefactor_y: float = 0.5,
) -> dict[str, list[float]]:
    validate_vectors(w_initial, w_target, adv, sigma)
    if gross_alpha <= 0:
        raise ValueError(f"gross_alpha must be positive; got {gross_alpha}")
    if not aum_grid or any(a <= 0 for a in aum_grid):
        raise ValueError("aum_grid must contain positive values")

    n = len(w_initial)
    friction_kappa = prefactor_y * sum(
        sigma[i] * (abs(w_target[i] - w_initial[i]) ** 1.5) / math.sqrt(adv[i])
        for i in range(n)
    )

    costs_dollars: list[float] = []
    costs_bps: list[float] = []
    net_alphas: list[float] = []
    dollar_alphas: list[float] = []

    for aum in aum_grid:
        c_dollars = friction_kappa * (aum ** 1.5)
        c_fraction = c_dollars / aum
        c_bps = c_fraction * 10000.0
        n_alpha = gross_alpha - c_fraction
        d_alpha = aum * n_alpha

        costs_dollars.append(round(c_dollars, 4))
        costs_bps.append(round(c_bps, 4))
        net_alphas.append(round(n_alpha, 6))
        dollar_alphas.append(round(d_alpha, 4))

    return {
        "aum": list(aum_grid),
        "cost_dollars": costs_dollars,
        "cost_bps": costs_bps,
        "net_alpha": net_alphas,
        "dollar_alpha": dollar_alphas,
    }


def find_capacity_limits(
    w_initial: list[float],
    w_target: list[float],
    adv: list[float],
    sigma: list[float],
    gross_alpha: float,
    prefactor_y: float = 0.5,
) -> dict[str, float]:
    validate_vectors(w_initial, w_target, adv, sigma)
    if gross_alpha <= 0:
        raise ValueError(f"gross_alpha must be positive; got {gross_alpha}")

    n = len(w_initial)
    friction_kappa = prefactor_y * sum(
        sigma[i] * (abs(w_target[i] - w_initial[i]) ** 1.5) / math.sqrt(adv[i])
        for i in range(n)
    )

    breakeven_aum = (gross_alpha / friction_kappa) ** 2
    optimal_aum = (4.0 / 9.0) * breakeven_aum
    max_dollar_alpha = (4.0 / 27.0) * (gross_alpha ** 3) / (friction_kappa ** 2)
    net_alpha_at_opt = gross_alpha / 3.0

    return {
        "breakeven_aum": round(breakeven_aum, 2),
        "optimal_aum": round(optimal_aum, 2),
        "max_dollar_alpha": round(max_dollar_alpha, 2),
        "net_alpha_at_optimal": round(net_alpha_at_opt, 6),
        "friction_kappa": round(friction_kappa, 12),
    }


def mitigate_costs(
    ranks: list[float],
    current_weights: list[float],
    target_n_assets: int,
    buffer_ratio: float = 1.5,
) -> list[float]:
    n = len(ranks)
    if len(current_weights) != n:
        raise ValueError("length mismatch")
    if target_n_assets <= 0 or target_n_assets > n:
        raise ValueError("invalid target_n_assets")
    if buffer_ratio < 1.0:
        raise ValueError("buffer_ratio < 1.0")

    k_hold = math.floor(target_n_assets * buffer_ratio)
    is_held = [w > 1e-6 for w in current_weights]
    retained = [i for i in range(n) if is_held[i] and ranks[i] <= k_hold]
    retained.sort(key=lambda idx: ranks[idx])

    if len(retained) >= target_n_assets:
        selected = retained[:target_n_assets]
    else:
        needed = target_n_assets - len(retained)
        unheld = [i for i in range(n) if i not in retained]
        unheld.sort(key=lambda idx: ranks[idx])
        selected = retained + unheld[:needed]

    w_each = round(1.0 / target_n_assets, 8)
    new_weights = [0.0] * n
    for idx in selected:
        new_weights[idx] = w_each
    diff = 1.0 - sum(new_weights)
    if abs(diff) > 1e-9:
        new_weights[selected[0]] += diff
    return new_weights
