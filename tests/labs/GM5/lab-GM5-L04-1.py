"""Lab GM5-L04-1: Carry Trade Unwind & Endogenous Crash Dynamics.

Models the August 2024 Yen-carry unwind and Brunnermeier, Nagel & Pedersen (2008)
mechanisms, simulating funding-rate surprises, crowded position stops, and FX jumps.
"""

from __future__ import annotations

from typing import Any


def simulate_carry_unwind(
    fx_spot_0: float,
    interest_differential_bps: float,
    aggregate_carry_notional: float,
    funding_rate_hike_bps: float,
    equity_vol_shock_pct: float,
    unwind_threshold_loss_pct: float = 0.02,
    fx_impact_lambda: float = 0.0001,
    n_days: int = 20,
) -> dict[str, Any]:
    """Simulate a dynamic carry-trade unwind with stop-loss triggered liquidations.

    Parameters
    ----------
    fx_spot_0 : float
        Initial exchange rate (e.g. USD/JPY at 160.0).
    interest_differential_bps : float
        Annualized carry spread in basis points (e.g. 500 bps).
    aggregate_carry_notional : float
        Total open carry trade positions in billions.
    funding_rate_hike_bps : float
        Central bank policy surprise on funding currency (e.g. +25 bps).
    equity_vol_shock_pct : float
        Simultaneous global risk aversion / equity sell-off shock.
    unwind_threshold_loss_pct : float
        Loss threshold triggering programmatic stop-loss deleveraging.
    fx_impact_lambda : float
        Price impact per billion of carry unwind (appreciating funding currency).
    n_days : int
        Days simulated.

    Returns
    -------
    dict[str, float | int | list[float]]
        Time series of spot FX, open positions, daily returns, and peak drawdown.
    """
    spot = fx_spot_0
    notional = aggregate_carry_notional

    spot_path = [spot]
    notional_path = [notional]
    daily_returns: list[float] = []

    daily_carry_return = (interest_differential_bps / 10000.0) / 252.0

    for day in range(1, n_days + 1):
        macro_shock = -(funding_rate_hike_bps / 10000.0) * 15.0 - equity_vol_shock_pct * 0.50 if day == 2 else 0.0

        # Current day return before programmatic stop-loss
        pre_unwind_ret = daily_carry_return + macro_shock

        # Programmatic unwinding condition: if cumulative or daily loss breaches stop
        if pre_unwind_ret < -unwind_threshold_loss_pct:
            # Proportion of position liquidated escalates with loss severity
            unwind_fraction = min(0.60, 2.5 * abs(pre_unwind_ret))
            unwind_volume = notional * unwind_fraction
            notional -= unwind_volume

            # Funding currency appreciation impact (e.g. USD/JPY drops)
            fx_impact = unwind_volume * fx_impact_lambda * spot
            spot -= fx_impact
        else:
            unwind_volume = 0.0

        spot = max(1.0, spot * (1.0 + pre_unwind_ret))
        spot_path.append(spot)
        notional_path.append(notional)

        day_ret = (spot_path[-1] - spot_path[-2]) / spot_path[-2]
        daily_returns.append(day_ret)

    peak_spot = max(spot_path)
    trough_spot = min(spot_path)
    max_drawdown_pct = ((trough_spot - peak_spot) / peak_spot) * 100.0
    total_unwound_pct = ((aggregate_carry_notional - notional) / aggregate_carry_notional) * 100.0

    return {
        "terminal_spot": spot_path[-1],
        "max_drawdown_pct": max_drawdown_pct,
        "total_unwound_pct": total_unwound_pct,
        "remaining_notional": notional_path[-1],
        "spot_path": spot_path,
        "daily_returns": daily_returns,
    }


def main() -> None:
    # Calibrated to USD/JPY summer 2024 episode
    initial_fx = 160.0  # USD/JPY
    carry_spread = 500.0  # 5.00% interest differential
    notional_b = 250.0  # $250B aggregate carry positioning

    res = simulate_carry_unwind(
        fx_spot_0=initial_fx,
        interest_differential_bps=carry_spread,
        aggregate_carry_notional=notional_b,
        funding_rate_hike_bps=25.0,  # BoJ +25 bps surprise hike
        equity_vol_shock_pct=0.08,  # Global equity risk aversion
        unwind_threshold_loss_pct=0.015,
        fx_impact_lambda=0.00015,
        n_days=10,
    )

    print("Initial USD/JPY Spot:", round(initial_fx, 2))
    print("Terminal USD/JPY Spot:", round(float(res["terminal_spot"]), 2))
    print("Maximum Spot Drawdown (%):", round(float(res["max_drawdown_pct"]), 2))
    print("Total Carry Notional Unwound (%):", round(float(res["total_unwound_pct"]), 2))
    print("Remaining Open Notional ($B):", round(float(res["remaining_notional"]), 2))


main()
