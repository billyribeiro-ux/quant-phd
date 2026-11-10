"""Reference solution for X4: Stablecoin Reserve Stress Test.

Implements full reserve portfolio stress testing, interest rate duration shocks,
liquidation waterfall accounting with asset-tier haircuts, peg-break search,
and liquidity coverage ratio calculations.
"""

from __future__ import annotations

from typing import Any

try:
    from integrity import (  # type: ignore[import-not-found, unused-ignore]
        validate_reserve_inputs,
        validate_waterfall_output,
    )
except ImportError:
    from .integrity import (
        validate_reserve_inputs,
        validate_waterfall_output,
    )

ORDERED_TIERS = ("cash", "overnight_repo", "tbills_short", "treasury_notes", "bank_deposits")


def validate_inputs(
    total_liabilities: float,
    reserve_assets: dict[str, dict[str, float]],
    rate_shock_bps: float,
    peg_threshold: float,
) -> None:
    """Validate all project inputs using integrity module."""
    validate_reserve_inputs(total_liabilities, reserve_assets, rate_shock_bps, peg_threshold)


def apply_rate_shock(
    reserve_assets: dict[str, dict[str, float]],
    rate_shock_bps: float,
) -> dict[str, dict[str, float]]:
    """Apply interest rate shock to reserve assets using modified duration.

    Price return dP/P = - duration * dy.
    Market value = par * max(0.0, 1.0 - duration * (rate_shock_bps / 10000.0)).
    """
    if rate_shock_bps < 0.0:
        raise ValueError("rate_shock_bps must be non-negative")

    dy = rate_shock_bps / 10000.0
    shocked: dict[str, dict[str, float]] = {}

    for tier, data in reserve_assets.items():
        par = float(data["par"])
        duration = float(data["duration"])
        haircut = float(data["haircut"])

        if par < 0.0 or duration < 0.0 or not (0.0 <= haircut < 1.0):
            raise ValueError(f"Invalid parameters in tier {tier}")

        price_factor = max(0.0, 1.0 - duration * dy)
        market_val = par * price_factor

        shocked[tier] = {
            "par": par,
            "duration": duration,
            "haircut": haircut,
            "market_value": market_val,
        }

    return shocked


def simulate_redemption_waterfall(
    total_liabilities: float,
    shocked_assets: dict[str, dict[str, float]],
    redemptions: float,
) -> dict[str, Any]:
    """Execute redemption liquidation waterfall across reserve asset tiers.

    Assets are liquidated in strict liquidity order:
    1. Cash (haircut = 0)
    2. Overnight reverse repo
    3. Short-dated T-bills
    4. Treasury notes
    5. Uninsured bank deposits

    For each tier with market value MV and haircut h:
    Available cash = MV * (1 - h).
    To satisfy redemption R:
    MV liquidated = R / (1 - h).
    Haircut loss = R * h / (1 - h).
    """
    if total_liabilities <= 0.0:
        raise ValueError("total_liabilities must be positive")
    if redemptions < 0.0:
        raise ValueError("redemptions cannot be negative")

    rem_redemption = redemptions
    total_haircut_loss = 0.0
    tier_details: dict[str, dict[str, float]] = {}

    # Deep copy market values
    current_mv: dict[str, float] = {}
    for tier in ORDERED_TIERS:
        if tier in shocked_assets:
            current_mv[tier] = float(shocked_assets[tier]["market_value"])
        else:
            current_mv[tier] = 0.0

    # Also include any custom tiers if present
    for tier, data in shocked_assets.items():
        if tier not in current_mv:
            current_mv[tier] = float(data["market_value"])

    active_order = [t for t in ORDERED_TIERS if t in shocked_assets] + [
        t for t in shocked_assets if t not in ORDERED_TIERS
    ]

    for tier in active_order:
        data = shocked_assets[tier]
        mv = current_mv[tier]
        h = float(data["haircut"])
        avail_cash = mv * (1.0 - h)

        if rem_redemption <= 0.0:
            tier_details[tier] = {
                "initial_mv": mv,
                "mv_liquidated": 0.0,
                "cash_raised": 0.0,
                "haircut_loss": 0.0,
                "remaining_mv": mv,
            }
            continue

        if rem_redemption <= avail_cash:
            cash_from_tier = rem_redemption
            mv_used = cash_from_tier / (1.0 - h)
            loss = mv_used - cash_from_tier
            current_mv[tier] -= mv_used
            total_haircut_loss += loss
            rem_redemption = 0.0
            tier_details[tier] = {
                "initial_mv": mv,
                "mv_liquidated": mv_used,
                "cash_raised": cash_from_tier,
                "haircut_loss": loss,
                "remaining_mv": current_mv[tier],
            }
        else:
            cash_from_tier = avail_cash
            mv_used = mv
            loss = mv * h
            total_haircut_loss += loss
            rem_redemption -= cash_from_tier
            current_mv[tier] = 0.0
            tier_details[tier] = {
                "initial_mv": mv,
                "mv_liquidated": mv_used,
                "cash_raised": cash_from_tier,
                "haircut_loss": loss,
                "remaining_mv": 0.0,
            }

    cash_raised = redemptions - rem_redemption
    unfulfilled = rem_redemption
    remaining_tokens = max(0.0, total_liabilities - redemptions)
    remaining_mv = sum(current_mv.values())

    if unfulfilled > 1e-9:
        # Run has exhausted all assets; default/insolvency
        nav = 0.0
    elif remaining_tokens <= 1e-9:
        # 100% of tokens redeemed at par
        nav = 1.0
    else:
        nav = remaining_mv / remaining_tokens

    result = {
        "nav": nav,
        "total_haircut_loss": total_haircut_loss,
        "cash_raised": cash_raised,
        "unfulfilled_redemptions": unfulfilled,
        "remaining_tokens": remaining_tokens,
        "remaining_market_value": remaining_mv,
        "tier_details": tier_details,
    }
    validate_waterfall_output(result)
    return result


def find_peg_break_run_size(
    total_liabilities: float,
    shocked_assets: dict[str, dict[str, float]],
    peg_threshold: float,
    tol: float = 1e-5,
) -> dict[str, Any]:
    """Find the minimal cumulative redemption run size R* that causes NAV < peg_threshold.

    Uses binary search over [0, total_liabilities].
    """
    if total_liabilities <= 0.0:
        raise ValueError("total_liabilities must be positive")
    if not (0.50 <= peg_threshold <= 1.00):
        raise ValueError("peg_threshold must be between 0.50 and 1.00")

    # Evaluate at R = 0
    res_0 = simulate_redemption_waterfall(total_liabilities, shocked_assets, 0.0)
    nav_0 = res_0["nav"]

    if nav_0 < peg_threshold:
        return {
            "peg_broken": True,
            "critical_run_amount": 0.0,
            "critical_run_pct": 0.0,
            "nav_at_break": nav_0,
        }

    # Evaluate right before total redemption
    res_max = simulate_redemption_waterfall(total_liabilities, shocked_assets, total_liabilities - 0.01)
    if res_max["nav"] >= peg_threshold:
        return {
            "peg_broken": False,
            "critical_run_amount": total_liabilities,
            "critical_run_pct": 1.0,
            "nav_at_break": res_max["nav"],
        }

    low = 0.0
    high = total_liabilities

    for _ in range(60):
        mid = (low + high) / 2.0
        nav_mid = simulate_redemption_waterfall(total_liabilities, shocked_assets, mid)["nav"]
        if nav_mid < peg_threshold:
            high = mid
        else:
            low = mid

    r_star = (low + high) / 2.0
    nav_break = simulate_redemption_waterfall(total_liabilities, shocked_assets, r_star)["nav"]

    return {
        "peg_broken": True,
        "critical_run_amount": round(r_star, 4),
        "critical_run_pct": round(r_star / total_liabilities, 6),
        "nav_at_break": round(nav_break, 6),
    }


def compute_liquidity_coverage_ratio(
    reserve_assets: dict[str, dict[str, float]],
    stressed_outflow_30d: float,
) -> float:
    """Compute Liquidity Coverage Ratio (LCR) = HQLA / stressed_outflow_30d.

    HQLA consists of cash and overnight repo par values.
    """
    if stressed_outflow_30d <= 0.0:
        raise ValueError("stressed_outflow_30d must be positive")

    cash_par = float(reserve_assets.get("cash", {}).get("par", 0.0))
    repo_par = float(reserve_assets.get("overnight_repo", {}).get("par", 0.0))
    hqla = cash_par + repo_par

    return hqla / stressed_outflow_30d


def run_stress_grid(
    total_liabilities: float,
    base_assets: dict[str, dict[str, float]],
    rate_shocks_bps: list[float],
    redemption_fractions: list[float],
    peg_threshold: float = 0.995,
) -> dict[str, Any]:
    """Evaluate reserve portfolio across a 2D grid of rate shocks and redemption sizes."""
    nav_matrix: list[list[float]] = []
    peg_breaks: dict[str, float] = {}

    for shock in rate_shocks_bps:
        shocked = apply_rate_shock(base_assets, shock)
        row: list[float] = []
        for frac in redemption_fractions:
            r = total_liabilities * frac
            res = simulate_redemption_waterfall(total_liabilities, shocked, r)
            row.append(round(res["nav"], 6))
        nav_matrix.append(row)

        pb = find_peg_break_run_size(total_liabilities, shocked, peg_threshold)
        peg_breaks[f"{shock:.1f}_bps"] = pb["critical_run_pct"]

    return {
        "rate_shocks_bps": rate_shocks_bps,
        "redemption_fractions": redemption_fractions,
        "nav_matrix": nav_matrix,
        "critical_run_pcts": peg_breaks,
    }
