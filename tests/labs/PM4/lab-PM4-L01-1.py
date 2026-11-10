"""Lab PM4-L01-1: Prepayment Modeling — PSA Benchmark vs. Schwartz-Torous Hazard Model.

SIMULATED: Evaluates the PSA benchmark prepayment schedule against the Schwartz & Torous (1989)
log-logistic proportional hazard model under interest rate incentive shifts.
"""

from __future__ import annotations

import numpy as np


def psa_cpr(month: int, speed: float = 100.0) -> float:
    """Compute annualized Conditional Prepayment Rate (CPR) under the PSA benchmark.

    Parameters
    ----------
    month : int
        Loan age in months (1-indexed).
    speed : float
        PSA speed percentage (e.g. 100.0 = 100% PSA).

    Returns
    -------
    float
        Annualized CPR as a decimal.
    """
    if month <= 0:
        raise ValueError("Month must be strictly positive")
    base_cpr = 0.06 if month >= 30 else 0.002 * month
    return float(base_cpr * (speed / 100.0))


def cpr_to_smm(cpr: float) -> float:
    """Convert annualized CPR to Single Monthly Mortality (SMM)."""
    return float(1.0 - (1.0 - cpr) ** (1.0 / 12.0))


def schwartz_torous_hazard(
    month: int,
    refi_incentive: float,
    burnout_factor: float = 1.0,
    gamma: float = 0.015,
    p: float = 2.5,
    beta: float = 40.0,
) -> float:
    """Compute monthly prepayment probability under Schwartz-Torous proportional hazard.

    Parameters
    ----------
    month : int
        Mortgage age in months.
    refi_incentive : float
        Spread between note rate and current refinancing rate (r_m - r).
    burnout_factor : float
        Fraction of sensitive pool remaining (between 0.0 and 1.0).
    gamma : float
        Scale parameter for log-logistic baseline hazard.
    p : float
        Shape parameter for log-logistic baseline hazard.
    beta : float
        Sensitivity parameter for refinancing incentive.

    Returns
    -------
    float
        Monthly hazard rate (SMM equivalent).
    """
    gt = gamma * month
    baseline = (gamma * p * (gt ** (p - 1.0))) / (1.0 + (gt**p))
    covariate_effect = float(np.exp(beta * refi_incentive))
    hazard = baseline * covariate_effect * burnout_factor
    return float(min(0.25, max(0.001, hazard)))


def main() -> None:
    test_months = [6, 12, 24, 30, 60, 120]

    print("PSA Benchmark Prepayment Rates (CPR and SMM):")
    print("Month | 100% PSA CPR | 100% PSA SMM | 150% PSA CPR | 200% PSA CPR")
    for m in test_months:
        cpr_100 = psa_cpr(m, 100.0)
        smm_100 = cpr_to_smm(cpr_100)
        cpr_150 = psa_cpr(m, 150.0)
        cpr_200 = psa_cpr(m, 200.0)
        print(f"{m:5d} | {cpr_100:12.4f} | {smm_100:12.5f} | {cpr_150:12.4f} | {cpr_200:12.4f}")

    print("\nSchwartz-Torous Hazard vs Refinancing Incentive (Month 60):")
    print("Refi Incentive (bps) | Fresh Pool SMM | Burned-Out Pool SMM (50%)")
    incentives_bps = [-200.0, -100.0, 0.0, 50.0, 100.0, 150.0, 200.0]
    for inc_bp in incentives_bps:
        inc = inc_bp / 10000.0
        smm_fresh = schwartz_torous_hazard(60, inc, burnout_factor=1.0)
        smm_burned = schwartz_torous_hazard(60, inc, burnout_factor=0.5)
        print(f"{inc_bp:20.1f} | {smm_fresh:14.5f} | {smm_burned:26.5f}")

    # Verify key qualitative properties
    cpr_30 = psa_cpr(30, 100.0)
    cpr_60 = psa_cpr(60, 100.0)
    assert abs(cpr_30 - 0.06) < 1e-6
    assert abs(cpr_60 - 0.06) < 1e-6

    smm_in_the_money = schwartz_torous_hazard(60, 0.015, burnout_factor=1.0)
    smm_out_of_money = schwartz_torous_hazard(60, -0.015, burnout_factor=1.0)
    assert smm_in_the_money > smm_out_of_money * 3.0


main()
