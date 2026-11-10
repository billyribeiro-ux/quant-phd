"""Deterministic instance generator for CAP1 replication package project."""

from __future__ import annotations

import numpy as np


def make_instance(seed: int) -> dict[str, object]:
    """Generate a synthetic cross-sectional panel for replication auditing.

    Returns deterministic stock returns, characteristics, market capitalizations,
    CRSP share codes, exchange codes, and delisting status.
    """
    rng = np.random.default_rng(seed)

    # Number of stocks and months
    n_stocks = int(rng.integers(60, 100))
    n_months = int(rng.integers(36, 60))
    n_obs = n_stocks * n_months

    # Identifiers and timestamps
    permnos = np.repeat(np.arange(10001, 10001 + n_stocks), n_months)
    months = np.tile(np.arange(1, n_months + 1), n_stocks)

    # CRSP share codes: mostly 10 and 11 (common stock), some 12, 31 (ADR, REIT)
    shrcd_choices = np.array([10, 11, 12, 31], dtype=np.int32)
    shrcd_probs = np.array([0.80, 0.12, 0.05, 0.03])
    # Fixed per stock
    stock_shrcd = rng.choice(shrcd_choices, size=n_stocks, p=shrcd_probs)
    shrcd = np.repeat(stock_shrcd, n_months)

    # Exchange codes: 1 (NYSE), 2 (AMEX), 3 (NASDAQ)
    stock_exchcd = rng.choice(np.array([1, 2, 3], dtype=np.int32), size=n_stocks, p=[0.45, 0.15, 0.40])
    exchcd = np.repeat(stock_exchcd, n_months)

    # Market equity (size): log-normal distribution, autocorrelated over time
    base_log_me = rng.normal(12.0, 1.8, size=n_stocks)
    me_matrix = np.zeros((n_stocks, n_months), dtype=np.float64)
    for i in range(n_stocks):
        innovations = rng.normal(0.005, 0.05, size=n_months)
        log_me = base_log_me[i] + np.cumsum(innovations)
        me_matrix[i, :] = np.exp(log_me)
    me = me_matrix.ravel()

    # Raw monthly returns with factor structure + idiosyncratic noise
    mkt = rng.normal(0.008, 0.045, size=n_months)
    smb = rng.normal(0.002, 0.030, size=n_months)
    hml = rng.normal(0.003, 0.028, size=n_months)

    betas = rng.normal(1.0, 0.3, size=n_stocks)
    ret_matrix = np.zeros((n_stocks, n_months), dtype=np.float64)
    for i in range(n_stocks):
        beta_i = betas[i]
        idioc = rng.normal(0.0, 0.08, size=n_months)
        # Heavy tails / occasional extreme values
        shocks = rng.choice([0.0, 0.35, -0.40], size=n_months, p=[0.97, 0.015, 0.015])
        ret_matrix[i, :] = 0.003 + beta_i * mkt + 0.3 * smb + 0.2 * hml + idioc + shocks
    raw_ret = ret_matrix.ravel()

    # Delisting indicators and codes
    # About 2-3% of stocks delist in their final month
    dlstcd = np.zeros(n_obs, dtype=np.int32)
    dlret = np.full(n_obs, np.nan, dtype=np.float64)

    delist_candidates = rng.choice(n_stocks, size=int(max(1, n_stocks * 0.04)), replace=False)
    for stock_idx in delist_candidates:
        delist_month = rng.integers(int(n_months * 0.6), n_months)
        flat_idx = stock_idx * n_months + delist_month
        # Delisting code: performance (500 or 580) vs non-performance (200)
        is_perf = rng.random() < 0.70
        dlstcd[flat_idx] = 580 if is_perf else 200
        # Sometimes DLRET is recorded, sometimes missing (nan)
        if rng.random() < 0.40:
            dlret[flat_idx] = -0.35 if is_perf else 0.02

    # Predictive characteristic / anomaly signal: e.g. momentum or profitability
    signal_matrix = np.zeros((n_stocks, n_months), dtype=np.float64)
    for i in range(n_stocks):
        signal_matrix[i, :] = rng.normal(0.12, 0.25, size=n_months)
        # Induce correlation between signal and subsequent return
        ret_matrix[i, 1:] += 0.04 * signal_matrix[i, :-1]
    signal = signal_matrix.ravel()

    return {
        "seed": seed,
        "n_stocks": n_stocks,
        "n_months": n_months,
        "permnos": permnos,
        "months": months,
        "shrcd": shrcd,
        "exchcd": exchcd,
        "me": me,
        "raw_ret": raw_ret,
        "dlstcd": dlstcd,
        "dlret": dlret,
        "signal": signal,
        "mkt": mkt,
        "smb": smb,
        "hml": hml,
    }
