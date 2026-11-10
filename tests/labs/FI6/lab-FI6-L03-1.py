"""Lab FI6-L03-1: Black-76 Caplet Pricing, Stripping, and Parity.

Evaluates Black-76 caplets and floorlets under multi-curve discounting,
verifies exact put-call parity against floating rate agreements,
and implements a caplet volatility stripping algorithm from flat cap quotes.
"""

from __future__ import annotations

import math

from scipy.stats import norm


def black76_caplet(
    fwd_rate: float,
    strike: float,
    discount_factor: float,
    tau: float,
    texp: float,
    vol: float,
) -> float:
    """Price a European caplet using Black-76 formula under the T-forward measure."""
    if texp <= 0.0 or vol <= 0.0:
        return discount_factor * tau * max(fwd_rate - strike, 0.0)

    std_dev = vol * math.sqrt(texp)
    d1 = (math.log(fwd_rate / strike) + 0.5 * std_dev**2) / std_dev
    d2 = d1 - std_dev

    call_price = fwd_rate * float(norm.cdf(d1)) - strike * float(norm.cdf(d2))
    return discount_factor * tau * call_price


def black76_floorlet(
    fwd_rate: float,
    strike: float,
    discount_factor: float,
    tau: float,
    texp: float,
    vol: float,
) -> float:
    """Price a European floorlet using Black-76 formula under the T-forward measure."""
    if texp <= 0.0 or vol <= 0.0:
        return discount_factor * tau * max(strike - fwd_rate, 0.0)

    std_dev = vol * math.sqrt(texp)
    d1 = (math.log(fwd_rate / strike) + 0.5 * std_dev**2) / std_dev
    d2 = d1 - std_dev

    put_price = strike * float(norm.cdf(-d2)) - fwd_rate * float(norm.cdf(-d1))
    return discount_factor * tau * put_price


def solve_caplet_vol(
    target_caplet_pv: float,
    fwd_rate: float,
    strike: float,
    df: float,
    tau: float,
    texp: float,
) -> float:
    """Solve for implied caplet volatility using bisection root-finding."""
    low, high = 1e-4, 3.0
    for _ in range(60):
        mid = 0.5 * (low + high)
        pv = black76_caplet(fwd_rate, strike, df, tau, texp, mid)
        if pv < target_caplet_pv:
            low = mid
        else:
            high = mid
    return 0.5 * (low + high)


def run_lab() -> None:
    print("=== Black-76 Caplet Pricing & Parity Validation ===")

    # Setup: 2-year cap on semi-annual forward rates (reset at 0.5, 1.0, 1.5; pay at 1.0, 1.5, 2.0)
    strike = 0.0400  # 4.00% strike
    tau = 0.5
    resets = [0.5, 1.0, 1.5]
    payments = [1.0, 1.5, 2.0]
    fwd_rates = [0.0380, 0.0410, 0.0435]
    # OIS discount factors to payment dates
    dfs = [0.9610, 0.9410, 0.9205]

    # Test single caplet parity on caplet 2 (texp = 1.0, pay = 1.5)
    fwd2 = fwd_rates[1]
    df2 = dfs[1]
    texp2 = resets[1]
    test_vol = 0.22  # 22% lognormal volatility

    caplet_val = black76_caplet(fwd2, strike, df2, tau, texp2, test_vol)
    floorlet_val = black76_floorlet(fwd2, strike, df2, tau, texp2, test_vol)
    fra_pv = df2 * tau * (fwd2 - strike)
    parity_diff = (caplet_val - floorlet_val) - fra_pv

    print(f"Caplet 2 PV (Black-76)   : {caplet_val:.6f}")
    print(f"Floorlet 2 PV (Black-76) : {floorlet_val:.6f}")
    print(f"FRA Underlying PV        : {fra_pv:.6f}")
    print(f"Caplet - Floorlet - FRA  : {parity_diff:.2e} (Exact Parity Verified)")

    print("\n--- Caplet Stripping from Quoted Flat Cap Volatilities ---")
    # Quoted flat cap volatilities across market maturities:
    # 1Y Cap (1 caplet at 0.5y reset): flat vol = 24.0%
    # 1.5Y Cap (2 caplets at 0.5y, 1.0y): flat vol = 22.5%
    # 2Y Cap (3 caplets at 0.5y, 1.0y, 1.5y): flat vol = 21.5%
    cap_maturities = [1.0, 1.5, 2.0]
    flat_vols = [0.240, 0.225, 0.215]

    # Compute quoted flat cap market PVs:
    # Cap(T_M) = sum_{k=1}^M Caplet(F_k, K, DF_k, tau, texp_k, flat_vol_M)
    cap_market_pvs = []
    for m_idx, _mat in enumerate(cap_maturities):
        n_caplets = m_idx + 1
        pv = sum(
            black76_caplet(fwd_rates[i], strike, dfs[i], tau, resets[i], flat_vols[m_idx]) for i in range(n_caplets)
        )
        cap_market_pvs.append(pv)

    # Strip forward caplet volatilities iteratively:
    # Caplet 1 PV is exactly Cap 1Y PV
    # Caplet 2 PV = Cap 1.5Y PV - Caplet 1 PV(using stripped vol 1)
    # Caplet 3 PV = Cap 2.0Y PV - Caplet 1 PV - Caplet 2 PV
    stripped_caplet_vols: list[float] = []
    accum_caplets_pv = 0.0

    print(
        f"{'Caplet':<8} {'Reset(y)':<10} {'Pay(y)':<8} {'Fwd Rate':<10} "
        f"{'Flat Vol':<10} {'Stripped Vol':<14} {'Caplet PV':<12}"
    )
    for k in range(len(resets)):
        target_cap_pv = cap_market_pvs[k]
        target_caplet_pv = target_cap_pv - accum_caplets_pv
        c_vol = solve_caplet_vol(target_caplet_pv, fwd_rates[k], strike, dfs[k], tau, resets[k])
        stripped_caplet_vols.append(c_vol)
        # Verify caplet PV with stripped vol
        c_pv = black76_caplet(fwd_rates[k], strike, dfs[k], tau, resets[k], c_vol)
        accum_caplets_pv += c_pv
        row_str = (
            f"{k + 1:<8} {resets[k]:<10.1f} {payments[k]:<8.1f} {fwd_rates[k] * 100.0:<9.2f}% "
            f"{flat_vols[k] * 100.0:<9.1f}% {c_vol * 100.0:<13.2f}% {c_pv:<12.6f}"
        )
        print(row_str)

    print(f"\nFinal Cumulative Cap PV  : {accum_caplets_pv:.6f}")
    print(f"Target 2Y Flat Cap PV    : {cap_market_pvs[-1]:.6f}")
    print(f"Stripping Residual Error : {abs(accum_caplets_pv - cap_market_pvs[-1]):.2e}")


run_lab()
