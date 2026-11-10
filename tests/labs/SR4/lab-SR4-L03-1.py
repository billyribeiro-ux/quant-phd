"""Lab SR4-L03-1: Basel III Capital and Supplementary Leverage Ratio Optimization.

SIMULATED. Formulates and solves the primary dealer balance-sheet constrained
optimization problem under joint risk-weighted capital (RWA) and unweighted
Supplementary Leverage Ratio (SLR) requirements (Basel Committee, 2014;
Adrian & Shin, 2010). Quantifies dealer intermediation capacity and the shadow
cost of leverage on zero-risk-weight Treasury securities.
"""

from __future__ import annotations


def solve_dealer_capacity(
    tier1_equity: float,
    slr_min: float,
    cet1_min: float,
    corp_weight: float,
    mbs_weight: float,
    treasury_weight: float,
    portfolio_mix: tuple[float, float, float],
    equity_cost_of_capital: float,
) -> dict[str, float | str | bool]:
    """Calculate dealer intermediation capacity and shadow costs under dual regulatory constraints.

    portfolio_mix: (share_corp, share_mbs, share_treasury) summing to 1.0.
    """
    share_c, share_m, share_t = portfolio_mix
    if abs(share_c + share_m + share_t - 1.0) > 1e-6:
        raise ValueError("portfolio shares must sum to 1.0")

    # 1. Capacity limit under unweighted SLR: TLE <= Tier1 / slr_min
    max_assets_slr = tier1_equity / slr_min

    # 2. Capacity limit under risk-weighted capital: RWA <= Tier1 / cet1_min
    # where RWA = Assets * (share_c * w_c + share_m * w_m + share_t * w_t)
    effective_risk_weight = share_c * corp_weight + share_m * mbs_weight + share_t * treasury_weight
    max_assets_rwa = tier1_equity / (cet1_min * effective_risk_weight) if effective_risk_weight > 0 else float("inf")

    # Binding constraint
    slr_binds = max_assets_slr <= max_assets_rwa
    binding_capacity = min(max_assets_slr, max_assets_rwa)
    binding_constraint = "SLR (Supplementary Leverage Ratio)" if slr_binds else "RWA (Risk-Weighted Capital)"

    # Shadow cost of leverage on zero-risk-weight Treasuries:
    # If SLR binds, expanding Treasury holdings by $1 requires holding $slr_min of Tier 1 equity.
    # At cost of equity r_e, the required hurdle spread is slr_min * r_e.
    # If RWA binds and Treasury risk weight is 0%, the hurdle spread is 0 bps!
    treasury_hurdle_bps = (slr_min * equity_cost_of_capital * 10000.0) if slr_binds else 0.0

    return {
        "tier1_equity": tier1_equity,
        "max_assets_slr": max_assets_slr,
        "max_assets_rwa": max_assets_rwa,
        "binding_capacity": binding_capacity,
        "binding_constraint": binding_constraint,
        "effective_risk_weight": effective_risk_weight,
        "slr_binds": slr_binds,
        "treasury_hurdle_bps": treasury_hurdle_bps,
    }


def main() -> None:
    tier1_equity = 50.0  # $50 billion Tier 1 Capital
    slr_min = 0.05  # 5.0% enhanced SLR for U.S. G-SIBs
    cet1_min = 0.10  # 10.0% CET1 / Tier 1 risk-based capital target
    cost_of_equity = 0.12  # 12.0% annual cost of equity capital

    # Asset risk weights:
    w_corp = 1.00  # 100% risk weight on corporate loans/bonds
    w_mbs = 0.20  # 20% risk weight on agency MBS
    w_ust = 0.00  # 0% risk weight on U.S. Treasuries / central bank reserves

    # Regime 1: High-risk traditional banking mix (Corp 50%, MBS 30%, Treasuries 20%)
    res_risky = solve_dealer_capacity(
        tier1_equity=tier1_equity,
        slr_min=slr_min,
        cet1_min=cet1_min,
        corp_weight=w_corp,
        mbs_weight=w_mbs,
        treasury_weight=w_ust,
        portfolio_mix=(0.50, 0.30, 0.20),
        equity_cost_of_capital=cost_of_equity,
    )

    # Regime 2: Low-risk wholesale market maker mix (Corp 10%, MBS 20%, Treasuries 70%)
    res_safe = solve_dealer_capacity(
        tier1_equity=tier1_equity,
        slr_min=slr_min,
        cet1_min=cet1_min,
        corp_weight=w_corp,
        mbs_weight=w_mbs,
        treasury_weight=w_ust,
        portfolio_mix=(0.10, 0.20, 0.70),
        equity_cost_of_capital=cost_of_equity,
    )

    print("=== DEALER BALANCE-SHEET CAPACITY AND SLR CONSTRAINTS (SIMULATED) ===")
    print(
        f"Tier 1 Capital: ${tier1_equity:.1f}B | "
        f"SLR Minimum: {slr_min * 100:.1f}% | "
        f"CET1 Minimum: {cet1_min * 100:.1f}%"
    )

    print(
        f"\nRegime 1: Traditional Credit Portfolio (Effective Risk Weight: "
        f"{res_risky['effective_risk_weight'] * 100:.1f}%):"
    )
    print(f"  SLR Capacity Ceiling: ${res_risky['max_assets_slr']:.1f}B")
    print(f"  RWA Capacity Ceiling: ${res_risky['max_assets_rwa']:.1f}B")
    print(f"  Binding Constraint: {res_risky['binding_constraint']}")
    print(f"  Treasury Intermediation Hurdle: {res_risky['treasury_hurdle_bps']:.1f} bps")

    print(
        "\nRegime 2: Treasury Market-Maker Portfolio (Effective Risk Weight: "
        f"{res_safe['effective_risk_weight'] * 100:.1f}%):"
    )
    print(f"  SLR Capacity Ceiling: ${res_safe['max_assets_slr']:.1f}B")
    print(f"  RWA Capacity Ceiling: ${res_safe['max_assets_rwa']:.1f}B")
    print(f"  Binding Constraint: {res_safe['binding_constraint']}")
    print(f"  Treasury Intermediation Hurdle: {res_safe['treasury_hurdle_bps']:.1f} bps")


main()
