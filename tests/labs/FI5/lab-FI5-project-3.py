"""Lab FI5-project-3: Rung 3 independent project verification check.

Validates the full inflation expectations decomposition and TIPS-Treasury puzzle
pricing engine across three stylized historical regimes: the 2008 GFC liquidity dislocation,
the 2017 low-inflation calm, and the 2022 post-pandemic inflation surge.
"""

from __future__ import annotations

from typing import Any


def evaluate_market_regime(
    regime_name: str,
    nominal_yield: float,
    real_yield: float,
    survey_inflation: float,
    tlp: float,
    cash_price: float,
    synth_price: float,
    mod_duration: float,
) -> dict[str, Any]:
    """Evaluate decomposition and puzzle basis for a market regime."""
    bei = nominal_yield - real_yield
    irp = bei - survey_inflation + tlp
    price_basis = cash_price - synth_price
    yield_basis_bps = (price_basis / (cash_price * mod_duration)) * 10_000.0

    # Diagnosis of dominant economic driver
    if tlp > 0.010:
        diagnosis = "Acute TIPS Illiquidity Dislocation"
    elif irp < 0.0:
        diagnosis = "Nominal Bonds as Deflation Hedges (Negative IRP)"
    else:
        diagnosis = "Procyclical Inflation Risk / Term Premium Expansion"

    return {
        "regime": regime_name,
        "nominal_yield_pct": nominal_yield * 100.0,
        "real_yield_pct": real_yield * 100.0,
        "bei_bps": bei * 10_000.0,
        "survey_inflation_bps": survey_inflation * 10_000.0,
        "tlp_bps": tlp * 10_000.0,
        "irp_bps": irp * 10_000.0,
        "price_basis": price_basis,
        "yield_basis_bps": yield_basis_bps,
        "diagnosis": diagnosis,
    }


def main() -> None:
    # Three historical episodes (SIMULATED stylized market parameters)
    episodes = [
        evaluate_market_regime(
            regime_name="October 2008 GFC Dislocation",
            nominal_yield=0.0380,
            real_yield=0.0335,
            survey_inflation=0.0175,
            tlp=0.0185,  # 185 bps TIPS liquidity discount
            cash_price=103.50,
            synth_price=98.80,
            mod_duration=8.20,
        ),
        evaluate_market_regime(
            regime_name="2017 Secular Stagnation Calm",
            nominal_yield=0.0235,
            real_yield=0.0050,
            survey_inflation=0.0195,
            tlp=0.0015,  # 15 bps orderly market
            cash_price=101.20,
            synth_price=100.40,
            mod_duration=8.80,
        ),
        evaluate_market_regime(
            regime_name="2022 Post-Pandemic Inflation Shock",
            nominal_yield=0.0385,
            real_yield=0.0090,
            survey_inflation=0.0250,
            tlp=0.0010,  # 10 bps orderly market
            cash_price=99.50,
            synth_price=98.50,
            mod_duration=8.50,
        ),
    ]

    print("Inflation Expectations Decomposition: Historical Regime Verification (SIMULATED):")
    print("=" * 86)
    for ep in episodes:
        print(f"Episode: {ep['regime']}")
        print(f"  Nominal / Real Yields:       {ep['nominal_yield_pct']:.2f}% / {ep['real_yield_pct']:.2f}%")
        print(f"  Breakeven Inflation (BEI):   {ep['bei_bps']:>6.1f} bps")
        print(f"  Survey Expected Inflation:   {ep['survey_inflation_bps']:>6.1f} bps")
        print(f"  TIPS Liquidity Premium (TLP):{ep['tlp_bps']:>6.1f} bps")
        print(f"  Inflation Risk Premium (IRP):{ep['irp_bps']:>6.1f} bps")
        pb = ep["price_basis"]
        yb = ep["yield_basis_bps"]
        print(f"  Fleckenstein Puzzle Basis:   ${pb:.2f} per $100 par ({yb:>5.1f} bps)")
        print(f"  Diagnosed Market Mechanism:  {ep['diagnosis']}")
        print("-" * 86)


main()
