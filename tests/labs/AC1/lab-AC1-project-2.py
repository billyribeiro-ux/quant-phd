from __future__ import annotations

# SIMULATED ledger: the ten transactions of Lab 1 (not a real company). Amounts are integer cents.
# Each entry is a date and a tuple of lines; each line is an (account, debit, credit) tuple.
ENTRIES = [
    ("2024-01-02", (("cash", 10_000_000, 0), ("common_stock", 0, 10_000_000))),
    ("2024-01-05", (("equipment", 4_000_000, 0), ("cash", 0, 4_000_000))),
    ("2024-01-10", (("inventory", 2_500_000, 0), ("accounts_payable", 0, 2_500_000))),
    ("2024-01-15", (("accounts_receivable", 2_400_000, 0), ("sales", 0, 2_400_000))),
    ("2024-01-20", (("cost_of_goods_sold", 1_200_000, 0), ("inventory", 0, 1_200_000))),
    ("2024-01-31", (("depreciation_expense", 100_000, 0), ("accumulated_depreciation", 0, 100_000))),
    ("2024-01-31", (("operating_expenses", 500_000, 0), ("cash", 0, 500_000))),
    ("2024-02-10", (("cash", 1_800_000, 0), ("accounts_receivable", 0, 1_800_000))),
    ("2024-02-14", (("accounts_payable", 2_500_000, 0), ("cash", 0, 2_500_000))),
    (
        "2024-02-20",
        (
            ("accounts_receivable", 1_600_000, 0),
            ("sales", 0, 1_600_000),
            ("cost_of_goods_sold", 900_000, 0),
            ("inventory", 0, 900_000),
        ),
    ),
]


def balance_through(end: str) -> dict[str, int]:
    """Debit minus credit for each account, over the entries dated on or before end (ISO dates compare)."""
    totals: dict[str, int] = {}
    for date, lines in ENTRIES:
        if date <= end:
            for account, debit, credit in lines:
                totals[account] = totals.get(account, 0) + debit - credit
    return totals


def retained(bal: dict[str, int]) -> int:
    """Retained earnings: net income to date less dividends to date (both in cents)."""
    income = -(
        bal.get("sales", 0)
        + bal.get("cost_of_goods_sold", 0)
        + bal.get("operating_expenses", 0)
        + bal.get("depreciation_expense", 0)
    )
    return income - bal.get("dividends", 0)


def main() -> None:
    jan = balance_through("2024-01-31")
    feb = balance_through("2024-02-29")

    def change(account: str) -> int:
        return feb.get(account, 0) - jan.get(account, 0)

    # Income statement for February: each flow account's change between the two month ends.
    sales = -change("sales")
    net_income = sales - change("cost_of_goods_sold") - change("operating_expenses") - change("depreciation_expense")

    # Cash flow statement for February, indirect method: each balance change sets its cash effect.
    operating = (
        net_income
        + change("depreciation_expense")
        - change("accounts_receivable")
        - change("inventory")
        - change("accounts_payable")
    )
    investing = -change("equipment")
    financing = -change("long_term_debt") - change("common_stock") - change("dividends")
    ending_cash = jan.get("cash", 0) + operating + investing + financing

    # Articulation for February: the two identities that tie the three statements together.
    cash_gap = feb.get("cash", 0) - ending_cash
    retained_change = retained(feb) - retained(jan)
    earnings_gap = retained_change - (net_income - change("dividends"))

    print("February net income", net_income, "operating", operating, "investing", investing, "financing", financing)
    print("ending cash", ending_cash, "cash gap", cash_gap)
    print("retained change", retained_change, "earnings gap", earnings_gap)


main()
