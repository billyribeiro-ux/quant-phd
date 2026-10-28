"""AC1 lab L02: sort a posted ledger into the income statement, the balance sheet and the cash-flow statement.

SIMULATED: the quarterly credit sales, cash sales, operating expense and cost percentage (55 to 65 per cent) are drawn
from a seeded random number generator for this lab. Cost of sales is that percentage of the quarter's sales. The
opening position, equipment, borrowing, dividends and depreciation are fixed amounts in the code. Collections are
four fifths of the receivable and payments are nine tenths of the payable, both fixed fractions of balances. It is
not a real company.
Amounts are integer cents and are printed in USD. The three statements are produced from one ledger, one at a
time; this lab does not yet check that they agree with one another. Standard library only; no network.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

SEED = 20261027
OPENING_YEAR = 2024
YEARS: tuple[int, ...] = (2025, 2026, 2027)

# Account -> type. A debit-normal account grows with debits; a credit-normal account grows with credits.
TYPES: dict[str, str] = {
    "cash": "asset",
    "accounts_receivable": "asset",
    "equipment": "asset",
    "accumulated_depreciation": "contra-asset",
    "accounts_payable": "liability",
    "long_term_debt": "liability",
    "common_stock": "equity",
    "dividends": "equity",
    "sales": "revenue",
    "cost_of_sales": "expense",
    "operating_expense": "expense",
    "depreciation_expense": "expense",
}
DEBIT_NORMAL = frozenset(
    {
        "cash",
        "accounts_receivable",
        "equipment",
        "dividends",
        "cost_of_sales",
        "operating_expense",
        "depreciation_expense",
    }
)
ACTIVITIES = ("operating", "investing", "financing", "noncash")


@dataclass(frozen=True)
class Line:
    """One side of one account, in integer cents. At most one of debit and credit is non-zero."""

    account: str
    debit: int = 0
    credit: int = 0


@dataclass(frozen=True)
class Entry:
    """A journal entry dated by fiscal year and quarter. activity classifies its cash effect."""

    year: int
    quarter: int
    memo: str
    activity: str
    lines: tuple[Line, ...]


def check_entry(entry: Entry) -> None:
    """Raise ValueError unless the entry is valid: known accounts, integer amounts, balanced, classified."""
    if entry.activity not in ACTIVITIES:
        raise ValueError(f"{entry.memo!r}: activity must be one of {ACTIVITIES}, not {entry.activity!r}")
    if not 1 <= entry.quarter <= 4:
        raise ValueError(f"{entry.memo!r}: quarter must be 1 to 4, not {entry.quarter}")
    debits = 0
    credits = 0
    for line in entry.lines:
        if line.account not in TYPES:
            raise ValueError(f"{entry.memo!r}: unknown account {line.account!r}")
        for amount in (line.debit, line.credit):
            if isinstance(amount, bool) or not isinstance(amount, int) or amount < 0:
                raise ValueError(f"{entry.memo!r}: amounts must be non-negative integer cents, got {amount!r}")
        if line.debit and line.credit:
            raise ValueError(f"{entry.memo!r}: one line carries both a debit and a credit on {line.account!r}")
        debits += line.debit
        credits += line.credit
    if debits != credits:
        raise ValueError(f"{entry.memo!r}: debits {debits} do not equal credits {credits}")


class Ledger:
    """Holds only entries that pass check_entry."""

    def __init__(self) -> None:
        self.entries: list[Entry] = []

    def post(self, entry: Entry) -> None:
        check_entry(entry)
        self.entries.append(entry)

    def net(self, account: str, year: int | None = None, through: int | None = None) -> int:
        """Debits minus credits. year selects one fiscal year; through selects every year up to that one."""
        total = 0
        for entry in self.entries:
            if year is not None and entry.year != year:
                continue
            if through is not None and entry.year > through:
                continue
            for line in entry.lines:
                if line.account == account:
                    total += line.debit - line.credit
        return total

    def balance(self, account: str, through: int) -> int:
        """The balance on the account's normal side at the end of the given year, in integer cents."""
        net = self.net(account, through=through)
        return net if account in DEBIT_NORMAL else -net


def money(cents: int) -> str:
    """Format integer cents as dollars and cents: 1234567 becomes 12,345.67 and -50 becomes -0.50."""
    sign = "-" if cents < 0 else ""
    dollars, rest = divmod(abs(cents), 100)
    return f"{sign}{dollars:,}.{rest:02d}"


def generate(ledger: Ledger, rng: random.Random) -> None:
    """Post the opening position and four quarters of each year, drawing every amount from rng."""
    ledger.post(
        Entry(
            OPENING_YEAR,
            4,
            "owner invests cash",
            "financing",
            (Line("cash", debit=800_000_000), Line("common_stock", credit=800_000_000)),
        )
    )
    ledger.post(
        Entry(
            OPENING_YEAR,
            4,
            "equipment A bought for cash",
            "investing",
            (Line("equipment", debit=500_000_000), Line("cash", credit=500_000_000)),
        )
    )
    for year in YEARS:
        for quarter in (1, 2, 3, 4):
            credit_sales = rng.randrange(180_000_000, 240_000_000)
            cash_sales = rng.randrange(20_000_000, 40_000_000)
            cost_percent = rng.randrange(55, 66)
            operating = rng.randrange(40_000_000, 50_000_000)
            if year == 2026 and quarter == 1:
                ledger.post(
                    Entry(
                        year,
                        quarter,
                        "equipment B bought for cash",
                        "investing",
                        (Line("equipment", debit=150_000_000), Line("cash", credit=150_000_000)),
                    )
                )
                ledger.post(
                    Entry(
                        year,
                        quarter,
                        "borrowing",
                        "financing",
                        (Line("cash", debit=100_000_000), Line("long_term_debt", credit=100_000_000)),
                    )
                )
            ledger.post(
                Entry(
                    year,
                    quarter,
                    "credit sale",
                    "noncash",
                    (Line("accounts_receivable", debit=credit_sales), Line("sales", credit=credit_sales)),
                )
            )
            ledger.post(
                Entry(
                    year,
                    quarter,
                    "cash sale",
                    "operating",
                    (Line("cash", debit=cash_sales), Line("sales", credit=cash_sales)),
                )
            )
            purchases = (credit_sales + cash_sales) * cost_percent // 100
            ledger.post(
                Entry(
                    year,
                    quarter,
                    "cost of sales on account",
                    "noncash",
                    (Line("cost_of_sales", debit=purchases), Line("accounts_payable", credit=purchases)),
                )
            )
            ledger.post(
                Entry(
                    year,
                    quarter,
                    "operating expense paid in cash",
                    "operating",
                    (Line("operating_expense", debit=operating), Line("cash", credit=operating)),
                )
            )
            collection = ledger.balance("accounts_receivable", year) * 4 // 5
            ledger.post(
                Entry(
                    year,
                    quarter,
                    "collection of receivables",
                    "operating",
                    (Line("cash", debit=collection), Line("accounts_receivable", credit=collection)),
                )
            )
            payment = ledger.balance("accounts_payable", year) * 9 // 10
            ledger.post(
                Entry(
                    year,
                    quarter,
                    "payment of payables",
                    "operating",
                    (Line("accounts_payable", debit=payment), Line("cash", credit=payment)),
                )
            )
            depreciation = 25_000_000 + (7_500_000 if year >= 2026 else 0)
            ledger.post(
                Entry(
                    year,
                    quarter,
                    "depreciation of equipment",
                    "noncash",
                    (
                        Line("depreciation_expense", debit=depreciation),
                        Line("accumulated_depreciation", credit=depreciation),
                    ),
                )
            )
            if quarter == 4:
                ledger.post(
                    Entry(
                        year,
                        quarter,
                        "dividends paid",
                        "financing",
                        (Line("dividends", debit=20_000_000), Line("cash", credit=20_000_000)),
                    )
                )


def income_statement(ledger: Ledger, year: int) -> dict[str, int]:
    """Revenue, cost lines and net income for one fiscal year, in integer cents (costs positive)."""
    sales = -ledger.net("sales", year=year)
    cost = ledger.net("cost_of_sales", year=year)
    opex = ledger.net("operating_expense", year=year)
    dep = ledger.net("depreciation_expense", year=year)
    return {
        "sales": sales,
        "cost_of_sales": cost,
        "operating_expense": opex,
        "depreciation": dep,
        "net_income": sales - cost - opex - dep,
    }


def balance_sheet(ledger: Ledger, year: int) -> dict[str, int]:
    """Balances at the end of one fiscal year (the opening position is year 2024). Retained earnings is the
    cumulative income statement less cumulative dividends, since the ledger has no closing entries."""
    cash = ledger.balance("cash", year)
    receivables = ledger.balance("accounts_receivable", year)
    equipment = ledger.balance("equipment", year)
    depreciated = ledger.balance("accumulated_depreciation", year)
    payables = ledger.balance("accounts_payable", year)
    debt = ledger.balance("long_term_debt", year)
    common = ledger.balance("common_stock", year)
    cumulative_income = -(
        ledger.net("sales", through=year)
        + ledger.net("cost_of_sales", through=year)
        + ledger.net("operating_expense", through=year)
        + ledger.net("depreciation_expense", through=year)
    )
    retained = cumulative_income - ledger.balance("dividends", year)
    assets = cash + receivables + equipment - depreciated
    liabilities = payables + debt
    equity = common + retained
    return {
        "cash": cash,
        "accounts_receivable": receivables,
        "equipment_at_cost": equipment,
        "accumulated_depreciation": depreciated,
        "total_assets": assets,
        "accounts_payable": payables,
        "long_term_debt": debt,
        "total_liabilities": liabilities,
        "common_stock": common,
        "retained_earnings": retained,
        "total_equity": equity,
        "total_liabilities_and_equity": liabilities + equity,
    }


def cash_flow_statement(ledger: Ledger, year: int) -> tuple[dict[str, int], dict[str, int]]:
    """The direct-method cash-flow statement: cash lines grouped by memo, and subtotals by activity."""
    by_memo: dict[str, int] = {}
    by_activity = {activity: 0 for activity in ACTIVITIES}
    for entry in ledger.entries:
        if entry.year != year:
            continue
        for line in entry.lines:
            if line.account == "cash":
                amount = line.debit - line.credit
                by_memo[entry.memo] = by_memo.get(entry.memo, 0) + amount
                by_activity[entry.activity] += amount
    return by_memo, by_activity


def main() -> None:
    ledger = Ledger()
    generate(ledger, random.Random(SEED))

    print("Income statement, USD (fiscal years)")
    columns = [income_statement(ledger, y) for y in YEARS]
    rows = ("sales", "cost_of_sales", "operating_expense", "depreciation", "net_income")
    print(f"{'':<22}" + "".join(f"{y:>18}" for y in YEARS))
    for row in rows:
        print(f"{row:<22}" + "".join(f"{money(c[row]):>18}" for c in columns))

    print()
    print("Balance sheet at fiscal year end, USD (2024 is the opening position)")
    years_bs = (OPENING_YEAR, *YEARS)
    sheets = [balance_sheet(ledger, y) for y in years_bs]
    print(f"{'':<30}" + "".join(f"{y:>18}" for y in years_bs))
    for row in sheets[0]:
        print(f"{row:<30}" + "".join(f"{money(s[row]):>18}" for s in sheets))
    balanced = [s["total_assets"] == s["total_liabilities_and_equity"] for s in sheets]
    print(f"total assets equal total liabilities and equity at every year end: {all(balanced)}")

    print()
    print("Cash-flow statement, direct method, USD")
    print(f"{'':<36}" + "".join(f"{y:>18}" for y in YEARS))
    memos = list(
        dict.fromkeys(e.memo for e in ledger.entries if e.year in YEARS and any(x.account == "cash" for x in e.lines))
    )
    statements = [cash_flow_statement(ledger, y) for y in YEARS]
    for memo in memos:
        cells = "".join(f"{money(by_memo.get(memo, 0)):>18}" for by_memo, _ in statements)
        print(f"{memo:<36}{cells}")
    for activity in ACTIVITIES[:3]:
        cells = "".join(f"{money(by_activity[activity]):>18}" for _, by_activity in statements)
        print(f"{'subtotal, ' + activity:<36}{cells}")
    net_change = [sum(by_activity.values()) for _, by_activity in statements]
    print(f"{'net change in cash':<36}" + "".join(f"{money(x):>18}" for x in net_change))
    ending = [sheets[i + 1]["cash"] for i in range(len(YEARS))]
    print(f"{'ending cash, balance sheet':<36}" + "".join(f"{money(x):>18}" for x in ending))
    print(f"lowest cash balance at any year end (USD): {money(min(s['cash'] for s in sheets))}")


main()
