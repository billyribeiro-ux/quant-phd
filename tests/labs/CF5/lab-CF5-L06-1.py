"""CF5 Lab L06-1: Chapter 11 Priority Cascade and Creditor Recovery Rates.

Simulates judicial reorganization waterfall under the Absolute Priority Rule,
computing recovery rates across DIP, senior secured, unsecured, and equity claims.
"""

from __future__ import annotations


def execute_chapter_11_waterfall(
    distributable_enterprise_value: float,
    dip_financing: float,
    admin_claims: float,
    senior_secured_claims: float,
    collateral_value: float,
    senior_unsecured_claims: float,
    subordinated_notes: float,
    equity_shares: float,
) -> dict[str, float]:
    """Execute strict absolute priority waterfall in corporate reorganization."""
    remaining_value = distributable_enterprise_value

    # 1. Superpriority DIP & Administrative claims
    dip_recovery = min(remaining_value, dip_financing)
    remaining_value -= dip_recovery
    admin_recovery = min(remaining_value, admin_claims)
    remaining_value -= admin_recovery

    # 2. Senior Secured Claims (secured up to collateral value, balance is deficiency unsecured)
    secured_collateral_portion = min(senior_secured_claims, collateral_value)
    secured_deficiency_portion = max(0.0, senior_secured_claims - secured_collateral_portion)

    secured_recovery = min(remaining_value, secured_collateral_portion)
    remaining_value -= secured_recovery

    # 3. General Unsecured Claims Pool (senior unsecured + secured deficiency)
    total_unsecured_pool = senior_unsecured_claims + secured_deficiency_portion
    unsecured_distributable = min(remaining_value, total_unsecured_pool)
    remaining_value -= unsecured_distributable

    unsecured_recovery_rate = unsecured_distributable / total_unsecured_pool if total_unsecured_pool > 0 else 0.0
    senior_unsecured_claims * unsecured_recovery_rate
    deficiency_recovery = secured_deficiency_portion * unsecured_recovery_rate
    total_senior_lender_recovery = secured_recovery + deficiency_recovery

    # 4. Subordinated Notes
    sub_recovery = min(remaining_value, subordinated_notes)
    remaining_value -= sub_recovery

    # 5. Common Equity
    equity_recovery = max(0.0, remaining_value)

    return {
        "dip_recovery_pct": float(dip_recovery / dip_financing) if dip_financing else 1.0,
        "admin_recovery_pct": float(admin_recovery / admin_claims) if admin_claims else 1.0,
        "senior_secured_recovery_pct": float(total_senior_lender_recovery / senior_secured_claims),
        "senior_unsecured_recovery_pct": float(unsecured_recovery_rate),
        "subordinated_recovery_pct": float(sub_recovery / subordinated_notes) if subordinated_notes else 0.0,
        "equity_recovery": float(equity_recovery),
    }


def main() -> None:
    print("CF5 Lab L06-1: Chapter 11 Absolute Priority Reorganization Waterfall")
    print("===================================================================")

    # Claim structure ($M)
    dip = 50.0  # $50M DIP financing
    admin = 20.0  # $20M professional / administrative fees
    sr_secured = 300.0  # $300M senior secured credit facility
    collateral = 220.0  # $220M collateral liquidation value (shortfall of $80M)
    sr_unsecured = 200.0  # $200M senior unsecured bonds
    sub_notes = 100.0  # $100M subordinated notes
    shares = 10.0  # 10M shares

    # Scenario A: Moderate Reorganization Value ($420M EV)
    scen_a = execute_chapter_11_waterfall(
        distributable_enterprise_value=420.0,
        dip_financing=dip,
        admin_claims=admin,
        senior_secured_claims=sr_secured,
        collateral_value=collateral,
        senior_unsecured_claims=sr_unsecured,
        subordinated_notes=sub_notes,
        equity_shares=shares,
    )
    print("Scenario A: Reorganization Value = $420M")
    print(f"  DIP Financing Recovery:       {scen_a['dip_recovery_pct']:.1%}")
    print(f"  Administrative Claims:        {scen_a['admin_recovery_pct']:.1%}")
    print(f"  Senior Secured Debt ($300M):  {scen_a['senior_secured_recovery_pct']:.1%}")
    print(f"  Senior Unsecured Debt ($200M):{scen_a['senior_unsecured_recovery_pct']:.1%}")
    print(f"  Subordinated Notes ($100M):   {scen_a['subordinated_recovery_pct']:.1%}")
    print(f"  Common Equity Distribution:   ${scen_a['equity_recovery']:.2f}M")

    # Scenario B: Severe Distress Liquidation Value ($250M EV)
    scen_b = execute_chapter_11_waterfall(
        distributable_enterprise_value=250.0,
        dip_financing=dip,
        admin_claims=admin,
        senior_secured_claims=sr_secured,
        collateral_value=collateral,
        senior_unsecured_claims=sr_unsecured,
        subordinated_notes=sub_notes,
        equity_shares=shares,
    )
    print("\nScenario B: Severe Distress Liquidation Value = $250M")
    print(f"  DIP Financing Recovery:       {scen_b['dip_recovery_pct']:.1%}")
    print(f"  Administrative Claims:        {scen_b['admin_recovery_pct']:.1%}")
    print(f"  Senior Secured Debt ($300M):  {scen_b['senior_secured_recovery_pct']:.1%}")
    print(f"  Senior Unsecured Debt ($200M):{scen_b['senior_unsecured_recovery_pct']:.1%}")
    print(f"  Subordinated Notes ($100M):   {scen_b['subordinated_recovery_pct']:.1%}")
    print(f"  Common Equity Distribution:   ${scen_b['equity_recovery']:.2f}M")


main()
