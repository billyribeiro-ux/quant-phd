"""Lab X4-L02-1: Cross-Sectional Crypto Risk Factors (CMKT, CSMB, CMOM) and Spanning Regressions.

SIMULATED weekly panel of 20 cryptocurrencies over 104 weeks.
Constructs cryptocurrency market (CMKT), size (CSMB), and momentum (CMOM) factors
following Liu, Tsyvinski & Wu (2022, JF), runs Fama-MacBeth risk premia estimation,
and tests factor spanning on a candidate network factor.
"""

from __future__ import annotations

import math
import random


def regress_ols(y: list[float], x_matrix: list[list[float]]) -> tuple[list[float], list[float], float]:
    """Multiple OLS regression: y = X * beta + eps (X includes intercept as column 0).

    Returns (betas, t_stats, r2).
    """
    n = len(y)
    p = len(x_matrix[0])

    # X^T * X
    xtx = [[sum(x_matrix[i][j] * x_matrix[i][k] for i in range(n)) for k in range(p)] for j in range(p)]
    # X^T * y
    xty = [sum(x_matrix[i][j] * y[i] for i in range(n)) for j in range(p)]

    # Solve via Gaussian elimination
    a = [row[:] for row in xtx]
    b = xty[:]
    for i in range(p):
        pivot = a[i][i]
        for j in range(i + 1, p):
            factor = a[j][i] / pivot
            for k in range(i, p):
                a[j][k] -= factor * a[i][k]
            b[j] -= factor * b[i]

    beta = [0.0] * p
    for i in range(p - 1, -1, -1):
        s = sum(a[i][j] * beta[j] for j in range(i + 1, p))
        beta[i] = (b[i] - s) / a[i][i]

    # Residuals & variance
    y_pred = [sum(x_matrix[i][j] * beta[j] for j in range(p)) for i in range(n)]
    residuals = [yi - ypi for yi, ypi in zip(y, y_pred, strict=True)]
    sse = sum(e**2 for e in residuals)
    mean_y = sum(y) / n
    sst = sum((yi - mean_y) ** 2 for yi in y)
    r2 = 1.0 - (sse / sst) if sst > 0 else 0.0

    sigma2 = sse / (n - p) if n > p else 0.0

    # Invert xtx for standard errors
    inv_xtx = [[1.0 if j == k else 0.0 for k in range(p)] for j in range(p)]
    a_inv = [row[:] for row in xtx]
    for i in range(p):
        piv = a_inv[i][i]
        for k in range(p):
            a_inv[i][k] /= piv
            inv_xtx[i][k] /= piv
        for j in range(p):
            if j != i:
                f = a_inv[j][i]
                for k in range(p):
                    a_inv[j][k] -= f * a_inv[i][k]
                    inv_xtx[j][k] -= f * inv_xtx[i][k]

    t_stats = [beta[j] / math.sqrt(max(1e-12, sigma2 * inv_xtx[j][j])) for j in range(p)]
    return beta, t_stats, r2


def main() -> None:
    print("Lab X4-L02-1 | Three-Factor Cryptocurrency Asset Pricing & Spanning")
    print("-------------------------------------------------------------------")

    rng = random.Random(101)
    n_assets = 20
    n_weeks = 104

    # Generate market capitalization, historical returns, and factor loadings
    # Liu, Tsyvinski & Wu (2022): CMKT (mkt excess), CSMB (size), CMOM (momentum)
    cmkt: list[float] = [rng.gauss(0.008, 0.065) for _ in range(n_weeks)]
    csmb: list[float] = [rng.gauss(0.005, 0.040) for _ in range(n_weeks)]
    cmom: list[float] = [rng.gauss(0.007, 0.045) for _ in range(n_weeks)]

    # Candidate network adoption anomaly factor (NVT factor)
    # Constructed to have beta on CMKT and CSMB, but zero true abnormal alpha
    nvt_factor: list[float] = [0.0005 + 0.35 * cmkt[t] + 0.40 * csmb[t] + rng.gauss(0.0, 0.020) for t in range(n_weeks)]

    # Asset return panel
    asset_returns: list[list[float]] = []  # shape: (n_assets, n_weeks)
    for i in range(n_assets):
        b_mkt = 0.70 + 0.05 * i
        b_smb = 1.20 - 0.10 * i
        b_mom = -0.40 + 0.05 * i
        ret_series: list[float] = []
        for t in range(n_weeks):
            idio = rng.gauss(0.0, 0.05)
            r = b_mkt * cmkt[t] + b_smb * csmb[t] + b_mom * cmom[t] + idio
            ret_series.append(r)
        asset_returns.append(ret_series)

    # First pass: Time-series regressions to estimate factor betas
    betas_mkt: list[float] = []
    betas_smb: list[float] = []
    betas_mom: list[float] = []

    x_mat_ts = [[1.0, cmkt[t], csmb[t], cmom[t]] for t in range(n_weeks)]
    for i in range(n_assets):
        b, _, _ = regress_ols(asset_returns[i], x_mat_ts)
        betas_mkt.append(b[1])
        betas_smb.append(b[2])
        betas_mom.append(b[3])

    # Second pass: Cross-sectional Fama-MacBeth regressions at each week t
    lambda_mkt_series: list[float] = []
    lambda_smb_series: list[float] = []
    lambda_mom_series: list[float] = []

    for t in range(n_weeks):
        y_cs = [asset_returns[i][t] for i in range(n_assets)]
        x_cs = [[1.0, betas_mkt[i], betas_smb[i], betas_mom[i]] for i in range(n_assets)]
        gammas, _, _ = regress_ols(y_cs, x_cs)
        lambda_mkt_series.append(gammas[1])
        lambda_smb_series.append(gammas[2])
        lambda_mom_series.append(gammas[3])

    # Average Fama-MacBeth risk premia and t-stats
    def mean_and_t(series: list[float]) -> tuple[float, float]:
        m = sum(series) / len(series)
        var = sum((s - m) ** 2 for s in series) / (len(series) - 1)
        se = math.sqrt(var / len(series))
        return m, m / se

    prem_mkt, t_mkt = mean_and_t(lambda_mkt_series)
    prem_smb, t_smb = mean_and_t(lambda_smb_series)
    prem_mom, t_mom = mean_and_t(lambda_mom_series)

    print("Fama-MacBeth Cross-Sectional Risk Premia (Weekly):")
    print(f"  CMKT Risk Premium: {prem_mkt:.4f} (t-stat = {t_mkt:.2f})")
    print(f"  CSMB Risk Premium: {prem_smb:.4f} (t-stat = {t_smb:.2f})")
    print(f"  CMOM Risk Premium: {prem_mom:.4f} (t-stat = {t_mom:.2f})")

    # Spanning Regression: Test whether NVT factor alpha is subsumed by 3-factor model
    # NVT_t = alpha + beta_mkt * CMKT_t + beta_smb * CSMB_t + beta_mom * CMOM_t + eps_t
    b_span, t_span, r2_span = regress_ols(nvt_factor, x_mat_ts)
    alpha_span = b_span[0]
    t_alpha_span = t_span[0]

    print("\nFactor Spanning Regression for Candidate Network (NVT) Factor:")
    print(f"  Spanning Alpha:   {alpha_span:.5f} (t-stat = {t_alpha_span:.2f})")
    print(f"  Beta on CMKT:     {b_span[1]:.4f} (t-stat = {t_span[1]:.2f})")
    print(f"  Beta on CSMB:     {b_span[2]:.4f} (t-stat = {t_span[2]:.2f})")
    print(f"  Beta on CMOM:     {b_span[3]:.4f} (t-stat = {t_span[3]:.2f})")
    print(f"  R-squared:        {r2_span:.4f}")

    # Spanned test: alpha is statistically indistinguishable from zero (|t| < 1.96)
    is_spanned = abs(t_alpha_span) < 1.96
    print(f"Candidate factor spanned by Liu-Tsyvinski-Wu 3-factor model: {is_spanned}")


main()
