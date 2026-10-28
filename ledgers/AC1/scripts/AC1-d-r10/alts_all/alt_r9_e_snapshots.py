"""Independent correct statements.py (round 9): per-day snapshots, regex dates, calendar month ends."""

from __future__ import annotations

import calendar
import re
from collections.abc import Mapping, Sequence
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

_ISO = re.compile(r"([0-9]{4})-([0-9]{2})-([0-9]{2})")
_MSG = "a date must be an ISO date, YYYY-MM-DD"


def _date_parts(value: object, msg: str) -> tuple[int, int, int]:
    if not isinstance(value, str):
        raise ValueError(msg)
    match = _ISO.fullmatch(value)
    if match is None:
        raise ValueError(msg)
    year, month, day = (int(g) for g in match.groups())
    if not 1 <= month <= 12 or not 1 <= day <= calendar.monthrange(year, month)[1]:
        raise ValueError(msg)
    return year, month, day


def _amount(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("an amount must be an integer number of cents")
    if value < 0:
        raise ValueError("an amount must not be negative")
    return value


class Ledger:
    def __init__(self, by_day: dict[str, dict[str, int]]) -> None:
        self._by_day = by_day
        self._days = sorted(by_day)

    def through(self, end: str) -> dict[str, int]:
        totals = dict.fromkeys(ACCOUNTS, 0)
        for day in self._days:
            if day > end:
                break
            for account, signed in self._by_day[day].items():
                totals[account] += signed
        return totals


def post(transactions: Sequence[Mapping[str, Any]]) -> Ledger:
    by_day: dict[str, dict[str, int]] = {}
    for entry in transactions:
        if not isinstance(entry, Mapping) or "date" not in entry or "lines" not in entry:
            raise ValueError("a transaction needs a date and lines")
        year, month, day = _date_parts(entry["date"], _MSG)
        iso = f"{year:04d}-{month:02d}-{day:02d}"
        lines = entry["lines"]
        if isinstance(lines, str) or not isinstance(lines, Sequence) or not lines:
            raise ValueError("a transaction needs at least one line")
        total = 0
        bucket = by_day.setdefault(iso, {})
        pending: list[tuple[str, int]] = []
        for line in lines:
            if not isinstance(line, Mapping):
                raise ValueError("a line needs an account, a debit and a credit")
            for key in ("account", "debit", "credit"):
                if key not in line:
                    raise ValueError("a line needs an account, a debit and a credit")
            account = line["account"]
            if account not in ACCOUNTS:
                raise ValueError("an account is not in the chart")
            debit = _amount(line["debit"])
            credit = _amount(line["credit"])
            if (debit > 0) + (credit > 0) != 1:
                raise ValueError("a line carries a debit or a credit, and exactly one")
            pending.append((account, debit - credit))
            total += debit - credit
        if total:
            raise ValueError("the debits of an entry must equal its credits")
        for account, signed in pending:
            bucket[account] = bucket.get(account, 0) + signed
    return Ledger(by_day)


def _period(period_end: str) -> tuple[str, str]:
    year, month, day = _date_parts(period_end, "a period end must be a month end")
    if day != calendar.monthrange(year, month)[1]:
        raise ValueError("a period end must be a month end")
    prev_year, prev_month = (year, month - 1) if month > 1 else (year - 1, 12)
    previous = f"{prev_year:04d}-{prev_month:02d}-{calendar.monthrange(prev_year, prev_month)[1]:02d}"
    return f"{year:04d}-{month:02d}-{day:02d}", previous


def balance_sheet(ledger: Ledger, period_end: str) -> dict[str, int]:
    end, _ = _period(period_end)
    b = ledger.through(end)
    accumulated = -b["accumulated_depreciation"]
    net_equipment = b["equipment"] - accumulated
    total_assets = b["cash"] + b["accounts_receivable"] + b["inventory"] + net_equipment
    payables = -b["accounts_payable"]
    debt = -b["long_term_debt"]
    stock = -b["common_stock"]
    income = -sum(b[a] for a in ("sales", "cost_of_goods_sold", "operating_expenses", "depreciation_expense"))
    retained = income - b["dividends"]
    liabilities = payables + debt
    equity = stock + retained
    return {
        "cash": b["cash"],
        "accounts_receivable": b["accounts_receivable"],
        "inventory": b["inventory"],
        "equipment": b["equipment"],
        "accumulated_depreciation": accumulated,
        "net_equipment": net_equipment,
        "total_assets": total_assets,
        "accounts_payable": payables,
        "long_term_debt": debt,
        "total_liabilities": liabilities,
        "common_stock": stock,
        "retained_earnings": retained,
        "total_equity": equity,
        "total_liabilities_and_equity": liabilities + equity,
    }


def _flow(ledger: Ledger, period_end: str) -> tuple[dict[str, int], dict[str, int], str]:
    end, prev = _period(period_end)
    now = ledger.through(end)
    before = ledger.through(prev)
    return now, {a: now[a] - before[a] for a in ACCOUNTS}, prev


def income_statement(ledger: Ledger, period_end: str) -> dict[str, int]:
    _, f, _ = _flow(ledger, period_end)
    sales = -f["sales"]
    gross = sales - f["cost_of_goods_sold"]
    net = gross - f["operating_expenses"] - f["depreciation_expense"]
    return {
        "sales": sales,
        "cost_of_goods_sold": f["cost_of_goods_sold"],
        "gross_profit": gross,
        "operating_expenses": f["operating_expenses"],
        "depreciation_expense": f["depreciation_expense"],
        "net_income": net,
    }


def cash_flow_statement(ledger: Ledger, period_end: str) -> dict[str, int]:
    now, f, prev = _flow(ledger, period_end)
    ni = income_statement(ledger, period_end)["net_income"]
    receivables = -f["accounts_receivable"]
    inventory = -f["inventory"]
    payables = -f["accounts_payable"]
    depreciation = f["depreciation_expense"]
    operations = ni + depreciation + receivables + inventory + payables
    capex = -f["equipment"]
    borrowing = -f["long_term_debt"]
    stock = -f["common_stock"]
    dividends = -f["dividends"]
    financing = borrowing + stock + dividends
    beginning = ledger.through(prev)["cash"]
    return {
        "net_income": ni,
        "depreciation": depreciation,
        "receivables": receivables,
        "inventory": inventory,
        "payables": payables,
        "cash_from_operations": operations,
        "capital_expenditure": capex,
        "cash_from_investing": capex,
        "net_borrowing": borrowing,
        "stock_issued": stock,
        "dividends_paid": dividends,
        "cash_from_financing": financing,
        "net_change_in_cash": operations + capex + financing,
        "beginning_cash": beginning,
        "ending_cash": beginning + operations + capex + financing,
    }


def articulation_check(ledger: Ledger, period_end: str) -> dict[str, int]:
    end, prev = _period(period_end)
    now = balance_sheet(ledger, end)
    before = balance_sheet(ledger, prev)
    cf = cash_flow_statement(ledger, end)
    inc = income_statement(ledger, end)
    return {
        "balance_gap": now["total_assets"] - now["total_liabilities_and_equity"],
        "cash_gap": now["cash"] - cf["ending_cash"],
        "retained_earnings_gap": now["retained_earnings"] - before["retained_earnings"] - inc["net_income"] - cf["dividends_paid"],
        "depreciation_gap": now["accumulated_depreciation"] - before["accumulated_depreciation"] - inc["depreciation_expense"],
    }
