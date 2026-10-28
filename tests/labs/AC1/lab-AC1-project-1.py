from __future__ import annotations

from typing import Any

# SIMULATED ledger: ten transactions for one company in January and February 2024 (not a real company).
# Every amount is an integer number of cents. Each line carries a debit or a credit, never both.
TRANSACTIONS: list[dict[str, Any]] = [
    # 1. Owners put in cash for shares.
    {
        "date": "2024-01-02",
        "lines": [
            {"account": "cash", "debit": 10_000_000, "credit": 0},
            {"account": "common_stock", "debit": 0, "credit": 10_000_000},
        ],
    },
    # 2. Equipment bought for cash.
    {
        "date": "2024-01-05",
        "lines": [
            {"account": "equipment", "debit": 4_000_000, "credit": 0},
            {"account": "cash", "debit": 0, "credit": 4_000_000},
        ],
    },
    # 3. Inventory bought on credit from a supplier.
    {
        "date": "2024-01-10",
        "lines": [
            {"account": "inventory", "debit": 2_500_000, "credit": 0},
            {"account": "accounts_payable", "debit": 0, "credit": 2_500_000},
        ],
    },
    # 4. A sale on credit.
    {
        "date": "2024-01-15",
        "lines": [
            {"account": "accounts_receivable", "debit": 2_400_000, "credit": 0},
            {"account": "sales", "debit": 0, "credit": 2_400_000},
        ],
    },
    # 5. The cost of the goods that were sold leaves inventory.
    {
        "date": "2024-01-20",
        "lines": [
            {"account": "cost_of_goods_sold", "debit": 1_200_000, "credit": 0},
            {"account": "inventory", "debit": 0, "credit": 1_200_000},
        ],
    },
    # 6. Depreciation for January: an expense, and a larger credit balance in accumulated depreciation.
    {
        "date": "2024-01-31",
        "lines": [
            {"account": "depreciation_expense", "debit": 100_000, "credit": 0},
            {"account": "accumulated_depreciation", "debit": 0, "credit": 100_000},
        ],
    },
    # 7. Operating expenses paid in cash.
    {
        "date": "2024-01-31",
        "lines": [
            {"account": "operating_expenses", "debit": 500_000, "credit": 0},
            {"account": "cash", "debit": 0, "credit": 500_000},
        ],
    },
    # 8. A customer pays the January invoice.
    {
        "date": "2024-02-10",
        "lines": [
            {"account": "cash", "debit": 1_800_000, "credit": 0},
            {"account": "accounts_receivable", "debit": 0, "credit": 1_800_000},
        ],
    },
    # 9. The supplier is paid.
    {
        "date": "2024-02-14",
        "lines": [
            {"account": "accounts_payable", "debit": 2_500_000, "credit": 0},
            {"account": "cash", "debit": 0, "credit": 2_500_000},
        ],
    },
    # 10. A February sale on credit, with its cost, in one transaction of four lines.
    {
        "date": "2024-02-20",
        "lines": [
            {"account": "accounts_receivable", "debit": 1_600_000, "credit": 0},
            {"account": "sales", "debit": 0, "credit": 1_600_000},
            {"account": "cost_of_goods_sold", "debit": 900_000, "credit": 0},
            {"account": "inventory", "debit": 0, "credit": 900_000},
        ],
    },
]


def post(transactions: list[dict[str, Any]]) -> list[tuple[str, str, int]]:
    """Check each entry and return its postings as (date, account, debit minus credit), in cents."""
    postings: list[tuple[str, str, int]] = []
    for entry in transactions:
        total = 0
        for line in entry["lines"]:
            debit, credit = int(line["debit"]), int(line["credit"])
            if (debit > 0) == (credit > 0):
                raise ValueError("a line carries a debit or a credit, and exactly one")
            postings.append((entry["date"], line["account"], debit - credit))
            total += debit - credit
        if total != 0:
            raise ValueError("unbalanced entry: the debits do not equal the credits")
    return postings


def balances_through(postings: list[tuple[str, str, int]], end: str) -> dict[str, int]:
    """Debit minus credit for each account, over the postings dated on or before end (ISO dates compare)."""
    totals: dict[str, int] = {}
    for date, account, signed in postings:
        if date <= end:
            totals[account] = totals.get(account, 0) + signed
    return totals


def main() -> None:
    postings = post(TRANSACTIONS)
    print("postings:", len(postings), "from", len(TRANSACTIONS), "entries, each entry balances")
    try:
        post([{"date": "2024-03-01", "lines": [{"account": "cash", "debit": 100, "credit": 0}]}])
    except ValueError as error:
        print("rejected:", error)

    for end in ("2024-01-31", "2024-02-29"):
        bal = balances_through(postings, end)
        # Assets are debit balances, net of the credit balance in accumulated depreciation.
        cash = bal.get("cash", 0)
        receivables = bal.get("accounts_receivable", 0)
        inventory = bal.get("inventory", 0)
        net_equipment = bal.get("equipment", 0) + bal.get("accumulated_depreciation", 0)
        assets = cash + receivables + inventory + net_equipment
        # Liabilities and common stock are credit balances, so their amounts are negated.
        payables = -bal.get("accounts_payable", 0)
        common_stock = -bal.get("common_stock", 0)
        # Net income to date is revenue less expenses; dividends reduce retained earnings.
        income_to_date = -(
            bal.get("sales", 0)
            + bal.get("cost_of_goods_sold", 0)
            + bal.get("operating_expenses", 0)
            + bal.get("depreciation_expense", 0)
        )
        retained = income_to_date - bal.get("dividends", 0)
        gap = assets - (payables + common_stock + retained)
        print(
            f"balance sheet {end}: assets {assets} (cash {cash}, receivables {receivables}, "
            f"inventory {inventory}, net equipment {net_equipment})"
        )
        print(f"  liabilities {payables}, common stock {common_stock}, retained earnings {retained}, gap {gap}")

    # Income statement for February: the change in each flow account between the two month ends.
    jan = balances_through(postings, "2024-01-31")
    feb = balances_through(postings, "2024-02-29")
    flow = {account: feb.get(account, 0) - jan.get(account, 0) for account in feb}
    sales = -flow.get("sales", 0)
    gross = sales - flow.get("cost_of_goods_sold", 0)
    net_income = gross - flow.get("operating_expenses", 0) - flow.get("depreciation_expense", 0)
    print("income statement February: sales", sales, "gross profit", gross, "net income", net_income)

    # Cash flow statement for February, indirect method: each balance change sets its cash effect.
    def change(account: str) -> int:
        return feb.get(account, 0) - jan.get(account, 0)

    operating = (
        net_income
        + flow.get("depreciation_expense", 0)
        - change("accounts_receivable")
        - change("inventory")
        - change("accounts_payable")
    )
    investing = -change("equipment")
    financing = -change("long_term_debt") - change("common_stock") - change("dividends")
    beginning = jan.get("cash", 0)
    ending = beginning + operating + investing + financing
    print(
        "cash flow February: operating",
        operating,
        "investing",
        investing,
        "financing",
        financing,
        "ending cash",
        ending,
    )
    print("ending cash equals the February balance sheet cash:", ending == feb.get("cash", 0))


main()
