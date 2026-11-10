"""PC2 Lab L02-1: Catalyst pricing lag and return asymmetry calculator.

SIMULATED. Evaluates catalyst outcome distributions, immediate reaction vs
post-announcement drift, holding costs, and risk/reward asymmetry for a 1-page trade pitch.
Standard library only.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CatalystOutcome:
    state: str
    price: float
    probability: float
    description: str


@dataclass(frozen=True)
class CatalystMetrics:
    expected_price: float
    gross_return: float
    net_return: float
    annualized_net_return: float
    immediate_jump_return: float
    drift_return: float
    upside_ratio: float
    downside_ratio: float
    asymmetry_ratio: float
    is_pitch_viable: bool


def evaluate_catalyst_trade(
    current_price: float,
    outcomes: list[CatalystOutcome],
    days_to_catalyst: int,
    post_catalyst_holding_days: int,
    drift_share: float = 0.35,
    annual_borrow_fee: float = 0.025,
    bid_ask_drag: float = 0.004,
    min_asymmetry: float = 2.0,
    min_net_return: float = 0.10,
) -> CatalystMetrics:
    """Evaluate financial asymmetry and net return of a catalyst-driven pitch."""
    prob_sum = sum(o.probability for o in outcomes)
    if abs(prob_sum - 1.0) > 1e-6:
        msg = f"Outcome probabilities must sum to 1.0, got {prob_sum:.4f}"
        raise ValueError(msg)

    exp_price = sum(o.probability * o.price for o in outcomes)
    gross_return = (exp_price - current_price) / current_price

    total_holding_days = days_to_catalyst + post_catalyst_holding_days
    holding_cost = annual_borrow_fee * (total_holding_days / 252.0)
    net_return = gross_return - holding_cost - bid_ask_drag

    annualized_net_return = net_return * (252.0 / total_holding_days)

    immediate_jump_return = net_return * (1.0 - drift_share)
    drift_return = net_return * drift_share

    bull_state = next(o for o in outcomes if "positive" in o.state.lower() or "bull" in o.state.lower())
    bear_state = next(o for o in outcomes if "negative" in o.state.lower() or "bear" in o.state.lower())

    upside_ratio = (bull_state.price - current_price) / current_price
    downside_ratio = (current_price - bear_state.price) / current_price

    asymmetry_ratio = upside_ratio / downside_ratio if downside_ratio > 0 else float("inf")

    is_pitch_viable = asymmetry_ratio >= min_asymmetry and net_return >= min_net_return

    return CatalystMetrics(
        expected_price=exp_price,
        gross_return=gross_return,
        net_return=net_return,
        annualized_net_return=annualized_net_return,
        immediate_jump_return=immediate_jump_return,
        drift_return=drift_return,
        upside_ratio=upside_ratio,
        downside_ratio=downside_ratio,
        asymmetry_ratio=asymmetry_ratio,
        is_pitch_viable=is_pitch_viable,
    )


def main() -> None:
    print("PC2 Lab L02-1: Catalyst Pricing Lag and Asymmetry Calculator")
    print("SIMULATED earnings catalyst trade pitch model")

    current_price = 50.00
    days_to_catalyst = 30
    post_holding_days = 45

    outcomes = [
        CatalystOutcome(
            state="Positive Surprise",
            price=66.00,
            probability=0.50,
            description="Enterprise backlog conversion exceeds guidance by >15%",
        ),
        CatalystOutcome(
            state="Inline Guidance",
            price=51.00,
            probability=0.30,
            description="Revenues meet consensus, operating margin flat",
        ),
        CatalystOutcome(
            state="Negative Surprise",
            price=42.00,
            probability=0.20,
            description="Customer contract delays defer bookings into subsequent quarter",
        ),
    ]

    print(f"Current Stock Price:                  ${current_price:.2f}")
    print(f"Holding Horizon:                      {days_to_catalyst}d to catalyst + {post_holding_days}d drift")
    print("-" * 72)
    print(f"{'State':18s} | {'Target ($)':10s} | {'Prob':6s} | {'Implied Return':15s}")
    print("-" * 72)
    for o in outcomes:
        ret = (o.price - current_price) / current_price * 100
        print(f"{o.state:18s} | ${o.price:9.2f} | {o.probability:6.2f} | {ret:+14.1f}%")
    print("-" * 72)

    res = evaluate_catalyst_trade(
        current_price=current_price,
        outcomes=outcomes,
        days_to_catalyst=days_to_catalyst,
        post_catalyst_holding_days=post_holding_days,
    )

    print(f"Expected Target Price:                ${res.expected_price:.2f}")
    print(f"Gross Expected Return:                {res.gross_return * 100:.2f}%")
    print(f"Net Return (After Drag & Costs):      {res.net_return * 100:.2f}%")
    print(f"Annualized Net Return:                {res.annualized_net_return * 100:.2f}%")
    print(f"  - Day 0 Immediate Jump Component:   {res.immediate_jump_return * 100:.2f}%")
    print(f"  - Post-Announcement Drift (60d):    {res.drift_return * 100:.2f}%")
    print(f"Upside to Bull State:                 {res.upside_ratio * 100:.2f}%")
    print(f"Downside to Bear State:               {res.downside_ratio * 100:.2f}%")
    print(f"Return Asymmetry Ratio (Bull/Bear):   {res.asymmetry_ratio:.2f}x")
    print(f"Pitch Viability Threshold Passed:     {res.is_pitch_viable}")


main()
