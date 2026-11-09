"""Lab FI1-L05-1: Duration, convexity, and DV01 with numerical finite-difference verification.

SIMULATED: 10-year fixed coupon bond evaluated at a semiannual yield.
Calculates analytical Macaulay duration, modified duration, convexity, and DV01,
holding them to central finite differences.
Standard library only; no network.
"""

from __future__ import annotations


def bond_price(face: float, coupon: float, periods: int, y: float) -> float:
    """Calculate bond price from periodic yield y."""
    v = 1.0 / (1.0 + y)
    annuity = (1.0 - v**periods) / y if y != 0.0 else float(periods)
    return coupon * annuity + face * (v**periods)


def main() -> None:
    face = 1000.0  # $1,000.00 face value
    coupon_annual = 0.05  # 5.0% annual coupon
    m = 2  # semiannual compounding frequency
    periods = 20  # 10 years * 2 = 20 periods
    c = (coupon_annual * face) / m  # $25.00 per period
    y_annual = 0.06  # 6.0% annual yield
    y = y_annual / m  # 3.0% yield per period

    # 1. Base price
    p0 = bond_price(face, c, periods, y)
    print(f"Bond Characteristics (Face = ${face:.2f}, Coupon = {coupon_annual:.1%}, 10yr Semiannual):")
    print(f"  Yield = {y_annual:.2%} per annum ({y:.2%} per period)")
    print(f"  Price P = ${p0:.4f}")

    # 2. Analytical Greeks
    # Macaulay duration in periods
    sum_t_cf = sum(k * c / ((1.0 + y) ** k) for k in range(1, periods + 1))
    sum_t_cf += periods * face / ((1.0 + y) ** periods)
    d_mac_periods = sum_t_cf / p0
    d_mac_years = d_mac_periods / m

    # Modified duration: D_mod = D_mac / (1 + y)
    d_mod_periods = d_mac_periods / (1.0 + y)
    d_mod_annual = d_mod_periods / m

    # Convexity: C = (1/P) * d^2 P / dy^2
    sum_t_t1_cf = sum(k * (k + 1) * c / ((1.0 + y) ** k) for k in range(1, periods + 1))
    sum_t_t1_cf += periods * (periods + 1) * face / ((1.0 + y) ** periods)
    convexity_periods = sum_t_t1_cf / (p0 * ((1.0 + y) ** 2))
    convexity_annual = convexity_periods / (m**2)

    # DV01: price change for 1 bp (0.0001) shift in annual yield
    dv01_analytic = p0 * d_mod_annual * 0.0001

    print("\nAnalytical Sensitivity Metrics:")
    print(f"  Macaulay Duration = {d_mac_years:.4f} years ({d_mac_periods:.4f} periods)")
    print(f"  Modified Duration = {d_mod_annual:.4f} years ({d_mod_periods:.4f} per period)")
    print(f"  Convexity         = {convexity_annual:.4f} years^2")
    print(f"  DV01              = ${dv01_analytic:.4f} per $1000 face")

    # 3. Numerical Verification via Central Finite Differences
    # Step size in annual yield
    h_annual = 1e-5
    h_period = h_annual / m

    p_up = bond_price(face, c, periods, y + h_period)
    p_down = bond_price(face, c, periods, y - h_period)

    # Numerical first derivative w.r.t annual yield
    dp_dy_num = (p_up - p_down) / (2.0 * h_annual)
    d_mod_num = -dp_dy_num / p0
    dv01_num = -(p_up - p_down) / (2.0 * h_annual) * 0.0001

    # Numerical second derivative w.r.t annual yield
    d2p_dy2_num = (p_up - 2.0 * p0 + p_down) / (h_annual**2)
    convexity_num = d2p_dy2_num / p0

    print("\nFinite-Difference Verification (step size h = 1e-5):")
    print(f"  Modified Duration (Numerical) = {d_mod_num:.4f}, |Error| = {abs(d_mod_num - d_mod_annual):.2e}")
    print(
        f"  Convexity (Numerical)         = {convexity_num:.4f}, |Error| = {abs(convexity_num - convexity_annual):.2e}"
    )
    print(f"  DV01 (Numerical)              = ${dv01_num:.4f}, |Error| = {abs(dv01_num - dv01_analytic):.2e}")

    assert abs(d_mod_num - d_mod_annual) < 1e-7
    assert abs(convexity_num - convexity_annual) < 1e-5
    assert abs(dv01_num - dv01_analytic) < 1e-7
    print("All sensitivity formulas verified against finite differences.")


main()
