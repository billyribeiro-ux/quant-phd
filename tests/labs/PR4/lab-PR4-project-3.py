"""Lab Project 3 (Rung 4 Stretch Extension): Rolling Dynamic EVT-GPD Engine.

Implements an automated rolling-window Peaks-Over-Threshold EVT risk engine
and evaluates out-of-sample dynamic backtesting accuracy across volatile regimes.
"""

from __future__ import annotations

import math

import numpy as np


def main() -> None:
    rng = np.random.default_rng(2026)
    t_total = 800
    window = 250
    alpha = 0.99

    # Generate synthetic returns with GARCH-like time-varying volatility bursts
    innovations = rng.standard_t(df=4, size=t_total)
    returns = np.zeros(t_total)
    sigma_t = 0.012

    for t in range(t_total):
        sigma_t = 0.028 if 300 <= t <= 450 else 0.012
        returns[t] = sigma_t * innovations[t]

    losses = -returns
    out_of_sample_losses = losses[window:]
    n_eval = len(out_of_sample_losses)

    evt_vars = []
    hist_vars = []

    # Rolling window parameter re-estimation
    for t in range(window, t_total):
        w_loss = losses[t - window : t]
        # Historical VaR
        h_v = float(np.quantile(w_loss, alpha, method="linear"))
        hist_vars.append(h_v)

        # EVT POT GPD VaR
        u = float(np.quantile(w_loss, 0.88, method="linear"))
        exc = w_loss[w_loss > u] - u
        n_u = len(exc)
        m_e = float(np.mean(exc))
        v_e = float(np.var(exc, ddof=1))
        xi = max(-0.5, min(0.9, 0.5 * (1.0 - (m_e**2) / v_e)))
        beta = max(1e-4, m_e * (1.0 - xi))
        factor = (window / n_u) * (1.0 - alpha)
        evt_v = u + (beta / xi) * (factor ** (-xi) - 1.0)
        evt_vars.append(evt_v)

    arr_evt_var = np.array(evt_vars)
    arr_hist_var = np.array(hist_vars)

    hits_evt = int(np.sum(out_of_sample_losses > arr_evt_var))
    hits_hist = int(np.sum(out_of_sample_losses > arr_hist_var))

    p = 1.0 - alpha
    expected_hits = n_eval * p

    def kupiec_lr(x: int, n: int) -> float:
        p_hat = x / n
        return float(
            -2.0
            * ((n - x) * math.log(1.0 - p) + x * math.log(p) - (n - x) * math.log(1.0 - p_hat) - x * math.log(p_hat))
        )

    lr_evt = max(0.0, kupiec_lr(hits_evt, n_eval))
    lr_hist = max(0.0, kupiec_lr(hits_hist, n_eval))

    p_evt = float(math.erfc(math.sqrt(lr_evt / 2.0)))
    p_hist = float(math.erfc(math.sqrt(lr_hist / 2.0)))

    print(f"Rolling Evaluation Periods: {n_eval} | Rolling Window Size: {window}")
    print(f"Expected 99% Out-of-Sample Violations: {expected_hits:.1f}")
    print("=" * 70)
    print(f"Rolling Historical VaR Exceptions: {hits_hist}/{n_eval} | LR: {lr_hist:.4f} | p-val: {p_hist:.4f}")
    print(f"Rolling EVT-GPD VaR Exceptions:    {hits_evt}/{n_eval} | LR: {lr_evt:.4f} | p-val: {p_evt:.4f}")
    print("-" * 70)
    print(f"EVT Tail Protection Ratio: {hits_hist / max(1, hits_evt):.2f}x fewer violations under regime shifts")


main()
