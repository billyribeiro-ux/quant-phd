"""Lab FI4-L03-1: Central bank balance sheet mechanics and reserve identity.

Verifies the Federal Reserve H.4.1 balance sheet accounting identity and
models reserve absorption dynamics from TGA and ON RRP fluctuations.
"""

from __future__ import annotations

from typing import NamedTuple


class FedBalanceSheet(NamedTuple):
    total_assets: int  # in millions USD
    currency: int
    reverse_repo: int  # includes ON RRP
    tga: int  # Treasury General Account
    other_liabilities: int

    @property
    def reserves(self) -> int:
        """Bank reserves derived from the fundamental balance sheet accounting identity."""
        return self.total_assets - (self.currency + self.reverse_repo + self.tga + self.other_liabilities)


def main() -> None:
    # Baseline balance sheet (SIMULATED, numbers in millions USD)
    # Total Assets: $7,500,000M ($7.5T)
    base = FedBalanceSheet(
        total_assets=7_500_000,
        currency=2_320_000,
        reverse_repo=1_250_000,
        tga=680_000,
        other_liabilities=210_000,
    )

    print("Baseline Federal Reserve Balance Sheet (SIMULATED, $ Millions):")
    print(f"  Total Assets (Securities + Loans): ${base.total_assets:,.0f}M")
    print("  Liabilities & Capital:")
    print(f"    Currency in Circulation:          ${base.currency:,.0f}M")
    print(f"    Reverse Repurchase Agreements:    ${base.reverse_repo:,.0f}M")
    print(f"    Treasury General Account (TGA):   ${base.tga:,.0f}M")
    print(f"    Other Liabilities & Capital:      ${base.other_liabilities:,.0f}M")
    print(f"    Bank Reserves (Residual):         ${base.reserves:,.0f}M")
    print(
        f"  Identity Check (Assets == Liab):     "
        f"{base.total_assets == base.currency + base.reverse_repo + base.tga + base.other_liabilities + base.reserves}"
    )

    # Stress Scenario 1: Corporate Tax Date (TGA surges by $220B, drained from commercial bank reserves)
    s1 = FedBalanceSheet(
        total_assets=base.total_assets,
        currency=base.currency,
        reverse_repo=base.reverse_repo,
        tga=base.tga + 220_000,
        other_liabilities=base.other_liabilities,
    )
    print("\nScenario 1: Treasury Tax Influx (TGA surges +$220,000M):")
    print(f"  New TGA Balance:      ${s1.tga:,.0f}M")
    print(f"  New Bank Reserves:    ${s1.reserves:,.0f}M")
    print(f"  Change in Reserves:   ${s1.reserves - base.reserves:,.0f}M (direct 1:1 reserve drain)")

    # Stress Scenario 2: Rate Spread Inversion (MMFs shift $350B into ON RRP)
    s2 = FedBalanceSheet(
        total_assets=base.total_assets,
        currency=base.currency,
        reverse_repo=base.reverse_repo + 350_000,
        tga=base.tga,
        other_liabilities=base.other_liabilities,
    )
    print("\nScenario 2: Money Market Fund Flight to ON RRP (+$350,000M):")
    print(f"  New ON RRP Balance:   ${s2.reverse_repo:,.0f}M")
    print(f"  New Bank Reserves:    ${s2.reserves:,.0f}M")
    print(f"  Change in Reserves:   ${s2.reserves - base.reserves:,.0f}M (reserve absorption by non-banks)")

    # Scenario 3: Quantitative Tightening ($95B asset runoff, absorbed partially by TGA and ON RRP)
    s3 = FedBalanceSheet(
        total_assets=base.total_assets - 95_000,
        currency=base.currency,
        reverse_repo=base.reverse_repo - 60_000,
        tga=base.tga - 35_000,
        other_liabilities=base.other_liabilities,
    )
    print("\nScenario 3: Quantitative Tightening ($95,000M Asset Runoff):")
    print(f"  New Assets:           ${s3.total_assets:,.0f}M")
    print(f"  New ON RRP:           ${s3.reverse_repo:,.0f}M (-$60,000M)")
    print(f"  New TGA:              ${s3.tga:,.0f}M (-$35,000M)")
    print(f"  New Bank Reserves:    ${s3.reserves:,.0f}M")
    print(f"  Change in Reserves:   ${s3.reserves - base.reserves:,.0f}M (cushioned completely by ON RRP & TGA)")


main()
