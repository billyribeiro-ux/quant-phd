"""Lab E7-L05-1: The Zero Lower Bound and Forward Guidance Yield Curve Response.

Simulates the term structure of interest rates under:
1. Unconstrained Taylor rule
2. Binding Zero Lower Bound (ZLB: i_t = max(0, i_t^Taylor))
3. Odyssean Forward Guidance committing to hold rates at zero for tau quarters beyond Liftoff.

Calculates the shadow rate and the long-term yield response via the expectations hypothesis.
"""

from __future__ import annotations


def calculate_yield_curve_under_zlb(
    shadow_rates: list[float],
    guidance_quarters: int,
) -> dict[str, list[float]]:
    """Compute realized policy rate path and zero-coupon yields for maturities 1..N quarters."""
    n = len(shadow_rates)
    zlb_rates: list[float] = []

    # Identify liftoff quarter in unconstrained path
    liftoff_quarter = 0
    for t, s in enumerate(shadow_rates):
        if s > 0.0:
            liftoff_quarter = t
            break

    effective_liftoff = liftoff_quarter + guidance_quarters

    for t, s in enumerate(shadow_rates):
        if t < effective_liftoff:
            zlb_rates.append(0.0)
        else:
            zlb_rates.append(max(0.0, s))

    # Yields for maturities m = 1 .. 8 quarters from date 0 under expectations hypothesis
    unconstrained_yields: list[float] = []
    zlb_yields: list[float] = []

    for m in range(1, min(9, n + 1)):
        y_uncon = sum(shadow_rates[:m]) / float(m)
        y_zlb = sum(zlb_rates[:m]) / float(m)
        unconstrained_yields.append(y_uncon)
        zlb_yields.append(y_zlb)

    return {
        "zlb_rates": zlb_rates,
        "unconstrained_yields": unconstrained_yields,
        "zlb_yields": zlb_yields,
    }


def main() -> None:
    # Deep recession shadow rate path over 12 quarters (in % annualized)
    shadow_path = [-2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 2.5]

    # Baseline ZLB without forward guidance (guidance_quarters = 0)
    base = calculate_yield_curve_under_zlb(shadow_path, guidance_quarters=0)

    # Odyssean Forward Guidance: commit to 2 extra quarters at zero (guidance_quarters = 2)
    guidance = calculate_yield_curve_under_zlb(shadow_path, guidance_quarters=2)

    print("Zero Lower Bound and Forward Guidance Dynamics:")
    print("  Date (Q) | Shadow Rate | Standard ZLB | Forward Guidance (tau=2)")
    for q in range(8):
        sq = f"{shadow_path[q]:6.2f}%"
        bq = f"{base['zlb_rates'][q]:5.2f}%"
        gq = f"{guidance['zlb_rates'][q]:5.2f}%"
        print(f"    Q{q:02d}    |   {sq}   |    {bq}    |         {gq}")

    print("\nExpectations Hypothesis Yields (at t=0):")
    print("  Maturity | Unconstrained | Baseline ZLB | With Guidance | Guidance Impact")
    for m in range(1, 9):
        uncon = base["unconstrained_yields"][m - 1]
        zlb = base["zlb_yields"][m - 1]
        fg = guidance["zlb_yields"][m - 1]
        impact_bps = (fg - zlb) * 100.0
        print(f"   {m}Q bond  |    {uncon:6.2f}%    |    {zlb:5.2f}%   |    {fg:5.2f}%    |    {impact_bps:5.1f} bps")


main()
