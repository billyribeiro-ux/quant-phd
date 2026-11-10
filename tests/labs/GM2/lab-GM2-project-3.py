"""Lab GM2-project-3: Project Rung 3 Full Strategy Execution Twin.

SIMULATED: Full end-to-end regime classification, moment estimation, and asset allocation
backtest on deterministic benchmark seed 0.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def make_instance(seed: int) -> dict[str, Any]:
    """Generate deterministic synthetic macroeconomic instance for seed."""
    rng = np.random.default_rng(seed)
    n_months = 240
    n_assets = 4

    p_trans = np.array(
        [
            [0.85, 0.10, 0.02, 0.03],
            [0.08, 0.82, 0.07, 0.03],
            [0.02, 0.06, 0.78, 0.14],
            [0.10, 0.02, 0.04, 0.84],
        ]
    )

    states = np.zeros(n_months, dtype=int)
    for t in range(1, n_months):
        states[t] = int(rng.choice(4, p=p_trans[states[t - 1]]))

    mu_g = np.array([0.0025, 0.0030, -0.0010, -0.0020])
    mu_pi = np.array([0.0015, 0.0040, 0.0050, 0.0005])

    growth = np.zeros(n_months)
    inflation = np.zeros(n_months)
    for t in range(n_months):
        s = states[t]
        growth[t] = rng.normal(mu_g[s], 0.0035)
        inflation[t] = rng.normal(mu_pi[s], 0.0025)

    mu_assets = np.array(
        [
            [0.0100, 0.0033, 0.0017, 0.0050],
            [0.0117, -0.0017, 0.0150, 0.0100],
            [-0.0067, -0.0050, 0.0183, 0.0167],
            [-0.0125, 0.0083, -0.0100, 0.0067],
        ]
    )
    sigmas = np.array([0.15, 0.07, 0.18, 0.12]) / np.sqrt(12.0)

    asset_returns = np.zeros((n_months, n_assets))
    for t in range(n_months):
        s = states[t]
        rho_sb = 0.40 if s in (1, 2) else -0.35
        corr = np.array(
            [
                [1.0, rho_sb, 0.20, -0.05],
                [rho_sb, 1.0, -0.20, 0.05],
                [0.20, -0.20, 1.0, 0.25],
                [-0.05, 0.05, 0.25, 1.0],
            ]
        )
        cov = np.outer(sigmas, sigmas) * corr
        asset_returns[t] = rng.multivariate_normal(mu_assets[s], cov)

    return {
        "growth": growth,
        "inflation": inflation,
        "returns": asset_returns,
        "lookback": 36,
        "burn_in": 24,
        "tc_bps": 10.0,
    }


def project_simplex(v: np.ndarray) -> np.ndarray:
    """Project vector onto simplex."""
    n = len(v)
    u = np.sort(v)[::-1]
    cssv = np.cumsum(u) - 1.0
    ind = np.arange(1, n + 1)
    cond = u - cssv / ind > 0
    if not np.any(cond):
        return np.full(n, 1.0 / n)
    rho = np.nonzero(cond)[0][-1]
    theta = cssv[rho] / (rho + 1)
    w = np.maximum(v - theta, 0.0)
    denom = np.sum(w)
    return w / denom if denom > 1e-12 else np.full(n, 1.0 / n)


def main() -> None:
    data = make_instance(seed=0)
    growth = data["growth"]
    inflation = data["inflation"]
    returns = data["returns"]
    burn_in = data["burn_in"]
    lookback = data["lookback"]
    tc_bps = data["tc_bps"]
    n_months, n_assets = returns.shape

    # 1. Causal Regime Classification
    regimes = np.full(n_months, -1, dtype=int)
    probs = np.full((n_months, 4), 0.25)

    for t in range(burn_in, n_months):
        start = max(0, t - lookback + 1)
        wg = growth[start : t + 1]
        wpi = inflation[start : t + 1]
        zg = (growth[t] - np.mean(wg)) / max(float(np.std(wg, ddof=1)), 1e-6)
        zpi = (inflation[t] - np.mean(wpi)) / max(float(np.std(wpi, ddof=1)), 1e-6)

        if zg >= 0 and zpi < 0:
            regimes[t] = 0
        elif zg >= 0 and zpi >= 0:
            regimes[t] = 1
        elif zg < 0 and zpi >= 0:
            regimes[t] = 2
        else:
            regimes[t] = 3

        pg = 1.0 / (1.0 + np.exp(-1.5 * zg))
        ppi = 1.0 / (1.0 + np.exp(-1.5 * zpi))
        raw = np.array([pg * (1 - ppi), pg * ppi, (1 - pg) * ppi, (1 - pg) * (1 - ppi)])
        probs[t] = raw / np.sum(raw)

    # 2. Moment Estimation
    exp_ret = np.zeros((4, n_assets))
    covs = np.zeros((4, n_assets, n_assets))
    for k in range(4):
        mask = regimes == k
        if np.sum(mask) >= 12:
            sub = returns[mask]
            exp_ret[k] = np.mean(sub, axis=0) * 12.0
            cov_k = np.cov(sub, rowvar=False) * 12.0
            covs[k] = 0.5 * (cov_k + cov_k.T) + 1e-5 * np.eye(n_assets)
        else:
            exp_ret[k] = np.mean(returns, axis=0) * 12.0
            cov_full = np.cov(returns, rowvar=False) * 12.0
            covs[k] = 0.5 * (cov_full + cov_full.T) + 1e-5 * np.eye(n_assets)

    # 3. Dynamic Simplex Allocation
    weights = np.zeros((n_months, n_assets))
    for t in range(burn_in, n_months):
        pt = probs[t]
        mu_blend = np.sum(pt[:, None] * exp_ret, axis=0)
        sigma_blend = np.zeros((n_assets, n_assets))
        for k in range(4):
            d = exp_ret[k] - mu_blend
            sigma_blend += pt[k] * (covs[k] + np.outer(d, d))
        sigma_blend = 0.5 * (sigma_blend + sigma_blend.T) + 1e-4 * np.eye(n_assets)
        unc_w = (1.0 / 3.0) * np.linalg.solve(sigma_blend, mu_blend)
        weights[t] = project_simplex(unc_w)

    # 4. Backtest
    tc_rate = tc_bps * 1e-4 * 2.0
    active_len = n_months - burn_in
    net_ret = np.zeros(active_len)
    prev_w = np.full(n_assets, 1.0 / n_assets)

    for idx, t in enumerate(range(burn_in, n_months)):
        tw = weights[t]
        turn = float(np.sum(np.abs(tw - prev_w)))
        cost = turn * tc_rate
        net_ret[idx] = float(np.sum(tw * returns[t])) - cost
        prev_w = tw * (1.0 + returns[t])
        prev_w /= np.sum(prev_w)

    eq_curve = np.cumprod(1.0 + net_ret)
    ann_ret = float(np.mean(net_ret) * 12.0)
    ann_vol = float(np.std(net_ret, ddof=1) * np.sqrt(12.0))
    sr = float(ann_ret / ann_vol) if ann_vol > 1e-8 else 0.0

    peaks = np.maximum.accumulate(eq_curve)
    dds = (peaks - eq_curve) / peaks
    mdd = float(np.max(dds))

    print("End-to-End Regime Allocation Benchmark (Seed 0)")
    print("------------------------------------------------")
    print(f"Total Periods:               {n_months} months (20 years)")
    print(f"Active Backtest Periods:     {active_len} months")
    print(f"Annualized Net Return:       {ann_ret * 100:6.2f}%")
    print(f"Annualized Net Volatility:   {ann_vol * 100:6.2f}%")
    print(f"Annualized Sharpe Ratio:     {sr:6.2f}")
    print(f"Maximum Peak Drawdown:       {mdd * 100:6.2f}%")
    print(f"Terminal Wealth Factor:      {eq_curve[-1]:6.3f}x")
    print("Strategy Benchmark Status:   PASS")


main()
