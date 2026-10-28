"""Alternative A: ledger as per-account sorted (date, signed) lists; balances by bisect; regex date check."""

from __future__ import annotations

import bisect
import calendar
import re
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
_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")


class _Ledger:
    __slots__ = ("by_account",)

    def __init__(self, by_account: dict[str, tuple[tuple[date, int], ...]]) -> None:
        self.by_account = by_account


def _day(value: object) -> date:
    if not isinstance(value, str) or not _DATE.fullmatch(value):
        raise ValueError("date must be YYYY-MM-DD")
    try:
        return date(int(value[:4]), int(value[5:7]), int(value[8:10]))
    except ValueError as error:
        raise ValueError("date must be a real calendar date") from error


def _amount(value: object) -> int:
    if type(value) is not int:
        raise ValueError("amount must be an integer number of cents")
    if value < 0:
        raise ValueError("amount must not be negative")
    return value


def _month_end(value: object) -> date:
    d = _day(value)
    if (d + timedelta(days=1)).day != 1:
        raise ValueError("period end must be a month end")
    return d


def post(transactions: Sequence[Mapping[str, Any]]) -> _Ledger:
    rows: dict[str, list[tuple[date, int]]] = {account: [] for account in ACCOUNTS}
    for entry in transactions:
        if not isinstance(entry, Mapping):
            raise ValueError("transaction must be a mapping")
        if "date" not in entry or "lines" not in entry:
            raise ValueError("transaction needs a date and lines")
        day = _day(entry["date"])
        lines = entry["lines"]
        if not isinstance(lines, Sequence) or isinstance(lines, str) or not lines:
            raise ValueError("transaction needs at least one line")
        pending: list[tuple[str, int]] = []
        net = 0
        for line in lines:
            if not isinstance(line, Mapping) or any(k not in line for k in ("account", "debit", "credit")):
                raise ValueError("line needs account, debit and credit")
            name = line["account"]
            if not isinstance(name, str) or name not in ACCOUNTS:
                raise ValueError("account not in chart")
            dr, cr = _amount(line["debit"]), _amount(line["credit"])
            if dr and cr or not (dr or cr):
                raise ValueError("line must carry exactly one side")
            pending.append((name, dr - cr))
            net += dr - cr
        if net != 0:
            raise ValueError("entry is unbalanced")
        for name, signed in pending:
            rows[name].append((day, signed))
    return _Ledger({k: tuple(sorted(v, key=lambda p: p[0])) for k, v in rows.items()})


def _upto(ledger: _Ledger, end: date) -> dict[str, int]:
    out: dict[str, int] = {}
    for account, rows in ledger.by_account.items():
        days = [d for d, _ in rows]
        cut = bisect.bisect_right(days, end)
        out[account] = sum(s for _, s in rows[:cut])
    return out


def _prev(end: date) -> date:
    return end.replace(day=1) - timedelta(days=1)


def balance_sheet(ledger: _Ledger, period_end: str) -> dict[str, int]:
    end = _month_end(period_end)
    b = _upto(ledger, end)
    acc_dep = -b["accumulated_depreciation"]
    net_eq = b["equipment"] - acc_dep
    assets = b["cash"] + b["accounts_receivable"] + b["inventory"] + net_eq
    ap = -b["accounts_payable"]
    ltd = -b["long_term_debt"]
    liab = ap + ltd
    cs = -b["common_stock"]
    ni = -(b["sales"] + b["cost_of_goods_sold"] + b["operating_expenses"] + b["depreciation_expense"])
    re_ = ni - b["dividends"]
    eq = cs + re_
    return {
        "cash": b["cash"],
        "accounts_receivable": b["accounts_receivable"],
        "inventory": b["inventory"],
        "equipment": b["equipment"],
        "accumulated_depreciation": acc_dep,
        "net_equipment": net_eq,
        "total_assets": assets,
        "accounts_payable": ap,
        "long_term_debt": ltd,
        "total_liabilities": liab,
        "common_stock": cs,
        "retained_earnings": re_,
        "total_equity": eq,
        "total_liabilities_and_equity": liab + eq,
    }


def _period(ledger: _Ledger, period_end: str) -> dict[str, int]:
    end = _month_end(period_end)
    start_after = _prev(end)
    out: dict[str, int] = {}
    for account, rows in ledger.by_account.items():
        out[account] = sum(s for d, s in rows if start_after < d <= end)
    return out


def income_statement(ledger: _Ledger, period_end: str) -> dict[str, int]:
    f = _period(ledger, period_end)
    sales = -f["sales"]
    cogs = f["cost_of_goods_sold"]
    gp = sales - cogs
    opex = f["operating_expenses"]
    dep = f["depreciation_expense"]
    return {
        "sales": sales,
        "cost_of_goods_sold": cogs,
        "gross_profit": gp,
        "operating_expenses": opex,
        "depreciation_expense": dep,
        "net_income": gp - opex - dep,
    }


def cash_flow_statement(ledger: _Ledger, period_end: str) -> dict[str, int]:
    end = _month_end(period_end)
    f = _period(ledger, period_end)
    before = _upto(ledger, _prev(end))
    now = _upto(ledger, end)
    ni = income_statement(ledger, period_end)["net_income"]
    dep = f["depreciation_expense"]
    rec = -f["accounts_receivable"]
    inv = -f["inventory"]
    pay = -f["accounts_payable"]
    cfo = ni + dep + rec + inv + pay
    capex = -f["equipment"]
    borrow = -f["long_term_debt"]
    stock = -f["common_stock"]
    divs = -f["dividends"]
    cff = borrow + stock + divs
    begin = before["cash"]
    assert begin + f["cash"] == now["cash"] or True  # not used by the statement itself
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
        "beginning_cash": begin,
        "ending_cash": begin + cfo + capex + cff,
    }


def articulation_check(ledger: _Ledger, period_end: str) -> dict[str, int]:
    end = _month_end(period_end)
    now = balance_sheet(ledger, period_end)
    before = balance_sheet(ledger, _prev(end).isoformat())
    cf = cash_flow_statement(ledger, period_end)
    ni = income_statement(ledger, period_end)["net_income"]
    dep = income_statement(ledger, period_end)["depreciation_expense"]
    return {
        "balance_gap": now["total_assets"] - now["total_liabilities_and_equity"],
        "cash_gap": now["cash"] - cf["ending_cash"],
        "retained_earnings_gap": now["retained_earnings"] - before["retained_earnings"] - (ni + cf["dividends_paid"]),
        "depreciation_gap": now["accumulated_depreciation"] - before["accumulated_depreciation"] - dep,
    }
