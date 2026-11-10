"""Lab FI6-L02-1: SOFR Compounding in Arrears and the ISDA Fallback Spread.

SIMULATED: Daily overnight SOFR path with weekend weighting, computing the
backward-looking compounded rate R_comp across observation conventions,
and demonstrating the 5-year historical median spread calibration.
"""

from __future__ import annotations


def compound_sofr_arrears(daily_rates: list[float], day_weights: list[int], day_count_basis: int = 360) -> float:
    """Calculate the compounded in arrears overnight rate according to ISDA/ARRC convention.

    Formula: R_comp = (360 / d_total) * [ prod_{i=1}^n (1 + r_i * n_i / 360) - 1 ]
    """
    total_days = sum(day_weights)
    prod = 1.0
    for r, n in zip(daily_rates, day_weights, strict=False):
        prod *= 1.0 + (r * n / float(day_count_basis))
    return float(day_count_basis) / float(total_days) * (prod - 1.0)


def simple_average_sofr(daily_rates: list[float], day_weights: list[int]) -> float:
    """Calculate simple weighted average of overnight SOFR rates."""
    total_days = sum(day_weights)
    return sum(r * n for r, n in zip(daily_rates, day_weights, strict=False)) / float(total_days)


def run_lab() -> None:
    print("=== SOFR Compounding in Arrears & ISDA Fallback Spread ===")

    # Simulated 90 calendar day quarter (65 business days, with weekend weights = 3 on Fridays)
    # Baseline SOFR starting at 4.30%, gradually rising to 4.55%
    import random

    rng = random.Random(42)
    base_rate = 0.0430
    daily_sofr: list[float] = []
    day_weights: list[int] = []

    calendar_days = 0
    day_idx = 0
    while calendar_days < 90:
        # 5-day work week: days 0, 1, 2, 3 have weight 1; day 4 (Friday) has weight 3
        weekday = day_idx % 5
        weight = 3 if weekday == 4 else 1
        calendar_days += weight
        # Shock with slight mean reversion
        rate = base_rate + 0.0025 * (calendar_days / 90.0) + rng.gauss(0.0, 0.0003)
        daily_sofr.append(rate)
        day_weights.append(weight)
        day_idx += 1

    r_comp = compound_sofr_arrears(daily_sofr, day_weights)
    r_avg = simple_average_sofr(daily_sofr, day_weights)
    compounding_effect_bps = (r_comp - r_avg) * 10000.0

    print(f"Observation Period       : {calendar_days} calendar days ({len(daily_sofr)} business days)")
    print(f"Daily SOFR Range         : {min(daily_sofr) * 100.0:.3f}% - {max(daily_sofr) * 100.0:.3f}%")
    print(f"Simple Weighted Average  : {r_avg * 100.0:.5f}% ({r_avg * 10000.0:.2f} bps)")
    print(f"Compounded in Arrears    : {r_comp * 100.0:.5f}% ({r_comp * 10000.0:.2f} bps)")
    print(f"Compounding Effect       : +{compounding_effect_bps:.3f} bps")

    # Observation Shift vs Payment Delay
    # With a 2-business-day observation shift, the rate weighting aligns with the observation period
    # while payment delay shifts the payment date without shifting observation dates
    print("\n--- Observation Conventions ---")
    print("Lookback with Observation Shift: Day weights determine interest weighting based on observation window.")
    print("Payment Delay: Interest weights strictly follow the interest accrual period dates.")

    # ISDA 5-Year Historical Fallback Spread Adjustment
    # On March 5, 2021, Bloomberg/ISDA fixed the 5-year historical median spread
    # for USD 3M LIBOR vs 3M SOFR at 26.161 bps.
    # Demonstrate median spread calculation over a simulated 5-year sample (20 quarterly observations)
    # where LIBOR = Compounded SOFR + credit/term risk premium
    libor_spreads_bps = [
        24.2,
        25.1,
        27.8,
        31.2,
        26.5,
        25.9,
        28.3,
        26.1,
        25.8,
        26.4,
        26.2,
        27.0,
        24.8,
        25.4,
        29.5,
        28.1,
        26.161,
        25.7,
        26.8,
        26.0,
    ]
    libor_spreads_sorted = sorted(libor_spreads_bps)
    n_obs = len(libor_spreads_sorted)
    median_spread = (libor_spreads_sorted[n_obs // 2 - 1] + libor_spreads_sorted[n_obs // 2]) / 2.0

    print("\n--- ISDA 2020 IBOR Fallbacks Protocol Spread ---")
    print(f"Sample Observations      : {n_obs} historical quarters")
    print("Official USD 3M Spread   : 26.161 bps (Bloomberg/ISDA benchmark)")
    print(f"Sample Median Spread     : {median_spread:.3f} bps")
    print(f"Fallback All-in Rate     : Compounded SOFR + 26.161 bps = {(r_comp + 0.0026161) * 100.0:.4f}%")


run_lab()
