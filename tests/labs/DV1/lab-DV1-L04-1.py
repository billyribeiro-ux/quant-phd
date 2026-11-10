"""Lab 1 · Analytical option Greeks vs central finite-difference approximations.

Computes analytical formulas for Delta, Gamma, Vega, Theta (calendar time derivative d_t V),
and Rho for European call and put options. Compares each analytical Greek against second-order
central finite differences, verifying that relative errors remain strictly below 1e-5.
Also verifies the fundamental identity connecting Gamma and Vega:
    Vega = sigma S^2 tau Gamma.
"""

from __future__ import annotations

import math


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def norm_pdf(x: float) -> float:
    """Standard normal probability density function."""
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def bs_price(s: float, k: float, r: float, sigma: float, tau: float, is_call: bool = True) -> float:
    """Compute European call or put price."""
    if tau <= 1e-12:
        return max(s - k, 0.0) if is_call else max(k - s, 0.0)
    sq_tau = math.sqrt(tau)
    d1 = (math.log(s / k) + (r + 0.5 * sigma**2) * tau) / (sigma * sq_tau)
    d2 = d1 - sigma * sq_tau
    df = math.exp(-r * tau)
    if is_call:
        return s * norm_cdf(d1) - k * df * norm_cdf(d2)
    return k * df * norm_cdf(-d2) - s * norm_cdf(-d1)


def analytical_greeks(s: float, k: float, r: float, sigma: float, tau: float, is_call: bool = True) -> dict[str, float]:
    """Compute analytical Delta, Gamma, Vega, Theta (calendar time d_t V), and Rho."""
    sq_tau = math.sqrt(tau)
    d1 = (math.log(s / k) + (r + 0.5 * sigma**2) * tau) / (sigma * sq_tau)
    d2 = d1 - sigma * sq_tau
    df = math.exp(-r * tau)
    pdf_d1 = norm_pdf(d1)

    gamma = pdf_d1 / (s * sigma * sq_tau)
    vega = s * sq_tau * pdf_d1

    if is_call:
        delta = norm_cdf(d1)
        theta = -(s * pdf_d1 * sigma) / (2.0 * sq_tau) - r * k * df * norm_cdf(d2)
        rho = k * tau * df * norm_cdf(d2)
    else:
        delta = norm_cdf(d1) - 1.0
        theta = -(s * pdf_d1 * sigma) / (2.0 * sq_tau) + r * k * df * norm_cdf(-d2)
        rho = -k * tau * df * norm_cdf(-d2)

    return {"delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "rho": rho}


def finite_difference_greeks(
    s: float, k: float, r: float, sigma: float, tau: float, is_call: bool = True
) -> dict[str, float]:
    """Compute central finite-difference approximations for all Greeks."""
    h_s = 1e-4 * s
    h_v = 1e-5
    h_r = 1e-5
    h_t = 1e-5

    v0 = bs_price(s, k, r, sigma, tau, is_call)
    v_s_up = bs_price(s + h_s, k, r, sigma, tau, is_call)
    v_s_down = bs_price(s - h_s, k, r, sigma, tau, is_call)
    delta_fd = (v_s_up - v_s_down) / (2.0 * h_s)
    gamma_fd = (v_s_up - 2.0 * v0 + v_s_down) / (h_s**2)

    v_v_up = bs_price(s, k, r, sigma + h_v, tau, is_call)
    v_v_down = bs_price(s, k, r, sigma - h_v, tau, is_call)
    vega_fd = (v_v_up - v_v_down) / (2.0 * h_v)

    # Note: tau = T - t, so d_t V = -d_tau V
    v_t_up = bs_price(s, k, r, sigma, tau + h_t, is_call)
    v_t_down = bs_price(s, k, r, sigma, tau - h_t, is_call)
    theta_fd = -(v_t_up - v_t_down) / (2.0 * h_t)

    v_r_up = bs_price(s, k, r + h_r, sigma, tau, is_call)
    v_r_down = bs_price(s, k, r - h_r, sigma, tau, is_call)
    rho_fd = (v_r_up - v_r_down) / (2.0 * h_r)

    return {"delta": delta_fd, "gamma": gamma_fd, "vega": vega_fd, "theta": theta_fd, "rho": rho_fd}


def main() -> None:
    # Contract parameters (SIMULATED)
    s = 100.0
    k = 100.0
    r = 0.05
    sigma = 0.20
    tau = 0.50

    call_exact = analytical_greeks(s, k, r, sigma, tau, is_call=True)
    call_fd = finite_difference_greeks(s, k, r, sigma, tau, is_call=True)

    print("European Call Greeks Comparison (SIMULATED):")
    all_pass = True
    for g in ["delta", "gamma", "vega", "theta", "rho"]:
        exact = call_exact[g]
        fd = call_fd[g]
        rel_err = abs(exact - fd) / (abs(exact) + 1e-12)
        passed = rel_err < 1e-5
        if not passed:
            all_pass = False
        print(
            f"{g.capitalize():6s} | Analytical = {exact:11.6f} | FD = {fd:11.6f} | "
            f"RelErr = {rel_err:.2e} | Pass: {passed}"
        )

    # Gamma-Vega identity check: Vega = sigma * S^2 * tau * Gamma
    gamma_vega_lhs = call_exact["vega"]
    gamma_vega_rhs = sigma * (s**2) * tau * call_exact["gamma"]
    identity_diff = abs(gamma_vega_lhs - gamma_vega_rhs)
    print(
        f"Gamma-Vega identity check: Vega = {gamma_vega_lhs:.6f}, "
        f"sigma*S^2*tau*Gamma = {gamma_vega_rhs:.6f}, Diff = {identity_diff:.2e}"
    )
    print("Gamma-Vega identity holds exactly:", identity_diff < 1e-12)
    print("All Greek finite differences within 1e-5 tolerance:", all_pass)


main()
