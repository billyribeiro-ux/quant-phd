"""Independent correct statements.py (round 9): bisect cutoffs on sorted postings, hand-written date parser."""

from __future__ import annotations

import bisect
from collections.abc import Mapping, Sequence
from datetime import date, timedelta
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

_MSG = "a date must be an ISO date, YYYY-MM-DD"


def _parse_iso(value: object, msg: str) -> date:
    if not isinstance(value, str):
        raise ValueError(msg)
    parts = value.split("-")
    if len(parts) != 3 or len(parts[0]) != 4 or len(parts[1]) != 2 or len(parts[2]) != 2:
        raise ValueError(msg)
    if not all(p.isascii() and p.isdigit() for p in parts):
        raise ValueError(msg)
    try:
        return date(int(parts[0]), int(parts[1]), int(parts[2]))
    except ValueError as error:
        raise ValueError(msg) from error


def _is_month_end(day: date) -> bool:
    return (day + timedelta(days=1)).day == 1


class _Ledger(tuple):
    """Sorted postings: (iso date, account, signed cents). Opaque to callers."""


def post(transactions: Sequence[Mapping[str, Any]]) -> _Ledger:
    rows: list[tuple[str, str, int]] = []
    for entry in transactions:
        if not isinstance(entry, Mapping):
            raise ValueError("a transaction needs a date and lines")
        if "date" not in entry or "lines" not in entry:
            raise ValueError("a transaction needs a date and lines")
        day = _parse_iso(entry["date"], _MSG).isoformat()
        lines = entry["lines"]
        if isinstance(lines, (str, bytes)) or not isinstance(lines, Sequence):
            raise ValueError("a transaction needs at least one line")
        if len(lines) == 0:
            raise ValueError("a transaction needs at least one line")
        net = 0
        staged: list[tuple[str, str, int]] = []
        for line in lines:
            if not isinstance(line, Mapping):
                raise ValueError("a line needs an account, a debit and a credit")
            if not {"account", "debit", "credit"}.issubset(line.keys()):
                raise ValueError("a line needs an account, a debit and a credit")
            account = line["account"]
            if not isinstance(account, str) or account not in ACCOUNTS:
                raise ValueError("an account is not in the chart")
            amounts = []
            for key in ("debit", "credit"):
                amount = line[key]
                if type(amount) is not int:
                    raise ValueError("an amount must be an integer number of cents")
                if amount < 0:
                    raise ValueError("an amount must not be negative")
                amounts.append(amount)
            debit, credit = amounts
            if (debit != 0) == (credit != 0):
                raise ValueError("a line carries a debit or a credit, and exactly one")
            staged.append((day, account, debit - credit))
            net += debit - credit
        if net != 0:
            raise ValueError("the debits of an entry must equal its credits")
        rows.extend(staged)
    rows.sort()
    return _Ledger(rows)


def _check_period(period_end: str) -> str:
    day = _parse_iso(period_end, "a period end must be a month end in YYYY-MM-DD form")
    if not _is_month_end(day):
        raise ValueError("a period end must be a month end in YYYY-MM-DD form")
    return day.isoformat()


def _through(ledger: _Ledger, end: str) -> dict[str, int]:
    cut = bisect.bisect_right(ledger, (end, "￿", 10**30))
    totals = dict.fromkeys(ACCOUNTS, 0)
    for _, account, signed in ledger[:cut]:
        totals[account] += signed
    return totals


def _previous_end(end: str) -> str:
    day = date.fromisoformat(end)
    return (day.replace(day=1) - timedelta(days=1)).isoformat()


def balance_sheet(ledger: _Ledger, period_end: str) -> dict[str, int]:
    end = _check_period(period_end)
    b = _through(ledger, end)
    acc = -b["accumulated_depreciation"]
    net_eq = b["equipment"] - acc
    assets = b["cash"] + b["accounts_receivable"] + b["inventory"] + net_eq
    ap = -b["accounts_payable"]
    ltd = -b["long_term_debt"]
    cs = -b["common_stock"]
    ni_to_date = -sum(b[k] for k in ("sales", "cost_of_goods_sold", "operating_expenses", "depreciation_expense"))
    re = ni_to_date - b["dividends"]
    tl = ap + ltd
    te = cs + re
    return {
        "cash": b["cash"],
        "accounts_receivable": b["accounts_receivable"],
        "inventory": b["inventory"],
        "equipment": b["equipment"],
        "accumulated_depreciation": acc,
        "net_equipment": net_eq,
        "total_assets": assets,
        "accounts_payable": ap,
        "long_term_debt": ltd,
        "total_liabilities": tl,
        "common_stock": cs,
        "retained_earnings": re,
        "total_equity": te,
        "total_liabilities_and_equity": tl + te,
    }


def _month(ledger: _Ledger, period_end: str) -> tuple[dict[str, int], dict[str, int]]:
    end = _check_period(period_end)
    now = _through(ledger, end)
    before = _through(ledger, _previous_end(end))
    return now, {k: now[k] - before[k] for k in ACCOUNTS}


def income_statement(ledger: _Ledger, period_end: str) -> dict[str, int]:
    _, flow = _month(ledger, period_end)
    sales = -flow["sales"]
    cogs = flow["cost_of_goods_sold"]
    opex = flow["operating_expenses"]
    dep = flow["depreciation_expense"]
    gross = sales - cogs
    return {
        "sales": sales,
        "cost_of_goods_sold": cogs,
        "gross_profit": gross,
        "operating_expenses": opex,
        "depreciation_expense": dep,
        "net_income": gross - opex - dep,
    }


def cash_flow_statement(ledger: _Ledger, period_end: str) -> dict[str, int]:
    now, flow = _month(ledger, period_end)
    before_cash = now["cash"] - flow["cash"]  # the balance at the previous month end
    ni = income_statement(ledger, period_end)["net_income"]
    dep = flow["depreciation_expense"]
    recv = -flow["accounts_receivable"]
    inv = -flow["inventory"]
    pay = -flow["accounts_payable"]
    ops = ni + dep + recv + inv + pay
    capex = -flow["equipment"]
    borrow = -flow["long_term_debt"]
    issued = -flow["common_stock"]
    div = -flow["dividends"]
    fin = borrow + issued + div
    return {
        "net_income": ni,
        "depreciation": dep,
        "receivables": recv,
        "inventory": inv,
        "payables": pay,
        "cash_from_operations": ops,
        "capital_expenditure": capex,
        "cash_from_investing": capex,
        "net_borrowing": borrow,
        "stock_issued": issued,
        "dividends_paid": div,
        "cash_from_financing": fin,
        "net_change_in_cash": ops + capex + fin,
        "beginning_cash": before_cash,
        "ending_cash": before_cash + ops + capex + fin,
    }


def articulation_check(ledger: _Ledger, period_end: str) -> dict[str, int]:
    end = _check_period(period_end)
    prev = _previous_end(end)
    now = balance_sheet(ledger, end)
    before = balance_sheet(ledger, prev)
    cf = cash_flow_statement(ledger, end)
    inc = income_statement(ledger, end)
    return {
        "balance_gap": now["total_assets"] - now["total_liabilities_and_equity"],
        "cash_gap": now["cash"] - cf["ending_cash"],
        "retained_earnings_gap": (now["retained_earnings"] - before["retained_earnings"]) - (inc["net_income"] + cf["dividends_paid"]),
        "depreciation_gap": (now["accumulated_depreciation"] - before["accumulated_depreciation"]) - inc["depreciation_expense"],
    }
