"""Lab 2 · Model-Free Implied Volatility & VIX Replication.

This lab implements the official Cboe VIX methodology on an embedded
two-term SPX option chain (SIMULATED), computes forward index levels F1 and F2,
strike intervals Delta K, near-term and next-term implied variances, and
interpolates to the 30-day constant-maturity VIX Index value.
"""

from __future__ import annotations

import math


def calculate_term_variance(
    options: list[tuple[float, str, float, float]],  # (strike, type, bid, ask)
    forward: float,
    rate: float,
    maturity: float,
) -> tuple[float, float, int]:
    """Compute annualized model-free implied variance for a single expiry term."""
    # Organize quotes by strike
    strikes_data: dict[float, dict[str, float]] = {}
    for k, opt_type, bid, ask in options:
        if k not in strikes_data:
            strikes_data[k] = {}
        mid = 0.5 * (bid + ask)
        strikes_data[k][f"{opt_type}_bid"] = bid
        strikes_data[k][f"{opt_type}_ask"] = ask
        strikes_data[k][f"{opt_type}_mid"] = mid

    sorted_strikes = sorted(strikes_data.keys())
    strikes_below = [k for k in sorted_strikes if k <= forward]
    k0 = max(strikes_below)

    selected_quotes: dict[float, float] = {}

    # ATM strike K0: average of put and call mid quotes
    call_mid = strikes_data[k0].get("call_mid", 0.0)
    put_mid = strikes_data[k0].get("put_mid", 0.0)
    if call_mid > 0.0 and put_mid > 0.0:
        selected_quotes[k0] = 0.5 * (call_mid + put_mid)
    else:
        selected_quotes[k0] = max(call_mid, put_mid)

    # OTM Puts below K0
    for k in reversed([k for k in sorted_strikes if k < k0]):
        bid = strikes_data[k].get("put_bid", 0.0)
        mid = strikes_data[k].get("put_mid", 0.0)
        if bid <= 0.0:
            break
        if mid > 0.0:
            selected_quotes[k] = mid

    # OTM Calls above K0
    for k in [k for k in sorted_strikes if k > k0]:
        bid = strikes_data[k].get("call_bid", 0.0)
        mid = strikes_data[k].get("call_mid", 0.0)
        if bid <= 0.0:
            break
        if mid > 0.0:
            selected_quotes[k] = mid

    valid_k = sorted(selected_quotes.keys())
    m = len(valid_k)

    # Calculate Delta K
    integral_sum = 0.0
    exp_rt = math.exp(rate * maturity)
    for i in range(m):
        k = valid_k[i]
        if i == 0:
            dk = valid_k[1] - valid_k[0]
        elif i == m - 1:
            dk = valid_k[m - 1] - valid_k[m - 2]
        else:
            dk = 0.5 * (valid_k[i + 1] - valid_k[i - 1])
        q_mid = selected_quotes[k]
        integral_sum += (dk / (k * k)) * exp_rt * q_mid

    sigma_sq = (2.0 / maturity) * integral_sum - (1.0 / maturity) * ((forward / k0 - 1.0) ** 2)
    return sigma_sq, k0, m


def main() -> None:
    print("=== Cboe Model-Free Implied Volatility (VIX) Replication ===")
    r = 0.025  # 2.5% risk-free rate

    # Embedded Near-Term Chain: T1 = 24 days (SIMULATED)
    t1 = 24.0 / 365.0
    f1 = 4503.20
    near_chain: list[tuple[float, str, float, float]] = [
        (4350.0, "put", 12.10, 12.50),
        (4400.0, "put", 20.40, 20.90),
        (4450.0, "put", 33.20, 33.80),
        (4500.0, "put", 52.10, 52.80),
        (4500.0, "call", 54.30, 55.00),
        (4550.0, "call", 28.40, 28.90),
        (4600.0, "call", 12.60, 13.00),
        (4650.0, "call", 4.30, 4.60),
    ]

    # Embedded Next-Term Chain: T2 = 31 days (SIMULATED)
    t2 = 31.0 / 365.0
    f2 = 4505.40
    next_chain: list[tuple[float, str, float, float]] = [
        (4350.0, "put", 18.20, 18.70),
        (4400.0, "put", 27.60, 28.20),
        (4450.0, "put", 41.50, 42.20),
        (4500.0, "put", 60.80, 61.60),
        (4500.0, "call", 65.10, 65.90),
        (4550.0, "call", 37.40, 38.00),
        (4600.0, "call", 19.80, 20.30),
        (4650.0, "call", 8.90, 9.30),
    ]

    sigma1_sq, k0_1, n1 = calculate_term_variance(near_chain, f1, r, t1)
    sigma2_sq, k0_2, n2 = calculate_term_variance(next_chain, f2, r, t2)

    vol1 = 100.0 * math.sqrt(max(0.0, sigma1_sq))
    vol2 = 100.0 * math.sqrt(max(0.0, sigma2_sq))

    print(f"Near-Term Expiry (T1={t1 * 365:.1f} days):")
    print(f"  Forward F1={f1:.2f}, K0={k0_1:.1f}, Strikes Used={n1}")
    print(f"  Sigma1^2={sigma1_sq:.6f}, Term Vol={vol1:.4f}%")

    print(f"\nNext-Term Expiry (T2={t2 * 365:.1f} days):")
    print(f"  Forward F2={f2:.2f}, K0={k0_2:.1f}, Strikes Used={n2}")
    print(f"  Sigma2^2={sigma2_sq:.6f}, Term Vol={vol2:.4f}%")

    # 30-Day Constant Maturity Interpolation
    n_t1 = 24.0 * 1440.0
    n_t2 = 31.0 * 1440.0
    n_30 = 30.0 * 1440.0
    n_365 = 365.0 * 1440.0

    w1 = (n_t2 - n_30) / (n_t2 - n_t1)
    w2 = (n_30 - n_t1) / (n_t2 - n_t1)

    interpolated_var = (t1 * sigma1_sq * w1 + t2 * sigma2_sq * w2) * (n_365 / n_30)
    vix = 100.0 * math.sqrt(max(0.0, interpolated_var))

    print("\n30-Day Interpolation:")
    print(f"  Weight T1 (w1)={w1:.4f}, Weight T2 (w2)={w2:.4f}")
    print(f"  30-Day Annualized Variance={interpolated_var:.6f}")
    print(f"  Replicated VIX Index={vix:.4f}")


main()
