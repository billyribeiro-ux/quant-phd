"""CF5 Lab L01-1: Merger Announcement Returns and the Grossman-Hart Free-Rider Condition.

Calculates cumulative abnormal returns (CAR) for target and acquirer across announcement
windows, and evaluates the Grossman-Hart tender offer success condition.
"""

from __future__ import annotations

import numpy as np


def compute_car(returns: np.ndarray, market_returns: np.ndarray, alpha: float, beta: float) -> float:
    """Calculate cumulative abnormal return using market model benchmark."""
    expected_returns = alpha + beta * market_returns
    abnormal_returns = returns - expected_returns
    return float(np.sum(abnormal_returns))


def evaluate_grossman_hart(
    pre_bid_price: float,
    post_raid_value: float,
    tender_price: float,
    dilution_benefit: float,
    toehold: float,
) -> dict[str, bool | float]:
    """Evaluate Grossman-Hart (1980) free-rider condition for an atomistic shareholder.

    An atomistic shareholder tenders if and only if:
      tender_price >= post_raid_value - dilution_benefit.
    The raid is profitable for the raider if:
      toehold * (post_raid_value - pre_bid_price) + (1 - toehold) * dilution_benefit >= raid_costs.
    """
    threshold_price = post_raid_value - dilution_benefit
    shareholder_tenders = tender_price >= threshold_price
    raider_gain_per_share = (post_raid_value - pre_bid_price) * toehold + (post_raid_value - tender_price) * (
        1.0 - toehold
    )
    return {
        "threshold_price": float(threshold_price),
        "shareholder_tenders": bool(shareholder_tenders),
        "raider_gain_per_share": float(raider_gain_per_share),
    }


def main() -> None:
    print("CF5 Lab L01-1: M&A Announcement Returns and Tender Offer Economics")
    print("==================================================================")

    # 1. Announcement CAR Simulation (Andrade, Mitchell & Stafford 2001 parameters)
    # 3-day event window [-1, +1]
    np.random.seed(42)
    mkt = np.array([0.002, -0.001, 0.003])
    # Target: beta = 1.1, alpha = 0.0001, major positive announcement shock
    target_returns = np.array([0.015, 0.142, 0.008])
    target_car = compute_car(target_returns, mkt, alpha=0.0001, beta=1.1)

    # Acquirer: beta = 0.95, alpha = 0.0002, slight negative announcement reaction
    acquirer_returns = np.array([-0.002, -0.008, 0.001])
    acquirer_car = compute_car(acquirer_returns, mkt, alpha=0.0002, beta=0.95)

    # Value-weighted combined synergy return (Target MV = $2B, Acquirer MV = $8B)
    target_mv = 2000.0
    acquirer_mv = 8000.0
    combined_dollar_gain = target_mv * target_car + acquirer_mv * acquirer_car
    combined_pct_return = combined_dollar_gain / (target_mv + acquirer_mv)

    print(f"Target 3-Day Announcement CAR:    +{target_car:.2%}")
    print(f"Acquirer 3-Day Announcement CAR:  {acquirer_car:.2%}")
    print(f"Combined Wealth Creation ($M):    ${combined_dollar_gain:.1f}M")
    print(f"Combined Synergy Return:          +{combined_pct_return:.2%}")

    # 2. Grossman-Hart (1980) Free-Rider Analysis
    # Pre-bid price q = $50, post-raid value v = $80
    q = 50.0
    v = 80.0
    # Case A: No dilution (phi = 0), no toehold (alpha = 0), bid p = $65
    case_a = evaluate_grossman_hart(
        pre_bid_price=q,
        post_raid_value=v,
        tender_price=65.0,
        dilution_benefit=0.0,
        toehold=0.0,
    )
    print("\nGrossman-Hart Case A (No dilution, bid $65 < post-raid $80):")
    print(f"  Threshold to tender: ${case_a['threshold_price']:.2f}")
    print(f"  Shareholder tenders: {case_a['shareholder_tenders']}")

    # Case B: Allowable dilution phi = $18, bid p = $65
    case_b = evaluate_grossman_hart(
        pre_bid_price=q,
        post_raid_value=v,
        tender_price=65.0,
        dilution_benefit=18.0,
        toehold=0.15,
    )
    print("\nGrossman-Hart Case B (Dilution phi=$18, toehold=15%, bid $65):")
    print(f"  Threshold to tender: ${case_b['threshold_price']:.2f}")
    print(f"  Shareholder tenders: {case_b['shareholder_tenders']}")
    print(f"  Raider Gain/Share:   ${case_b['raider_gain_per_share']:.2f}")


main()
