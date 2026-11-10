"""PC2 Lab L04-1: Fractional Kelly and liquidity-constrained position sizing calculator.

SIMULATED. Implements institutional position sizing integrating discrete Kelly growth optimization,
fractional de-leveraging (0.25x-0.5x), fund risk policy caps, and Almgren-Chriss liquidity horizons.
Standard library only.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PositionSizingResult:
    full_kelly_fraction: float
    half_kelly_fraction: float
    quarter_kelly_fraction: float
    policy_nav_cap: float
    liquidity_cap: float
    binding_weight: float
    allocated_capital: float
    binding_constraint: str
    expected_dollar_gain: float
    max_dollar_loss: float
    days_to_liquidate: float


def calculate_institutional_sizing(
    nav: float,
    win_prob: float,
    upside_gain: float,
    downside_loss: float,
    max_nav_weight: float,
    average_daily_volume: float,
    max_adv_participation: float,
    target_liquidation_days: float,
    kelly_fraction_multiplier: float = 0.25,
) -> PositionSizingResult:
    """Calculate institutional position sizing across Kelly, policy, and liquidity constraints."""
    if not (0.0 < win_prob < 1.0):
        msg = f"Win probability must be in (0, 1), got {win_prob}"
        raise ValueError(msg)
    if upside_gain <= 0.0 or downside_loss <= 0.0:
        msg = "Upside gain and downside loss must be strictly positive"
        raise ValueError(msg)

    # Discrete Kelly formula: f* = (p * b - (1 - p) * a) / (a * b)
    numerator = win_prob * upside_gain - (1.0 - win_prob) * downside_loss
    denominator = upside_gain * downside_loss
    full_kelly = max(0.0, numerator / denominator)

    half_kelly = full_kelly * 0.50
    quarter_kelly = full_kelly * 0.25
    target_fraction = full_kelly * kelly_fraction_multiplier

    # Liquidity constraint: Max position = Days * Participation * ADV
    max_liquidity_capital = target_liquidation_days * max_adv_participation * average_daily_volume
    liquidity_cap_weight = max_liquidity_capital / nav

    # Compare constraints
    constraints = {
        "Fractional Kelly": target_fraction,
        "Policy NAV Cap": max_nav_weight,
        "Liquidity Participation Cap": liquidity_cap_weight,
    }

    binding_name = min(constraints, key=constraints.get)  # type: ignore[arg-type]
    binding_weight = constraints[binding_name]
    allocated_capital = binding_weight * nav

    expected_gain = allocated_capital * (win_prob * upside_gain - (1.0 - win_prob) * downside_loss)
    max_loss = allocated_capital * downside_loss

    daily_liquidation_capacity = max_adv_participation * average_daily_volume
    actual_days_to_liquidate = (
        allocated_capital / daily_liquidation_capacity if daily_liquidation_capacity > 0 else float("inf")
    )

    return PositionSizingResult(
        full_kelly_fraction=full_kelly,
        half_kelly_fraction=half_kelly,
        quarter_kelly_fraction=quarter_kelly,
        policy_nav_cap=max_nav_weight,
        liquidity_cap=liquidity_cap_weight,
        binding_weight=binding_weight,
        allocated_capital=allocated_capital,
        binding_constraint=binding_name,
        expected_dollar_gain=expected_gain,
        max_dollar_loss=max_loss,
        days_to_liquidate=actual_days_to_liquidate,
    )


def main() -> None:
    print("PC2 Lab L04-1: Fractional Kelly & Liquidity-Adjusted Position Sizing")
    print("SIMULATED institutional equity long position sizing model")

    portfolio_nav = 100_000_000.0  # $100M fund NAV
    win_probability = 0.60
    base_upside = 0.35  # +35% upside in base case
    bear_downside = 0.15  # -15% downside to stop / bear case

    policy_max_weight = 0.05  # 5.0% single position mandate cap
    adv = 12_000_000.0  # $12M Average Daily Volume
    max_adv_participation = 0.10  # 10% maximum ADV participation rate
    liquidation_days_target = 3.0  # 3 days maximum exit horizon

    print(f"Fund NAV:                             ${portfolio_nav:,.2f}")
    print(
        f"Trade Payoff Odds:                    Win {win_probability * 100:.1f}%, "
        f"+{base_upside * 100:.1f}% / -{bear_downside * 100:.1f}%"
    )
    print(f"Average Daily Volume (ADV):           ${adv:,.2f}")
    daily_cap = max_adv_participation * adv
    print(f"Max Participation Rate:               {max_adv_participation * 100:.1f}% ADV (${daily_cap:,.2f} / day)")
    print(f"Mandated Liquidation Horizon:         {liquidation_days_target:.1f} trading days")
    print("-" * 75)

    res = calculate_institutional_sizing(
        nav=portfolio_nav,
        win_prob=win_probability,
        upside_gain=base_upside,
        downside_loss=bear_downside,
        max_nav_weight=policy_max_weight,
        average_daily_volume=adv,
        max_adv_participation=max_adv_participation,
        target_liquidation_days=liquidation_days_target,
        kelly_fraction_multiplier=0.25,
    )

    policy_dollars = res.policy_nav_cap * portfolio_nav
    liq_dollars = res.liquidity_cap * portfolio_nav

    print(f"Unconstrained Full Kelly Fraction:    {res.full_kelly_fraction * 100:.2f}% NAV")
    print(f"Half Kelly Fraction (0.50x):          {res.half_kelly_fraction * 100:.2f}% NAV")
    print(f"Quarter Kelly Fraction (0.25x):       {res.quarter_kelly_fraction * 100:.2f}% NAV")
    print(f"Fund Mandate Risk Policy Cap:         {res.policy_nav_cap * 100:.2f}% NAV (${policy_dollars:,.2f})")
    print(f"Liquidity Exit Ceiling (3d @ 10% ADV):{res.liquidity_cap * 100:.2f}% NAV (${liq_dollars:,.2f})")
    print("-" * 75)
    print(f"BINDING ALLOCATION WEIGHT:            {res.binding_weight * 100:.2f}% NAV")
    print(f"Allocated Capital:                    ${res.allocated_capital:,.2f}")
    print(f"Governing Constraint:                 {res.binding_constraint}")
    print(f"Expected Trade Dollar Return:         ${res.expected_dollar_gain:,.2f}")
    print(f"Maximum Dollar Loss at Stop-Loss:     ${res.max_dollar_loss:,.2f}")
    print(f"Time to Liquidate at 10% ADV:         {res.days_to_liquidate:.2f} trading days")


main()
