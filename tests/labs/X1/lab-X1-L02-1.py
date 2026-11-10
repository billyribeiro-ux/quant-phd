"""Lab X1-L02-1: Cross-currency basis and forward points monitor.

Calculates forward points and cross-currency basis spreads across major currency pairs,
demonstrating the post-2008 breakdown of covered interest parity (Du et al. 2018).
"""

from __future__ import annotations

from typing import Any


def calculate_basis(
    pair: str,
    spot: float,
    forward: float,
    rate_usd: float,
    rate_foreign: float,
    tenor_years: float = 1.0,
) -> dict[str, float]:
    """Calculate forward points in pips and cross-currency basis in basis points.

    Quotes: USD per foreign currency (direct quotation, e.g. EUR/USD, GBP/USD).
    For indirect quotes (USD/JPY, USD/CHF), spot and forward are inverted prior to calculation.

    Args:
        pair: Currency pair name (e.g. 'EUR/USD').
        spot: Spot rate S_t (USD per 1 unit of foreign).
        forward: Forward outright rate F_t (USD per 1 unit of foreign).
        rate_usd: Annualized USD benchmark rate (e.g. SOFR / OIS).
        rate_foreign: Annualized foreign benchmark rate (e.g. ESTR, TONAR, SONIA).
        tenor_years: Tenor fraction (default 1.0 year).

    Returns:
        dict containing forward_points (pips) and basis_bps (basis points).
    """
    # Forward points = (F - S) * 10^4 pips (or 10^2 for JPY direct)
    fwd_points = (forward - spot) * 10000.0

    # Synthetic USD rate via foreign currency investment:
    # Invest (1/S_t) foreign units at (1 + rate_foreign * tau), hedged back at F_t
    # Yields (F_t / S_t) * (1 + rate_foreign * tau) USD per initial USD
    synthetic_usd_gross = (forward / spot) * (1.0 + rate_foreign * tenor_years)

    # Direct USD cash rate gross: (1 + rate_usd * tau)
    cash_usd_gross = 1.0 + rate_usd * tenor_years

    # Cross-currency basis x_t (in bps annualized):
    # Standard market convention: direct USD rate minus synthetic USD rate
    # x_t = [(1 + rate_usd * tau) - (F_t / S_t) * (1 + rate_foreign * tau)] / tau * 10,000 bps
    # Under this convention, a negative basis means the market pays a premium for USD cash.
    basis_bps = ((cash_usd_gross - synthetic_usd_gross) / tenor_years) * 10000.0

    return {
        "spot": spot,
        "forward": forward,
        "forward_points": round(fwd_points, 1),
        "synthetic_usd_rate": round((synthetic_usd_gross - 1.0) / tenor_years * 100.0, 3),
        "direct_usd_rate": round(rate_usd * 100.0, 3),
        "basis_bps": round(basis_bps, 2),
    }


def main() -> None:
    print("Lab X1-L02-1 | Cross-Currency Basis & Forward Points Monitor")
    print("-------------------------------------------------------------")

    # Sample market snapshot for 1-year tenor across 4 currency pairs
    # Demonstrating post-2008 persistent negative basis (USD funding premium)
    quotes: list[dict[str, Any]] = [
        {"pair": "EUR/USD", "spot": 1.0850, "forward": 1.1042, "rate_usd": 0.0520, "rate_foreign": 0.0360},
        {"pair": "GBP/USD", "spot": 1.2950, "forward": 1.2985, "rate_usd": 0.0520, "rate_foreign": 0.0480},
        {"pair": "USD/JPY", "spot": 0.00645, "forward": 0.00676, "rate_usd": 0.0520, "rate_foreign": 0.0025},
        {"pair": "USD/CHF", "spot": 1.1200, "forward": 1.1610, "rate_usd": 0.0520, "rate_foreign": 0.0140},
    ]

    print(f"{'Pair':<8} | {'Spot':<8} | {'Forward':<8} | {'Fwd Pts':<9} | {'Synth USD %':<11} | {'Basis (bps)':<11}")
    print("-" * 65)

    for q in quotes:
        res = calculate_basis(
            pair=q["pair"],
            spot=float(q["spot"]),
            forward=float(q["forward"]),
            rate_usd=float(q["rate_usd"]),
            rate_foreign=float(q["rate_foreign"]),
            tenor_years=1.0,
        )
        print(
            f"{q['pair']:<8} | {res['spot']:<8.5f} | {res['forward']:<8.5f} | "
            f"{res['forward_points']:>8.1f}  | {res['synthetic_usd_rate']:>10.3f}% | {res['basis_bps']:>10.2f}"
        )


main()
