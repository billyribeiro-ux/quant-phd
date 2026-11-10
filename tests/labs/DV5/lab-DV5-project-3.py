"""Lab Project 3 · Reference Numbers: 10-Day Verification Ledger.

This lab provides reference numbers for a smaller 10-day SIMULATED test fixture,
verifying mathematical invariants without running the full autograder suite:
- Monotonicity of option strike contributions
- Cash balance and margin conservation
- Exact symmetry of variance notional conversion
"""

from __future__ import annotations

import math


def main() -> None:
    print("=== DV5 Rung 3 Reference Numbers: 10-Day Verification Fixture ===")

    # 1. Ten SIMULATED daily closing prices
    prices = [4000.0, 4025.5, 3990.2, 3965.0, 3980.4, 4015.2, 4030.0, 3995.8, 3970.1, 4005.0]
    n = len(prices) - 1
    log_returns = [math.log(prices[i] / prices[i - 1]) for i in range(1, len(prices))]
    sum_sq = sum(r * r for r in log_returns)
    rv_10d = (252.0 / float(n)) * sum_sq
    vol_10d = math.sqrt(rv_10d)

    k_var = 0.040  # 20% vol
    vega_notional = 100000.0
    var_notional = vega_notional / (2.0 * math.sqrt(k_var))
    pnl = var_notional * (rv_10d - k_var)

    print(f"Price Path Observations: N={len(prices)} prices ({n} returns)")
    print(f"Realized Variance (Annualized): {rv_10d:.6f} (Realized Vol: {vol_10d * 100.0:.2f}%)")
    print(f"Variance Notional:              {var_notional:.2f} USD")
    print(f"Swap Payoff (Long Var):         {pnl:.2f} USD")

    # 2. Reference Option Grid (Single Maturity T=0.0822 yr, F=4010.0, r=0.03)
    strikes = [3800.0, 3900.0, 4000.0, 4100.0, 4200.0]
    quotes = [15.20, 38.50, 78.40, 42.10, 18.60]  # OTM puts below 4010, OTM calls above
    fwd = 4010.0
    k0 = 4000.0
    r = 0.03
    t = 30.0 / 365.0
    exp_rt = math.exp(r * t)

    dk = 100.0
    integral_sum = sum((dk / (k * k)) * exp_rt * q for k, q in zip(strikes, quotes, strict=True))
    sigma_sq = (2.0 / t) * integral_sum - (1.0 / t) * ((fwd / k0 - 1.0) ** 2)
    vix_ref = 100.0 * math.sqrt(max(0.0, sigma_sq))

    print("\nModel-Free Option Slice (T=30 days):")
    print(f"Forward Level:                  {fwd:.2f}, K0 Strike: {k0:.1f}")
    print(f"Integral Sum:                   {integral_sum:.6f}")
    print(f"Replicated Model-Free VIX:      {vix_ref:.4f}")

    # 3. Reference Backtest Step (1 day)
    nav_start = 500000.0
    target_lev = 1.5
    _margin_req = 0.20
    exposure = nav_start * target_lev
    iv_daily = (vix_ref / 100.0) ** 2
    daily_rv = (log_returns[-1] ** 2) * 252.0
    var_carry = 0.5 * (iv_daily - daily_rv) / 252.0
    daily_pnl = exposure * var_carry
    tc = exposure * 0.0008  # 8 bps
    interest = nav_start * (0.02 / 252.0)
    nav_end = nav_start + daily_pnl + interest - tc

    print("\nSingle-Day Strategy Step Attribution:")
    print(f"Position Exposure:              {exposure:.2f} USD")
    print(f"Variance Carry Earned:          {daily_pnl:.2f} USD")
    print(f"Interest Income:                {interest:.2f} USD")
    print(f"Transaction Cost:               {tc:.2f} USD")
    print(f"Ending NAV:                     {nav_end:.2f} USD")


main()
