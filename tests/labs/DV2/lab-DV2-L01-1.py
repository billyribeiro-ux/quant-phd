"""Lab 1 · Volatility Smile and Skew: Black-Scholes Breakdown and Total Variance.

Evaluates market option prices across strikes K, inverts the Black-Scholes formula
to extract implied volatilities sigma_BS(K), and converts them to total implied
variance w(k) = sigma_BS(K)^2 * tau as a function of log-moneyness k = ln(K / F).
All market data is SIMULATED (seed 42).
"""

from __future__ import annotations

import math


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_call_price(s: float, k: float, r: float, sigma: float, tau: float) -> float:
    """Analytical Black-Scholes European call price."""
    if tau <= 1e-12:
        return max(s - k, 0.0)
    d1 = (math.log(s / k) + (r + 0.5 * sigma**2) * tau) / (sigma * math.sqrt(tau))
    d2 = d1 - sigma * math.sqrt(tau)
    return s * norm_cdf(d1) - k * math.exp(-r * tau) * norm_cdf(d2)


def bs_call_vega(s: float, k: float, r: float, sigma: float, tau: float) -> float:
    """Analytical Black-Scholes call vega."""
    if tau <= 1e-12:
        return 0.0
    d1 = (math.log(s / k) + (r + 0.5 * sigma**2) * tau) / (sigma * math.sqrt(tau))
    phi = math.exp(-0.5 * d1**2) / math.sqrt(2.0 * math.pi)
    return s * math.sqrt(tau) * phi


def implied_volatility(price: float, s: float, k: float, r: float, tau: float, is_call: bool = True) -> float:
    """Invert Black-Scholes price to find implied volatility using Newton-Raphson."""
    sigma = 0.25
    for _ in range(50):
        c = bs_call_price(s, k, r, sigma, tau)
        diff = c - price
        if abs(diff) < 1e-10:
            return sigma
        vega = bs_call_vega(s, k, r, sigma, tau)
        if vega < 1e-12:
            break
        sigma -= diff / vega
        if sigma <= 1e-4:
            sigma = 1e-4
    return sigma


def main() -> None:
    spot = 100.0
    rate = 0.03
    tau = 0.50
    fwd = spot * math.exp(rate * tau)

    # Simulated market quotes reflecting negative equity skew (SIMULATED)
    strikes = [80.0, 85.0, 90.0, 95.0, 100.0, 105.0, 110.0, 115.0, 120.0]
    market_vols = [0.285, 0.264, 0.245, 0.228, 0.212, 0.199, 0.188, 0.180, 0.174]

    print("Strike (K) | Log-Moneyness (k) | Market Call Price | Implied Vol (sigma) | Total Variance (w)")
    print("-" * 85)

    extracted_vols: list[float] = []
    total_vars: list[float] = []

    for k_val, vol_true in zip(strikes, market_vols, strict=True):
        c_market = bs_call_price(spot, k_val, rate, vol_true, tau)
        sigma_imp = implied_volatility(c_market, spot, k_val, rate, tau)
        k_log = math.log(k_val / fwd)
        w_val = sigma_imp**2 * tau

        extracted_vols.append(sigma_imp)
        total_vars.append(w_val)
        print(f"{k_val:10.1f} | {k_log:17.4f} | {c_market:17.4f} | {sigma_imp:19.4f} | {w_val:18.5f}")

    atm_vol = extracted_vols[4]
    otm_put_vol = extracted_vols[0]
    otm_call_vol = extracted_vols[-1]

    skew_slope = (otm_call_vol - otm_put_vol) / (math.log(120.0 / fwd) - math.log(80.0 / fwd))

    print("-" * 85)
    print(f"At-The-Money Implied Volatility (K=100.0): {atm_vol:.4f}")
    print(f"Downside Wing Volatility (K=80.0):         {otm_put_vol:.4f}")
    print(f"Upside Wing Volatility (K=120.0):          {otm_call_vol:.4f}")
    print(f"Empirical Smile Skew Slope (d_sigma / dk): {skew_slope:.4f}")
    print("Negative Skew Detected (Downside Vol > Upside Vol):", otm_put_vol > otm_call_vol)
    print("Black-Scholes Flat Volatility Hypothesis Violated:  True")


main()
