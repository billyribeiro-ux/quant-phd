"""Reference solution for GM5 Project: Crisis Mechanism Dossier & Simulator.

Implements quantitative crisis simulation engines:
1. Balance sheet leverage, haircuts, and margin call deficits.
2. Forced liquidation quantities under leverage and margin constraints.
3. Fire-sale market impact and price degradation.
4. Dynamic liquidity spirals (interlinked loss and margin spirals).
5. Central bank / policy backstop interventions.
6. Systemic crisis regime classification.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def compute_margin_call(
    position: float,
    price: float,
    cash: float,
    debt: float,
    haircut: float,
) -> dict[str, float]:
    """Compute balance sheet equity, margin requirement, deficit, and leverage.

    Parameters
    ----------
    position : float
        Units of risky asset held (Q >= 0).
    price : float
        Current market price of asset (P > 0).
    cash : float
        Unencumbered cash held (C >= 0).
    debt : float
        Borrowed repo/margin debt financing (D >= 0).
    haircut : float
        Regulatory/prime-broker margin requirement (0 < haircut < 1).

    Returns
    -------
    dict[str, float]
        Dictionary with asset_value, equity, required_margin, margin_deficit,
        current_leverage, and max_leverage.
    """
    if position < 0.0 or price <= 0.0 or cash < 0.0 or debt < 0.0 or haircut <= 0.0:
        raise ValueError("Invalid balance sheet parameters")

    asset_value = position * price
    equity = asset_value + cash - debt
    required_margin = haircut * asset_value

    margin_deficit = max(0.0, required_margin - equity)

    current_leverage = (asset_value / equity) if equity > 0.0 else float("inf")
    max_leverage = 1.0 / haircut if haircut > 0.0 else float("inf")

    return {
        "asset_value": float(asset_value),
        "equity": float(equity),
        "required_margin": float(required_margin),
        "margin_deficit": float(margin_deficit),
        "current_leverage": float(current_leverage),
        "max_leverage": float(max_leverage),
    }


def calculate_forced_sales(
    position: float,
    price: float,
    cash: float,
    debt: float,
    haircut: float,
    target_leverage: float | None = None,
) -> dict[str, float]:
    """Calculate the required forced liquidation quantity to resolve a margin deficit.

    If cash is available, it is applied first to cover the deficit.
    Any remaining deficit is resolved by liquidating risky assets where proceeds
    pay down debt. If equity <= 0, the entire remaining position is liquidated.

    Parameters
    ----------
    position : float
        Current position units.
    price : float
        Current asset price.
    cash : float
        Unencumbered cash.
    debt : float
        Outstanding debt.
    haircut : float
        Margin requirement fraction.
    target_leverage : float | None
        Optional target leverage. If None, targets max_leverage = 1 / haircut.

    Returns
    -------
    dict[str, float]
        Dictionary with forced_qty, forced_proceeds, remaining_position, post_sale_debt.
    """
    if position <= 0.0:
        return {
            "forced_qty": 0.0,
            "forced_proceeds": 0.0,
            "remaining_position": 0.0,
            "post_sale_debt": float(debt),
        }

    status = compute_margin_call(position, price, cash, debt, haircut)
    equity = status["equity"]

    if equity <= 0.0:
        # Complete insolvency: fire-sale entire position
        forced_qty = position
        forced_proceeds = forced_qty * price
        remaining_pos = 0.0
        post_debt = max(0.0, debt - forced_proceeds)
        return {
            "forced_qty": float(forced_qty),
            "forced_proceeds": float(forced_proceeds),
            "remaining_position": float(remaining_pos),
            "post_sale_debt": float(post_debt),
        }

    deficit = status["margin_deficit"]
    if deficit <= 1e-12:
        return {
            "forced_qty": 0.0,
            "forced_proceeds": 0.0,
            "remaining_position": float(position),
            "post_sale_debt": float(debt),
        }

    # Cash covers part of deficit
    cash_used = min(cash, deficit)
    remaining_deficit = deficit - cash_used

    if remaining_deficit <= 1e-12:
        return {
            "forced_qty": 0.0,
            "forced_proceeds": 0.0,
            "remaining_position": float(position),
            "post_sale_debt": float(debt),
        }

    denom = haircut * price
    forced_qty = (haircut * position * price - equity) / denom if denom > 0.0 else position
    forced_qty = max(0.0, min(position, forced_qty))

    forced_proceeds = forced_qty * price
    remaining_pos = max(0.0, position - forced_qty)
    post_debt = max(0.0, debt - forced_proceeds - cash_used)

    return {
        "forced_qty": float(forced_qty),
        "forced_proceeds": float(forced_proceeds),
        "remaining_position": float(remaining_pos),
        "post_sale_debt": float(post_debt),
    }


def estimate_fire_sale_discount(
    forced_volume: float,
    market_depth: float,
    permanent_impact_coef: float = 0.0,
) -> dict[str, float]:
    """Estimate temporary and permanent price impact from forced asset liquidation.

    Follows Kyle (1985) and Almgren-Chriss (2001) market impact specifications:
        Delta P_temp = lambda * Delta Q
        Delta P_perm = gamma * (Delta Q)^2

    Parameters
    ----------
    forced_volume : float
        Total liquidation volume (Delta Q >= 0).
    market_depth : float
        Linear price impact parameter lambda > 0.
    permanent_impact_coef : float
        Nonlinear permanent impact coefficient gamma >= 0.

    Returns
    -------
    dict[str, float]
        Dictionary with temporary_impact, permanent_impact, total_price_drop,
        and effective_discount.
    """
    if forced_volume < 0.0 or market_depth < 0.0 or permanent_impact_coef < 0.0:
        raise ValueError("Inputs must be non-negative")

    temp_impact = market_depth * forced_volume
    perm_impact = permanent_impact_coef * (forced_volume**2)
    total_drop = temp_impact + perm_impact
    effective_discount = 0.5 * temp_impact + perm_impact

    return {
        "temporary_impact": float(temp_impact),
        "permanent_impact": float(perm_impact),
        "total_price_drop": float(total_drop),
        "effective_discount": float(effective_discount),
    }


def simulate_liquidity_spiral(
    p0: float,
    q0: float,
    cash0: float,
    debt0: float,
    haircut0: float,
    exogenous_shocks: list[float] | np.ndarray,
    lambda_impact: float,
    target_leverage: float | None = None,
    haircut_sensitivity: float = 0.0,
    max_haircut: float = 0.50,
    policy_backstop: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Simulate a multi-period liquidity spiral coupling loss and margin spirals.

    At each period t:
    1. Exogenous fundamental shock hits asset price.
    2. Endogenous haircut updates based on price volatility:
       h_t = min(max_haircut, h_{t-1} + haircut_sensitivity * |Delta P_shock / P|)
    3. Balance sheet revalued; margin deficit evaluated.
    4. Forced liquidation volume calculated.
    5. Fire-sale price impact applied, depressing price further.
    6. Policy backstop (if active) halts price declines below floor or purchases assets.
    7. Insolvency check (equity <= 0).

    Returns
    -------
    dict[str, Any]
        Complete time-series arrays and summary diagnostics.
    """
    shocks = [float(s) for s in exogenous_shocks]
    n_steps = len(shocks)

    prices: list[float] = [float(p0)]
    positions: list[float] = [float(q0)]
    equities: list[float] = [float(q0 * p0 + cash0 - debt0)]
    debts: list[float] = [float(debt0)]
    cashes: list[float] = [float(cash0)]
    haircuts: list[float] = [float(haircut0)]
    margin_calls: list[float] = [0.0]
    forced_sales: list[float] = [0.0]

    current_p = float(p0)
    current_q = float(q0)
    current_cash = float(cash0)
    current_debt = float(debt0)
    current_h = float(haircut0)
    insolvent = False
    backstop_interventions = 0

    backstop_floor = 0.0
    backstop_active = False
    if policy_backstop is not None and policy_backstop.get("enabled", False):
        backstop_floor = float(policy_backstop.get("price_floor", 0.0))
        backstop_active = True

    cumulative_exogenous_drop = 0.0

    for t in range(n_steps):
        shock_pct = shocks[t]
        # Exogenous price jump
        delta_p_exo = current_p * shock_pct
        if delta_p_exo < 0.0:
            cumulative_exogenous_drop += abs(delta_p_exo)
        price_after_shock = max(0.01, current_p + delta_p_exo)

        # Endogenous haircut spiral
        if haircut_sensitivity > 0.0:
            h_jump = haircut_sensitivity * abs(shock_pct)
            current_h = min(max_haircut, current_h + h_jump)

        # Revalue balance sheet
        equity_before_sale = current_q * price_after_shock + current_cash - current_debt

        if equity_before_sale <= 0.0:
            insolvent = True
            forced_result = calculate_forced_sales(current_q, price_after_shock, current_cash, current_debt, current_h)
            forced_qty = forced_result["forced_qty"]
            # Impact of final dump
            impact = estimate_fire_sale_discount(forced_qty, lambda_impact)
            final_p = max(0.01, price_after_shock - impact["total_price_drop"])
            if backstop_active and final_p < backstop_floor:
                final_p = backstop_floor
                backstop_interventions += 1

            prices.append(final_p)
            positions.append(0.0)
            equities.append(0.0)
            debts.append(forced_result["post_sale_debt"])
            cashes.append(0.0)
            haircuts.append(current_h)
            margin_calls.append(max(0.0, current_h * current_q * price_after_shock))
            forced_sales.append(forced_qty)
            break

        # Calculate forced sales to meet margin
        forced_result = calculate_forced_sales(
            current_q, price_after_shock, current_cash, current_debt, current_h, target_leverage
        )
        forced_qty = forced_result["forced_qty"]

        # Market impact of forced sales
        impact = estimate_fire_sale_discount(forced_qty, lambda_impact)
        price_after_impact = max(0.01, price_after_shock - impact["total_price_drop"])

        if backstop_active and price_after_impact < backstop_floor:
            price_after_impact = backstop_floor
            backstop_interventions += 1

        # Post-sale update
        current_p = price_after_impact
        current_q = forced_result["remaining_position"]
        current_debt = forced_result["post_sale_debt"]
        current_cash = max(
            0.0,
            current_cash - (forced_result["forced_proceeds"] if forced_result["forced_proceeds"] < 0 else 0.0),
        )
        new_equity = current_q * current_p + current_cash - current_debt
        if new_equity <= 0.0:
            insolvent = True
            new_equity = 0.0

        margin_status = compute_margin_call(current_q, current_p, current_cash, current_debt, current_h)

        prices.append(current_p)
        positions.append(current_q)
        equities.append(new_equity)
        debts.append(current_debt)
        cashes.append(current_cash)
        haircuts.append(current_h)
        margin_calls.append(margin_status["margin_deficit"])
        forced_sales.append(forced_qty)

    total_drop = float(p0) - prices[-1]
    spiral_multiplier = total_drop / cumulative_exogenous_drop if cumulative_exogenous_drop > 1e-09 else 1.0

    leverages = [(q * p / e) if e > 0.0 else float("inf") for q, p, e in zip(positions, prices, equities, strict=False)]

    return {
        "prices": prices,
        "positions": positions,
        "equities": equities,
        "debts": debts,
        "cashes": cashes,
        "haircuts": haircuts,
        "leverages": leverages,
        "margin_calls": margin_calls,
        "forced_sales": forced_sales,
        "insolvent": insolvent,
        "total_forced_volume": float(sum(forced_sales)),
        "spiral_multiplier": float(spiral_multiplier),
        "backstop_interventions": backstop_interventions,
    }


def evaluate_policy_intervention(
    baseline_run: dict[str, Any],
    backstopped_run: dict[str, Any],
) -> dict[str, float]:
    """Evaluate quantitative benefits of a policy backstop relative to baseline crash."""
    p_baseline = baseline_run["prices"][-1]
    p_backstopped = backstopped_run["prices"][-1]
    price_preservation = float(p_backstopped - p_baseline)

    e_baseline = baseline_run["equities"][-1]
    e_backstopped = backstopped_run["equities"][-1]
    equity_mitigation = float(e_backstopped - e_baseline)

    vol_baseline = baseline_run["total_forced_volume"]
    vol_backstopped = backstopped_run["total_forced_volume"]
    forced_vol_reduction = float(vol_baseline - vol_backstopped)

    mult_baseline = baseline_run["spiral_multiplier"]
    mult_backstopped = backstopped_run["spiral_multiplier"]
    multiplier_attenuation = float(mult_baseline - mult_backstopped)

    avoided_insolvency = 1.0 if (baseline_run["insolvent"] and not backstopped_run["insolvent"]) else 0.0

    return {
        "price_preservation": price_preservation,
        "equity_loss_mitigation": equity_mitigation,
        "forced_volume_reduction": forced_vol_reduction,
        "multiplier_attenuation": multiplier_attenuation,
        "avoided_insolvency": avoided_insolvency,
    }


def classify_crisis_regime(
    initial_leverage: float,
    haircut_increase: float,
    spiral_multiplier: float,
    defaulted: bool,
) -> str:
    """Classify systemic crisis regime based on amplification and balance sheet state."""
    if defaulted or spiral_multiplier > 3.0:
        return "CATASTROPHIC_RUNAWAY"
    if spiral_multiplier > 1.5 and haircut_increase > 0.05:
        return "MARGIN_SPIRAL"
    if spiral_multiplier > 1.2:
        return "LOSS_SPIRAL"
    return "ORDERLY_ABSORPTION"
