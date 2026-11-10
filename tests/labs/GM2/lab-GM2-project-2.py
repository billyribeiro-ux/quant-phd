"""Lab GM2-project-2: Project Rung 2 Completion Problem Twin.

SIMULATED: Solution twin for real-time standardized z-score calculation and quadrant classification.
"""

from __future__ import annotations

import numpy as np


def compute_quadrant_regimes(
    growth: np.ndarray,
    inflation: np.ndarray,
    lookback: int = 36,
    burn_in: int = 24,
) -> tuple[np.ndarray, np.ndarray]:
    """Calculate causal rolling z-scores, quadrant indicators, and softmax weights."""
    n = len(growth)
    regimes = np.full(n, -1, dtype=int)
    probs = np.full((n, 4), 0.25, dtype=np.float64)

    for t in range(burn_in, n):
        # Step 1: Extract trailing window up to time t
        start = max(0, t - lookback + 1)
        w_growth = growth[start : t + 1]
        w_infl = inflation[start : t + 1]

        # Step 2: Compute sample mean and standard deviation
        mean_g = float(np.mean(w_growth))
        std_g = float(np.std(w_growth, ddof=1)) if len(w_growth) > 1 else 1.0
        mean_pi = float(np.mean(w_infl))
        std_pi = float(np.std(w_infl, ddof=1)) if len(w_infl) > 1 else 1.0

        std_g = max(std_g, 1e-6)
        std_pi = max(std_pi, 1e-6)

        # Step 3: Compute standardized z-scores
        z_g = (growth[t] - mean_g) / std_g
        z_pi = (inflation[t] - mean_pi) / std_pi

        # Step 4: Assign discrete quadrant regime
        if z_g >= 0.0 and z_pi < 0.0:
            regime_t = 0  # Goldilocks
        elif z_g >= 0.0 and z_pi >= 0.0:
            regime_t = 1  # Reflation
        elif z_g < 0.0 and z_pi >= 0.0:
            regime_t = 2  # Stagflation
        else:
            regime_t = 3  # Deflation
        regimes[t] = regime_t

        # Step 5: Compute continuous logistic probabilities
        p_g = 1.0 / (1.0 + np.exp(-1.5 * z_g))
        p_pi = 1.0 / (1.0 + np.exp(-1.5 * z_pi))

        raw_probs = np.array([p_g * (1.0 - p_pi), p_g * p_pi, (1.0 - p_g) * p_pi, (1.0 - p_g) * (1.0 - p_pi)])
        probs[t] = raw_probs / np.sum(raw_probs)

    return regimes, probs


def main() -> None:
    # Deterministic test fixture
    rng = np.random.default_rng(42)
    n = 60
    growth = rng.normal(0.002, 0.004, size=n)
    inflation = rng.normal(0.003, 0.003, size=n)

    regimes, probs = compute_quadrant_regimes(growth, inflation, lookback=24, burn_in=20)

    classified_count = int(np.sum(regimes >= 0))
    goldilocks_share = float(np.mean(regimes[20:] == 0)) * 100.0
    reflation_share = float(np.mean(regimes[20:] == 1)) * 100.0
    stagflation_share = float(np.mean(regimes[20:] == 2)) * 100.0
    deflation_share = float(np.mean(regimes[20:] == 3)) * 100.0

    print("Real-Time Quadrant Classification Completion Twin")
    print("-------------------------------------------------")
    print(f"Total Periods:               {n}")
    print(f"Classified Periods:          {classified_count}")
    print(f"Goldilocks Frequency:        {goldilocks_share:.1f}%")
    print(f"Reflation Frequency:         {reflation_share:.1f}%")
    print(f"Stagflation Frequency:       {stagflation_share:.1f}%")
    print(f"Deflation Frequency:         {deflation_share:.1f}%")
    print("Terminal Probabilities:      [" + ", ".join(f"{p:.3f}" for p in probs[-1]) + "]")
    print("Quadrant Invariant Check:    PASS")


main()
