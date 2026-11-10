"""Lab CR2-L01-1: Single-name CDS valuation, running spread, upfront fee, and risky PV01.

Demonstrates mark-to-market valuation of a credit default swap under constant hazard rate,
calculating premium leg PV, default protection leg PV, upfront fee, and risky PV01.
Standard library only; no network.
"""

from __future__ import annotations

import math


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def main() -> None:
    # CDS contract parameters
    tenor = 5.0
    coupon_freq = 4
    dt = 1.0 / coupon_freq
    num_periods = round(tenor * coupon_freq)

    # Market observables
    hazard_rate = 0.0180  # 180 bps default intensity
    recovery = 0.40  # 40% senior unsecured recovery
    r = 0.03  # 3% continuously compounded risk-free rate
    quoted_running_spread_bps = 100.0  # standard 100 bp post-Big Bang coupon

    times = [(k + 1) * dt for k in range(num_periods)]

    # Compute premium leg (with default accrual) and protection leg
    prem_pv01 = 0.0
    prot_pv = 0.0

    print("Quarterly Cash Flow Schedule (Tenor = 5Y, lambda = 180 bp, R = 40%):")
    print("  Quarter | Time (yr) | Discount D(t) | Survival Q(t) | Default Prob | Risky PV01 (bp)")
    print("----------+-----------+---------------+---------------+--------------+----------------")

    for k, tk in enumerate(times):
        t_prev = times[k - 1] if k > 0 else 0.0
        df_k = math.exp(-r * tk)
        df_mid = math.exp(-r * 0.5 * (t_prev + tk))
        q_prev = math.exp(-hazard_rate * t_prev)
        q_k = math.exp(-hazard_rate * tk)
        dp_k = q_prev - q_k

        # 1 bp premium leg component
        step_pv01 = 0.0001 * (dt * df_k * q_k + 0.5 * dt * df_mid * dp_k)
        prem_pv01 += step_pv01
        prot_pv += (1.0 - recovery) * df_mid * dp_k

        if (k + 1) in [1, 4, 8, 12, 16, 20]:
            print(
                f"    {k + 1:2d}    |   {tk:4.2f}    |    {df_k:6.4f}     |    "
                f"{q_k:6.4f}     |    {dp_k:6.4f}    |     {step_pv01 * 10000:6.3f}"
            )

    running_c = quoted_running_spread_bps / 10000.0
    premium_leg_pv = (running_c / 0.0001) * prem_pv01
    upfront_fee = prot_pv - premium_leg_pv
    par_spread_bps = (prot_pv / (prem_pv01 * 10000.0)) * 10000.0

    # Theoretical continuous approximation: par_spread ~ lambda * (1 - R)
    approx_par_bps = hazard_rate * (1.0 - recovery) * 10000.0

    print("\nValuation Summary (Notional = 10000000):")
    print(f"  Risky PV01 (Risky Duration): {prem_pv01 * 10000:6.4f} years")
    print(f"  Protection Leg PV:           {prot_pv * 10_000_000:10.2f}")
    print(f"  Premium Leg PV (100 bp):     {premium_leg_pv * 10_000_000:10.2f}")
    print(f"  Upfront Fee (Buyer pays):    {upfront_fee * 10_000_000:10.2f} ({upfront_fee * 100:5.2f}%)")
    print(f"  Exact Par CDS Spread:        {par_spread_bps:6.2f} bp")
    err_bps = par_spread_bps - approx_par_bps
    print(f"  Continuous Approximation:    {approx_par_bps:6.2f} bp (error = {err_bps:+.2f} bp)")

    # Assertions on financial identities
    assert prem_pv01 > 0.0
    assert prot_pv > 0.0
    assert abs(prot_pv - (par_spread_bps / 10000.0 / 0.0001) * prem_pv01) < 1e-10


main()
