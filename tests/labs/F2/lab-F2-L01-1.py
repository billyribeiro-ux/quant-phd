"""Lab F2-L01-1: Size and Value Portfolio Sorts and Factor Construction.

Simulates monthly equity returns and fundamental characteristics (Market Equity ME
and Book-to-Market BE/ME) to construct canonical Fama-French (1993) 2x3 size
and value portfolios, computing SMB, HML, and empirical cross-sectional diagnostics.
"""

from __future__ import annotations

import numpy as np


def simulate_size_and_value(seed: int = 42) -> dict[str, float | int]:
    """Simulate 2x3 size-value sorting and factor return generation."""
    rng = np.random.default_rng(seed)
    n_stocks = 300
    n_months = 120

    # Simulate market equity (log-normal, size variation across 3 orders of magnitude)
    log_me = rng.normal(loc=6.0, scale=1.5, size=n_stocks)
    me = np.exp(log_me)

    # Simulate book-to-market (correlated negatively with size, log-normal)
    log_bm = -0.3 * (log_me - 6.0) + rng.normal(loc=-0.5, scale=0.6, size=n_stocks)
    bm = np.exp(log_bm)

    # NYSE-like median breakpoint for size (50th percentile)
    # 30th and 70th percentile breakpoints for book-to-market
    size_median = float(np.median(me))
    bm_p30 = float(np.percentile(bm, 30))
    bm_p70 = float(np.percentile(bm, 70))

    # Portfolio masks
    small = me <= size_median
    big = me > size_median

    value = bm >= bm_p70
    neutral = (bm >= bm_p30) & (bm < bm_p70)
    growth = bm < bm_p30

    # True factor underlying structure (monthly annualized excess returns)
    # Market factor: 6% mean, 16% vol
    # Size factor (SMB): 2.5% mean, 10% vol
    # Value factor (HML): 4.0% mean, 12% vol
    mkt_ret = rng.normal(0.06 / 12, 0.16 / np.sqrt(12), size=n_months)
    smb_true = rng.normal(0.025 / 12, 0.10 / np.sqrt(12), size=n_months)
    hml_true = rng.normal(0.040 / 12, 0.12 / np.sqrt(12), size=n_months)

    # Stock betas to factors
    beta_mkt = 0.8 + 0.4 * rng.uniform(0, 1, size=n_stocks)
    beta_smb = np.where(
        small,
        0.8 + 0.2 * rng.normal(0, 0.2, size=n_stocks),
        -0.3 + 0.2 * rng.normal(0, 0.2, size=n_stocks),
    )
    beta_hml = np.where(value, 0.7, np.where(growth, -0.6, 0.05)) + rng.normal(0, 0.15, size=n_stocks)

    # Generate monthly stock returns (T x N)
    stock_returns = np.zeros((n_months, n_stocks))
    for t in range(n_months):
        idio = rng.normal(0, 0.25 / np.sqrt(12), size=n_stocks)
        stock_returns[t, :] = beta_mkt * mkt_ret[t] + beta_smb * smb_true[t] + beta_hml * hml_true[t] + idio

    # Value-weighted 2x3 portfolio returns
    # Portfolios: S/V, S/N, S/G, B/V, B/N, B/G
    def calc_vw_ret(mask: np.ndarray) -> np.ndarray:
        w = me[mask] / np.sum(me[mask])
        return np.asarray(stock_returns[:, mask] @ w)

    r_sv = calc_vw_ret(small & value)
    r_sn = calc_vw_ret(small & neutral)
    r_sg = calc_vw_ret(small & growth)
    r_bv = calc_vw_ret(big & value)
    r_bn = calc_vw_ret(big & neutral)
    r_bg = calc_vw_ret(big & growth)

    # Fama-French (1993) SMB and HML formulas:
    # SMB = 1/3 (S/V + S/N + S/G) - 1/3 (B/V + B/N + B/G)
    # HML = 1/2 (S/V + B/V) - 1/2 (S/G + B/G)
    smb = (r_sv + r_sn + r_sg) / 3.0 - (r_bv + r_bn + r_bg) / 3.0
    hml = (r_sv + r_bv) / 2.0 - (r_sg + r_bg) / 2.0

    mean_smb_ann = float(np.mean(smb) * 12 * 100)
    std_smb_ann = float(np.std(smb, ddof=1) * np.sqrt(12) * 100)
    t_smb = float(np.mean(smb) / (np.std(smb, ddof=1) / np.sqrt(n_months)))

    mean_hml_ann = float(np.mean(hml) * 12 * 100)
    std_hml_ann = float(np.std(hml, ddof=1) * np.sqrt(12) * 100)
    t_hml = float(np.mean(hml) / (np.std(hml, ddof=1) / np.sqrt(n_months)))

    corr_smb_hml = float(np.corrcoef(smb, hml)[0, 1])

    return {
        "n_stocks": n_stocks,
        "n_months": n_months,
        "mean_smb_ann": round(mean_smb_ann, 2),
        "std_smb_ann": round(std_smb_ann, 2),
        "t_smb": round(t_smb, 2),
        "mean_hml_ann": round(mean_hml_ann, 2),
        "std_hml_ann": round(std_hml_ann, 2),
        "t_hml": round(t_hml, 2),
        "corr_smb_hml": round(corr_smb_hml, 4),
    }


def main() -> None:
    print("Lab F2-L01-1 | Size and Value Portfolio Sorts (Fama-French 1993)")
    print("----------------------------------------------------------------")
    res = simulate_size_and_value(seed=42)
    print(f"Sample size: {res['n_stocks']} equities over {res['n_months']} months")
    print(
        f"SMB Annualized Premium:   {res['mean_smb_ann']:+.2f}% (vol {res['std_smb_ann']:.2f}%, t = {res['t_smb']:.2f})"
    )
    print(
        f"HML Annualized Premium:   {res['mean_hml_ann']:+.2f}% (vol {res['std_hml_ann']:.2f}%, t = {res['t_hml']:.2f})"
    )
    print(f"SMB-HML Correlation:      {res['corr_smb_hml']:+.4f}")


main()
