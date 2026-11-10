"""Lab FI5-project-1: Inflation-expectations decomposition worked example (Rung 1).

A fully worked implementation of the inflation-expectations decomposition pipeline.
Analyzes TIPS mechanics, computes breakevens, replicates synthetic Treasuries,
measures the Fleckenstein puzzle basis, and decomposes breakevens into expected inflation,
the inflation risk premium, and the TIPS liquidity premium.
"""

from __future__ import annotations

from typing import Any


def run_pipeline(
    nominal_yield: float,
    real_yield: float,
    survey_inflation: float,
    liquidity_proxy: float,
    beta_liq: float,
    base_cpi: float,
    ref_cpi: float,
    real_coupon: float,
    maturity_years: int,
    cash_price: float,
    swap_rate: float,
    mod_duration: float,
) -> dict[str, Any]:
    """Execute end-to-end inflation expectations decomposition pipeline."""
    # 1. Breakeven yield
    bei = nominal_yield - real_yield

    # 2. TIPS cash flows with deflation floor
    index_ratio = ref_cpi / base_cpi
    face = 100.0
    adjusted_coupon = face * (real_coupon / 2.0) * index_ratio
    adjusted_principal = face * max(1.0, index_ratio)
    floor_benefit = face * max(0.0, 1.0 - index_ratio)

    # 3. Synthetic Treasury replication & puzzle basis
    synth_yield = (1.0 + real_yield) * (1.0 + swap_rate) - 1.0
    # Approximate synthetic price via yield difference from nominal
    synth_price = cash_price * (1.0 - mod_duration * (synth_yield - nominal_yield))
    price_basis = cash_price - synth_price
    yield_basis_bps = (price_basis / (cash_price * mod_duration)) * 10_000.0

    # 4. Tripartite breakeven decomposition
    tlp = beta_liq * liquidity_proxy
    irp = bei - survey_inflation + tlp

    return {
        "bei_bps": bei * 10_000.0,
        "index_ratio": index_ratio,
        "adjusted_coupon": adjusted_coupon,
        "adjusted_principal": adjusted_principal,
        "floor_benefit": floor_benefit,
        "synth_yield": synth_yield,
        "price_basis": price_basis,
        "yield_basis_bps": yield_basis_bps,
        "expected_inflation_bps": survey_inflation * 10_000.0,
        "tlp_bps": tlp * 10_000.0,
        "irp_bps": irp * 10_000.0,
    }


def main() -> None:
    # Stylized inputs for 10-year maturity
    res = run_pipeline(
        nominal_yield=0.0425,
        real_yield=0.0195,
        survey_inflation=0.0205,
        liquidity_proxy=0.0020,
        beta_liq=1.0,
        base_cpi=260.00,
        ref_cpi=299.00,
        real_coupon=0.0150,
        maturity_years=10,
        cash_price=101.50,
        swap_rate=0.0235,
        mod_duration=8.40,
    )

    print("Inflation Expectations Decomposition Pipeline (Worked Example):")
    print("=" * 68)
    print(f"  Breakeven Inflation (BEI):         {res['bei_bps']:>6.1f} bps")
    print(f"  TIPS Index Ratio:                  {res['index_ratio']:>8.4f}")
    print(f"  Adjusted Semiannual Coupon:       ${res['adjusted_coupon']:>6.2f} per $100 par")
    p_adj = res["adjusted_principal"]
    fl_ben = res["floor_benefit"]
    print(f"  Adjusted Principal (Maturity):    ${p_adj:>6.2f} (Floor: ${fl_ben:.2f})")
    print(f"  Synthetic Treasury Yield:          {res['synth_yield']:.2%}")
    print(f"  Puzzle Mispricing Price Basis:    ${res['price_basis']:>6.3f} per $100 par")
    print(f"  Puzzle Implied Yield Basis:        {res['yield_basis_bps']:>6.1f} bps")
    print("-" * 68)
    print("  Tripartite Decomposition of Breakeven:")
    print(f"    Expected Inflation E[pi]:        {res['expected_inflation_bps']:>6.1f} bps")
    print(f"    TIPS Liquidity Premium (TLP):    {res['tlp_bps']:>6.1f} bps")
    print(f"    Inflation Risk Premium (IRP):    {res['irp_bps']:>6.1f} bps")
    print(
        f"    Identity Check: E[pi] + IRP - TLP = "
        f"{res['expected_inflation_bps'] + res['irp_bps'] - res['tlp_bps']:.1f} bps"
    )
    print("=" * 68)


main()
