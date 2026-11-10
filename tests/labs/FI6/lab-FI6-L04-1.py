"""Lab FI6-L04-1: European Swaptions: Black-76 vs. Bachelier Normal Model.

Compares European swaption valuation under Black-76 and the Bachelier (1900) normal model.
Demonstrates the breakdown of lognormal Black-76 under negative interest rates
and verifies Bachelier put-call parity and analytical Greeks against finite differences.
"""

from __future__ import annotations

import math

from scipy.stats import norm


def black76_swaption(
    fwd_swap: float,
    strike: float,
    annuity: float,
    texp: float,
    vol_black: float,
    is_payer: bool = True,
) -> float:
    """Price European swaption using Black-76 formula. Raises ValueError if fwd_swap or strike <= 0."""
    if fwd_swap <= 0.0 or strike <= 0.0:
        raise ValueError(f"Black-76 requires strictly positive rates. Got S={fwd_swap}, K={strike}")

    std_dev = vol_black * math.sqrt(texp)
    d1 = (math.log(fwd_swap / strike) + 0.5 * std_dev**2) / std_dev
    d2 = d1 - std_dev

    if is_payer:
        val = fwd_swap * float(norm.cdf(d1)) - strike * float(norm.cdf(d2))
    else:
        val = strike * float(norm.cdf(-d2)) - fwd_swap * float(norm.cdf(-d1))

    return annuity * val


def bachelier_swaption(
    fwd_swap: float,
    strike: float,
    annuity: float,
    texp: float,
    vol_normal: float,
    is_payer: bool = True,
) -> float:
    """Price European swaption using Bachelier normal model: dS = sigma_N * dW."""
    if texp <= 0.0 or vol_normal <= 0.0:
        intrinsic = max(fwd_swap - strike, 0.0) if is_payer else max(strike - fwd_swap, 0.0)
        return annuity * intrinsic

    std_dev = vol_normal * math.sqrt(texp)
    d = (fwd_swap - strike) / std_dev

    pdf_d = float(norm.pdf(d))
    cdf_d = float(norm.cdf(d))

    if is_payer:
        call_val = (fwd_swap - strike) * cdf_d + std_dev * pdf_d
        return annuity * call_val
    else:
        cdf_minus_d = float(norm.cdf(-d))
        put_val = (strike - fwd_swap) * cdf_minus_d + std_dev * pdf_d
        return annuity * put_val


def bachelier_greeks(
    fwd_swap: float,
    strike: float,
    annuity: float,
    texp: float,
    vol_normal: float,
) -> dict[str, float]:
    """Analytical Greeks for Bachelier payer swaption."""
    std_dev = vol_normal * math.sqrt(texp)
    d = (fwd_swap - strike) / std_dev
    pdf_d = float(norm.pdf(d))
    cdf_d = float(norm.cdf(d))

    delta = annuity * cdf_d
    gamma = annuity * pdf_d / std_dev
    vega = annuity * math.sqrt(texp) * pdf_d  # dPrice / dSigma_N
    return {"delta": delta, "gamma": gamma, "vega": vega}


def run_lab() -> None:
    print("=== European Swaptions: Black-76 vs. Bachelier Normal Model ===")

    # Scenario 1: Standard positive rate environment
    # 1Y into 5Y swaption (texp = 1.0, tenor = 5.0)
    annuity_pos = 4.520  # 5-year swap annuity
    texp = 1.0
    fwd_swap_pos = 0.0400  # 4.00%
    strike_pos = 0.0400  # ATM
    vol_black = 0.20  # 20% lognormal vol
    # Normal vol ATM approximation: sigma_N approx S * sigma_B = 0.04 * 0.20 = 0.0080 (80 bps/year)
    vol_normal_pos = fwd_swap_pos * vol_black

    p_black = black76_swaption(fwd_swap_pos, strike_pos, annuity_pos, texp, vol_black, is_payer=True)
    r_black = black76_swaption(fwd_swap_pos, strike_pos, annuity_pos, texp, vol_black, is_payer=False)
    p_bach = bachelier_swaption(fwd_swap_pos, strike_pos, annuity_pos, texp, vol_normal_pos, is_payer=True)
    r_bach = bachelier_swaption(fwd_swap_pos, strike_pos, annuity_pos, texp, vol_normal_pos, is_payer=False)

    print("--- Positive Rates (ATM S = 4.00%, K = 4.00%, 1Yx5Y) ---")
    print(f"Black-76 Payer Swaption   : {p_black:.6f}")
    print(f"Bachelier Payer Swaption  : {p_bach:.6f} (Diff: {(p_bach - p_black) * 10000.0:.2f} bps of annuity)")
    print(f"Black-76 Put-Call Parity  : {(p_black - r_black) - annuity_pos * (fwd_swap_pos - strike_pos):.2e}")
    print(f"Bachelier Put-Call Parity : {(p_bach - r_bach) - annuity_pos * (fwd_swap_pos - strike_pos):.2e}")

    # Scenario 2: Negative rate environment (EUR/CHF market conditions, e.g., 2015-2021)
    fwd_swap_neg = -0.0035  # -35 bps
    strike_neg = -0.0020  # -20 bps (OTM payer)
    annuity_neg = 4.950
    vol_normal_neg = 0.0055  # 55 bps/year normal vol

    print("\n--- Negative Rates Environment (S = -0.35%, K = -0.20%) ---")
    try:
        black76_swaption(fwd_swap_neg, strike_neg, annuity_neg, texp, vol_black, is_payer=True)
    except ValueError as exc:
        print(f"Black-76 Execution Result : FAILED -> {exc}")

    p_bach_neg = bachelier_swaption(fwd_swap_neg, strike_neg, annuity_neg, texp, vol_normal_neg, is_payer=True)
    r_bach_neg = bachelier_swaption(fwd_swap_neg, strike_neg, annuity_neg, texp, vol_normal_neg, is_payer=False)
    parity_neg = (p_bach_neg - r_bach_neg) - annuity_neg * (fwd_swap_neg - strike_neg)

    print(f"Bachelier Payer Swaption  : {p_bach_neg:.6f}")
    print(f"Bachelier Receiver Swapt  : {r_bach_neg:.6f}")
    print(f"Bachelier Put-Call Parity : {parity_neg:.2e} (Exact Parity Maintained)")

    # Greeks and Finite Difference Verification
    print("\n--- Bachelier Greeks vs. Numerical Finite Differences ---")
    greeks = bachelier_greeks(fwd_swap_pos, strike_pos, annuity_pos, texp, vol_normal_pos)
    h_s = 1e-5
    p_up = bachelier_swaption(fwd_swap_pos + h_s, strike_pos, annuity_pos, texp, vol_normal_pos, is_payer=True)
    p_dn = bachelier_swaption(fwd_swap_pos - h_s, strike_pos, annuity_pos, texp, vol_normal_pos, is_payer=True)
    num_delta = (p_up - p_dn) / (2.0 * h_s)
    num_gamma = (p_up - 2.0 * p_bach + p_dn) / (h_s**2)

    h_v = 1e-5
    p_v_up = bachelier_swaption(fwd_swap_pos, strike_pos, annuity_pos, texp, vol_normal_pos + h_v, is_payer=True)
    p_v_dn = bachelier_swaption(fwd_swap_pos, strike_pos, annuity_pos, texp, vol_normal_pos - h_v, is_payer=True)
    num_vega = (p_v_up - p_v_dn) / (2.0 * h_v)

    print(
        f"Delta (Analytic vs. Num)  : {greeks['delta']:.6f} vs. {num_delta:.6f} "
        f"(Diff: {abs(greeks['delta'] - num_delta):.2e})"
    )
    print(
        f"Gamma (Analytic vs. Num)  : {greeks['gamma']:.4f} vs. {num_gamma:.4f} "
        f"(Diff: {abs(greeks['gamma'] - num_gamma):.2e})"
    )
    print(
        f"Vega  (Analytic vs. Num)  : {greeks['vega']:.6f} vs. {num_vega:.6f} "
        f"(Diff: {abs(greeks['vega'] - num_vega):.2e})"
    )


run_lab()
