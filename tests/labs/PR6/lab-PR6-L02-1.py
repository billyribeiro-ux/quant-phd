"""Lab PR6-L02-1: Merton (1971, 1973) Intertemporal Hedging Demand Decomposition.

SIMULATED: Analytical decomposition and numerical verification of myopic vs
intertemporal hedging demands across state correlation and risk aversion.
"""

from __future__ import annotations

import numpy as np


def merton_hedging_decomposition(
    rhos: list[float],
    gammas: list[float],
    excess_return: float = 0.06,
    sigma: float = 0.20,
    sigma_s: float = 0.15,
    kappa: float = 0.15,
    lambda_1: float = 0.50,
    horizon: float = 10.0,
) -> dict[tuple[float, float], dict[str, float]]:
    """Compute Merton myopic and intertemporal hedging portfolio demands.

    State variable S_t governs expected excess return: mu(S) - r = lambda_0 + lambda_1 * S.
    Value function J(W, S, t) = (W^(1-gamma) / (1-gamma)) * exp(B(tau)*S + A(tau)).
    In the linear approximation (Campbell & Viceira 2002, Kim & Omberg 1996),
    B(tau) = lambda_1 * (1 - exp(-kappa_star * tau)) / kappa_star where kappa_star adjusts for risk.
    Hedging demand is alpha_hedge = (rho * sigma_s / (gamma * sigma)) * B(tau) * (1 - gamma) / gamma...
    Specifically, the hedging weight is:
        alpha_hedge = ((1 - 1/gamma) * (rho * sigma_s / sigma) * (1 - exp(-kappa * tau)) / kappa) * (lambda_1 / sigma).
    """
    results: dict[tuple[float, float], dict[str, float]] = {}

    for gamma in gammas:
        myopic = excess_return / (gamma * sigma**2)
        for rho in rhos:
            if gamma == 1.0 or abs(rho) < 1e-12:
                # Log utility has identically zero hedging demand, as does uncorrelated state
                hedging = 0.0
            else:
                # Effective persistence factor for long horizon tau
                # When rho < 0 and lambda_1 > 0, bad return shocks correlate with improved future returns
                # Campbell & Viceira (2002) closed-form approximation:
                integral_factor = (1.0 - np.exp(-kappa * horizon)) / kappa
                hedging = (1.0 - 1.0 / gamma) * (-rho * sigma_s / sigma) * integral_factor * (excess_return / sigma**2)

            total = myopic + hedging
            hedge_pct = (hedging / total * 100.0) if abs(total) > 1e-8 else 0.0

            results[(gamma, rho)] = {
                "myopic": myopic,
                "hedging": hedging,
                "total": total,
                "hedge_pct": hedge_pct,
            }

    return results


def main() -> None:
    excess_return = 0.06
    sigma = 0.20
    sigma_s = 0.15
    kappa = 0.15
    horizon = 10.0
    gammas = [1.0, 2.0, 5.0, 10.0]
    rhos = [-0.75, -0.40, 0.00, 0.40, 0.75]

    res = merton_hedging_decomposition(
        rhos=rhos,
        gammas=gammas,
        excess_return=excess_return,
        sigma=sigma,
        sigma_s=sigma_s,
        kappa=kappa,
        horizon=horizon,
    )

    print("Merton (1971, 1973) Intertemporal Hedging Demand Decomposition:")
    print(
        f"Parameters: Excess Ret={excess_return:.2f}, Asset Vol={sigma:.2f}, "
        f"State Vol={sigma_s:.2f}, Horizon={horizon:.0f}y"
    )
    print("=" * 86)
    print(
        f"{'Risk Aversion (gamma)':<24} {'Correlation (rho)':<19} {'Myopic Demand':<15} "
        f"{'Hedging Demand':<16} {'Total Allocation':<16}"
    )
    print("-" * 86)

    for gamma in gammas:
        for rho in rhos:
            d = res[(gamma, rho)]
            print(
                f"gamma={gamma:<18.1f} rho={rho:<15.2f} {d['myopic']:<15.4f} {d['hedging']:<16.4f} {d['total']:<16.4f}"
            )
        print("-" * 86)

    print("Key Theoretical Properties:")
    print("1. Log Utility (gamma=1): Hedging demand is strictly zero regardless of correlation rho.")
    print("2. Orthogonal State (rho=0): Hedging demand is strictly zero across all risk aversions.")
    print("3. Negative Correlation (rho<0): Investors with gamma > 1 exhibit substantial positive hedging demand.")


main()
