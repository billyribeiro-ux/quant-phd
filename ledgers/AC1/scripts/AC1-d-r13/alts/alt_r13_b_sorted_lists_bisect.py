"""Alternative r13 B: per-account sorted lists of (ISO date, signed cents), bisect cutoffs, flows as bisect windows."""

from __future__ import annotations

import bisect
import calendar
import re
from datetime import date, timedelta
from typing import Any

ACCOUNTS: dict[str, str] = {
    "cash": "asset", "accounts_receivable": "asset", "inventory": "asset", "equipment": "asset",
    "accumulated_depreciation": "contra_asset", "accounts_payable": "liability", "long_term_debt": "liability",
    "common_stock": "equity", "dividends": "distribution", "sales": "revenue", "cost_of_goods_sold": "expense",
    "operating_expenses": "expense", "depreciation_expense": "expense",
}
_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def _checked(value: object) -> str:
    if not isinstance(value, str) or _DATE.fullmatch(value) is None:
        raise ValueError("date")
    try:
        date.fromisoformat(value)
    except ValueError as error:
        raise ValueError("date") from error
    return value


def _cents(value: object) -> int:
    if type(value) is not int:
        raise ValueError("amount")
    if value < 0:
        raise ValueError("amount")
    return value


def _month_end(value: object) -> str:
    text = _checked(value)
    d = date.fromisoformat(text)
    if d.day != calendar.monthrange(d.year, d.month)[1]:
        raise ValueError("period end")
    return text


def _prev_iso(end: str) -> str:
    d = date.fromisoformat(end)
    return (d.replace(day=1) - timedelta(days=1)).isoformat()


def post(transactions: Any) -> dict[str, list[tuple[str, int]]]:
    book: dict[str, list[tuple[str, int]]] = {account: [] for account in ACCOUNTS}
    for entry in transactions:
        if not isinstance(entry, dict) or "date" not in entry or "lines" not in entry:
            raise ValueError("transaction")
        day = _checked(entry["date"])
        lines = entry["lines"]
        if isinstance(lines, str) or not isinstance(lines, (list, tuple)) or not lines:
            raise ValueError("lines")
        pending: list[tuple[str, int]] = []
        total = 0
        for line in lines:
            if not isinstance(line, dict) or not {"account", "debit", "credit"} <= line.keys():
                raise ValueError("line")
            name = line["account"]
            if not isinstance(name, str) or name not in ACCOUNTS:
                raise ValueError("account")
            d, c = _cents(line["debit"]), _cents(line["credit"])
            if (d == 0) == (c == 0):
                raise ValueError("debit or credit")
            pending.append((name, d - c))
            total += d - c
        if total != 0:
            raise ValueError("balance")
        for name, signed in pending:
            bisect.insort(book[name], (day, signed))
    return book  # type: ignore[return-value]


def _sum_upto(book: dict[str, list[tuple[str, int]]], account: str, end: str) -> int:
    rows = book[account]
    cut = bisect.bisect_right(rows, (end, float("inf")))  # type: ignore[arg-type]
    return sum(s for _, s in rows[:cut])


def _sum_window(book: dict[str, list[tuple[str, int]]], account: str, prev: str, end: str) -> int:
    rows = book[account]
    lo = bisect.bisect_right(rows, (prev, float("inf")))  # type: ignore[arg-type]
    hi = bisect.bisect_right(rows, (end, float("inf")))  # type: ignore[arg-type]
    return sum(s for _, s in rows[lo:hi])


def _bal(book: Any, end: str) -> dict[str, int]:
    return {a: _sum_upto(book, a, end) for a in ACCOUNTS}


def _win(book: Any, end: str) -> dict[str, int]:
    prev = _prev_iso(end)
    return {a: _sum_window(book, a, prev, end) for a in ACCOUNTS}


def balance_sheet(book: Any, period_end: str) -> dict[str, int]:
    end = _month_end(period_end)
    b = _bal(book, end)
    acc = -b["accumulated_depreciation"]
    neteq = b["equipment"] - acc
    ta = b["cash"] + b["accounts_receivable"] + b["inventory"] + neteq
    ap = -b["accounts_payable"]
    ltd = -b["long_term_debt"]
    tl = ap + ltd
    cs = -b["common_stock"]
    re_ = -(b["sales"] + b["cost_of_goods_sold"] + b["operating_expenses"] + b["depreciation_expense"]) - b["dividends"]
    te = cs + re_
    return {
        "cash": b["cash"], "accounts_receivable": b["accounts_receivable"], "inventory": b["inventory"],
        "equipment": b["equipment"], "accumulated_depreciation": acc, "net_equipment": neteq,
        "total_assets": ta, "accounts_payable": ap, "long_term_debt": ltd, "total_liabilities": tl,
        "common_stock": cs, "retained_earnings": re_, "total_equity": te, "total_liabilities_and_equity": tl + te,
    }


def income_statement(book: Any, period_end: str) -> dict[str, int]:
    end = _month_end(period_end)
    w = _win(book, end)
    sales = -w["sales"]
    cogs = w["cost_of_goods_sold"]
    gp = sales - cogs
    opex = w["operating_expenses"]
    dep = w["depreciation_expense"]
    return {"sales": sales, "cost_of_goods_sold": cogs, "gross_profit": gp, "operating_expenses": opex,
            "depreciation_expense": dep, "net_income": gp - opex - dep}


def cash_flow_statement(book: Any, period_end: str) -> dict[str, int]:
    end = _month_end(period_end)
    w = _win(book, end)
    beginning = _bal(book, _prev_iso(end))["cash"]
    ni = income_statement(book, end)["net_income"]
    dep = w["depreciation_expense"]
    rec = -w["accounts_receivable"]
    inv = -w["inventory"]
    pay = -w["accounts_payable"]
    ops = ni + dep + rec + inv + pay
    capex = -w["equipment"]
    fin = -w["long_term_debt"] + -w["common_stock"] + -w["dividends"]
    return {
        "net_income": ni, "depreciation": dep, "receivables": rec, "inventory": inv, "payables": pay,
        "cash_from_operations": ops, "capital_expenditure": capex, "cash_from_investing": capex,
        "net_borrowing": -w["long_term_debt"], "stock_issued": -w["common_stock"], "dividends_paid": -w["dividends"],
        "cash_from_financing": fin, "net_change_in_cash": ops + capex + fin, "beginning_cash": beginning,
        "ending_cash": beginning + ops + capex + fin,
    }


def articulation_check(book: Any, period_end: str) -> dict[str, int]:
    end = _month_end(period_end)
    now = balance_sheet(book, end)
    before = balance_sheet(book, _prev_iso(end))
    cf = cash_flow_statement(book, end)
    ni = income_statement(book, end)
    return {
        "balance_gap": now["total_assets"] - now["total_liabilities_and_equity"],
        "cash_gap": now["cash"] - cf["ending_cash"],
        "retained_earnings_gap": (now["retained_earnings"] - before["retained_earnings"]) - (ni["net_income"] + cf["dividends_paid"]),
        "depreciation_gap": (now["accumulated_depreciation"] - before["accumulated_depreciation"]) - ni["depreciation_expense"],
    }
