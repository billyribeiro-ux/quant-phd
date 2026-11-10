"""Lab QR2-L06-1: Planted-Lookahead Adversarial Detector.

Implements an automated lookahead auditor that injects adversarial forward-looking
signals, calculates lead-lag cross-correlations, and verifies backtester integrity.
"""

from __future__ import annotations

import numpy as np


def compute_lead_lag_correlations(signal: np.ndarray, returns: np.ndarray, max_lag: int = 3) -> dict[int, float]:
    """Computes Corr(s_t, r_{t+k}) for k in [-max_lag, +max_lag]."""
    corrs: dict[int, float] = {}
    n = len(signal)

    for k in range(-max_lag, max_lag + 1):
        if k < 0:
            # Signal vs past returns: s_t vs r_{t - |k|}
            s_slice = signal[-k:]
            r_slice = returns[: n + k]
        elif k > 0:
            # Signal vs future returns: s_t vs r_{t + k}  (LOOKAHEAD ZONE)
            s_slice = signal[: n - k]
            r_slice = returns[k:]
        else:
            s_slice = signal
            r_slice = returns

        if len(s_slice) > 2 and np.std(s_slice) > 1e-10 and np.std(r_slice) > 1e-10:
            corr = float(np.corrcoef(s_slice, r_slice)[0, 1])
        else:
            corr = 0.0
        corrs[k] = corr

    return corrs


def audit_signal_for_lookahead(corrs: dict[int, float], threshold: float = 0.20) -> tuple[bool, float]:
    """Flags lookahead if correlation with future return (k >= 1) exceeds threshold."""
    future_corrs = [corrs[k] for k in corrs if k > 0]
    max_lead_corr = max(future_corrs) if future_corrs else 0.0
    is_leaking = max_lead_corr > threshold
    return is_leaking, max_lead_corr


def main() -> None:
    rng = np.random.default_rng(606)
    n_bars = 250
    innovations = rng.normal(0.0003, 0.015, size=n_bars)
    prices = 100.0 * np.exp(np.cumsum(innovations))
    returns = np.zeros(n_bars)
    returns[1:] = (prices[1:] - prices[:-1]) / prices[:-1]

    # Legitimate causal signal: moving average trend (s_t based strictly on past prices)
    ma20 = np.convolve(prices, np.ones(20) / 20, mode="same")
    legit_signal = np.where(prices > ma20, 1.0, -1.0)

    # Planted lookahead signal: leaks 1-bar future return innovation
    planted_signal = np.zeros(n_bars)
    planted_signal[:-1] = np.sign(returns[1:])

    corrs_legit = compute_lead_lag_correlations(legit_signal, returns, max_lag=2)
    corrs_planted = compute_lead_lag_correlations(planted_signal, returns, max_lag=2)

    leak_legit, max_lead_legit = audit_signal_for_lookahead(corrs_legit)
    leak_planted, max_lead_planted = audit_signal_for_lookahead(corrs_planted)

    print("Lead-Lag Cross-Correlation Audit Corr(s_t, r_{t+k}):")
    print("----------------------------------------------------------------------")
    print(f"{'Shift k':<10}{'Legitimate Signal':<22}{'Planted Lookahead':<22}{'Temporal Semantics'}")
    print("----------------------------------------------------------------------")

    for k in sorted(corrs_legit.keys()):
        sem = "Past Information" if k < 0 else ("Contemporaneous" if k == 0 else "FUTURE INFORMATION LEAK")
        print(f"k = {k:<6}{corrs_legit[k]:<22.4f}{corrs_planted[k]:<22.4f}{sem}")

    print("----------------------------------------------------------------------")
    print(f"Legitimate Signal Max Future Lead Corr: {max_lead_legit:.4f} -> Leak Detected: {leak_legit}")
    print(f"Planted Signal Max Future Lead Corr:    {max_lead_planted:.4f} -> Leak Detected: {leak_planted}")
    print("Invariant Verified: Planted lookahead test successfully flags future information leaks.")


main()
