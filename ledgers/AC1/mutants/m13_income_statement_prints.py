"""income_statement prints a debugging line, so the statement functions are not silent.

Written by the AC1-d round 2 verifier from grader/reference.py; one error applied.
"""

from __future__ import annotations

import calendar
from collections.abc import Mapping, Sequence
from datetime import date, timedelta
from numbers import Integral
from typing import Any

ACCOUNTS: dict[str, str] = {
    "cash": "asset",
    "accounts_receivable": "asset",
    "inventory": "asset",
    "equipment": "asset",
    "accumulated_depreciation": "contra_asset",
    "accounts_payable": "liability",
    "long_term_debt": "liability",
    "common_stock": "equity",
    "dividends": "distribution",
    "sales": "revenue",
    "cost_of_goods_sold": "expense",
    "operating_expenses": "expense",
    "depreciation_expense": "expense",
}

# A ledger is opaque to callers: a tuple of (date, account, debit minus credit in cents).
Ledger = tuple[tuple[str, str, int], ...]


def _iso_date(value: object) -> str:
    if not isinstance(value, str) or len(value) != 10:
        raise ValueError("a date must be an ISO date, YYYY-MM-DD")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as error:
        raise ValueError("a date must be an ISO date, YYYY-MM-DD") from error
    if parsed.isoformat() != value:
        raise ValueError("a date must be an ISO date, YYYY-MM-DD")
    return value


def _cents(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, Integral):
        raise ValueError("an amount must be an integer number of cents")
    if value < 0:
        raise ValueError("an amount must not be negative")
    return int(value)


def _month_end(value: object) -> str:
    text = _iso_date(value)
    parsed = date.fromisoformat(text)
    if parsed.day != calendar.monthrange(parsed.year, parsed.month)[1]:
        raise ValueError("a period end must be the last day of a calendar month")
    return text


def _previous_month_end(end: str) -> str:
    first = date.fromisoformat(end).replace(day=1)
    return (first - timedelta(days=1)).isoformat()


def post(transactions: Sequence[Mapping[str, Any]]) -> Ledger:
    postings: list[tuple[str, str, int]] = []
    for entry in transactions:
        if not isinstance(entry, Mapping) or "date" not in entry or "lines" not in entry:
            raise ValueError("a transaction needs a date and its lines")
        day = _iso_date(entry["date"])
        lines = entry["lines"]
        if isinstance(lines, str) or not isinstance(lines, Sequence) or len(lines) == 0:
            raise ValueError("a transaction needs at least one line")
        total = 0
        for line in lines:
            if not isinstance(line, Mapping) or not {"account", "debit", "credit"} <= set(line):
                raise ValueError("a line needs an account, a debit and a credit")
            account = line["account"]
            if not isinstance(account, str) or account not in ACCOUNTS:
                raise ValueError("an unknown account is not in the chart of accounts")
            debit, credit = _cents(line["debit"]), _cents(line["credit"])
            if (debit > 0) == (credit > 0):
                raise ValueError("a line carries a debit or a credit, and exactly one")
            postings.append((day, account, debit - credit))
            total += debit - credit
        if total != 0:
            raise ValueError("unbalanced entry: the debits must equal the credits")
    return tuple(postings)


def _balances(ledger: Ledger, end: str) -> dict[str, int]:
    totals = dict.fromkeys(ACCOUNTS, 0)
    for day, account, signed in ledger:
        if day <= end:
            totals[account] += signed
    return totals


def balance_sheet(ledger: Ledger, period_end: str) -> dict[str, int]:
    end = _month_end(period_end)
    bal = _balances(ledger, end)
    accumulated = -bal["accumulated_depreciation"]
    net_equipment = bal["equipment"] - accumulated
    total_assets = bal["cash"] + bal["accounts_receivable"] + bal["inventory"] + net_equipment
    payables = -bal["accounts_payable"]
    debt = -bal["long_term_debt"]
    total_liabilities = payables + debt
    common = -bal["common_stock"]
    income = -(bal["sales"] + bal["cost_of_goods_sold"] + bal["operating_expenses"] + bal["depreciation_expense"])
    retained = income - bal["dividends"]
    total_equity = common + retained
    return {
        "cash": bal["cash"],
        "accounts_receivable": bal["accounts_receivable"],
        "inventory": bal["inventory"],
        "equipment": bal["equipment"],
        "accumulated_depreciation": accumulated,
        "net_equipment": net_equipment,
        "total_assets": total_assets,
        "accounts_payable": payables,
        "long_term_debt": debt,
        "total_liabilities": total_liabilities,
        "common_stock": common,
        "retained_earnings": retained,
        "total_equity": total_equity,
        "total_liabilities_and_equity": total_liabilities + total_equity,
    }


def _flows(ledger: Ledger, period_end: str) -> tuple[dict[str, int], dict[str, int], dict[str, int]]:
    end = _month_end(period_end)
    prev = _previous_month_end(end)
    now, before = _balances(ledger, end), _balances(ledger, prev)
    return now, before, {account: now[account] - before[account] for account in ACCOUNTS}


def income_statement(ledger: Ledger, period_end: str) -> dict[str, int]:
    print("income", period_end)
    _, _, flow = _flows(ledger, period_end)
    sales = -flow["sales"]
    cost = flow["cost_of_goods_sold"]
    gross = sales - cost
    operating = flow["operating_expenses"]
    depreciation = flow["depreciation_expense"]
    return {
        "sales": sales,
        "cost_of_goods_sold": cost,
        "gross_profit": gross,
        "operating_expenses": operating,
        "depreciation_expense": depreciation,
        "net_income": gross - operating - depreciation,
    }


def cash_flow_statement(ledger: Ledger, period_end: str) -> dict[str, int]:
    now, before, flow = _flows(ledger, period_end)
    net_income = income_statement(ledger, period_end)["net_income"]
    depreciation = flow["depreciation_expense"]
    receivables = -(now["accounts_receivable"] - before["accounts_receivable"])
    inventory = -(now["inventory"] - before["inventory"])
    payables = -(now["accounts_payable"] - before["accounts_payable"])
    operations = net_income + depreciation + receivables + inventory + payables
    capital_expenditure = -flow["equipment"]
    net_borrowing = -flow["long_term_debt"]
    stock_issued = -flow["common_stock"]
    dividends_paid = -flow["dividends"]
    financing = net_borrowing + stock_issued + dividends_paid
    beginning = before["cash"]
    return {
        "net_income": net_income,
        "depreciation": depreciation,
        "receivables": receivables,
        "inventory": inventory,
        "payables": payables,
        "cash_from_operations": operations,
        "capital_expenditure": capital_expenditure,
        "cash_from_investing": capital_expenditure,
        "net_borrowing": net_borrowing,
        "stock_issued": stock_issued,
        "dividends_paid": dividends_paid,
        "cash_from_financing": financing,
        "net_change_in_cash": operations + capital_expenditure + financing,
        "beginning_cash": beginning,
        "ending_cash": beginning + operations + capital_expenditure + financing,
    }


def articulation_check(ledger: Ledger, period_end: str) -> dict[str, int]:
    end = _month_end(period_end)
    prev = _previous_month_end(end)
    now, before = balance_sheet(ledger, end), balance_sheet(ledger, prev)
    cash_flow = cash_flow_statement(ledger, end)
    net_income = income_statement(ledger, end)["net_income"]
    return {
        "balance_gap": now["total_assets"] - now["total_liabilities_and_equity"],
        "cash_gap": now["cash"] - cash_flow["ending_cash"],
        "retained_earnings_gap": (now["retained_earnings"] - before["retained_earnings"])
        - (net_income + cash_flow["dividends_paid"]),
        "depreciation_gap": (now["accumulated_depreciation"] - before["accumulated_depreciation"])
        - income_statement(ledger, end)["depreciation_expense"],
    }
