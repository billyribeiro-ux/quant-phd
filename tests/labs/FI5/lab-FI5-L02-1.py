"""Lab FI5-L02-1: Breakeven inflation curve construction, Fisher relation, and carry attribution.

Standard library only. Computes nominal-real breakeven inflation rates across maturities,
quantifies the compounding cross-product wedge in the Fisher relation, prices zero-coupon
inflation swaps (ZCIS), and attributes 3-month horizon carry under seasonal CPI dynamics.
"""

from __future__ import annotations

from typing import Any


def compute_breakeven_curve(
    nominal_yields: dict[int, float],
    real_yields: dict[int, float],
) -> list[dict[str, Any]]:
    """Compute breakeven inflation rates and Fisher compounding wedges.

    Linear breakeven: BEI_lin = y_N - y_R
    Exact geometric breakeven: BEI_geom = (1 + y_N) / (1 + y_R) - 1
    Compounding wedge: BEI_lin - BEI_geom = y_R * BEI_geom
    """
    maturities = sorted(set(nominal_yields.keys()) & set(real_yields.keys()))
    curve = []

    for mat in maturities:
        y_n = nominal_yields[mat]
        y_r = real_yields[mat]
        bei_linear = y_n - y_r
        bei_geometric = (1.0 + y_n) / (1.0 + y_r) - 1.0
        wedge_bps = (bei_linear - bei_geometric) * 10_000.0

        curve.append(
            {
                "maturity": mat,
                "nominal_yield": y_n,
                "real_yield": y_r,
                "bei_linear": bei_linear,
                "bei_geometric": bei_geometric,
                "wedge_bps": wedge_bps,
            }
        )

    return curve


def price_zero_coupon_inflation_swap(
    maturity_years: int,
    nominal_discount_factor: float,
    expected_inflation_rate: float,
) -> dict[str, float]:
    """Price a Zero-Coupon Inflation Swap (ZCIS) under no-arbitrage.

    At maturity T, floating leg pays: [CPI_T / CPI_0 - 1] * Notional
    Fixed leg pays: [(1 + S)^T - 1] * Notional
    Par swap rate S satisfies: (1 + S)^T = E[CPI_T / CPI_0]
    """
    compounded_factor = (1.0 + expected_inflation_rate) ** maturity_years
    par_swap_rate = compounded_factor ** (1.0 / maturity_years) - 1.0

    pv_floating = nominal_discount_factor * (compounded_factor - 1.0)
    pv_fixed_at_par = nominal_discount_factor * ((1.0 + par_swap_rate) ** maturity_years - 1.0)

    return {
        "maturity": float(maturity_years),
        "par_swap_rate": par_swap_rate,
        "pv_floating": pv_floating,
        "pv_fixed_at_par": pv_fixed_at_par,
        "net_pv_par": pv_floating - pv_fixed_at_par,
    }


def attribute_breakeven_carry(
    nominal_yield: float,
    real_yield: float,
    horizon_years: float,
    expected_annual_cpi_growth: float,
    seasonal_adjustment_annualized: float,
) -> dict[str, float]:
    """Attribute horizon carry on a long TIPS / short Treasury breakeven position.

    Carry consists of:
    1. Yield carry: Real coupon accrual minus Nominal coupon accrual: (y_R - y_N) * dt
    2. Inflation accrual carry: Actual CPI index growth: (pi + s) * dt
    3. Net carry: Yield carry + Inflation accrual carry
    """
    dt = horizon_years
    yield_carry_pct = (real_yield - nominal_yield) * dt * 100.0
    total_cpi_rate = expected_annual_cpi_growth + seasonal_adjustment_annualized
    inflation_accrual_pct = total_cpi_rate * dt * 100.0
    net_carry_pct = yield_carry_pct + inflation_accrual_pct
    net_carry_bps = net_carry_pct * 100.0

    return {
        "horizon_months": dt * 12.0,
        "yield_carry_bps": yield_carry_pct * 100.0,
        "inflation_accrual_bps": inflation_accrual_pct * 100.0,
        "net_carry_bps": net_carry_bps,
    }


def main() -> None:
    # 1. Breakeven Inflation Curve Construction (SIMULATED UST & TIPS yields)
    nominal_yields = {2: 0.0435, 5: 0.0410, 10: 0.0425, 30: 0.0450}
    real_yields = {2: 0.0185, 5: 0.0175, 10: 0.0190, 30: 0.0215}

    curve = compute_breakeven_curve(nominal_yields, real_yields)

    print("Breakeven Inflation Term Structure (SIMULATED):")
    print("  Tenor  Nominal Yld  Real Yld  Linear BEI  Geom BEI  Fisher Wedge")
    for row in curve:
        print(
            f"   {row['maturity']:2d}Y      {row['nominal_yield']:.2%}     "
            f"{row['real_yield']:.2%}     {row['bei_linear']:.2%}     "
            f"{row['bei_geometric']:.2%}     {row['wedge_bps']:+5.1f} bps"
        )

    # 2. Zero-Coupon Inflation Swap (ZCIS) Pricing
    # 10-year maturity, nominal DF = 0.655, expected inflation = 2.30%
    zcis = price_zero_coupon_inflation_swap(
        maturity_years=10,
        nominal_discount_factor=0.655,
        expected_inflation_rate=0.0230,
    )
    print("\n10Y Zero-Coupon Inflation Swap Par Pricing:")
    print(f"  Maturity:                 {zcis['maturity']:.0f} years")
    print(f"  Par Inflation Swap Rate:  {zcis['par_swap_rate']:.2%}")
    print(f"  Floating Leg PV (per $1): {zcis['pv_floating']:.4f}")
    print(f"  Fixed Leg PV (per $1):    {zcis['pv_fixed_at_par']:.4f}")
    print(f"  Net Par Discrepancy:      {zcis['net_pv_par']:+.1e}")

    # 3. 3-Month Breakeven Carry Attribution (Spring vs Autumn Seasonality)
    # 10Y BEI position: Long 10Y TIPS, Short 10Y Treasury
    # Spring: CPI seasonally high (+1.20% annualized boost)
    carry_spring = attribute_breakeven_carry(
        nominal_yield=0.0425,
        real_yield=0.0190,
        horizon_years=0.25,
        expected_annual_cpi_growth=0.0235,
        seasonal_adjustment_annualized=+0.0120,
    )
    # Autumn: CPI seasonally weak (-1.00% annualized drag)
    carry_autumn = attribute_breakeven_carry(
        nominal_yield=0.0425,
        real_yield=0.0190,
        horizon_years=0.25,
        expected_annual_cpi_growth=0.0235,
        seasonal_adjustment_annualized=-0.0100,
    )

    print("\n3-Month Breakeven Carry Attribution (Long TIPS / Short Nominal):")
    print("  Component                  Spring (Positive)  Autumn (Negative)")
    sp_yc = carry_spring["yield_carry_bps"]
    au_yc = carry_autumn["yield_carry_bps"]
    sp_ia = carry_spring["inflation_accrual_bps"]
    au_ia = carry_autumn["inflation_accrual_bps"]
    sp_nc = carry_spring["net_carry_bps"]
    au_nc = carry_autumn["net_carry_bps"]
    print(f"  Yield Carry (y_R - y_N):      {sp_yc:+6.1f} bps      {au_yc:+6.1f} bps")
    print(f"  Inflation Accrual:            {sp_ia:+6.1f} bps      {au_ia:+6.1f} bps")
    print(f"  Net Horizon Carry:            {sp_nc:+6.1f} bps      {au_nc:+6.1f} bps")


main()
