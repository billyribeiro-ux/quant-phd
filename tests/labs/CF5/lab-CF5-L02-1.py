"""CF5 Lab L02-1: Synergy DCF Valuation, Overpayment Thresholds, and Winner's Curse.

Values operational and financial synergies, evaluates the net bidder equity gain,
and simulates bidding shading in a common-value M&A auction.
"""

from __future__ import annotations

import numpy as np


def value_synergies(
    annual_cost_savings: np.ndarray,
    integration_costs: np.ndarray,
    terminal_annual_savings: float,
    discount_rate: float,
    terminal_growth: float,
    tax_rate: float,
) -> dict[str, float]:
    """Discount projected after-tax synergies net of integration expenses."""
    n = len(annual_cost_savings)
    periods = np.arange(1, n + 1, dtype=np.float64)
    after_tax_savings = annual_cost_savings * (1.0 - tax_rate)
    after_tax_integration = integration_costs * (1.0 - tax_rate)
    net_synergy_cf = after_tax_savings - after_tax_integration

    pv_explicit = float(np.sum(net_synergy_cf / np.power(1.0 + discount_rate, periods)))
    terminal_net_cf = terminal_annual_savings * (1.0 - tax_rate)
    terminal_value = (terminal_net_cf * (1.0 + terminal_growth)) / (discount_rate - terminal_growth)
    pv_terminal = float(terminal_value / np.power(1.0 + discount_rate, float(n)))
    pv_total = pv_explicit + pv_terminal

    return {
        "pv_explicit": pv_explicit,
        "terminal_value": float(terminal_value),
        "pv_terminal": pv_terminal,
        "pv_total": pv_total,
    }


def simulate_auction_winner_curse(
    true_value: float,
    n_bidders: int,
    noise_sigma: float,
    n_simulations: int,
    seed: int = 42,
) -> dict[str, float]:
    """Simulate common-value auction where unshaded bidding produces the winner's curse."""
    rng = np.random.default_rng(seed)
    signals = true_value + rng.normal(0.0, noise_sigma, size=(n_simulations, n_bidders))

    # Naive bidding (bids equal signal)
    winning_naive_bids = np.max(signals, axis=1)
    naive_winner_returns = true_value - winning_naive_bids

    # Sophisticated bidding: shade bid by order statistic bias
    # E[max(X_1...X_N)] - mu ~= sigma * sqrt(2 * ln(N)) for normal distribution
    shading_factor = noise_sigma * np.sqrt(2.0 * np.log(n_bidders))
    winning_shaded_bids = winning_naive_bids - shading_factor
    shaded_winner_returns = true_value - winning_shaded_bids

    return {
        "true_value": true_value,
        "mean_naive_winning_bid": float(np.mean(winning_naive_bids)),
        "mean_naive_profit": float(np.mean(naive_winner_returns)),
        "mean_shaded_winning_bid": float(np.mean(winning_shaded_bids)),
        "mean_shaded_profit": float(np.mean(shaded_winner_returns)),
    }


def main() -> None:
    print("CF5 Lab L02-1: Synergy DCF and Common-Value Auction Economics")
    print("=============================================================")

    # 1. Synergy DCF ($M)
    savings = np.array([10.0, 25.0, 45.0, 60.0, 70.0])
    integration = np.array([20.0, 15.0, 5.0, 0.0, 0.0])
    wacc = 0.095
    g = 0.02
    tax = 0.25
    syn = value_synergies(
        annual_cost_savings=savings,
        integration_costs=integration,
        terminal_annual_savings=70.0,
        discount_rate=wacc,
        terminal_growth=g,
        tax_rate=tax,
    )
    print(f"PV Explicit Net Synergies:  ${syn['pv_explicit']:.2f}M")
    print(f"PV Terminal Synergies:      ${syn['pv_terminal']:.2f}M")
    print(f"Total PV of Synergies:      ${syn['pv_total']:.2f}M")

    # Overpayment boundary
    takeover_premium_paid = 180.0  # 36% premium
    net_acquirer_surplus = syn["pv_total"] - takeover_premium_paid
    print(f"Takeover Premium Paid:      ${takeover_premium_paid:.2f}M")
    print(f"Net Acquirer Value Created: ${net_acquirer_surplus:.2f}M")
    print(f"Deal Status:                {'Value-Accretive' if net_acquirer_surplus > 0 else 'Overpayment'}")

    # 2. Winner's Curse Auction Simulation
    auction = simulate_auction_winner_curse(
        true_value=500.0,
        n_bidders=6,
        noise_sigma=40.0,
        n_simulations=10000,
        seed=42,
    )
    print("\nM&A Common-Value Auction Simulation (N=6 bidders, sigma=$40M):")
    print(f"  Target Standalone Value:  ${auction['true_value']:.2f}M")
    print(f"  Naive Winning Bid:        ${auction['mean_naive_winning_bid']:.2f}M")
    print(f"  Naive Winner Profit:      ${auction['mean_naive_profit']:.2f}M (Winner's Curse)")
    print(f"  Shaded Winning Bid:       ${auction['mean_shaded_winning_bid']:.2f}M")
    print(f"  Shaded Winner Profit:     ${auction['mean_shaded_profit']:.2f}M")


main()
