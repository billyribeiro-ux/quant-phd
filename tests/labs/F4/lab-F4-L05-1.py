"""Lab F4-L05-1: Dynamic Momentum and Crash-Risk Overlay Performance.

Implements the Daniel & Moskowitz (2016) dynamic volatility and crash-risk overlay
strategy, comparing Static WML vs Vol-Scaled WML vs Dynamic DM across simulated
macro cycles with panic rebounds.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    rng = np.random.default_rng(999)
    n_months = 360
    dt = 1.0 / 12.0
    rf = 0.02 / 12.0

    # Market returns with bull markets and two severe bear market crashes with rebounds
    mkt = rng.normal(0.08 * dt, 0.14 * np.sqrt(dt), size=n_months)
    # Episode 1: Bear 80..100, Rebound 101..104
    mkt[80:101] = -0.50 * dt + rng.normal(0.0, 0.04, size=21)
    mkt[101:105] = 0.12 + rng.uniform(0.01, 0.05, size=4)
    # Episode 2: Bear 250..270, Rebound 271..274
    mkt[250:271] = -0.50 * dt + rng.normal(0.0, 0.04, size=21)
    mkt[271:275] = 0.12 + rng.uniform(0.01, 0.05, size=4)

    # Momentum baseline return: positive drift in normal times, massive crash in rebounds
    wml_raw = rng.normal(0.09 * dt, 0.15 * np.sqrt(dt), size=n_months)
    # Crashes in rebound months (short leg explodes)
    wml_raw[101:105] = -0.22 + rng.normal(0.0, 0.03, size=4)
    wml_raw[271:275] = -0.22 + rng.normal(0.0, 0.03, size=4)

    # 1. Trailing realized volatility (causal 6-month window)
    vol_est = np.zeros(n_months)
    for t in range(n_months):
        hist = wml_raw[max(0, t - 6) : t]
        vol_est[t] = 0.15 if len(hist) < 3 else max(0.04, float(np.std(hist, ddof=1)) * np.sqrt(12.0))

    # 2. Panic state detection (trailing 2-year market return < 0)
    panic = np.zeros(n_months, dtype=bool)
    for t in range(24, n_months):
        panic[t] = np.sum(mkt[t - 24 : t]) < 0.0

    # 3. Strategy exposure weights
    target_vol = 0.15
    max_lev = 2.0
    w_static = np.ones(n_months)
    w_vol = np.clip(target_vol / vol_est, 0.0, max_lev)
    w_dm = w_vol.copy()
    w_dm[panic] *= 0.20  # crash overlay down-scales exposure in panic states

    # 4. Strategy returns (net of turnover costs: 15 bps per turn)
    cost_mult = 15.0 * 1e-4

    def sim_strategy(weights: np.ndarray) -> tuple[float, float, float, float]:
        gross = weights * wml_raw
        turnover = np.abs(np.diff(weights, prepend=weights[0]))
        net = gross - turnover * cost_mult
        ann_ret = float(np.mean(net - rf)) * 12.0
        ann_vol = float(np.std(net, ddof=1)) * np.sqrt(12.0)
        sharpe = ann_ret / max(1e-6, ann_vol)
        cum = np.cumprod(1.0 + net)
        max_dd = float(np.max((np.maximum.accumulate(cum) - cum) / np.maximum.accumulate(cum)))
        c = net - np.mean(net)
        skew = float(np.mean(c**3)) / max(1e-8, float(np.mean(c**2)) ** 1.5)
        return sharpe, max_dd, skew, ann_ret

    sh_stat, dd_stat, sk_stat, ret_stat = sim_strategy(w_static)
    sh_vol, dd_vol, sk_vol, ret_vol = sim_strategy(w_vol)
    sh_dm, dd_dm, sk_dm, ret_dm = sim_strategy(w_dm)

    print("=== DYNAMIC MOMENTUM STRATEGY COMPARISON (30 YEARS) ===")
    print(f"Static WML:      Sharpe={sh_stat:.2f}, MaxDD={dd_stat:.2%}, Skewness={sk_stat:.2f}, AnnRet={ret_stat:+.2%}")
    print(f"Vol-Scaled WML:  Sharpe={sh_vol:.2f}, MaxDD={dd_vol:.2%}, Skewness={sk_vol:.2f}, AnnRet={ret_vol:+.2%}")
    print(f"Dynamic DM:      Sharpe={sh_dm:.2f}, MaxDD={dd_dm:.2%}, Skewness={sk_dm:.2f}, AnnRet={ret_dm:+.2%}")


main()
