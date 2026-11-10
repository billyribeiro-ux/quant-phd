"""Lab F3-L03-1: Time-Series Momentum (TSMOM) vs Cross-Sectional Momentum (CSMOM).

Compares time-series momentum (Moskowitz, Ooi & Pedersen 2012) with cross-sectional
momentum (Jegadeesh & Titman 1993) across 12 diversified liquid futures assets,
highlighting dynamic net market exposure, volatility scaling, and crisis alpha.
"""

from __future__ import annotations

import numpy as np


def simulate_tsmom_vs_csmom(seed: int = 42) -> dict[str, float]:
    """Simulate and compare TSMOM and CSMOM across market regimes."""
    rng = np.random.default_rng(seed)
    n_months = 240
    n_assets = 12
    target_vol_ann = 0.10

    # 1. Simulate asset returns with shared macro factor + idiosyncratic components
    # Include an explicit market crisis period (months 100 to 112)
    macro_factor = rng.normal(0.06 / 12, 0.16 / np.sqrt(12), size=n_months)
    # Severe crisis: 12-month crash of -45% cumulative in macro factor
    macro_factor[100:112] = rng.normal(-0.45 / 12, 0.25 / np.sqrt(12), size=12)

    betas = rng.uniform(0.5, 1.5, size=n_assets)
    returns = np.zeros((n_months, n_assets))
    for i in range(n_assets):
        idio = rng.normal(0.0, 0.20 / np.sqrt(12), size=n_months)
        returns[:, i] = betas[i] * macro_factor + idio

    # 2. Compute TSMOM and CSMOM strategies
    lookback = 12
    t_start = lookback

    tsmom_returns = np.zeros(n_months - t_start)
    csmom_returns = np.zeros(n_months - t_start)
    market_returns = macro_factor[t_start:]

    for idx, t in enumerate(range(t_start, n_months)):
        past_12m = np.sum(returns[t - lookback : t, :], axis=0)
        # Trailing volatility estimate (annualized)
        hist_vol = np.std(returns[max(0, t - 24) : t, :], axis=0, ddof=1) * np.sqrt(12)
        hist_vol = np.maximum(hist_vol, 0.05)  # clamp

        # TSMOM positions: sign(past_12m) scaled by target_vol / hist_vol
        ts_pos = np.sign(past_12m) * (target_vol_ann / hist_vol) / n_assets
        tsmom_returns[idx] = float(np.sum(ts_pos * returns[t, :]))

        # CSMOM positions: demeaned rank weights (dollar-neutral)
        ranks = np.argsort(np.argsort(past_12m))
        cs_weights = (ranks - np.mean(ranks)) / np.sum(np.abs(ranks - np.mean(ranks)))
        csmom_returns[idx] = float(np.sum(cs_weights * returns[t, :]))

    # Performance metrics
    def calc_stats(r: np.ndarray) -> tuple[float, float, float, float]:
        mean_ann = float(np.mean(r) * 12 * 100)
        vol_ann = float(np.std(r, ddof=1) * np.sqrt(12) * 100)
        sr = float(mean_ann / vol_ann) if vol_ann > 0 else 0.0
        # Performance during crash (months 100 to 112, offset by lookback)
        crash_slice = r[100 - t_start : 112 - t_start]
        crash_ret = float(np.sum(crash_slice) * 100)
        return round(mean_ann, 2), round(vol_ann, 2), round(sr, 2), round(crash_ret, 2)

    mkt_m, mkt_v, mkt_sr, mkt_cr = calc_stats(market_returns)
    ts_m, ts_v, ts_sr, ts_cr = calc_stats(tsmom_returns)
    cs_m, cs_v, cs_sr, cs_cr = calc_stats(csmom_returns)

    # Beta to market
    cov_ts_mkt = float(np.cov(tsmom_returns, market_returns)[0, 1])
    cov_cs_mkt = float(np.cov(csmom_returns, market_returns)[0, 1])
    var_mkt = float(np.var(market_returns, ddof=1))
    beta_ts = round(cov_ts_mkt / var_mkt, 2)
    beta_cs = round(cov_cs_mkt / var_mkt, 2)

    return {
        "mkt_mean": mkt_m,
        "mkt_vol": mkt_v,
        "mkt_sr": mkt_sr,
        "mkt_crash": mkt_cr,
        "ts_mean": ts_m,
        "ts_vol": ts_v,
        "ts_sr": ts_sr,
        "ts_crash": ts_cr,
        "ts_beta": beta_ts,
        "cs_mean": cs_m,
        "cs_vol": cs_v,
        "cs_sr": cs_sr,
        "cs_crash": cs_cr,
        "cs_beta": beta_cs,
    }


def main() -> None:
    print("Lab F3-L03-1 | Time-Series Momentum vs Cross-Sectional Momentum")
    print("-------------------------------------------------------------")
    res = simulate_tsmom_vs_csmom(seed=42)
    header = (
        f"{'Strategy':<10} | {'Mean %':<8} | {'Vol %':<8} | {'Sharpe':<8} | "
        f"{'Crash Return %':<16} | {'Market Beta':<12}"
    )
    print(header)
    print("-" * 72)
    mm, mv, msr = res["mkt_mean"], res["mkt_vol"], res["mkt_sr"]
    mcr = res["mkt_crash"]
    print(f"{'Market':<10} | {mm:<8.2f} | {mv:<8.2f} | {msr:<8.2f} | {mcr:<16.2f} | {1.00:<12.2f}")

    tm, tv, tsr = res["ts_mean"], res["ts_vol"], res["ts_sr"]
    tcr, tb = res["ts_crash"], res["ts_beta"]
    print(f"{'TSMOM':<10} | {tm:<8.2f} | {tv:<8.2f} | {tsr:<8.2f} | {tcr:<16.2f} | {tb:<12.2f}")

    cm, cv, csr = res["cs_mean"], res["cs_vol"], res["cs_sr"]
    ccr, cb = res["cs_crash"], res["cs_beta"]
    print(f"{'CSMOM':<10} | {cm:<8.2f} | {cv:<8.2f} | {csr:<8.2f} | {ccr:<16.2f} | {cb:<12.2f}")
    print("-" * 72)
    print(f"TSMOM delivers crisis alpha ({res['ts_crash']:+.2f}% during market crash) via dynamic short positioning.")


main()
