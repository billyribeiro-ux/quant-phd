"""AC1 lab L03: link the three statements and check the articulation identities that it prints.

SIMULATED: the firm is generated from a seeded random number generator for this lab. It is not a real company.
The same ledger as Lab 2 is used. Amounts are integer cents and are printed in USD. The indirect cash-flow
statement is derived from the income statement and the balance sheet, and each printed identity linking the statements
is checked against the ledger. The investing and financing equalities of Proposition 3.1 are not printed.
Depreciation follows a straight-line schedule computed here. Standard library
only; no network.
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
    """One side of one account, in integer cents. Exactly one of debit and credit is non-zero."""

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


def indirect_operating(ledger: Ledger, year: int) -> dict[str, int]:
    """Operating cash flow by the indirect method: net income, plus depreciation, less the increase in
    receivables, plus the increase in payables. Every input comes from the statements or the balance sheet."""
    income = income_statement(ledger, year)
    receivables_change = ledger.balance("accounts_receivable", year) - ledger.balance("accounts_receivable", year - 1)
    payables_change = ledger.balance("accounts_payable", year) - ledger.balance("accounts_payable", year - 1)
    return {
        "net_income": income["net_income"],
        "depreciation_add_back": income["depreciation"],
        "less_increase_in_receivables": -receivables_change,
        "plus_increase_in_payables": payables_change,
        "operating": income["net_income"] + income["depreciation"] - receivables_change + payables_change,
    }


# Straight-line schedule for the two pieces of equipment in the ledger. Cost in integer cents; life in years;
# first_quarter counts quarters from 1 (2025 Q1 is 1). The costs divide exactly into quarters, so no remainder rule
# is needed; depreciation_schedule rejects a cost that does not.
ASSETS: tuple[tuple[str, int, int, int], ...] = (
    ("equipment A", 500_000_000, 5, 1),
    ("equipment B", 150_000_000, 5, 5),
)


def depreciation_schedule(year: int) -> int:
    """Accumulated straight-line depreciation at the end of a fiscal year, in integer cents."""
    quarters_through = (year - YEARS[0] + 1) * 4
    total = 0
    for name, cost, life_years, first_quarter in ASSETS:
        quarters_of_life = life_years * 4
        if cost % quarters_of_life:
            raise ValueError(f"{name}: cost {cost} does not divide into {quarters_of_life} quarters exactly")
        per_quarter = cost // quarters_of_life
        in_service = max(0, min(quarters_through, quarters_of_life) - first_quarter + 1)
        total += per_quarter * in_service
    return total


def main() -> None:
    ledger = Ledger()
    generate(ledger, random.Random(SEED))
    sheets = {y: balance_sheet(ledger, y) for y in (OPENING_YEAR, *YEARS)}

    print("Check 1: the balance sheet balances at every year end (USD)")
    for year in (OPENING_YEAR, *YEARS):
        gap = sheets[year]["total_assets"] - sheets[year]["total_liabilities_and_equity"]
        print(f"{year} year end: assets less liabilities and equity = {money(gap)}")

    print()
    print("Check 2: operating cash flow, indirect method against direct method (USD)")
    print(f"{'':<34}" + "".join(f"{y:>16}" for y in YEARS))
    indirect = {y: indirect_operating(ledger, y) for y in YEARS}
    direct = {y: cash_flow_statement(ledger, y)[1]["operating"] for y in YEARS}
    for key in ("net_income", "depreciation_add_back", "less_increase_in_receivables", "plus_increase_in_payables"):
        print(f"{key:<34}" + "".join(f"{money(indirect[y][key]):>16}" for y in YEARS))
    print(f"{'operating, indirect':<34}" + "".join(f"{money(indirect[y]['operating']):>16}" for y in YEARS))
    print(f"{'operating, direct (cash lines)':<34}" + "".join(f"{money(direct[y]):>16}" for y in YEARS))
    print(f"indirect equals direct: {all(indirect[y]['operating'] == direct[y] for y in YEARS)}")

    print()
    print("Check 3: retained earnings and net equipment roll forward (USD)")
    for year in YEARS:
        income = income_statement(ledger, year)["net_income"]
        dividends = ledger.net("dividends", year=year)
        opening_re = sheets[year - 1]["retained_earnings"]
        closing_re = sheets[year]["retained_earnings"]
        capex = ledger.net("equipment", year=year)
        dep = income_statement(ledger, year)["depreciation"]
        net_before = sheets[year - 1]["equipment_at_cost"] - sheets[year - 1]["accumulated_depreciation"]
        net_after = sheets[year]["equipment_at_cost"] - sheets[year]["accumulated_depreciation"]
        print(
            f"{year}: retained earnings {money(opening_re)} + net income {money(income)} "
            f"- dividends {money(dividends)} = {money(closing_re)}: {opening_re + income - dividends == closing_re}"
        )
        print(
            f"      net equipment {money(net_before)} + additions {money(capex)} "
            f"- depreciation {money(dep)} = {money(net_after)}: {net_before + capex - dep == net_after}"
        )

    print()
    print("Check 4: cash flows to the balance sheet cash (USD)")
    for year in YEARS:
        _, by_activity = cash_flow_statement(ledger, year)
        opening_cash = sheets[year - 1]["cash"]
        ending_cash = sheets[year]["cash"]
        net = by_activity["operating"] + by_activity["investing"] + by_activity["financing"]
        print(
            f"{year}: opening {money(opening_cash)} + operating {money(by_activity['operating'])} "
            f"+ investing {money(by_activity['investing'])} + financing {money(by_activity['financing'])} "
            f"= {money(opening_cash + net)}; balance sheet cash {money(ending_cash)}: "
            f"{opening_cash + net == ending_cash}"
        )

    print()
    print("Check 5: accumulated depreciation in the ledger against the straight-line schedule (USD)")
    for year in (OPENING_YEAR, *YEARS):
        ledger_value = sheets[year]["accumulated_depreciation"]
        schedule_value = depreciation_schedule(year) if year >= YEARS[0] else 0
        print(
            f"{year} year end: ledger {money(ledger_value)}, "
            f"schedule {money(schedule_value)}: {ledger_value == schedule_value}"
        )

    print()
    print("Check 6: the gap that each omitted term leaves in an identity (USD)")
    for year in YEARS:
        missing_add_back = indirect[year]["operating"] - indirect[year]["depreciation_add_back"]
        difference = direct[year] - missing_add_back
        print(
            f"{year}: operating without the depreciation add-back is {money(missing_add_back)}; "
            f"the gap to the ledger is {money(difference)}, equal to depreciation: "
            f"{difference == indirect[year]['depreciation_add_back']}"
        )
    for year in YEARS:
        opening_re = sheets[year - 1]["retained_earnings"]
        closing_re = sheets[year]["retained_earnings"]
        income = income_statement(ledger, year)["net_income"]
        dividends = ledger.net("dividends", year=year)
        without_deduction = opening_re + income
        print(
            f"{year}: retained earnings with no dividend deduction would be {money(without_deduction)}, "
            f"balance sheet {money(closing_re)}; the gap {money(without_deduction - closing_re)} equals dividends: "
            f"{without_deduction - closing_re == dividends}"
        )

    print()
    articulated = all(
        indirect[y]["operating"] == direct[y]
        and sheets[y - 1]["cash"] + sum(cash_flow_statement(ledger, y)[1][a] for a in ACTIVITIES[:3])
        == sheets[y]["cash"]
        and sheets[y]["retained_earnings"] - sheets[y - 1]["retained_earnings"]
        == income_statement(ledger, y)["net_income"] - ledger.net("dividends", year=y)
        for y in YEARS
    )
    print(f"all articulation identities hold in every year: {articulated}")


main()
