"""Lab CAP4-L03-1: Pre-Registration Protocol Hash & Forking Path Diagnostic.

Evaluates methodological pre-registration by generating a cryptographic SHA-256 specification hash,
executing a multi-path specification curve across researcher degrees of freedom, and contrasting
pre-registered effect sizes against post-hoc cherry-picked extremes.
"""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any

import numpy as np


def main() -> None:
    np.random.seed(42)

    # 1. Define pre-registered study specification parameters
    preregistration_spec: dict[str, Any] = {
        "hypothesis": "Cross-sectional momentum premium conditioned on intermediary leverage",
        "sample_start": "1972-01-01",
        "sample_end": "2024-12-31",
        "asset_universe": "CRSP common equities excluding microcaps (< 20th NYSE percentile)",
        "rebalancing": "Monthly value-weighted decile spreads",
        "controls": ["size", "book_to_market", "operating_profitability", "investment"],
        "clustering": "Two-way firm and calendar quarter",
        "primary_loss": "Mean cross-sectional pricing error under Shanken correction",
        "significance_threshold": 0.005,  # Stricter pre-registered hurdle
    }

    # Generate immutable cryptographic SHA-256 hash of the protocol
    spec_json = json.dumps(preregistration_spec, sort_keys=True)
    spec_hash = hashlib.sha256(spec_json.encode("utf-8")).hexdigest()

    # 2. Simulate a garden of forking paths (24 specification variations)
    # Varying: microcap filter (3 options), weighting (2 options), control lags (4 options)
    # Underlying true effect is 0.25% monthly (t ~ 2.1)
    true_alpha = 0.0025
    t_obs = 300
    noise = np.random.normal(0.0, 0.012, size=(24, t_obs))

    estimates: list[float] = []
    t_stats: list[float] = []
    p_values: list[float] = []

    for i in range(24):
        # Specific choice variations add small sample selection perturbations
        bias_shift = (i - 12) * 0.00015
        monthly_series = true_alpha + bias_shift + noise[i]
        est_mean = float(np.mean(monthly_series))
        se = float(np.std(monthly_series, ddof=1) / np.sqrt(t_obs))
        t_val = float(est_mean / se)
        # Two-tailed p-value normal approximation
        p_val = float(2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(t_val) / np.sqrt(2.0)))))
        estimates.append(est_mean)
        t_stats.append(t_val)
        p_values.append(p_val)

    # Pre-registered path is path 0 (baseline)
    prereg_est = estimates[0]
    prereg_t = t_stats[0]
    prereg_p = p_values[0]

    # Post-hoc cherry-picked max t-statistic across forking paths
    cherry_picked_idx = int(np.argmax(t_stats))
    cherry_est = estimates[cherry_picked_idx]
    cherry_t = t_stats[cherry_picked_idx]
    cherry_p = p_values[cherry_picked_idx]

    median_est = float(np.median(estimates))
    median_t = float(np.median(t_stats))

    print(f"Pre-Registration Protocol Hash: {spec_hash[:16]}...")
    print(f"Total Forking Paths Evaluated: {len(estimates)}")
    print(f"Pre-Registered Estimate: {prereg_est * 100:.3f}% (t={prereg_t:.2f}, p={prereg_p:.4f})")
    print(f"Median Specification Estimate: {median_est * 100:.3f}% (t={median_t:.2f})")
    print(f"Post-Hoc Cherry-Picked: {cherry_est * 100:.3f}% (t={cherry_t:.2f}, p={cherry_p:.4f})")
    print(f"Inflation Factor (Cherry / Pre-Reg t): {cherry_t / prereg_t:.2f}")


main()
