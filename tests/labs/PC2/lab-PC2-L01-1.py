"""PC2 Lab L01-1: Multi-scenario valuation and payoff distribution calculator.

SIMULATED. Evaluates base, bull, and bear scenario cash flows, probability-weighted
expected values, skewness, and margin of safety for an institutional equity memo.
Standard library only.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Scenario:
    name: str
    target_price: float
    probability: float
    operating_margin: float
    revenue_growth: float
    terminal_multiple: float


@dataclass(frozen=True)
class ValuationDistribution:
    expected_price: float
    expected_return: float
    standard_deviation: float
    skewness: float
    downside_risk: float
    upside_potential: float
    risk_reward_ratio: float
    margin_of_safety: float
    is_actionable: bool


def calculate_scenario_distribution(
    current_price: float,
    scenarios: list[Scenario],
    hurdle_return: float = 0.15,
    min_risk_reward: float = 2.0,
    min_margin_of_safety: float = 0.15,
) -> ValuationDistribution:
    """Compute probability-weighted valuation metrics across scenarios."""
    prob_sum = sum(s.probability for s in scenarios)
    if abs(prob_sum - 1.0) > 1e-6:
        msg = f"Scenario probabilities must sum to 1.0, got {prob_sum:.4f}"
        raise ValueError(msg)

    exp_price = sum(s.probability * s.target_price for s in scenarios)
    exp_return = (exp_price - current_price) / current_price

    variance = sum(s.probability * (s.target_price - exp_price) ** 2 for s in scenarios)
    std_dev = math.sqrt(variance)

    if std_dev > 1e-9:
        skewness = sum(s.probability * ((s.target_price - exp_price) / std_dev) ** 3 for s in scenarios)
    else:
        skewness = 0.0

    bear_scenario = next(s for s in scenarios if s.name.lower() == "bear")
    base_scenario = next(s for s in scenarios if s.name.lower() == "base")

    downside_risk = (current_price - bear_scenario.target_price) / current_price
    upside_potential = (base_scenario.target_price - current_price) / current_price

    risk_reward_ratio = upside_potential / downside_risk if downside_risk > 0 else float("inf")
    margin_of_safety = (exp_price - current_price) / exp_price if exp_price > 0 else 0.0

    is_actionable = (
        exp_return >= hurdle_return
        and risk_reward_ratio >= min_risk_reward
        and margin_of_safety >= min_margin_of_safety
    )

    return ValuationDistribution(
        expected_price=exp_price,
        expected_return=exp_return,
        standard_deviation=std_dev,
        skewness=skewness,
        downside_risk=downside_risk,
        upside_potential=upside_potential,
        risk_reward_ratio=risk_reward_ratio,
        margin_of_safety=margin_of_safety,
        is_actionable=is_actionable,
    )


def main() -> None:
    print("PC2 Lab L01-1: Multi-Scenario Valuation and Payoff Distribution")
    print("SIMULATED equity memo valuation model")

    current_market_price = 70.00

    scenarios = [
        Scenario(
            name="Bear",
            target_price=55.00,
            probability=0.25,
            operating_margin=0.18,
            revenue_growth=0.04,
            terminal_multiple=12.0,
        ),
        Scenario(
            name="Base",
            target_price=105.00,
            probability=0.55,
            operating_margin=0.24,
            revenue_growth=0.10,
            terminal_multiple=16.0,
        ),
        Scenario(
            name="Bull",
            target_price=145.00,
            probability=0.20,
            operating_margin=0.28,
            revenue_growth=0.16,
            terminal_multiple=20.0,
        ),
    ]

    print(f"Current Market Price: ${current_market_price:.2f}")
    print("-" * 65)
    print(f"{'Scenario':8s} | {'Target ($)':10s} | {'Prob':6s} | {'Margin':8s} | {'Growth':8s} | {'Exit Mult':9s}")
    print("-" * 65)
    for s in scenarios:
        print(
            f"{s.name:8s} | ${s.target_price:9.2f} | {s.probability:6.2f} | "
            f"{s.operating_margin * 100:6.1f}% | {s.revenue_growth * 100:6.1f}% | {s.terminal_multiple:9.1f}x"
        )
    print("-" * 65)

    metrics = calculate_scenario_distribution(current_market_price, scenarios)

    print(f"Probability-Weighted Expected Price: ${metrics.expected_price:.2f}")
    print(f"Expected Return:                      {metrics.expected_return * 100:.2f}%")
    print(f"Valuation Standard Deviation:        ${metrics.standard_deviation:.2f}")
    print(f"Distribution Skewness:                {metrics.skewness:.4f}")
    print(f"Downside Risk to Bear Case:           {metrics.downside_risk * 100:.2f}%")
    print(f"Upside Potential to Base Case:        {metrics.upside_potential * 100:.2f}%")
    print(f"Risk/Reward Ratio (Base/Bear):        {metrics.risk_reward_ratio:.2f}x")
    print(f"Margin of Safety:                     {metrics.margin_of_safety * 100:.2f}%")
    print(f"Investment Actionable (Pass Hurdle):  {metrics.is_actionable}")


main()
