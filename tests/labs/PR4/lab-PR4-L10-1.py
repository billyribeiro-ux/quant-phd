"""Lab 10: Integrated Enterprise Risk Engine Architecture and Model Risk Diagnostics.

Demonstrates unified multi-model risk comparison (Historical, Gaussian, Student-t, EVT)
and quantifies model risk capital buffers per Federal Reserve SR 11-7 / SR 26-2 standards.
"""

from __future__ import annotations

import math

import numpy as np
import scipy.stats


def main() -> None:
    rng = np.random.default_rng(42)
    n_days = 1000
    portfolio_equity = 25_000_000.0  # $25M institutional trading book
    alpha = 0.99

    # Generate leptokurtic asset return innovations (Student-t with df=4)
    returns = rng.standard_t(df=4, size=n_days) * 0.012 - 0.0003
    losses = -returns

    # 1. Historical Simulation Engine
    var_hist = float(np.quantile(losses, alpha, method="linear"))
    es_hist = float(np.mean(losses[losses > var_hist]))

    # 2. Parametric Gaussian Engine
    mu = float(np.mean(losses))
    sigma = float(np.std(losses, ddof=1))
    z = float(scipy.stats.norm.ppf(alpha))
    phi = float(scipy.stats.norm.pdf(z))
    var_norm = mu + sigma * z
    es_norm = mu + sigma * (phi / (1.0 - alpha))

    # 3. Parametric Student-t Engine (df = 4)
    df = 4
    scale = sigma * math.sqrt((df - 2.0) / float(df))
    q = float(scipy.stats.t.ppf(alpha, df=df))
    g_q = float(scipy.stats.t.pdf(q, df=df))
    var_stud = mu + scale * q
    es_stud = mu + scale * ((g_q / (1.0 - alpha)) * ((df + q * q) / (df - 1.0)))

    # 4. Extreme Value Theory POT / GPD Engine
    u = float(np.quantile(losses, 0.90, method="linear"))
    excesses = losses[losses > u] - u
    n_u = len(excesses)
    m_e = float(np.mean(excesses))
    v_e = float(np.var(excesses, ddof=1))
    xi = 0.5 * (1.0 - (m_e**2) / v_e)
    beta = m_e * (1.0 - xi)
    factor = (n_days / n_u) * (1.0 - alpha)
    var_evt = u + (beta / xi) * (factor ** (-xi) - 1.0)
    es_evt = (var_evt + beta - xi * u) / (1.0 - xi)

    # 5. Model Discrepancy & Model Risk Capital Buffer
    dollar_es_norm = portfolio_equity * es_norm
    dollar_es_evt = portfolio_equity * es_evt
    model_risk_spread = dollar_es_evt - dollar_es_norm

    print(f"Portfolio Base Equity: ${portfolio_equity:,.2f} | Confidence: {alpha * 100:.1f}%")
    print("=" * 70)
    print(f"{'Risk Engine Architecture':<28} | {'1-Day VaR':<14} | {'1-Day ES':<14} | {'Capital ($)':<16}")
    print("-" * 70)
    print(
        f"{'Historical Simulation':<28} | {var_hist:<14.5f} | {es_hist:<14.5f} | ${portfolio_equity * es_hist:14,.2f}"
    )
    print(f"{'Parametric Gaussian':<28} | {var_norm:<14.5f} | {es_norm:<14.5f} | ${dollar_es_norm:14,.2f}")
    es_stud_cap = portfolio_equity * es_stud
    print(f"{'Parametric Student-t (df=4)':<28} | {var_stud:<14.5f} | {es_stud:<14.5f} | ${es_stud_cap:14,.2f}")
    print(f"{'EVT Peaks-Over-Threshold':<28} | {var_evt:<14.5f} | {es_evt:<14.5f} | ${dollar_es_evt:14,.2f}")
    print("=" * 70)
    print("Model Risk Assessment (Federal Reserve SR 11-7 / SR 26-2):")
    print(f"  Model Discrepancy (EVT ES minus Gaussian ES): ${model_risk_spread:,.2f}")
    pct_gap = (es_evt - es_norm) / es_norm * 100.0
    print(f"  Relative Model Risk Underestimation Gap:     {pct_gap:+.2f}%")


main()
