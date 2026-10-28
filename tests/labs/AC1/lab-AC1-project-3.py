from __future__ import annotations

# SIMULATED ledger for reference numbers (not a real company). Amounts are integer cents, dates are ISO.
# Each entry is a date and a tuple of lines; the debits of each entry equal its credits.
ENTRIES = [
    ("2024-01-03", (("cash", 5_000_000, 0), ("common_stock", 0, 5_000_000))),
    ("2024-01-08", (("dividends", 300_000, 0), ("cash", 0, 300_000))),
    ("2024-02-05", (("cash", 2_000_000, 0), ("long_term_debt", 0, 2_000_000))),
    ("2024-02-06", (("inventory", 600_000, 0), ("cash", 0, 600_000))),
    ("2024-02-12", (("cash", 900_000, 0), ("sales", 0, 900_000))),
    ("2024-02-12", (("cost_of_goods_sold", 500_000, 0), ("inventory", 0, 500_000))),
    ("2024-03-04", (("equipment", 3_000_000, 0), ("cash", 0, 3_000_000))),
    ("2024-03-15", (("cash", 1_000_000, 0), ("common_stock", 0, 1_000_000))),
    ("2024-03-20", (("operating_expenses", 250_000, 0), ("accounts_payable", 0, 250_000))),
    ("2024-03-31", (("depreciation_expense", 80_000, 0), ("accumulated_depreciation", 0, 80_000))),
    ("2024-03-31", (("dividends", 150_000, 0), ("cash", 0, 150_000))),
]


def balance_through(end: str) -> dict[str, int]:
    """Debit minus credit for each account, over the entries dated on or before end (ISO dates compare)."""
    totals: dict[str, int] = {}
    for date, lines in ENTRIES:
        if date <= end:
            for account, debit, credit in lines:
                totals[account] = totals.get(account, 0) + debit - credit
    return totals


def income_to_date(bal: dict[str, int]) -> int:
    """Net income to date: revenue less cost of goods sold, operating expenses and depreciation."""
    return -(
        bal.get("sales", 0)
        + bal.get("cost_of_goods_sold", 0)
        + bal.get("operating_expenses", 0)
        + bal.get("depreciation_expense", 0)
    )


def main() -> None:
    feb = balance_through("2024-02-29")
    mar = balance_through("2024-03-31")

    def change(account: str) -> int:
        return mar.get(account, 0) - feb.get(account, 0)

    # Balance sheet at 2024-03-31: assets are debit balances, less the credit in accumulated depreciation.
    cash = mar.get("cash", 0)
    net_equipment = mar.get("equipment", 0) + mar.get("accumulated_depreciation", 0)
    inventory = mar.get("inventory", 0)
    assets = cash + inventory + net_equipment
    liabilities = -(mar.get("accounts_payable", 0) + mar.get("long_term_debt", 0))
    common_stock = -mar.get("common_stock", 0)
    retained = income_to_date(mar) - mar.get("dividends", 0)
    print("balance sheet 2024-03-31: cash", cash, "inventory", inventory, "net equipment", net_equipment)
    print(
        "balance sheet 2024-03-31: assets",
        assets,
        "liabilities",
        liabilities,
        "common stock",
        common_stock,
        "retained earnings",
        retained,
    )

    # Income statement for March: the change in each flow account from 2024-02-29 to 2024-03-31.
    net_income = -(
        change("sales") + change("cost_of_goods_sold") + change("operating_expenses") + change("depreciation_expense")
    )
    print("income statement March: net income", net_income, "depreciation", change("depreciation_expense"))

    # Cash flow statement for March, indirect method.
    operating = (
        net_income
        + change("depreciation_expense")
        - change("accounts_receivable")
        - change("inventory")
        - change("accounts_payable")
    )
    investing = -change("equipment")
    financing = -change("long_term_debt") - change("common_stock") - change("dividends")
    beginning = feb.get("cash", 0)
    ending = beginning + operating + investing + financing
    print("cash flow March: operating", operating, "investing", investing, "financing", financing)
    print("cash flow March: beginning cash", beginning, "ending cash", ending)
    print("ending cash less balance sheet cash:", ending - cash)


main()
