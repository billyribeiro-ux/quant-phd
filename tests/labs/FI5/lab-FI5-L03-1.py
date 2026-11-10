"""Lab FI5-L03-1: Tripartite decomposition of breakeven inflation: expectations, IRP, and TLP.

Standard library only. Decomposes breakeven inflation rates into survey-adjusted expected
inflation, the inflation risk premium (IRP), and the TIPS liquidity premium (TLP),
following D'Amico, Kim, and Wei (2018) and Campbell, Sunderam, and Viceira (2017).
"""

from __future__ import annotations

from typing import Any


def decompose_breakeven(
    nominal_yield: float,
    real_yield: float,
    expected_inflation: float,
    tips_liquidity_premium: float,
) -> dict[str, float]:
    """Perform the fundamental tripartite decomposition of breakeven inflation.

    BEI = y_N - y_R
    Identity: BEI = E[pi] + IRP - TLP
    Therefore: IRP = BEI - E[pi] + TLP
    """
    bei = nominal_yield - real_yield
    irp = bei - expected_inflation + tips_liquidity_premium

    # Identity check to machine precision
    reconstructed_bei = expected_inflation + irp - tips_liquidity_premium
    discrepancy = abs(bei - reconstructed_bei)

    return {
        "nominal_yield": nominal_yield,
        "real_yield": real_yield,
        "bei": bei,
        "expected_inflation": expected_inflation,
        "tips_liquidity_premium": tips_liquidity_premium,
        "inflation_risk_premium": irp,
        "identity_discrepancy": discrepancy,
    }


def analyze_historical_regimes(
    regimes: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Analyze tripartite decomposition across distinct market stress episodes."""
    results = []
    for reg in regimes:
        decomp = decompose_breakeven(
            nominal_yield=reg["y_n"],
            real_yield=reg["y_r"],
            expected_inflation=reg["exp_pi"],
            tips_liquidity_premium=reg["tlp"],
        )
        results.append(
            {
                "regime": reg["name"],
                "bei_bps": decomp["bei"] * 10_000.0,
                "exp_pi_bps": decomp["expected_inflation"] * 10_000.0,
                "tlp_bps": decomp["tips_liquidity_premium"] * 10_000.0,
                "irp_bps": decomp["inflation_risk_premium"] * 10_000.0,
            }
        )
    return results


def main() -> None:
    # 1. 10-Year Breakeven Tripartite Decomposition (SIMULATED D'Amico et al. calibration)
    # y_N = 4.25%, y_R = 1.95% -> BEI = 2.30% (230 bps)
    # Expected Inflation (Survey/SPF) = 2.05% (205 bps)
    # TIPS Liquidity Premium (TLP) = 0.20% (20 bps)
    decomp_baseline = decompose_breakeven(
        nominal_yield=0.0425,
        real_yield=0.0195,
        expected_inflation=0.0205,
        tips_liquidity_premium=0.0020,
    )

    print("10Y Breakeven Tripartite Decomposition (Baseline SIMULATED):")
    print(f"  Nominal Yield (y_N):           {decomp_baseline['nominal_yield']:.2%}")
    print(f"  Real TIPS Yield (y_R):         {decomp_baseline['real_yield']:.2%}")
    print(f"  Breakeven Inflation (BEI):     {decomp_baseline['bei'] * 10_000:.1f} bps")
    print(f"  Expected Inflation E[pi]:      {decomp_baseline['expected_inflation'] * 10_000:.1f} bps")
    print(f"  TIPS Liquidity Premium (TLP):  {decomp_baseline['tips_liquidity_premium'] * 10_000:.1f} bps")
    print(f"  Inflation Risk Premium (IRP):  {decomp_baseline['inflation_risk_premium'] * 10_000:.1f} bps")
    print(f"  Identity Discrepancy:          {decomp_baseline['identity_discrepancy']:.1e}")

    # 2. Historical Stress Regimes Comparison
    # Regime 1: Mid-2006 (Orderly pre-crisis, positive IRP, low TLP)
    # Regime 2: October 2008 (Lehman GFC crisis: acute TLP spike, depressed BEI)
    # Regime 3: Mid-2022 (Inflation surge: elevated E[pi], low TLP, positive IRP)
    regimes_data = [
        {"name": "2006 Pre-Crisis", "y_n": 0.0510, "y_r": 0.0255, "exp_pi": 0.0210, "tlp": 0.0015},
        {"name": "2008 Lehman GFC", "y_n": 0.0380, "y_r": 0.0335, "exp_pi": 0.0180, "tlp": 0.0190},
        {"name": "2022 Inflation Surge", "y_n": 0.0310, "y_r": 0.0030, "exp_pi": 0.0250, "tlp": 0.0010},
    ]

    regime_results = analyze_historical_regimes(regimes_data)

    print("\nHistorical Regime Comparison (SIMULATED Stylized Data):")
    print("  Regime               BEI (bps)   E[pi] (bps)   TLP (bps)   IRP (bps)")
    for r in regime_results:
        print(
            f"  {r['regime']:<20s} {r['bei_bps']:>8.1f}   {r['exp_pi_bps']:>10.1f}   "
            f"{r['tlp_bps']:>8.1f}   {r['irp_bps']:>8.1f}"
        )


main()
