"""Lab 2: Expected Shortfall, Coherence Axioms, and Rockafellar-Uryasev Optimization.

Demonstrates the subadditivity of Expected Shortfall on the Artzner portfolio
and validates the Rockafellar-Uryasev (2000) variational formulation.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    rng = np.random.default_rng(42)

    # 1. Coherence on Discrete Credit Portfolio (Artzner et al. 1999 setup)
    p_default = 0.008
    notional = 100.0
    n_sims = 100_000
    alpha = 0.99

    l1 = (rng.uniform(0.0, 1.0, size=n_sims) < p_default) * notional
    l2 = (rng.uniform(0.0, 1.0, size=n_sims) < p_default) * notional
    l_combined = l1 + l2

    def compute_es(loss_arr: np.ndarray, a: float) -> float:
        var = float(np.quantile(loss_arr, a, method="linear"))
        tail = loss_arr[loss_arr > var]
        return float(np.mean(tail)) if len(tail) > 0 else var

    es_l1 = compute_es(l1, alpha)
    es_l2 = compute_es(l2, alpha)
    es_port = compute_es(l_combined, alpha)

    print(f"Stand-alone ES_0.99(L1): {es_l1:.2f}")
    print(f"Stand-alone ES_0.99(L2): {es_l2:.2f}")
    print(f"Sum of Stand-alone ES: {es_l1 + es_l2:.2f}")
    print(f"Portfolio ES_0.99(L1 + L2): {es_port:.2f}")
    print(f"ES Subadditivity Holds: {es_port <= (es_l1 + es_l2)}")

    # 2. Rockafellar-Uryasev (2000) Convex Variational Objective on Gaussian losses
    losses_norm = rng.normal(loc=0.001, scale=0.02, size=50_000)
    var_empirical = float(np.quantile(losses_norm, alpha, method="linear"))
    es_empirical = float(np.mean(losses_norm[losses_norm > var_empirical]))

    # Evaluate F_alpha(v) = v + (1 / (1 - alpha)) * E[max(0, L - v)]
    candidate_vs = np.linspace(var_empirical * 0.7, var_empirical * 1.3, 100)
    f_vals = [float(v + (1.0 / (1.0 - alpha)) * np.mean(np.maximum(0.0, losses_norm - v))) for v in candidate_vs]

    min_idx = int(np.argmin(f_vals))
    v_opt = candidate_vs[min_idx]
    f_min = f_vals[min_idx]

    print(f"Empirical VaR_0.99: {var_empirical:.6f}")
    print(f"Rockafellar-Uryasev Argmin v*: {v_opt:.6f}")
    print(f"Empirical ES_0.99: {es_empirical:.6f}")
    print(f"Rockafellar-Uryasev Min F(v*): {f_min:.6f}")
    print(f"RU Optimization Discrepancy: {abs(f_min - es_empirical):.6f}")


main()
