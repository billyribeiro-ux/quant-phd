"""Alternative correct implementation (not the reference): ledger is a dict of account -> list of (date, signed cents)."""

from __future__ import annotations

import calendar
import re
from datetime import date, timedelta
from typing import Any

ACCOUNTS = {
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
_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _day(value: Any) -> date:
    if not isinstance(value, str) or not _DATE.match(value):
        raise ValueError("date must be YYYY-MM-DD")
    try:
        return date(int(value[:4]), int(value[5:7]), int(value[8:]))
    except ValueError as error:
        raise ValueError("date is not a real calendar date") from error


def _amount(value: Any) -> int:
    if type(value) is not int:
        raise ValueError("amount must be an integer number of cents")
    if value < 0:
        raise ValueError("amount must not be negative")
    return value


def post(transactions: Any) -> dict[str, list[tuple[date, int]]]:
    ledger: dict[str, list[tuple[date, int]]] = {account: [] for account in ACCOUNTS}
    for entry in transactions:
        if not isinstance(entry, dict) or "date" not in entry or "lines" not in entry:
            raise ValueError("transaction needs date and lines")
        when = _day(entry["date"])
        lines = entry["lines"]
        if not isinstance(lines, list) or not lines:
            raise ValueError("transaction needs at least one line")
        pending = []
        net = 0
        for line in lines:
            if not isinstance(line, dict) or any(k not in line for k in ("account", "debit", "credit")):
                raise ValueError("line needs account, debit and credit")
            account = line["account"]
            if account not in ACCOUNTS:
                raise ValueError("account outside chart")
            dr, cr = _amount(line["debit"]), _amount(line["credit"])
            if (dr and cr) or (not dr and not cr):
                raise ValueError("line needs exactly one side")
            net += dr - cr
            pending.append((account, dr - cr))
        if net != 0:
            raise ValueError("entry does not balance")
        for account, signed in pending:
            ledger[account].append((when, signed))
    return ledger


def _through(ledger: dict[str, list[tuple[date, int]]], end: date) -> dict[str, int]:
    return {a: sum(s for d, s in rows if d <= end) for a, rows in ledger.items()}


def _end(value: Any) -> date:
    d = _day(value)
    if d.day != calendar.monthrange(d.year, d.month)[1]:
        raise ValueError("period end must be a month end")
    return d


def _prev(end: date) -> date:
    return end.replace(day=1) - timedelta(days=1)


def balance_sheet(ledger: Any, period_end: Any) -> dict[str, int]:
    end = _end(period_end)
    b = _through(ledger, end)
    acc = -b["accumulated_depreciation"]
    net_eq = b["equipment"] - acc
    assets = b["cash"] + b["accounts_receivable"] + b["inventory"] + net_eq
    ap = -b["accounts_payable"]
    ltd = -b["long_term_debt"]
    liab = ap + ltd
    stock = -b["common_stock"]
    re_ = -(b["sales"] + b["cost_of_goods_sold"] + b["operating_expenses"] + b["depreciation_expense"]) - b["dividends"]
    eq = stock + re_
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
        "total_liabilities": liab,
        "common_stock": stock,
        "retained_earnings": re_,
        "total_equity": eq,
        "total_liabilities_and_equity": liab + eq,
    }


def _flow(ledger: Any, end: date) -> tuple[dict[str, int], dict[str, int], dict[str, int]]:
    now = _through(ledger, end)
    before = _through(ledger, _prev(end))
    return now, before, {a: now[a] - before[a] for a in ACCOUNTS}


def income_statement(ledger: Any, period_end: Any) -> dict[str, int]:
    _, _, f = _flow(ledger, _end(period_end))
    sales = -f["sales"]
    cogs = f["cost_of_goods_sold"]
    gross = sales - cogs
    opex = f["operating_expenses"]
    dep = f["depreciation_expense"]
    return {
        "sales": sales,
        "cost_of_goods_sold": cogs,
        "gross_profit": gross,
        "operating_expenses": opex,
        "depreciation_expense": dep,
        "net_income": gross - opex - dep,
    }


def cash_flow_statement(ledger: Any, period_end: Any) -> dict[str, int]:
    end = _end(period_end)
    now, before, f = _flow(ledger, end)
    ni = income_statement(ledger, period_end)["net_income"]
    dep = f["depreciation_expense"]
    rec = before["accounts_receivable"] - now["accounts_receivable"]
    inv = before["inventory"] - now["inventory"]
    pay = before["accounts_payable"] - now["accounts_payable"]
    cfo = ni + dep + rec + inv + pay
    capex = -f["equipment"]
    borrow = -f["long_term_debt"]
    stock = -f["common_stock"]
    divs = -f["dividends"]
    cff = borrow + stock + divs
    beg = before["cash"]
    return {
        "net_income": ni,
        "depreciation": dep,
        "receivables": rec,
        "inventory": inv,
        "payables": pay,
        "cash_from_operations": cfo,
        "capital_expenditure": capex,
        "cash_from_investing": capex,
        "net_borrowing": borrow,
        "stock_issued": stock,
        "dividends_paid": divs,
        "cash_from_financing": cff,
        "net_change_in_cash": cfo + capex + cff,
        "beginning_cash": beg,
        "ending_cash": beg + cfo + capex + cff,
    }


def articulation_check(ledger: Any, period_end: Any) -> dict[str, int]:
    end = _end(period_end)
    now = balance_sheet(ledger, period_end)
    before = balance_sheet(ledger, _prev(end).isoformat())
    cf = cash_flow_statement(ledger, period_end)
    inc = income_statement(ledger, period_end)
    return {
        "balance_gap": now["total_assets"] - now["total_liabilities_and_equity"],
        "cash_gap": now["cash"] - cf["ending_cash"],
        "retained_earnings_gap": now["retained_earnings"] - before["retained_earnings"] - (inc["net_income"] + cf["dividends_paid"]),
        "depreciation_gap": now["accumulated_depreciation"] - before["accumulated_depreciation"] - inc["depreciation_expense"],
    }
