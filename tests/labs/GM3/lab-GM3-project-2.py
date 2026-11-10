"""Lab GM3-project-2: Rung 2 Completion Problem Twin — Out-of-Sample Drift Evaluation and Decay Test.

SIMULATED: Solution twin for evaluating post-publication decay of pre-FOMC drift
by comparing in-sample (1994-2011) and out-of-sample (2012-2023) event windows via Welch's t-test.
"""

from __future__ import annotations

import math

import numpy as np


def main() -> None:
    rng = np.random.default_rng(42)
    n_is = 144
    n_oos = 100

    # In-sample drift returns: mean ~ +50 bps, std ~ 105 bps
    is_drift_bps = rng.normal(50.5, 105.0, size=n_is)
    # Out-of-sample drift returns: mean ~ +2 bps (decayed), std ~ 105 bps
    oos_drift_bps = rng.normal(2.0, 105.0, size=n_oos)

    mu_is = float(np.mean(is_drift_bps))
    var_is = float(np.var(is_drift_bps, ddof=1))

    mu_oos = float(np.mean(oos_drift_bps))
    var_oos = float(np.var(oos_drift_bps, ddof=1))

    decay_ratio = mu_oos / mu_is if abs(mu_is) > 1e-12 else 0.0
    diff = mu_oos - mu_is

    se_welch = math.sqrt(var_is / n_is + var_oos / n_oos)
    welch_t = diff / se_welch

    # Welch p-value (two-sided normal approximation for large df)
    welch_p = math.erfc(abs(welch_t) / math.sqrt(2.0))

    # OOS survival check (OOS mean > 0 and OOS t-stat significant at 5%)
    se_oos = math.sqrt(var_oos / n_oos)
    t_oos = mu_oos / se_oos
    p_oos = math.erfc(abs(t_oos) / math.sqrt(2.0))
    survived = 1 if (mu_oos > 0 and p_oos < 0.05) else 0

    print("Out-of-Sample Announcements:", n_oos)
    print("In-Sample Mean Drift (bps):", round(mu_is, 4))
    print("Out-of-Sample Mean Drift (bps):", round(mu_oos, 4))
    print("Decay Ratio (OOS / IS):", round(decay_ratio, 4))
    print("Difference (OOS - IS bps):", round(diff, 4))
    print("Welch Two-Sample t-statistic:", round(welch_t, 4))
    print("Welch p-value:", round(welch_p, 4))
    print("Drift Survived OOS (1=Yes, 0=No):", survived)


main()
