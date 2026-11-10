"""Lab E6-L09-1: Heterogeneous agents: Hand-to-mouth share and aggregate interest rate sensitivity.

Evaluates the closed-form aggregate IS interest rate sensitivity in a tractable
heterogeneous-agent (HANK / TANK) economy with hand-to-mouth share mu and procyclical
labor income elasticity lambda > 1.
Computes the analytical amplification factor S(mu) / S(0) = (1 - mu) / (1 - mu * lambda)
over a parameter grid, showing how household heterogeneity amplifies the transmission of
real interest rate innovations.
"""

from __future__ import annotations


def hank_interest_sensitivity(sigma: float, mu: float, lambda_val: float) -> tuple[float, float]:
    """Compute aggregate real interest rate sensitivity and amplification factor.

    Parameters
    ----------
    sigma : float
        Intertemporal elasticity / CRRA risk aversion of unconstrained households.
    mu : float
        Share of hand-to-mouth households in the population (0 <= mu < 1/lambda).
    lambda_val : float
        Cyclicality of labor income relative to aggregate output (lambda > 1).

    Returns
    -------
    tuple[float, float]
        (aggregate_sensitivity, amplification_factor)
    """
    if mu * lambda_val >= 1.0:
        raise ValueError("Indeterminate/explosive Keynesian cross multiplier: mu * lambda >= 1")

    base_sensitivity = 1.0 / sigma
    amplification = (1.0 - mu) / (1.0 - mu * lambda_val)
    aggregate_sensitivity = base_sensitivity * amplification
    return aggregate_sensitivity, amplification


def main() -> None:
    sigma = 1.0  # Unit risk aversion
    lambda_val = 1.25  # Labor income elasticity under sticky-price countercyclical markups

    print("Heterogeneous-Agent Aggregate Sensitivity Check:")
    print(f"Parameters: sigma={sigma}, labor income elasticity lambda={lambda_val}")
    print("Representative-agent (RANK) baseline sensitivity S(0) = 1.0000\n")

    mu_grid = [0.0, 0.1, 0.2, 0.3, 0.4]
    for mu in mu_grid:
        sens, amp = hank_interest_sensitivity(sigma, mu, lambda_val)
        print(f"  Hand-to-mouth share mu = {mu:.1f}: aggregate sensitivity S = {sens:6.4f}, amplification = {amp:6.4f}")


main()
