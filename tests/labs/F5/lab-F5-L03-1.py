"""Lab F5-L03-1: The Anomaly Replication Crisis and Benchmark Sensitivity.

Quantifies the anomaly replication rate across 100 candidate cross-sectional
anomalies, contrasting Hou, Xue & Zhang (2020) value-weighting and q-factor
controls against Jensen, Kelly & Pedersen (2023) equal-weighting and raw spreads.
"""

from __future__ import annotations

import numpy as np


def evaluate_anomaly_replication(seed: int = 42) -> dict[str, float | int]:
    """Simulate anomaly panels and compute replication rates under divergent methodologies."""
    rng = np.random.default_rng(seed)
    n_anomalies = 100
    n_months = 360  # 30 years of monthly data

    # 1. Simulate q-factor benchmark returns (Market, Size, Investment, ROE)
    # Annualized means: MKT 6%, ME 2.5%, I/A 4.0%, ROE 6.0%; vols 16%, 10%, 8%, 9%
    mkt = rng.normal(0.06 / 12, 0.16 / np.sqrt(12), size=n_months)
    me = rng.normal(0.025 / 12, 0.10 / np.sqrt(12), size=n_months)
    ia = rng.normal(0.040 / 12, 0.08 / np.sqrt(12), size=n_months)
    roe = rng.normal(0.060 / 12, 0.09 / np.sqrt(12), size=n_months)
    q_factors = np.column_stack([np.ones(n_months), mkt, me, ia, roe])
    capm_factors = np.column_stack([np.ones(n_months), mkt])

    # 2. Simulate anomaly returns
    # Equal-weighted (EW) anomalies have higher average spreads (microcap premium)
    # Value-weighted (VW) anomalies have lower spreads (attenuated in mega-caps)
    # Many anomalies are correlated with Investment (I/A) and ROE factors
    t_stats_ew_raw = np.zeros(n_anomalies)
    t_stats_vw_raw = np.zeros(n_anomalies)
    t_stats_vw_capm = np.zeros(n_anomalies)
    t_stats_vw_q = np.zeros(n_anomalies)

    for i in range(n_anomalies):
        # Latent exposures
        b_mkt = float(rng.normal(0.0, 0.25))
        b_me = float(rng.normal(0.2, 0.3))
        b_ia = float(rng.normal(0.3, 0.4))
        b_roe = float(rng.normal(0.3, 0.4))

        # True idiosyncratic alpha (monthly): 40% have true alpha, 60% are noise/spanned
        has_true_alpha = rng.uniform(0, 1) < 0.35
        true_alpha = float(rng.uniform(0.0015, 0.0035)) if has_true_alpha else 0.0

        idio_vol = float(rng.uniform(0.025, 0.045))
        eps = rng.normal(0.0, idio_vol, size=n_months)

        # Baseline VW factor return
        r_vw = true_alpha + b_mkt * mkt + b_me * me + b_ia * ia + b_roe * roe + eps

        # EW factor return adds microcap spread (+0.25% / mo) and higher idio vol
        r_ew = r_vw + rng.normal(0.0025, 0.010, size=n_months)

        # T-stats for raw returns
        se_ew_raw = float(np.std(r_ew, ddof=1) / np.sqrt(n_months))
        t_stats_ew_raw[i] = float(np.mean(r_ew) / se_ew_raw)

        se_vw_raw = float(np.std(r_vw, ddof=1) / np.sqrt(n_months))
        t_stats_vw_raw[i] = float(np.mean(r_vw) / se_vw_raw)

        # CAPM alpha regression on VW
        b_capm, _, _, _ = np.linalg.lstsq(capm_factors, r_vw, rcond=None)
        alpha_capm = float(b_capm[0])
        res_capm = r_vw - capm_factors @ b_capm
        s2_capm = float(np.sum(res_capm**2) / (n_months - 2))
        cov_capm = s2_capm * np.linalg.inv(capm_factors.T @ capm_factors)
        t_stats_vw_capm[i] = float(alpha_capm / np.sqrt(cov_capm[0, 0]))

        # q-factor alpha regression on VW
        b_q, _, _, _ = np.linalg.lstsq(q_factors, r_vw, rcond=None)
        alpha_q = float(b_q[0])
        res_q = r_vw - q_factors @ b_q
        s2_q = float(np.sum(res_q**2) / (n_months - 5))
        cov_q = s2_q * np.linalg.inv(q_factors.T @ q_factors)
        t_stats_vw_q[i] = float(alpha_q / np.sqrt(cov_q[0, 0]))

    # Compute replication rates at |t| >= 1.96 and |t| >= 3.00
    rate_ew_raw_196 = float(np.mean(np.abs(t_stats_ew_raw) >= 1.96) * 100)
    rate_vw_raw_196 = float(np.mean(np.abs(t_stats_vw_raw) >= 1.96) * 100)
    rate_vw_capm_196 = float(np.mean(np.abs(t_stats_vw_capm) >= 1.96) * 100)
    rate_vw_q_196 = float(np.mean(np.abs(t_stats_vw_q) >= 1.96) * 100)

    rate_ew_raw_300 = float(np.mean(np.abs(t_stats_ew_raw) >= 3.00) * 100)
    rate_vw_raw_300 = float(np.mean(np.abs(t_stats_vw_raw) >= 3.00) * 100)
    rate_vw_q_300 = float(np.mean(np.abs(t_stats_vw_q) >= 3.00) * 100)

    return {
        "n_anomalies": n_anomalies,
        "n_months": n_months,
        "rate_ew_raw_196": round(rate_ew_raw_196, 1),
        "rate_vw_raw_196": round(rate_vw_raw_196, 1),
        "rate_vw_capm_196": round(rate_vw_capm_196, 1),
        "rate_vw_q_196": round(rate_vw_q_196, 1),
        "rate_ew_raw_300": round(rate_ew_raw_300, 1),
        "rate_vw_raw_300": round(rate_vw_raw_300, 1),
        "rate_vw_q_300": round(rate_vw_q_300, 1),
    }


def main() -> None:
    print("Lab F5-L03-1 | The Anomaly Replication Crisis and Benchmark Sensitivity")
    print("----------------------------------------------------------------------")
    res = evaluate_anomaly_replication(seed=42)
    print(f"Sample: {res['n_anomalies']} published anomaly strategies over {res['n_months']} months")
    print("Replication Rates (|t| >= 1.96):")
    print(f"  1. Equal-Weighted Raw Spreads (JKP style):  {res['rate_ew_raw_196']:.1f}% replicate")
    print(f"  2. Value-Weighted Raw Spreads:              {res['rate_vw_raw_196']:.1f}% replicate")
    print(f"  3. Value-Weighted CAPM Alphas:              {res['rate_vw_capm_196']:.1f}% replicate")
    print(f"  4. Value-Weighted q-factor Alphas (HXZ):    {res['rate_vw_q_196']:.1f}% replicate")
    print("Replication Rates under Conservative Hurdle (|t| >= 3.00, Harvey et al.):")
    print(f"  5. Equal-Weighted Raw Spreads:              {res['rate_ew_raw_300']:.1f}% replicate")
    print(f"  6. Value-Weighted Raw Spreads:              {res['rate_vw_raw_300']:.1f}% replicate")
    print(f"  7. Value-Weighted q-factor Alphas (HXZ):    {res['rate_vw_q_300']:.1f}% replicate")


main()
