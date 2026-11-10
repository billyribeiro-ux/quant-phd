"""Lab GM4-project-1: Rung 1 Worked Example: End-to-End Atlas A20 Engine Pipeline.

SIMULATED. Complete worked instance demonstrating MacroView specification,
DV01-neutral curve hedge ratio calculation, carry attribution, and scenario stress revaluation.
"""

from __future__ import annotations

from typing import Any


def run_worked_example() -> dict[str, Any]:
    # 1. View Definition: 25 bps steepening expected over 90 days with 75% confidence
    view_move_bps = 25.0
    confidence = 0.75
    horizon_years = 90.0 / 365.0

    # 2. Leg Parameters: 2Y Note vs 10Y Note
    dv01_2y = 42.50  # per $1M
    dv01_10y = 85.00  # per $1M
    yield_2y = 0.042
    yield_10y = 0.046
    dur_2y = 1.95
    dur_10y = 8.10
    roll_bps_2y = 6.0
    roll_bps_10y = 16.0
    repo_rate = 0.038

    # 3. Hedge Ratio and Sizing: $10M front-end notional
    notional_2y = 10_000_000.0
    hedge_ratio = dv01_2y / dv01_10y  # 0.50
    notional_10y = -notional_2y * hedge_ratio  # -$5M short 10Y

    net_dv01 = (notional_2y / 1e6) * dv01_2y + (notional_10y / 1e6) * dv01_10y

    # 4. Carry & Roll-Down Attribution
    gross_carry_2y = yield_2y * horizon_years
    roll_2y = (roll_bps_2y * 1e-4) * dur_2y * horizon_years
    drag_2y = repo_rate * horizon_years
    net_carry_2y_bps = (gross_carry_2y + roll_2y - drag_2y) * 10_000.0

    gross_carry_10y = yield_10y * horizon_years
    roll_10y = (roll_bps_10y * 1e-4) * dur_10y * horizon_years
    drag_10y = repo_rate * horizon_years
    net_carry_10y_bps = (gross_carry_10y + roll_10y - drag_10y) * 10_000.0

    # Portfolio net carry: weighted by signed notional
    w_2y = 10.0 / 15.0
    w_10y = -5.0 / 15.0
    port_carry_bps = w_2y * net_carry_2y_bps + w_10y * net_carry_10y_bps

    # 5. Kelly Sizing
    expected_return = (view_move_bps * 1e-4) * confidence
    vol_est = 0.065
    var_est = vol_est**2
    quarter_kelly = 0.25 * (expected_return / var_est)
    capped_kelly = min(4.0, max(-4.0, quarter_kelly))

    return {
        "hedge_ratio": hedge_ratio,
        "notional_2y": notional_2y,
        "notional_10y": notional_10y,
        "net_dv01": net_dv01,
        "carry_2y_bps": net_carry_2y_bps,
        "carry_10y_bps": net_carry_10y_bps,
        "portfolio_net_carry_bps": port_carry_bps,
        "quarter_kelly_weight": capped_kelly,
    }


def main() -> None:
    res = run_worked_example()
    print("=== Atlas A20 Worked Example: 2s10s Steepener ===")
    print(f"DV01 Hedge Ratio (10Y per 2Y): {res['hedge_ratio']:.4f}")
    print(f"Front-End (2Y) Notional: ${res['notional_2y']:,.0f}")
    print(f"Back-End (10Y) Notional: ${res['notional_10y']:,.0f}")
    print(f"Net Portfolio DV01 ($): {res['net_dv01']:.2f}")
    print(f"2Y Net Carry: {res['carry_2y_bps']:.1f} bps")
    print(f"10Y Net Carry: {res['carry_10y_bps']:.1f} bps")
    print(f"Portfolio Net Carry: {res['portfolio_net_carry_bps']:.1f} bps")
    print(f"Quarter Kelly Leverage Weight: {res['quarter_kelly_weight']:.2f}x")


main()
