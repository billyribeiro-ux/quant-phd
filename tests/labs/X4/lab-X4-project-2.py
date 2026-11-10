"""Lab X4-project-2: Rung 2 completion problem for liquidation haircut and NAV calculation.

SIMULATED sample redemption run on a stylized 2-tier reserve portfolio.
On the project page, the market value consumed, haircut loss, and remaining token NAV
are blanked:
mv_used = ___
loss = ___
nav = ___
The twin contains the complete solution.
"""

from __future__ import annotations


def compute_liquidation_step(
    redemption_amount: float,
    tier_market_value: float,
    haircut: float,
) -> tuple[float, float, float]:
    """Calculate asset market value consumed, haircut loss, and cash raised."""
    avail_cash = tier_market_value * (1.0 - haircut)
    if redemption_amount <= avail_cash:
        cash_raised = redemption_amount
        mv_used = cash_raised / (1.0 - haircut)
        loss = mv_used - cash_raised
    else:
        cash_raised = avail_cash
        mv_used = tier_market_value
        loss = tier_market_value * haircut
    return mv_used, loss, cash_raised


def compute_post_run_nav(
    remaining_asset_value: float,
    remaining_tokens: float,
) -> float:
    """Calculate Net Asset Value per remaining unredeemed token."""
    if remaining_tokens <= 1e-9:
        return 1.0
    return remaining_asset_value / remaining_tokens


def main() -> None:
    print("Lab X4-project-2 | Liquidation Step and NAV Calculation (Rung 2)")
    print("----------------------------------------------------------------")

    liabilities = 10000.0
    redemptions = 3000.0

    # Stylized 2-tier portfolio: Tier 1 cash buffer ($1000M), Tier 2 repo ($9000M with 1% haircut)
    cash_mv = 1000.0
    repo_mv = 9000.0
    repo_haircut = 0.010

    # Step 1: Liquidate cash (haircut = 0)
    cash_used, cash_loss, cash_raised = compute_liquidation_step(redemptions, cash_mv, 0.0)
    rem_redemptions = redemptions - cash_raised

    # Step 2: Liquidate repo for remaining redemptions
    repo_used, repo_loss, repo_raised = compute_liquidation_step(rem_redemptions, repo_mv, repo_haircut)

    total_loss = cash_loss + repo_loss
    total_cash = cash_raised + repo_raised
    rem_tokens = liabilities - total_cash
    rem_assets = (cash_mv - cash_used) + (repo_mv - repo_used)

    nav = compute_post_run_nav(rem_assets, rem_tokens)

    print(f"Redemptions Requested:       ${redemptions:.1f}M")
    print(f"Cash Buffer Used:            ${cash_used:.1f}M (Loss: ${cash_loss:.2f}M)")
    print(f"Repo Market Value Used:      ${repo_used:.2f}M (Loss: ${repo_loss:.2f}M)")
    print(f"Total Haircut Liquidation:   ${total_loss:.2f}M")
    print(f"Remaining Unredeemed Tokens: ${rem_tokens:.1f}M")
    print(f"Remaining Reserve Assets:    ${rem_assets:.2f}M")
    print(f"Post-Run Secondary NAV:      ${nav:.6f}")

    assert abs(total_cash - redemptions) < 1e-6
    assert nav < 1.0000


main()
