"""Starter code for BK2: Berk-Green Fund Economics Model (fund_model.py).

Complete each function below according to the specification.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FundParameters:
    """Parameters governing a mutual fund under the Berk-Green model."""

    prior_mean: float
    prior_variance: float
    noise_variance: float
    fee_rate: float
    cost_parameter: float
    initial_aum: float


def update_belief(
    prior_mean: float,
    prior_variance: float,
    signal: float,
    noise_variance: float,
) -> tuple[float, float]:
    """Update Gaussian beliefs N(mu, sigma^2) given an observed signal."""
    raise NotImplementedError("Implement update_belief")


def capacity_aum(
    expected_skill: float,
    fee_rate: float,
    cost_parameter: float,
) -> float:
    """Compute rational equilibrium capacity AUM where expected net alpha is zero."""
    raise NotImplementedError("Implement capacity_aum")


def gross_alpha(skill: float, aum: float, cost_parameter: float) -> float:
    """Compute fund gross alpha before management fees."""
    raise NotImplementedError("Implement gross_alpha")


def net_alpha(
    skill: float,
    aum: float,
    cost_parameter: float,
    fee_rate: float,
) -> float:
    """Compute fund net alpha delivered to investors after fees."""
    raise NotImplementedError("Implement net_alpha")


def extract_signal(gross_return: float, aum: float, cost_parameter: float) -> float:
    """Extract signal of skill from realized gross return and fund scale."""
    raise NotImplementedError("Implement extract_signal")


def manager_rent_share(total_fees: float, investor_profit: float) -> float:
    """Compute the fraction of economic surplus captured by fund managers."""
    raise NotImplementedError("Implement manager_rent_share")


def simulate_fund_lifecycle(
    params: FundParameters,
    true_skill: float,
    noise_shocks: list[float],
) -> dict[str, Any]:
    """Simulate the multi-period Berk-Green fund lifecycle."""
    raise NotImplementedError("Implement simulate_fund_lifecycle")
