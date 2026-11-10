"""Lab 1 for PM2 L01: Staged Venture Financing as a Real Option to Abandon.

SIMULATED: A high-tech startup requiring $10.0M total capital across two phases:
Phase 1: $3.0M upfront for technical proof of concept (duration 1.5 years).
Phase 2: $7.0M expansion capital (duration 2.5 years) if Phase 1 succeeds.
Probability of Phase 1 success = 0.40; if successful, Phase 2 expected payoff is $35.0M.
If Phase 1 fails (prob 0.60), Phase 2 expected payoff is only $4.0M.
Discount rate = 20% annualized (risk-adjusted hurdle rate for early-stage venture).

Standard library and NumPy only; fully deterministic.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    r = 0.20  # 20% discount rate
    t1 = 1.5  # Phase 1 duration in years
    t2 = 4.0  # Total duration to final exit in years

    inv_1 = 3.0  # $3.0M Phase 1 investment at t=0
    inv_2 = 7.0  # $7.0M Phase 2 investment at t=1.5

    prob_success = 0.40
    prob_failure = 0.60

    exit_success = 35.0  # Gross payoff if successful at t=4.0
    exit_failure = 4.0  # Gross payoff if failed at t=4.0

    df_1 = np.exp(-r * t1)
    df_2 = np.exp(-r * t2)

    # 1. Upfront Lump-Sum Financing (No Staging, full $10M committed at t=0)
    # The VC invests $3.0M at t=0 and commits $7.0M at t=1.5 regardless of outcome
    pv_investments_lump = inv_1 + inv_2 * df_1
    expected_exit_lump = prob_success * exit_success + prob_failure * exit_failure
    pv_exit_lump = expected_exit_lump * df_2
    npv_lump = pv_exit_lump - pv_investments_lump

    # 2. Staged Financing (Milestone-Contingent Real Option)
    # At t=1.5, VC exercises option to expand only if Phase 2 NPV > 0:
    # Net payoff at t=1.5 given success: PV(exit) - inv_2
    pv_exit_given_success_t1 = exit_success * np.exp(-r * (t2 - t1))
    npv_phase2_success = pv_exit_given_success_t1 - inv_2

    pv_exit_given_failure_t1 = exit_failure * np.exp(-r * (t2 - t1))
    npv_phase2_failure = pv_exit_given_failure_t1 - inv_2

    # Rational VC abandons if npv_phase2 < 0
    phase2_proceed_success = npv_phase2_success > 0.0
    phase2_proceed_failure = npv_phase2_failure > 0.0

    # Valuation of staging option at t=0:
    pv_phase2_decision = prob_success * max(0.0, npv_phase2_success) + prob_failure * max(0.0, npv_phase2_failure)
    npv_staged = -inv_1 + pv_phase2_decision * df_1

    option_value_abandon = npv_staged - npv_lump

    print(f"Lump-Sum Upfront Financing NPV: ${npv_lump:.3f}M")
    print(f"Phase 2 Continuation Decision (Success): {phase2_proceed_success} (NPV: ${npv_phase2_success:.2f}M)")
    print(f"Phase 2 Continuation Decision (Failure): {phase2_proceed_failure} (NPV: ${npv_phase2_failure:.2f}M)")
    print(f"Staged Financing Option-Adjusted NPV: ${npv_staged:.3f}M")
    print(f"Real Option Value of Abandonment: ${option_value_abandon:.3f}M")


main()
