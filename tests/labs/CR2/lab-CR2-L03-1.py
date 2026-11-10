"""Lab CR2-L03-1: CDS-bond basis measurement and negative basis trade arbitrage economics.

Demonstrates basis calculation, repo funding mechanics, haircut leverage drag,
and returns on equity across financial crisis friction regimes.
"""

from __future__ import annotations


def main() -> None:
    # 5-Year benchmark and instrument parameters
    risk_free_rate = 0.0300  # 3.00% benchmark yield
    cds_spread_bps = 95.0  # 95 bp par CDS spread
    bond_cash_spread_bps = 135.0  # 135 bp par bond Z-spread / ASW

    # Repo and funding market observables
    repo_spread_bps = 15.0  # Repo rate = r + 15 bp
    haircuts = [0.02, 0.05, 0.10, 0.15, 0.25]  # Haircuts from normal to crisis

    # 1. Basis definition
    basis_bps = cds_spread_bps - bond_cash_spread_bps
    gross_carry_bps = -basis_bps  # Cash spread - CDS spread

    print("CDS-Bond Basis Economics (5Y Tenor, Notional = 10000000):")
    print(f"  Par CDS Spread:       {cds_spread_bps:6.1f} bp")
    print(f"  Bond Cash Spread:     {bond_cash_spread_bps:6.1f} bp")
    print(f"  CDS-Bond Basis:       {basis_bps:6.1f} bp (Negative Basis Regime)")
    print(f"  Gross Carry:          {gross_carry_bps:6.1f} bp")

    print("\nLeveraged Negative Basis Trade Structure:")
    print("  1. Long 10M Face Value 5Y Corporate Bond (earns r + 135 bp).")
    print("  2. Long 10M 5Y CDS Protection (pays 95 bp).")
    print("  3. Finance (1 - Haircut) in term repo market at repo rate (r + 15 bp).")
    print("  4. Fund Haircut with firm equity capital.")

    print("\nHaircut Sensitivity & Return on Regulatory Capital (ROE):")
    print("  Haircut (%) | Equity Capital |   Repo Debt    |   Net Carry    | Return on Equity (%)")
    print("--------------+----------------+----------------+----------------+----------------------")

    for h in haircuts:
        equity_cap = 10_000_000.0 * h
        repo_debt = 10_000_000.0 * (1.0 - h)

        # Revenue: Bond coupon (r + 135 bp)
        bond_income = 10_000_000.0 * (risk_free_rate + bond_cash_spread_bps / 10000.0)
        # Cost 1: CDS protection
        cds_cost = 10_000_000.0 * (cds_spread_bps / 10000.0)
        # Cost 2: Repo interest
        repo_rate = risk_free_rate + repo_spread_bps / 10000.0
        repo_cost = repo_debt * repo_rate

        net_income = bond_income - cds_cost - repo_cost
        roe = (net_income / equity_cap) * 100.0

        print(
            f"    {h * 100:4.1f}%    |   {equity_cap:10.0f}   |   {repo_debt:10.0f}   |   "
            f"{net_income:10.0f}   |        {roe:5.2f}%"
        )

    # Invariants
    assert basis_bps < 0.0
    assert gross_carry_bps > 0.0


main()
