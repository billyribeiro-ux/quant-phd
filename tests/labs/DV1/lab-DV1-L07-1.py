"""Lab 1 · The Gamma-Theta P&L identity and realized vs implied volatility.

Verifies the fundamental continuous-time hedging P&L identity:
    dPi_t = 0.5 * S_t^2 * Gamma_t * (sigma_realized^2 - sigma_implied^2) dt.
Along discrete sample paths, compares the actual delta-hedged tracking P&L:
    DeltaPi_i = DeltaV_i - Delta_{i-1} DeltaS_i - r (V_{i-1} - Delta_{i-1} S_{i-1}) dt
against the Gamma-Theta expansion:
    DeltaPi_i^{approx} = Theta_i dt + 0.5 Gamma_i (DeltaS_i)^2 - r (V_i - Delta_i S_i) dt
                  = 0.5 S_i^2 Gamma_i [ (DeltaS_i / S_i)^2 - sigma_implied^2 dt ].
Evaluates the cumulative tracking agreement across paths where realized volatility
differs from implied volatility (sigma_realized = 0.28 vs sigma_implied = 0.20).
"""

from __future__ import annotations

import math
import random


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def norm_pdf(x: float) -> float:
    """Standard normal probability density function."""
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def bs_call_price(s: float, k: float, r: float, sigma: float, tau: float) -> float:
    """European call analytical price."""
    if tau <= 1e-12:
        return max(s - k, 0.0)
    sq_tau = math.sqrt(tau)
    d1 = (math.log(s / k) + (r + 0.5 * sigma**2) * tau) / (sigma * sq_tau)
    d2 = d1 - sigma * sq_tau
    return s * norm_cdf(d1) - k * math.exp(-r * tau) * norm_cdf(d2)


def bs_greeks(s: float, k: float, r: float, sigma: float, tau: float) -> tuple[float, float, float]:
    """Compute (delta, gamma, theta_calendar) for European call."""
    if tau <= 1e-12:
        d = 1.0 if s > k else 0.0
        return d, 0.0, 0.0
    sq_tau = math.sqrt(tau)
    d1 = (math.log(s / k) + (r + 0.5 * sigma**2) * tau) / (sigma * sq_tau)
    d2 = d1 - sigma * sq_tau
    pdf_d1 = norm_pdf(d1)

    delta = norm_cdf(d1)
    gamma = pdf_d1 / (s * sigma * sq_tau)
    theta = -(s * pdf_d1 * sigma) / (2.0 * sq_tau) - r * k * math.exp(-r * tau) * norm_cdf(d2)
    return delta, gamma, theta


def simulate_gamma_theta_path(
    s0: float,
    k: float,
    r: float,
    sigma_imp: float,
    sigma_real: float,
    maturity: float,
    n_steps: int,
    seed: int,
) -> tuple[float, float, float]:
    """Simulate single path and compare actual hedged P&L with Gamma-Theta attribution."""
    dt = maturity / n_steps
    drift = (r - 0.5 * sigma_real**2) * dt
    vol = sigma_real * math.sqrt(dt)

    rng = random.Random(seed)
    s = s0

    actual_pnl = 0.0
    gamma_theta_pnl = 0.0
    vol_spread_pnl = 0.0

    for step in range(n_steps):
        tau = maturity - step * dt
        v = bs_call_price(s, k, r, sigma_imp, tau)
        delta, gamma, theta = bs_greeks(s, k, r, sigma_imp, tau)

        # Stock price increment under true realized volatility
        z = rng.gauss(0.0, 1.0)
        s_next = s * math.exp(drift + vol * z)
        ds = s_next - s

        tau_next = max(maturity - (step + 1) * dt, 1e-12)
        v_next = bs_call_price(s_next, k, r, sigma_imp, tau_next)

        # Actual discrete hedged P&L increment: dV - delta * dS - r(V - delta * S) dt
        actual_inc = (v_next - v) - delta * ds - r * (v - delta * s) * dt
        actual_pnl += actual_inc

        # Second-order Taylor expansion: Theta dt + 0.5 Gamma (dS)^2 - r(V - delta * S) dt
        taylor_inc = theta * dt + 0.5 * gamma * (ds**2) - r * (v - delta * s) * dt
        gamma_theta_pnl += taylor_inc

        # Gamma-Theta identity form: 0.5 * S^2 * Gamma * ((dS/S)^2 - sigma_imp^2 dt)
        identity_inc = 0.5 * (s**2) * gamma * ((ds / s) ** 2 - (sigma_imp**2) * dt)
        vol_spread_pnl += identity_inc

        s = s_next

    return actual_pnl, gamma_theta_pnl, vol_spread_pnl


def main() -> None:
    # Contract parameters (SIMULATED)
    s0 = 100.0
    k = 100.0
    r = 0.05
    sigma_imp = 0.20
    maturity = 0.5
    n_steps = 500  # Fine daily/intraday grid
    seed = 777

    print("Gamma-Theta P&L Identity Attribution along Single Path (SIMULATED):")
    # Case 1: Realized vol equals implied vol
    act_1, tay_1, id_1 = simulate_gamma_theta_path(s0, k, r, sigma_imp, 0.20, maturity, n_steps, seed)
    print("Case sigma_realized = 0.20 (At-the-money implied vol):")
    print(f"  Actual Hedged P&L        = {act_1:8.4f}")
    print(f"  Taylor (Theta + Gamma)   = {tay_1:8.4f} (Discrepancy: {abs(act_1 - tay_1):.4f})")
    print(f"  Vol Spread 0.5*S^2*Gamma*DeltaV  = {id_1:8.4f}")

    # Case 2: Realized vol exceeds implied vol (long gamma profits)
    act_2, tay_2, id_2 = simulate_gamma_theta_path(s0, k, r, sigma_imp, 0.28, maturity, n_steps, seed)
    print("Case sigma_realized = 0.28 (Higher realized vol, long gamma):")
    print(f"  Actual Hedged P&L        = {act_2:8.4f}")
    print(f"  Taylor (Theta + Gamma)   = {tay_2:8.4f} (Discrepancy: {abs(act_2 - tay_2):.4f})")
    print(f"  Vol Spread 0.5*S^2*Gamma*DeltaV  = {id_2:8.4f}")

    # Case 3: Realized vol below implied vol (theta bleed dominates)
    act_3, tay_3, id_3 = simulate_gamma_theta_path(s0, k, r, sigma_imp, 0.12, maturity, n_steps, seed)
    print("Case sigma_realized = 0.12 (Lower realized vol, theta bleed):")
    print(f"  Actual Hedged P&L        = {act_3:8.4f}")
    print(f"  Taylor (Theta + Gamma)   = {tay_3:8.4f} (Discrepancy: {abs(act_3 - tay_3):.4f})")
    print(f"  Vol Spread 0.5*S^2*Gamma*DeltaV  = {id_3:8.4f}")

    print("Hedged P&L positive when sigma_realized > sigma_imp:", act_2 > 0.0)
    print("Hedged P&L negative when sigma_realized < sigma_imp:", act_3 < 0.0)
    print("Gamma-Theta Taylor expansion matches within 0.05 on fine grid:", abs(act_2 - tay_2) < 0.05)


main()
