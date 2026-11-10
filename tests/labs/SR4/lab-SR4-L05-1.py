"""Lab SR4-L05-1: Quantitative Regulatory-Impact Analysis Framework.

SIMULATED. Implements a quantitative Regulatory Impact Analysis (RIA) model
evaluating post-2020 reforms to the Supplementary Leverage Ratio (SLR) and
dealer intermediation capacity (Federal Reserve Board, 2020, 2025; Basel
Committee, 2014). Solves for social welfare trade-offs between market liquidity
benefits, sovereign borrowing cost savings, and incremental systemic risk.
"""

from __future__ import annotations


def evaluate_regulatory_regime(
    regime_name: str,
    dealer_equity: float,
    slr_threshold: float,
    treasury_exemption: bool,
    annual_treasury_volume: float,
    public_debt_issuance: float,
    default_prob_annual: float,
    systemic_bailout_cost: float,
) -> dict[str, float | str]:
    """Calculate market liquidity gains, sovereign savings, and net annual welfare."""
    if dealer_equity <= 0 or slr_threshold <= 0:
        raise ValueError("equity and threshold must be positive")

    # Dealer intermediation capacity for Treasuries ($ billions)
    # If exempt, Treasuries do not consume SLR capacity; capacity is bounded by risk capital (~$1,200B)
    if treasury_exemption:
        treasury_capacity = 1200.0
        effective_spread_bps = 0.20  # Tight bid-ask spread
        issuance_spread_bps = 1.00  # Low sovereign yield concession
    else:
        # Bounded by (Equity / SLR) - Non-Treasury assets ($800B)
        max_total = dealer_equity / slr_threshold
        treasury_capacity = max(100.0, max_total - 800.0)
        # Tighter capacity implies higher intermediation spread
        capacity_factor = 400.0 / treasury_capacity
        effective_spread_bps = 0.20 * capacity_factor
        issuance_spread_bps = 1.00 * capacity_factor

    # 1. Market Liquidity Annual Savings ($ billions):
    # Reduction in transaction costs = Volume * (Spread_baseline - Spread_regime)
    # Baseline spread: 0.80 bps
    spread_reduction_bps = max(0.0, 0.80 - effective_spread_bps)
    liquidity_benefit = annual_treasury_volume * (spread_reduction_bps / 10000.0)

    # 2. Sovereign Debt Service Annual Savings ($ billions):
    # Concession reduction on annual new issuance
    # Baseline issuance concession: 4.0 bps
    issuance_savings_bps = max(0.0, 4.00 - issuance_spread_bps)
    sovereign_benefit = public_debt_issuance * (issuance_savings_bps / 10000.0)

    # 3. Expected Annual Systemic Risk Cost ($ billions):
    # Expected annual loss = default_probability * systemic_bailout_cost
    expected_risk_cost = default_prob_annual * systemic_bailout_cost

    # Net Social Benefit ($ billions / year)
    net_welfare = liquidity_benefit + sovereign_benefit - expected_risk_cost

    return {
        "regime_name": regime_name,
        "treasury_capacity": treasury_capacity,
        "bid_ask_spread_bps": effective_spread_bps,
        "liquidity_benefit": liquidity_benefit,
        "sovereign_benefit": sovereign_benefit,
        "expected_risk_cost": expected_risk_cost,
        "net_welfare": net_welfare,
    }


def main() -> None:
    equity = 60.0  # $60B Tier 1 capital
    annual_volume = 150000.0  # $150,000B ($150T) annual secondary Treasury trading volume
    debt_issuance = 4000.0  # $4,000B ($4T) annual gross Treasury issuance
    bailout_cost = 500.0  # $500B social cost of G-SIB systemic distress

    # Regime 1: Baseline Status Quo (Strict 5.0% SLR, No Exemption)
    # Default prob: 0.10% (10 bps/year)
    reg_baseline = evaluate_regulatory_regime(
        regime_name="1. Status Quo (5.0% SLR, No Exemption)",
        dealer_equity=equity,
        slr_threshold=0.05,
        treasury_exemption=False,
        annual_treasury_volume=annual_volume,
        public_debt_issuance=debt_issuance,
        default_prob_annual=0.0010,
        systemic_bailout_cost=bailout_cost,
    )

    # Regime 2: Full Treasury Exemption (Permanent Relief)
    # Higher leverage on safe assets slightly raises default prob to 0.16%
    reg_exempt = evaluate_regulatory_regime(
        regime_name="2. Full Exemption (Reserves & Treasuries Excluded)",
        dealer_equity=equity,
        slr_threshold=0.05,
        treasury_exemption=True,
        annual_treasury_volume=annual_volume,
        public_debt_issuance=debt_issuance,
        default_prob_annual=0.0016,
        systemic_bailout_cost=bailout_cost,
    )

    # Regime 3: Calibrated Buffer Reform (3.5% Base SLR + 1.0% G-SIB Surcharge, Partial Relief)
    # Default prob: 0.12%
    reg_calibrated = evaluate_regulatory_regime(
        regime_name="3. Calibrated Reform (4.0% Recalibrated SLR)",
        dealer_equity=equity,
        slr_threshold=0.04,
        treasury_exemption=False,
        annual_treasury_volume=annual_volume,
        public_debt_issuance=debt_issuance,
        default_prob_annual=0.0012,
        systemic_bailout_cost=bailout_cost,
    )

    print("=== REGULATORY IMPACT ANALYSIS (RIA) COMPARATIVE WELFARE (SIMULATED) ===")
    for reg in (reg_baseline, reg_exempt, reg_calibrated):
        print(f"\n{reg['regime_name']}:")
        print(f"  Treasury Intermediation Capacity: ${float(reg['treasury_capacity']):.1f}B")
        print(f"  Effective Secondary Bid-Ask Spread: {float(reg['bid_ask_spread_bps']):.2f} bps")
        print(f"  Annual Secondary Liquidity Benefit: ${float(reg['liquidity_benefit']):.2f}B")
        print(f"  Annual Sovereign Borrowing Savings: ${float(reg['sovereign_benefit']):.2f}B")
        print(f"  Annual Expected Systemic Risk Cost: ${float(reg['expected_risk_cost']):.2f}B")
        print(f"  Net Annual Social Welfare: ${float(reg['net_welfare']):.2f}B")


main()
