"""Lab 1: Empirical Value-at-Risk and Non-Subadditivity Proof.

Demonstrates Value-at-Risk computation on empirical loss distributions
and proves the failure of subadditivity: VaR(L1 + L2) > VaR(L1) + VaR(L2).
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    # Set seed for exact deterministic reproduction
    rng = np.random.default_rng(42)

    # 1. Continuous financial asset loss distribution (Gaussian vs heavy-tailed)
    n_days = 1000
    daily_vol = 0.015
    losses_normal = rng.normal(loc=0.0005, scale=daily_vol, size=n_days)

    alpha_95 = 0.95
    alpha_99 = 0.99

    var_norm_95 = float(np.quantile(losses_normal, alpha_95, method="linear"))
    var_norm_99 = float(np.quantile(losses_normal, alpha_99, method="linear"))

    print(f"Continuous 95% Historical VaR: {var_norm_95:.6f}")
    print(f"Continuous 99% Historical VaR: {var_norm_99:.6f}")

    # 2. Canonical Artzner et al. (1999) Non-Subadditivity Counterexample
    # Two independent credit or digital option positions, each with default probability p = 0.8%
    # and default loss of 100 currency units.
    p_default = 0.008
    notional = 100.0
    n_sims = 100_000

    l1 = (rng.uniform(0.0, 1.0, size=n_sims) < p_default) * notional
    l2 = (rng.uniform(0.0, 1.0, size=n_sims) < p_default) * notional
    l_combined = l1 + l2

    var_l1_99 = float(np.quantile(l1, alpha_99, method="linear"))
    var_l2_99 = float(np.quantile(l2, alpha_99, method="linear"))
    var_port_99 = float(np.quantile(l_combined, alpha_99, method="linear"))

    print(f"Stand-alone VaR_0.99(L1): {var_l1_99:.2f}")
    print(f"Stand-alone VaR_0.99(L2): {var_l2_99:.2f}")
    print(f"Sum of Stand-alone VaRs: {var_l1_99 + var_l2_99:.2f}")
    print(f"Portfolio VaR_0.99(L1 + L2): {var_port_99:.2f}")
    print(f"VaR Subadditivity Holds: {var_port_99 <= (var_l1_99 + var_l2_99)}")


main()
