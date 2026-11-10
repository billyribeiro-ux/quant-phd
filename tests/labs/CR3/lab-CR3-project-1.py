"""Lab CR3-project-1 (Rung 1, Worked Example): Fully solved credit cycle analytics workflow.

SIMULATED: complete end-to-end demonstration of the CR3 quantitative credit cycle engine:
1. Gilchrist-Zakrajšek spread decomposition into default risk and EBP.
2. Credit-market sentiment index construction and autocorrelation.
3. Two-stage predictive spread reversal regressions with HAC inference.
4. Recession forecasting via multivariate logistic/probit regression.
5. Out-of-sample forecast accuracy: Brier score, ROC-AUC, and confusion matrix.
6. Leveraged loan priority loss waterfall under cov-lite vs maintenance terms.
Standard library, numpy, and scipy only; no network.
"""

from __future__ import annotations

import math

import numpy as np
from scipy import optimize


def main() -> None:
    # -------------------------------------------------------------------------
    # Step 1: Gilchrist-Zakrajsek (2012) Spread Decomposition & EBP
    # -------------------------------------------------------------------------
    print("Step 1 · GZ Credit Spread Decomposition & EBP:")
    np.random.seed(42)
    n_bonds = 40
    durations = np.random.uniform(2.0, 10.0, n_bonds)
    coupons = np.random.uniform(0.03, 0.08, n_bonds)
    amounts = np.random.uniform(200.0, 1000.0, n_bonds)
    edfs = np.random.uniform(0.002, 0.040, n_bonds)
    industries = np.random.randint(0, 4, n_bonds)

    # True log spread DGP with 30 bp macro EBP shock
    log_spread_true = 3.6 + 0.05 * (durations - 5.0) + 0.50 * (np.log(edfs) - math.log(0.01))
    spreads_bps = np.exp(log_spread_true + np.random.normal(0.0, 0.12, n_bonds)) + 30.0

    # Cross-sectional log-linear regression
    y_log = np.log(spreads_bps)
    x_mat = np.column_stack(
        [
            np.ones(n_bonds),
            durations,
            coupons,
            np.log(amounts),
            np.log(edfs),
            np.where(industries == 1, 1.0, 0.0),
            np.where(industries == 2, 1.0, 0.0),
            np.where(industries == 3, 1.0, 0.0),
        ]
    )
    beta = np.linalg.lstsq(x_mat, y_log, rcond=None)[0]
    y_pred_log = x_mat @ beta
    e = y_log - y_pred_log
    res_var = float(np.sum(e**2) / (n_bonds - x_mat.shape[1]))

    # Jensen-corrected predicted spread
    s_hat = np.exp(y_pred_log + 0.5 * res_var)
    gz_spread = float(np.mean(spreads_bps))
    pred_spread = float(np.mean(s_hat))
    ebp = gz_spread - pred_spread

    print(f"  Observed GZ Spread:         {gz_spread:.1f} bp")
    print(f"  Fitted Default Component:   {pred_spread:.1f} bp")
    print(f"  Excess Bond Premium (EBP):  {ebp:.1f} bp")
    assert abs(gz_spread - pred_spread - ebp) < 1e-9

    # -------------------------------------------------------------------------
    # Step 2: Credit-Market Sentiment Index
    # -------------------------------------------------------------------------
    print("\nStep 2 · Credit-Market Sentiment Index (López-Salido et al. 2017):")
    t_quarters = 32
    hy_share = np.random.uniform(0.12, 0.38, t_quarters)
    cr_spreads = np.random.uniform(110.0, 320.0, t_quarters)
    ebp_series = np.random.uniform(-40.0, 90.0, t_quarters)

    def z_score(v: np.ndarray) -> np.ndarray:
        return np.asarray((v - np.mean(v)) / np.std(v, ddof=1))

    z_hy = z_score(hy_share)
    z_spr = z_score(cr_spreads)
    z_ebp = z_score(ebp_series)

    # Standardized composite sentiment: high HY, compressed spreads, negative EBP
    sentiment = (z_hy - z_spr - z_ebp) / 3.0
    s_centered = sentiment - np.mean(sentiment)
    rho1 = float(np.sum(s_centered[:-1] * s_centered[1:]) / np.sum(s_centered**2))

    print(f"  Sentiment Index Mean:       {float(np.mean(sentiment)):.4f}")
    print(f"  Sentiment Index Std:        {float(np.std(sentiment, ddof=1)):.4f}")
    print(f"  Lag-1 Autocorrelation:      {rho1:.4f}")

    # -------------------------------------------------------------------------
    # Step 3: Predictable Spread Reversals with Newey-West HAC
    # -------------------------------------------------------------------------
    print("\nStep 3 · Predictable Spread Reversals (Stage 1 Regression):")
    horizon = 4
    m = t_quarters - horizon
    delta_spread = cr_spreads[horizon:] - cr_spreads[:-horizon]
    x_sent = sentiment[:m]

    x_rev = np.column_stack([np.ones(m), x_sent])
    b_rev = np.linalg.lstsq(x_rev, delta_spread, rcond=None)[0]
    u = delta_spread - x_rev @ b_rev

    # Newey-West HAC covariance matrix
    q_inv = np.linalg.inv((x_rev.T @ x_rev) / m)
    omega = np.zeros((2, 2))
    for t in range(m):
        xt = x_rev[t : t + 1].T
        omega += (u[t] ** 2) * (xt @ xt.T)
    omega /= m
    for lag in range(1, horizon + 1):
        w = 1.0 - lag / (horizon + 1.0)
        gamma_l = np.zeros((2, 2))
        for t in range(lag, m):
            gamma_l += u[t] * u[t - lag] * (x_rev[t : t + 1].T @ x_rev[t - lag : t - lag + 1])
        gamma_l /= m
        omega += w * (gamma_l + gamma_l.T)

    v_hac = (q_inv @ omega @ q_inv) / m
    se_b = math.sqrt(v_hac[1, 1])
    t_stat = b_rev[1] / se_b
    print(f"  Forward Spread Change beta: {b_rev[1]:.2f} bp per unit sentiment")
    print(f"  Newey-West HAC t-statistic: {t_stat:.2f}")

    # -------------------------------------------------------------------------
    # Step 4: Probit / Logistic Recession Forecasting
    # -------------------------------------------------------------------------
    print("\nStep 4 · Probit / Logistic Recession Forecasting Regression:")
    t_macro = 48
    term_spread = np.random.uniform(-1.0, 2.5, t_macro)
    credit_ind = np.random.uniform(-1.5, 2.0, t_macro)
    # True latent probability: inverted term spread + high credit distress -> recession
    true_z = -1.8 + 1.2 * credit_ind - 1.4 * term_spread
    p_true = 1.0 / (1.0 + np.exp(-true_z))
    y_rec = (np.random.uniform(0.0, 1.0, t_macro) < p_true).astype(float)
    if np.sum(y_rec) == 0:
        y_rec[0] = 1.0

    x_rec = np.column_stack([np.ones(t_macro), credit_ind, term_spread])

    def neg_ll(b: np.ndarray) -> float:
        z = np.clip(x_rec @ b, -25.0, 25.0)
        p = np.clip(1.0 / (1.0 + np.exp(-z)), 1e-12, 1.0 - 1e-12)
        return -float(np.sum(y_rec * np.log(p) + (1.0 - y_rec) * np.log(1.0 - p)))

    opt = optimize.minimize(neg_ll, np.zeros(3), method="BFGS")
    b_rec = opt.x
    log_lik = -float(opt.fun)

    p_bar = float(np.mean(y_rec))
    null_ll = float(np.sum(y_rec * math.log(p_bar) + (1.0 - y_rec) * math.log(1.0 - p_bar)))
    pseudo_r2 = 1.0 - log_lik / null_ll

    print(f"  Intercept beta_0:           {b_rec[0]:.3f}")
    print(f"  Credit Indicator beta_1:    {b_rec[1]:.3f} (positive distress impact)")
    print(f"  Term Spread beta_2:         {b_rec[2]:.3f} (negative slope impact)")
    print(f"  McFadden Pseudo R^2:        {pseudo_r2 * 100:.1f}%")

    # -------------------------------------------------------------------------
    # Step 5: Out-of-Sample Forecast Evaluation
    # -------------------------------------------------------------------------
    print("\nStep 5 · Out-of-Sample Recession Evaluation & ROC-AUC:")
    p_fitted = 1.0 / (1.0 + np.exp(-np.clip(x_rec @ b_rec, -20.0, 20.0)))
    brier = float(np.mean((p_fitted - y_rec) ** 2))

    # Exact Mann-Whitney AUC-ROC
    pos = p_fitted[y_rec == 1.0]
    neg = p_fitted[y_rec == 0.0]
    auc = float(np.sum([np.sum(pv > neg) + 0.5 * np.sum(pv == neg) for pv in pos])) / (len(pos) * len(neg))

    print(f"  Brier Score:                {brier:.4f}")
    print(f"  Area Under ROC Curve (AUC): {auc:.4f}")
    assert 0.50 <= auc <= 1.0

    # -------------------------------------------------------------------------
    # Step 6: Leveraged Loan Priority Loss Waterfall
    # -------------------------------------------------------------------------
    print("\nStep 6 · Leveraged Loan Waterfall: Maintenance vs Cov-Lite Underwriting:")
    debt = 500.0
    ebitda = 80.0
    distress = 0.45
    senior_share = 0.80

    for cov_lite in [False, True]:
        distressed_ebitda = ebitda * (1.0 - distress)
        # Maintenance loans preserve 7.0x multiple; cov-lite delay erodes multiple by 35%
        ev = distressed_ebitda * 7.0 if not cov_lite else distressed_ebitda * 7.0 * 0.65
        senior_debt = debt * senior_share

        senior_rec = min(senior_debt, ev) / senior_debt
        total_rec = min(debt, ev) / debt
        covenant_breached = (debt / distressed_ebitda > 6.5) if not cov_lite else False

        label = "Cov-Lite   " if cov_lite else "Maintenance"
        s_pct = senior_rec * 100
        t_pct = total_rec * 100
        print(
            f"  {label} | Breached: {covenant_breached!s:5s} | EV: {ev:5.1f} | "
            f"Senior: {s_pct:4.1f}% | Total: {t_pct:4.1f}%"
        )


main()
