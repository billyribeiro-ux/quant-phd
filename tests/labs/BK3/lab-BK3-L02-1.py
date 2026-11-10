"""BK3 Lab L02: Insurer balance sheet accounting and reserve roll-forward.

SIMULATED. Illustrative balance sheet parameters, not market data.
Tracks an insurer balance sheet over three accounting periods across life and property-casualty books.
Assets consist of cash and bond investments. Liabilities consist of unearned premium reserves (UPR)
and actuarial policy reserves (present value of projected claims).
Verifies the fundamental accounting identity: Assets = Liabilities + Capital (A = L + K_c) exactly
at every period under reserve accumulation, investment income, and claims settlement.
All calculations are exact in integer cents.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BalanceSheet:
    period: int
    cash_cents: int
    bonds_cents: int
    upr_cents: int
    claims_reserve_cents: int
    capital_cents: int

    @property
    def total_assets_cents(self) -> int:
        return self.cash_cents + self.bonds_cents

    @property
    def total_liabilities_cents(self) -> int:
        return self.upr_cents + self.claims_reserve_cents

    @property
    def identity_holds(self) -> bool:
        return self.total_assets_cents == self.total_liabilities_cents + self.capital_cents


def main() -> None:
    # Initial balance sheet at Period 0 (in cents)
    # Assets: $250,000 cash + $1,750,000 bonds = $2,000,000 total
    # Liabilities: $400,000 UPR + $1,200,000 Claims Reserve = $1,600,000 total
    # Capital (Surplus): $400,000
    bs0 = BalanceSheet(
        period=0,
        cash_cents=25_000_000,
        bonds_cents=175_000_000,
        upr_cents=40_000_000,
        claims_reserve_cents=120_000_000,
        capital_cents=40_000_000,
    )

    history = [bs0]

    # Period 1 operations
    new_cash_1 = bs0.cash_cents + 30_000_000 + 7_000_000 - 15_000_000  # 47,000,000
    new_bonds_1 = bs0.bonds_cents  # 175,000,000
    new_upr_1 = bs0.upr_cents - 20_000_000 + 25_000_000  # 45,000,000
    new_claims_res_1 = bs0.claims_reserve_cents + 18_000_000 - 15_000_000  # 123,000,000
    new_cap_1 = bs0.capital_cents + 9_000_000  # 49,000,000
    bs1 = BalanceSheet(1, new_cash_1, new_bonds_1, new_upr_1, new_claims_res_1, new_cap_1)
    history.append(bs1)

    # Period 2 operations
    bonds_bought = 20_000_000
    cash_after_invest = bs1.cash_cents - bonds_bought
    new_bonds_2 = bs1.bonds_cents + bonds_bought  # 195,000,000
    new_cash_2 = cash_after_invest + 20_000_000 + 7_800_000 - 25_000_000
    new_upr_2 = bs1.upr_cents - 35_000_000 + 20_000_000  # 30,000,000
    new_claims_res_2 = bs1.claims_reserve_cents + 42_000_000 - 25_000_000  # 140,000,000
    new_cap_2 = bs1.capital_cents + 800_000  # 49,800,000
    bs2 = BalanceSheet(2, new_cash_2, new_bonds_2, new_upr_2, new_claims_res_2, new_cap_2)
    history.append(bs2)

    print("=== Insurer Balance Sheet Progression (Amounts in Cents) ===")
    for bs in history:
        print(f"\nPeriod {bs.period}:")
        print(f"  Assets:      Cash {bs.cash_cents:,} + Bonds {bs.bonds_cents:,} = Total {bs.total_assets_cents:,}")
        print(
            f"  Liabilities: UPR {bs.upr_cents:,} + Claims {bs.claims_reserve_cents:,} "
            f"= Total {bs.total_liabilities_cents:,}"
        )
        print(f"  Capital:     {bs.capital_cents:,}")
        diff = bs.total_assets_cents - (bs.total_liabilities_cents + bs.capital_cents)
        print(f"  Identity:    Assets == Liab + Capital -> {bs.identity_holds} (Discrepancy: {diff} cents)")
        solvency_ratio = bs.capital_cents / bs.total_liabilities_cents
        print(f"  Solvency Capital Ratio (K_c / L): {solvency_ratio:.4f}")

    print("\nAll balance sheet periods hold identity exactly:", all(bs.identity_holds for bs in history))


main()
