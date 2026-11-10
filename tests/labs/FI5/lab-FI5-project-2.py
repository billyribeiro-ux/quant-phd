"""Lab FI5-project-2: Inflation-expectations decomposition completion problem (Rung 2).

Solution twin for the completion problem: implements deflation floor protected principal
and the fundamental tripartite decomposition formula for the inflation risk premium.
"""

from __future__ import annotations


def compute_completion_components(
    base_cpi: float,
    ref_cpi: float,
    face_value: float,
    nominal_yield: float,
    real_yield: float,
    survey_inflation: float,
    tlp: float,
) -> tuple[float, float, float]:
    """Compute deflation-protected principal, breakeven inflation, and inflation risk premium."""
    index_ratio = ref_cpi / base_cpi

    # Blank 1 in completion problem: principal with deflation floor
    adjusted_principal = max(1.0, index_ratio) * face_value

    # Breakeven inflation
    bei = nominal_yield - real_yield

    # Blank 2 in completion problem: inflation risk premium from tripartite identity
    irp = bei - survey_inflation + tlp

    return index_ratio, adjusted_principal, irp


def main() -> None:
    # Deflationary stress scenario inputs
    base_cpi = 250.00
    ref_cpi = 237.50  # Cumulative deflation: index ratio = 0.95
    face_value = 100.00

    nominal_yield = 0.0350  # 3.50%
    real_yield = 0.0210  # 2.10% -> BEI = 1.40%
    survey_inflation = 0.0180  # 1.80%
    tlp = 0.0060  # 0.60% (60 bps TIPS illiquidity penalty)

    idx_ratio, adj_principal, irp = compute_completion_components(
        base_cpi, ref_cpi, face_value, nominal_yield, real_yield, survey_inflation, tlp
    )

    print("Completed Inflation Expectations Analytics (SIMULATED):")
    print(f"  Calculated Index Ratio:         {idx_ratio:.4f}")
    print(f"  Deflation Protected Principal: ${adj_principal:.2f}")
    print(f"  Breakeven Inflation (BEI):      {(nominal_yield - real_yield) * 10_000:.1f} bps")
    print(f"  Expected Inflation E[pi]:       {survey_inflation * 10_000:.1f} bps")
    print(f"  TIPS Liquidity Premium (TLP):   {tlp * 10_000:.1f} bps")
    print(f"  Derived Inflation Risk Premium: {irp * 10_000:.1f} bps")


main()
