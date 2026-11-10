"""Lab S0-L03-1: Missing-data mechanisms (MCAR, MAR, MNAR) on simulated returns.

Demonstrates the effect of missing-data mechanisms on location estimation:
MCAR preserves unbiasedness; MAR introduces marginal bias that observed covariates
can correct via IPW; MNAR creates irreparable survivorship bias when bad returns drop out.
Data label: SIMULATED synthetic panel.
"""

from __future__ import annotations

import random
import statistics


def main() -> None:
    # SIMULATED panel of N=5000 asset returns and firm characteristics
    seed = 42
    rng = random.Random(seed)
    n = 5000

    # Observable covariate X (e.g., firm size or liquidity score in [0, 1])
    x = [rng.uniform(0.0, 1.0) for _ in range(n)]
    eps = [rng.gauss(0.0, 0.10) for _ in range(n)]
    # True return DGP: E[Y | X] = 0.02 + 0.06 * X; true E[Y] = 0.05
    y = [0.02 + 0.06 * x[i] + eps[i] for i in range(n)]
    true_mean = statistics.mean(y)

    # 1. MCAR: 30% missing uniformly, independent of X and Y
    m_mcar = [1 if rng.random() < 0.30 else 0 for _ in range(n)]
    y_mcar = [y[i] for i in range(n) if m_mcar[i] == 0]
    mean_mcar = statistics.mean(y_mcar)

    # 2. MAR: missingness depends on observable X (60% missing for small X, 10% for large X)
    p_mar = [0.60 if x[i] < 0.50 else 0.10 for i in range(n)]
    m_mar = [1 if rng.random() < p_mar[i] else 0 for i in range(n)]
    y_mar = [y[i] for i in range(n) if m_mar[i] == 0]
    mean_mar_naive = statistics.mean(y_mar)

    # Inverse probability weighting (IPW) using propensity P(observed | X) = 1 - P(missing | X)
    obs_weights = [1.0 / (1.0 - p_mar[i]) for i in range(n) if m_mar[i] == 0]
    mean_mar_ipw = sum(w * y_val for w, y_val in zip(obs_weights, y_mar, strict=True)) / sum(obs_weights)

    # 3. MNAR: missingness depends directly on unobserved return Y (delisting shock below -10%)
    p_mnar = [0.85 if y[i] < -0.10 else 0.05 for i in range(n)]
    m_mnar = [1 if rng.random() < p_mnar[i] else 0 for i in range(n)]
    y_mnar = [y[i] for i in range(n) if m_mnar[i] == 0]
    mean_mnar = statistics.mean(y_mnar)

    print(f"Sample size: {n}")
    print(f"True population mean: {true_mean:.5f}")
    print(f"MCAR mean: {mean_mcar:.5f} (bias: {mean_mcar - true_mean:+.5f})")
    print(f"MAR naive mean: {mean_mar_naive:.5f} (bias: {mean_mar_naive - true_mean:+.5f})")
    print(f"MAR IPW-adjusted mean: {mean_mar_ipw:.5f} (bias: {mean_mar_ipw - true_mean:+.5f})")
    print(f"MNAR mean: {mean_mnar:.5f} (bias: {mean_mnar - true_mean:+.5f})")
    print(f"MCAR bias within 0.005: {abs(mean_mcar - true_mean) < 0.005}")
    print(f"IPW corrects MAR within 0.002: {abs(mean_mar_ipw - true_mean) < 0.002}")
    print(f"MNAR produces positive survivorship bias: {mean_mnar - true_mean > 0.010}")


main()
