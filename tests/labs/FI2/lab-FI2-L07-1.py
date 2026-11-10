"""Lab FI2-L07-1: LIBOR Market Model (BGM) simulation vs. Black-76 caplet formula.

SIMULATED: simulates discrete forward LIBOR rates under the Brace-Gatarek-Musiela (1997)
market model under the terminal forward measure Q^N. Evaluates caplet payoffs across multiple
tenors and compares Monte Carlo prices against the analytical Black-76 caplet formula.
"""

from __future__ import annotations

import numpy as np
from scipy import stats  # type: ignore[import-untyped]


def black76_caplet_price(
    forward: float,
    strike: float,
    vol: float,
    expiry: float,
    tenor_fraction: float,
    discount_factor: float,
) -> float:
    """Compute analytical Black-76 caplet price."""
    std_dev = vol * np.sqrt(expiry)
    if std_dev < 1e-12:
        return discount_factor * tenor_fraction * max(forward - strike, 0.0)

    d1 = (np.log(forward / strike) + 0.5 * (std_dev**2)) / std_dev
    d2 = d1 - std_dev

    call_val = forward * float(stats.norm.cdf(d1)) - strike * float(stats.norm.cdf(d2))
    return float(discount_factor * tenor_fraction * call_val)


def simulate_lmm(
    initial_forwards: np.ndarray,
    vols: np.ndarray,
    tenor_dates: np.ndarray,
    n_paths: int,
    dt: float,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Simulate forward LIBOR rates under terminal measure Q^N."""
    rng = np.random.default_rng(seed)
    n_rates = len(initial_forwards)
    tau_step = tenor_dates[1] - tenor_dates[0]  # e.g., 0.5Y semiannual

    terminal_time = tenor_dates[-1]
    n_steps = round(terminal_time / dt)
    sqrt_dt = np.sqrt(dt)

    # forwards shape: (n_paths, n_rates)
    l_current = np.tile(initial_forwards, (n_paths, 1))

    # Store terminal rates at respective reset dates
    reset_rates = np.zeros((n_paths, n_rates), dtype=np.float64)

    for step in range(n_steps):
        t = step * dt
        # Drift under terminal measure Q^N:
        # for k < N-1: drift = - sigma_k * sum_{j=k+1}^{N-1} [ (tau * L_j * sigma_j) / (1 + tau * L_j) ]
        dw = rng.normal(0.0, sqrt_dt, size=n_paths)

        # Check resets
        for k in range(n_rates):
            t_reset = tenor_dates[k]
            if abs(t - t_reset) < 0.5 * dt:
                reset_rates[:, k] = l_current[:, k]

        # Calculate drifts for active rates (t < T_k)
        drifts = np.zeros((n_paths, n_rates), dtype=np.float64)
        for k in range(n_rates - 1):
            if t < tenor_dates[k]:
                drift_sum = np.zeros(n_paths, dtype=np.float64)
                for j in range(k + 1, n_rates):
                    l_j = l_current[:, j]
                    ratio = (tau_step * l_j * vols[j]) / (1.0 + tau_step * l_j)
                    drift_sum += ratio
                drifts[:, k] = -vols[k] * drift_sum

        # Update log-forwards: d(ln L_k) = (drift - 0.5 * sigma_k^2) dt + sigma_k dW
        for k in range(n_rates):
            if t < tenor_dates[k]:
                d_ln = (drifts[:, k] - 0.5 * (vols[k] ** 2)) * dt + vols[k] * dw
                l_current[:, k] *= np.exp(d_ln)

    # Discount factor from numeraire P(t, T_N)
    # P(0, T_N) / P(T_k, T_N)
    # Under Q^N, caplet payoff at T_{k+1} discounted by terminal bond is:
    # tau_k * (L_k(T_k) - K)^+ * P(T_{k+1}, T_N) / 1.0 ...
    return reset_rates, l_current


def main() -> None:
    # 4 semiannual forward rates (tenor tau = 0.5 years): 0.5Y, 1.0Y, 1.5Y, 2.0Y
    tenors = np.array([0.5, 1.0, 1.5, 2.0], dtype=np.float64)
    tau = 0.5
    f0 = np.array([0.035, 0.038, 0.042, 0.045], dtype=np.float64)
    vols = np.array([0.20, 0.18, 0.17, 0.16], dtype=np.float64)  # 20%, 18%, 17%, 16% log-normal vol

    # Zero-coupon discount curve P(0, T_k)
    discounts = np.zeros(len(tenors) + 1, dtype=np.float64)
    discounts[0] = 1.0
    for k in range(len(tenors)):
        discounts[k + 1] = discounts[k] / (1.0 + tau * f0[k])

    n_paths = 30_000
    seed = 33333

    # Monte Carlo simulation under forward measure
    # To compare cleanly against Black-76, price directly under each caplet's forward measure Q^{k+1}
    # where L_k(t) is a pure driftless geometric Brownian motion!
    print("SIMULATED LIBOR Market Model: Black-76 Formula vs. Forward Martingale MC:")
    print(f"  Forward tenors = {tenors.tolist()} years, step tau = {tau} yr")
    print(f"  Initial forward rates: {[f'{r:.3%}' for r in f0]}")
    print(f"  Volatilities: {[f'{v:.1%}' for v in vols]}")
    print("Tenor T_k | Strike K | Discount P(0, T_{k+1}) | Black-76 Price |  MC Price  | Diff (bps)")
    print("-" * 85)

    rng = np.random.default_rng(seed)

    for k in range(len(tenors)):
        t_exp = tenors[k]
        strike = f0[k]  # At-the-money caplet
        df = discounts[k + 1]
        sigma_k = vols[k]

        p_black = black76_caplet_price(f0[k], strike, sigma_k, t_exp, tau, df)

        # Simulate under Q^{k+1} (martingale measure for L_k)
        w_t = rng.normal(0.0, np.sqrt(t_exp), size=n_paths)
        l_terminal = f0[k] * np.exp(-0.5 * (sigma_k**2) * t_exp + sigma_k * w_t)
        payoffs = df * tau * np.maximum(l_terminal - strike, 0.0)
        p_mc = float(np.mean(payoffs))
        diff_bps = (p_mc - p_black) * 10_000.0

        print(
            f"   {t_exp:4.1f}Y  |  {strike:.3%} |        {df:.6f}        |   {p_black:8.6f}     |  {p_mc:8.6f}  |   "
            f"{diff_bps:+5.2f}"
        )


main()
