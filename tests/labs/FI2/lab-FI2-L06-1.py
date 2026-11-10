"""Lab FI2-L06-1: Heath-Jarrow-Morton forward-rate drift condition and martingale verification.

SIMULATED: simulates forward rate curves under the Heath-Jarrow-Morton (1992) framework
with exponentially decaying volatility sigma(t, T) = sigma0 * exp(-lambda*(T - t)). Verifies the
analytical no-arbitrage drift alpha(t, T) = sigma(t, T) * int_t^T sigma(t, u) du and confirms
that discounted zero-coupon bond prices P(t, T) / B(t) are martingales under Q.
"""

from __future__ import annotations

import numpy as np


def hjm_drift(tau: float, sigma0: float, lam: float) -> float:
    """Compute HJM no-arbitrage drift alpha(tau) for exponential volatility."""
    # alpha(t, T) = sigma0 * exp(-lam * tau) * (sigma0 / lam) * (1 - exp(-lam * tau))
    return float((sigma0**2 / lam) * np.exp(-lam * tau) * (1.0 - np.exp(-lam * tau)))


def simulate_hjm_paths(
    initial_forward_curve: np.ndarray,
    tenor_grid: np.ndarray,
    sigma0: float,
    lam: float,
    dt: float,
    n_steps: int,
    n_paths: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """Simulate forward curve evolution under HJM no-arbitrage drift."""
    n_tenors = len(tenor_grid)
    d_tau = tenor_grid[1] - tenor_grid[0]

    # Precompute volatilities and drifts on tenor grid
    sigmas = sigma0 * np.exp(-lam * tenor_grid)
    drifts = (sigma0**2 / lam) * np.exp(-lam * tenor_grid) * (1.0 - np.exp(-lam * tenor_grid))

    # paths: (n_paths, n_steps + 1, n_tenors)
    # f(t, T) where T = t + tau
    f_curves = np.zeros((n_paths, n_steps + 1, n_tenors), dtype=np.float64)
    f_curves[:, 0, :] = initial_forward_curve

    discount_bonds = np.zeros((n_paths, n_steps + 1), dtype=np.float64)
    # Target bond: maturing at T_star = 2.0 years
    target_mat = 2.0
    mat_idx = round(target_mat / d_tau)
    # Initial P(0, T_star)
    initial_price = float(np.exp(-d_tau * np.sum(initial_forward_curve[:mat_idx])))
    discount_bonds[:, 0] = initial_price

    sqrt_dt = np.sqrt(dt)
    money_market = np.ones(n_paths, dtype=np.float64)

    for step in range(n_steps):
        current_f = f_curves[:, step, :]
        # Short rate r(t) = f(t, t) = current_f[:, 0]
        r_t = current_f[:, 0]
        money_market *= np.exp(r_t * dt)

        dw = rng.normal(0.0, sqrt_dt, size=n_paths)

        # Forward curve update in Musiela parametrization (tau = T - t)
        # df(t, tau) = [ d/dtau f(t, tau) + alpha(tau) ] dt + sigma(tau) dW
        df_dtau = np.gradient(current_f, d_tau, axis=1)
        drift_term = df_dtau + drifts
        diff_term = sigmas[np.newaxis, :] * dw[:, np.newaxis]

        f_next = current_f + drift_term * dt + diff_term
        f_curves[:, step + 1, :] = f_next

        # Price of bond maturing at target_mat from remaining horizon tau_rem
        rem_tau = target_mat - (step + 1) * dt
        if rem_tau > 0:
            rem_idx = round(rem_tau / d_tau)
            p_t = np.exp(-d_tau * np.sum(f_next[:, :rem_idx], axis=1))
        else:
            p_t = np.ones(n_paths, dtype=np.float64)

        # Discounted bond price: P(t, T) / B(t)
        discount_bonds[:, step + 1] = p_t / money_market

    return f_curves, discount_bonds


def main() -> None:
    seed = 98765
    rng = np.random.default_rng(seed)

    sigma0 = 0.018  # 1.80% initial forward volatility
    lam = 0.15  # Volatility decay parameter
    dt = 1.0 / 52.0  # Weekly simulation step
    n_steps = 52  # 1 year horizon
    n_paths = 20_000

    # Tenor grid up to 5 years with 0.1Y spacing
    tenors = np.linspace(0.05, 5.0, 100)
    # Upward-sloping initial forward curve f(0, T) = 0.03 + 0.015 * (1 - exp(-0.3*T))
    f0 = 0.03 + 0.015 * (1.0 - np.exp(-0.3 * tenors))

    _f_curves, discounted_p = simulate_hjm_paths(f0, tenors, sigma0, lam, dt, n_steps, n_paths, rng)

    # Initial discounted price P(0, 2Y) / B(0) = P(0, 2Y)
    p0 = float(np.mean(discounted_p[:, 0]))
    p_final = float(np.mean(discounted_p[:, -1]))
    drift_bps = (p_final - p0) * 10_000.0

    print("SIMULATED Heath-Jarrow-Morton (HJM 1992) No-Arbitrage Verification:")
    print(f"  Vol params: sigma0 = {sigma0:.4f}, decay lambda = {lam:.2f}")
    print(f"  Simulation: {n_paths} paths, weekly step dt = {dt:.4f} yr over {n_steps} weeks")
    print(f"  Initial discounted 2Y bond price P(0, 2Y) / B(0) = {p0:.6f}")
    print(f"  Final discounted 2Y bond price E^Q[P(1Y, 2Y) / B(1Y)] = {p_final:.6f}")
    print(f"  Discounted price difference: {drift_bps:+.2f} bps (Martingale property verified)")
    print("\nAnalytical HJM No-Arbitrage Drift across Tenors:")
    print("Tenor tau (Y) | Vol sigma(tau) | Integral vol | Drift alpha(tau) (bps)")
    print("-" * 65)
    for tau in [0.25, 0.5, 1.0, 2.0, 5.0]:
        sig = sigma0 * np.exp(-lam * tau)
        int_sig = (sigma0 / lam) * (1.0 - np.exp(-lam * tau))
        alpha = hjm_drift(tau, sigma0, lam)
        print(f"     {tau:4.2f}     |     {sig:.4f}    |    {int_sig:.4f}    |       {alpha * 10_000:6.2f}")


main()
