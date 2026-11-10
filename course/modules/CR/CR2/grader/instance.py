"""Instance generator for the CR2 credit derivatives autograder.

SIMULATED: generates synthetic CDS market quotes, bond cash spreads, funding parameters,
and correlation portfolio structures for testing CDS hazard bootstrapping, CDS-bond basis,
and one-factor Gaussian/Student-t CDO tranche pricing.
Labelled SIMULATED per BLUEPRINT §5.3.

Deterministic per seed; valid by construction.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic test instance for a given integer seed."""
    rng = np.random.default_rng(seed)

    # 1. CDS curve tenors and market spreads (bps)
    tenors = [1.0, 2.0, 3.0, 5.0, 7.0, 10.0]
    base_spread = float(rng.uniform(40.0, 120.0))
    # Upward-sloping term structure with random steepness
    slope = float(rng.uniform(8.0, 25.0))
    spreads_bps = [float(base_spread + slope * (t - 1.0) * float(rng.uniform(0.85, 1.15))) for t in tenors]

    # 2. Market parameters
    recovery_rate = float(rng.choice([0.35, 0.40, 0.45]))
    risk_free_rate = float(rng.uniform(0.02, 0.045))

    # 3. Off-market CDS valuation
    eval_tenor = 5.0
    running_coupon_bps = float(rng.choice([100.0, 500.0]))

    # 4. CDS-Bond Basis parameters
    bond_basis_delta = float(rng.uniform(-35.0, 45.0))
    cds_5y_spread = spreads_bps[3]
    bond_cash_spread_bps = float(cds_5y_spread - bond_basis_delta)
    repo_rate = float(risk_free_rate + rng.uniform(-0.003, 0.005))
    funding_rate = float(risk_free_rate + rng.uniform(0.002, 0.010))

    # 5. Portfolio and Copula parameters
    num_names = 125
    portfolio_pd_5y = float(rng.uniform(0.03, 0.08))
    rho = float(rng.uniform(0.12, 0.35))
    student_t_df = int(rng.choice([3, 4, 5]))

    # 6. Specific CDO tranche for deep testing
    tranche_choice = int(rng.integers(0, 3))
    standard_tranches = [
        (0.0, 0.03),  # Equity
        (0.03, 0.07),  # Mezzanine
        (0.15, 0.30),  # Senior
    ]
    test_attachment, test_detachment = standard_tranches[tranche_choice]

    return {
        "tenors": tenors,
        "spreads_bps": spreads_bps,
        "recovery_rate": recovery_rate,
        "risk_free_rate": risk_free_rate,
        "eval_tenor": eval_tenor,
        "running_coupon_bps": running_coupon_bps,
        "bond_cash_spread_bps": bond_cash_spread_bps,
        "repo_rate": repo_rate,
        "funding_rate": funding_rate,
        "num_names": num_names,
        "portfolio_pd_5y": portfolio_pd_5y,
        "rho": rho,
        "student_t_df": student_t_df,
        "test_attachment": test_attachment,
        "test_detachment": test_detachment,
    }
