"""Lab FI1-L06-1: Bootstrapping the zero curve from coupon bonds.

SIMULATED: synthetic coupon bonds across 10 semiannual maturities.
Honest-pending note: real H.15 constant-maturity snapshot is pending Board redistribution
verification under Phase 2 Architect Ruling 5. This lab runs on a SIMULATED curve.
Standard library only; no network.
"""

from __future__ import annotations

from fractions import Fraction


def bootstrap_zero_curve(bonds: list[dict[str, object]]) -> list[tuple[int, float, float]]:
    """Bootstrap discount factors and zero rates from a sequential set of coupon bonds.

    Returns a list of tuples: (period n, discount factor DF_n, zero rate z_n per period).
    """
    n_bonds = len(bonds)
    dfs: list[Fraction] = [Fraction(1, 1)]  # DF_0 = 1
    results: list[tuple[int, float, float]] = []

    for n in range(1, n_bonds + 1):
        b = bonds[n - 1]
        fc = b["face_cents"]
        pc = b["price_cents"]
        assert isinstance(fc, int)
        assert isinstance(pc, int)
        cr = b["coupon_rate"]
        assert isinstance(cr, Fraction)

        price_ratio = Fraction(pc, fc)
        sum_prior_df = sum(dfs[1:n])
        df_n = (price_ratio - cr * sum_prior_df) / (1 + cr)
        dfs.append(df_n)

        z_n = float(df_n) ** (-1.0 / n) - 1.0
        results.append((n, float(df_n), z_n))

    return results


def main() -> None:
    # 1. Construct a set of 10 par bonds with ascending coupon rates
    # Maturities 1 through 10 semiannual periods (0.5 to 5.0 years)
    face_cents = 100_000  # $1,000.00
    par_coupons_annual = [0.030, 0.033, 0.036, 0.038, 0.040, 0.042, 0.044, 0.045, 0.046, 0.047]

    bonds = []
    for n, c_ann in enumerate(par_coupons_annual, start=1):
        c_period = Fraction(round(c_ann / 2 * 100_000), 100_000)
        # Par bond price equals face value on coupon date
        bonds.append(
            {
                "periods": n,
                "coupon_rate": c_period,
                "face_cents": face_cents,
                "price_cents": face_cents,
            }
        )

    # 2. Run bootstrapping
    curve = bootstrap_zero_curve(bonds)

    print("Bootstrapped Zero Curve (from 10 Semiannual Par Bonds):")
    print("Period | Maturity | Par Coupon (Ann) | Discount Factor | Zero Rate (Ann)")
    print("-" * 72)
    for n, df_n, zn in curve:
        mat_years = n * 0.5
        c_ann = par_coupons_annual[n - 1]
        zn_annual = zn * 2.0  # bond equivalent annual zero rate
        print(f"{n:6d} | {mat_years:6.1f} yr | {c_ann:16.3%} | {df_n:15.6f} | {zn_annual:15.4%}")
    print("-" * 72)

    # 3. Repricing check: reprice each input bond using bootstrapped discount factors
    print("\nRepricing Verification against Input Prices ($1000.00 Par):")
    max_error = 0.0
    for b in bonds:
        period_num = b["periods"]
        assert isinstance(period_num, int)
        c = b["coupon_rate"]
        assert isinstance(c, Fraction)
        c_float = float(c)
        # Cash flows: c * face at k=1..n-1, (1+c)*face at n
        pv = 0.0
        for k in range(1, period_num):
            df_k = curve[k - 1][1]
            pv += c_float * (face_cents / 100.0) * df_k
        df_n = curve[period_num - 1][1]
        pv += (1.0 + c_float) * (face_cents / 100.0) * df_n

        err = abs(pv - 1000.0)
        if err > max_error:
            max_error = err
        print(f"  Bond {period_num:2d} (tau = {period_num * 0.5:4.1f} yr): Repriced = ${pv:.6f}, |Error| = {err:.2e}")
        assert err < 1e-9

    print(f"\nMax repricing error across all 10 bonds = {max_error:.2e}")
    print("Bootstrapping exact repricing theorem verified: error < 1e-9 on all bonds.")


main()
