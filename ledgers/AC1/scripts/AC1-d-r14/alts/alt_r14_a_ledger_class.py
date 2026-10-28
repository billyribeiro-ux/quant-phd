"""Round-14 alternative A: ledger is a class wrapping a list; string-compare cutoffs; regex date check."""
from __future__ import annotations

import calendar
import re
from datetime import date, timedelta
from typing import Any

ACCOUNTS = {
    "cash": "asset", "accounts_receivable": "asset", "inventory": "asset", "equipment": "asset",
    "accumulated_depreciation": "contra_asset", "accounts_payable": "liability", "long_term_debt": "liability",
    "common_stock": "equity", "dividends": "distribution", "sales": "revenue", "cost_of_goods_sold": "expense",
    "operating_expenses": "expense", "depreciation_expense": "expense",
}
_DATE = re.compile(r"\A(\d{4})-(\d{2})-(\d{2})\Z")
_MSG = "a date must be an ISO date, YYYY-MM-DD"


class Ledger:
    __slots__ = ("rows",)

    def __init__(self, rows: list[tuple[str, str, int]]) -> None:
        self.rows = tuple(rows)


def _day(value: object) -> str:
    if type(value) is not str:
        raise ValueError(_MSG)
    m = _DATE.match(value)
    if not m:
        raise ValueError(_MSG)
    try:
        date(int(m[1]), int(m[2]), int(m[3]))
    except ValueError as exc:
        raise ValueError(_MSG) from exc
    return value


def _amount(value: object) -> int:
    if type(value) is not int and not (isinstance(value, int) and not isinstance(value, bool)):
        raise ValueError("an amount must be an integer number of cents")
    if value < 0:
        raise ValueError("an amount must not be negative")
    return value


def _month_end(value: object) -> str:
    text = _day(value)
    d = date.fromisoformat(text)
    if d.day != calendar.monthrange(d.year, d.month)[1]:
        raise ValueError("a period end must be the last day of a calendar month")
    return text


def _prev(end: str) -> str:
    d = date.fromisoformat(end)
    return (d.replace(day=1) - timedelta(days=1)).isoformat()


def post(transactions: Any) -> Ledger:
    rows: list[tuple[str, str, int]] = []
    for t in transactions:
        if not isinstance(t, dict) or "date" not in t or "lines" not in t:
            raise ValueError("a transaction needs a date and its lines")
        day = _day(t["date"])
        lines = t["lines"]
        if isinstance(lines, str) or not hasattr(lines, "__len__") or len(lines) == 0:
            raise ValueError("a transaction needs at least one line")
        net = 0
        for ln in lines:
            if not isinstance(ln, dict) or not all(k in ln for k in ("account", "debit", "credit")):
                raise ValueError("a line needs an account, a debit and a credit")
            acct = ln["account"]
            if acct not in ACCOUNTS:
                raise ValueError("an unknown account is not in the chart of accounts")
            dr, cr = _amount(ln["debit"]), _amount(ln["credit"])
            if (dr > 0) == (cr > 0):
                raise ValueError("a line carries a debit or a credit, and exactly one")
            rows.append((day, acct, dr - cr))
            net += dr - cr
        if net:
            raise ValueError("unbalanced entry: the debits must equal the credits")
    return Ledger(rows)


def _bal(ledger: Ledger, end: str) -> dict[str, int]:
    out = {k: 0 for k in ACCOUNTS}
    for day, acct, s in ledger.rows:
        if day <= end:
            out[acct] += s
    return out


def balance_sheet(ledger: Ledger, period_end: str) -> dict[str, int]:
    end = _month_end(period_end)
    b = _bal(ledger, end)
    acc = -b["accumulated_depreciation"]
    net_eq = b["equipment"] - acc
    ta = b["cash"] + b["accounts_receivable"] + b["inventory"] + net_eq
    pay = -b["accounts_payable"]
    debt = -b["long_term_debt"]
    tl = pay + debt
    com = -b["common_stock"]
    inc = -(b["sales"] + b["cost_of_goods_sold"] + b["operating_expenses"] + b["depreciation_expense"])
    re_ = inc - b["dividends"]
    te = com + re_
    return {
        "cash": b["cash"], "accounts_receivable": b["accounts_receivable"], "inventory": b["inventory"],
        "equipment": b["equipment"], "accumulated_depreciation": acc, "net_equipment": net_eq,
        "total_assets": ta, "accounts_payable": pay, "long_term_debt": debt, "total_liabilities": tl,
        "common_stock": com, "retained_earnings": re_, "total_equity": te,
        "total_liabilities_and_equity": tl + te,
    }


def _flow(ledger: Ledger, end: str) -> tuple[dict[str, int], dict[str, int], dict[str, int]]:
    prev = _prev(end)
    now, before = _bal(ledger, end), _bal(ledger, prev)
    return now, before, {k: now[k] - before[k] for k in ACCOUNTS}


def income_statement(ledger: Ledger, period_end: str) -> dict[str, int]:
    _, _, f = _flow(ledger, _month_end(period_end))
    sales = -f["sales"]
    cogs = f["cost_of_goods_sold"]
    gp = sales - cogs
    opx = f["operating_expenses"]
    dep = f["depreciation_expense"]
    return {"sales": sales, "cost_of_goods_sold": cogs, "gross_profit": gp, "operating_expenses": opx,
            "depreciation_expense": dep, "net_income": gp - opx - dep}


def cash_flow_statement(ledger: Ledger, period_end: str) -> dict[str, int]:
    end = _month_end(period_end)
    now, before, f = _flow(ledger, end)
    ni = income_statement(ledger, end)["net_income"]
    dep = f["depreciation_expense"]
    ar = -f["accounts_receivable"]
    inv = -f["inventory"]
    ap = -f["accounts_payable"]
    ops = ni + dep + ar + inv + ap
    capex = -f["equipment"]
    borrow = -f["long_term_debt"]
    stock = -f["common_stock"]
    divs = -f["dividends"]
    fin = borrow + stock + divs
    begin = before["cash"]
    return {"net_income": ni, "depreciation": dep, "receivables": ar, "inventory": inv, "payables": ap,
            "cash_from_operations": ops, "capital_expenditure": capex, "cash_from_investing": capex,
            "net_borrowing": borrow, "stock_issued": stock, "dividends_paid": divs,
            "cash_from_financing": fin, "net_change_in_cash": ops + capex + fin, "beginning_cash": begin,
            "ending_cash": begin + ops + capex + fin}


def articulation_check(ledger: Ledger, period_end: str) -> dict[str, int]:
    end = _month_end(period_end)
    prev = _prev(end)
    now, before = balance_sheet(ledger, end), balance_sheet(ledger, prev)
    cf = cash_flow_statement(ledger, end)
    ni = income_statement(ledger, end)["net_income"]
    dep = income_statement(ledger, end)["depreciation_expense"]
    return {
        "balance_gap": now["total_assets"] - now["total_liabilities_and_equity"],
        "cash_gap": now["cash"] - cf["ending_cash"],
        "retained_earnings_gap": (now["retained_earnings"] - before["retained_earnings"]) - (ni + cf["dividends_paid"]),
        "depreciation_gap": (now["accumulated_depreciation"] - before["accumulated_depreciation"]) - dep,
    }
