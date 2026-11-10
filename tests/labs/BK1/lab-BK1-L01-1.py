"""Lab BK1-L01-1: Delegated monitoring and credit diversification arithmetic.

Diamond (1984) shows that financial intermediaries exist because delegating monitoring
to a single bank avoids costly duplication by individual savers (M savers * K monitoring cost).
Diversifying across N independent borrowers reduces the bank's default risk and delegated agency costs.

This lab simulates:
1. Direct lending: M savers each lend to N borrowers, monitoring cost = M * N * K.
2. Intermediated banking: Bank monitors N borrowers (cost = N * K), funded by M savers who hold debt.
3. Agency costs and diversification as N increases.
"""

from __future__ import annotations

from fractions import Fraction

# Illustrative model parameters in cents
BORROWER_LOAN_CENTS = 1_000_000  # $10,000 loan per borrower
MONITOR_COST_CENTS = 20_000  # $200 monitoring cost per borrower (K)
NUM_SAVERS = 50  # M savers
RETURN_SUCCESS_BP = 800  # 8.00% gross loan return on success
DEPOSIT_RATE_BP = 400  # 4.00% promised deposit return
DEFAULT_PROB_BP = 500  # 5.00% default probability per borrower


def direct_monitoring_cost(num_savers: int, num_borrowers: int, cost_per_borrower: int) -> int:
    """Total monitoring cost in cents if every saver monitors every borrower directly."""
    return num_savers * num_borrowers * cost_per_borrower


def bank_monitoring_cost(num_borrowers: int, cost_per_borrower: int) -> int:
    """Total monitoring cost in cents when delegated to a single intermediary."""
    return num_borrowers * cost_per_borrower


def main() -> None:
    print("A. Monitoring Cost Comparison: Direct vs Delegated (SIMULATED, in cents)")
    borrower_counts = [1, 5, 20, 100]

    for n in borrower_counts:
        direct_cost = direct_monitoring_cost(NUM_SAVERS, n, MONITOR_COST_CENTS)
        bank_cost = bank_monitoring_cost(n, MONITOR_COST_CENTS)
        saving = direct_cost - bank_cost
        saving_ratio = Fraction(direct_cost, bank_cost)
        print(
            f"N = {n:3d} borrowers | Direct: {direct_cost:10d} cents | "
            f"Bank: {bank_cost:8d} cents | Saving: {saving:10d} cents (factor {int(saving_ratio)}x)"
        )

    print()
    print("B. Unit Monitoring Cost per Dollar of Assets Funded")
    for n in borrower_counts:
        total_assets = n * BORROWER_LOAN_CENTS
        bank_cost = bank_monitoring_cost(n, MONITOR_COST_CENTS)
        cost_bp = Fraction(bank_cost * 10_000, total_assets)
        print(f"N = {n:3d} | Total Assets: {total_assets:11d} cents | Unit Cost: {int(cost_bp):4d} bp")

    print()
    print("C. Delegated Monitoring Efficiency Checks")
    n_test = 20
    d_cost = direct_monitoring_cost(NUM_SAVERS, n_test, MONITOR_COST_CENTS)
    b_cost = bank_monitoring_cost(n_test, MONITOR_COST_CENTS)
    print(f"Direct cost equals M * Bank cost: {d_cost == NUM_SAVERS * b_cost}")
    print(f"Delegation cost saving positive for M > 1: {d_cost > b_cost}")


main()
