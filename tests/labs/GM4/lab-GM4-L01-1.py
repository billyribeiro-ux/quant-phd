"""Lab GM4-L01-1: Trade-Expression Comparator.

Compares delta-one outright, duration-weighted futures spread, and synthetic forward
expressions for a macroeconomic cross-market divergence view.
"""

from __future__ import annotations

import math


def evaluate_expression_metrics(
    notional: float,
    expected_alpha_bps: float,
    beta_risk_factor: float,
    factor_vol: float,
    idiosyncratic_vol: float,
    margin_haircut: float,
    financing_cost_rate: float,
    holding_period_years: float,
) -> dict[str, float]:
    """Compute capital required, basis risk, financing drag, and information ratio for an expression."""
    capital_required = notional * margin_haircut
    gross_alpha = notional * (expected_alpha_bps * 1e-4)

    # Tracking error variance: beta mismatch + idiosyncratic
    tracking_var = (beta_risk_factor**2) * (factor_vol**2) + (idiosyncratic_vol**2)
    tracking_error_dollar = notional * math.sqrt(tracking_var * holding_period_years)

    financing_drag = capital_required * financing_cost_rate * holding_period_years
    net_alpha = gross_alpha - financing_drag
    return_on_capital = net_alpha / capital_required if capital_required > 0 else 0.0

    return {
        "capital_required": capital_required,
        "gross_alpha": gross_alpha,
        "financing_drag": financing_drag,
        "net_alpha": net_alpha,
        "tracking_error": tracking_error_dollar,
        "return_on_capital": return_on_capital,
    }


def main() -> None:
    notional = 10_000_000.0  # $10M trade notional
    expected_move_bps = 35.0  # 35 bps expected divergence
    horizon_years = 0.5  # 6-month trade horizon

    # Expression 1: Outright delta-one cash sovereign bond spread (unhedged level risk)
    exp1 = evaluate_expression_metrics(
        notional=notional,
        expected_alpha_bps=expected_move_bps,
        beta_risk_factor=0.25,  # Substantial residual level beta
        factor_vol=0.12,
        idiosyncratic_vol=0.03,
        margin_haircut=0.10,  # 10% cash repo haircut
        financing_cost_rate=0.048,
        holding_period_years=horizon_years,
    )

    # Expression 2: Duration-weighted futures calendar spread (low basis risk, high leverage)
    exp2 = evaluate_expression_metrics(
        notional=notional,
        expected_alpha_bps=expected_move_bps,
        beta_risk_factor=0.02,  # Near-zero duration mismatch
        factor_vol=0.12,
        idiosyncratic_vol=0.015,
        margin_haircut=0.03,  # 3% exchange initial margin
        financing_cost_rate=0.045,
        holding_period_years=horizon_years,
    )

    # Expression 3: Synthetic forward via cross-currency basis swap
    exp3 = evaluate_expression_metrics(
        notional=notional,
        expected_alpha_bps=expected_move_bps - 8.0,  # 8 bps cross-currency basis friction
        beta_risk_factor=0.05,
        factor_vol=0.12,
        idiosyncratic_vol=0.02,
        margin_haircut=0.05,  # 5% bilateral collateral
        financing_cost_rate=0.042,
        holding_period_years=horizon_years,
    )

    print("--- Expression 1: Cash Sovereign Spread ---")
    print(f"Capital Required: ${exp1['capital_required']:,.0f}")
    print(f"Net Alpha: ${exp1['net_alpha']:,.0f}")
    print(f"Tracking Error: ${exp1['tracking_error']:,.0f}")
    print(f"Return on Capital: {exp1['return_on_capital'] * 100:.2f}%")

    print("\n--- Expression 2: Futures Duration-Weighted Spread ---")
    print(f"Capital Required: ${exp2['capital_required']:,.0f}")
    print(f"Net Alpha: ${exp2['net_alpha']:,.0f}")
    print(f"Tracking Error: ${exp2['tracking_error']:,.0f}")
    print(f"Return on Capital: {exp2['return_on_capital'] * 100:.2f}%")

    print("\n--- Expression 3: Synthetic Forward Swap ---")
    print(f"Capital Required: ${exp3['capital_required']:,.0f}")
    print(f"Net Alpha: ${exp3['net_alpha']:,.0f}")
    print(f"Tracking Error: ${exp3['tracking_error']:,.0f}")
    print(f"Return on Capital: {exp3['return_on_capital'] * 100:.2f}%")


main()
