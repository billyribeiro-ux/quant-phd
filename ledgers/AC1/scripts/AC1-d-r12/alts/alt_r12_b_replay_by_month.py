"""Alternative B: ledger is a flat tuple of postings; statements replay postings with an exclusive next-day cutoff.

Dates use datetime.strptime. Amounts are checked with operator.index plus an explicit bool exclusion.
"""

from __future__ import annotations

import calendar
import operator
from collections.abc import Mapping, Sequence
from datetime import datetime, timedelta
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


def _day(value: Any) -> datetime:
    if not isinstance(value, str) or len(value) != 10 or value[4] != "-" or value[7] != "-":
        raise ValueError("bad date")
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError as error:
        raise ValueError("bad date") from error


def _cents(value: Any) -> int:
    if isinstance(value, bool):
        raise ValueError("bool is not an amount")
    try:
        n = operator.index(value)
    except TypeError as error:
        raise ValueError("amount must be an integer") from error
    if n < 0:
        raise ValueError("negative amount")
    return n


def post(transactions: Sequence[Mapping[str, Any]]) -> tuple[tuple[datetime, str, int], ...]:
    out: list[tuple[datetime, str, int]] = []
    for tx in transactions:
        if not isinstance(tx, Mapping) or "date" not in tx or "lines" not in tx:
            raise ValueError("transaction needs date and lines")
        when = _day(tx["date"])
        lines = tx["lines"]
        if isinstance(lines, (str, bytes)) or not isinstance(lines, Sequence) or len(lines) < 1:
            raise ValueError("no lines")
        staged: list[tuple[datetime, str, int]] = []
        for ln in lines:
            if not isinstance(ln, Mapping) or not {"account", "debit", "credit"} <= set(ln.keys()):
                raise ValueError("line shape")
            acct = ln["account"]
            if not isinstance(acct, str) or acct not in ACCOUNTS:
                raise ValueError("account outside chart")
            d, c = _cents(ln["debit"]), _cents(ln["credit"])
            if (d == 0) == (c == 0):
                raise ValueError("one side per line")
            staged.append((when, acct, d - c))
        if sum(x[2] for x in staged) != 0:
            raise ValueError("unbalanced")
        out.extend(staged)
    return tuple(out)


def _month_end(value: Any) -> datetime:
    d = _day(value)
    if d.day != calendar.monthrange(d.year, d.month)[1]:
        raise ValueError("not a month end")
    return d


def _through(ledger: Any, end: datetime) -> dict[str, int]:
    cutoff = end + timedelta(days=1)
    totals = dict.fromkeys(ACCOUNTS, 0)
    for when, acct, s in ledger:
        if when < cutoff:
            totals[acct] += s
    return totals


def _window(ledger: Any, end: datetime) -> dict[str, int]:
    now = _through(ledger, end)
    prior = _through(ledger, end.replace(day=1) - timedelta(days=1))
    return {a: now[a] - prior[a] for a in ACCOUNTS}


def balance_sheet(ledger: Any, period_end: str) -> dict[str, int]:
    end = _month_end(period_end)
    b = _through(ledger, end)
    acc = -b["accumulated_depreciation"]
    neteq = b["equipment"] - acc
    ta = b["cash"] + b["accounts_receivable"] + b["inventory"] + neteq
    ap = -b["accounts_payable"]
    ltd = -b["long_term_debt"]
    tl = ap + ltd
    cs = -b["common_stock"]
    earn = -(b["sales"] + b["cost_of_goods_sold"] + b["operating_expenses"] + b["depreciation_expense"])
    re_ = earn - b["dividends"]
    te = cs + re_
    return {
        "cash": b["cash"],
        "accounts_receivable": b["accounts_receivable"],
        "inventory": b["inventory"],
        "equipment": b["equipment"],
        "accumulated_depreciation": acc,
        "net_equipment": neteq,
        "total_assets": ta,
        "accounts_payable": ap,
        "long_term_debt": ltd,
        "total_liabilities": tl,
        "common_stock": cs,
        "retained_earnings": re_,
        "total_equity": te,
        "total_liabilities_and_equity": tl + te,
    }


def income_statement(ledger: Any, period_end: str) -> dict[str, int]:
    w = _window(ledger, _month_end(period_end))
    sales = -w["sales"]
    cogs = w["cost_of_goods_sold"]
    gross = sales - cogs
    ox = w["operating_expenses"]
    dep = w["depreciation_expense"]
    return {
        "sales": sales,
        "cost_of_goods_sold": cogs,
        "gross_profit": gross,
        "operating_expenses": ox,
        "depreciation_expense": dep,
        "net_income": gross - ox - dep,
    }


def cash_flow_statement(ledger: Any, period_end: str) -> dict[str, int]:
    end = _month_end(period_end)
    w = _window(ledger, end)
    prior = _through(ledger, end.replace(day=1) - timedelta(days=1))
    ni = income_statement(ledger, period_end)["net_income"]
    dep = w["depreciation_expense"]
    rec = -w["accounts_receivable"]
    inv = -w["inventory"]
    pay = -w["accounts_payable"]
    ops = ni + dep + rec + inv + pay
    capex = -w["equipment"]
    borrow = -w["long_term_debt"]
    stock = -w["common_stock"]
    divs = -w["dividends"]
    fin = borrow + stock + divs
    begin = prior["cash"]
    return {
        "net_income": ni,
        "depreciation": dep,
        "receivables": rec,
        "inventory": inv,
        "payables": pay,
        "cash_from_operations": ops,
        "capital_expenditure": capex,
        "cash_from_investing": capex,
        "net_borrowing": borrow,
        "stock_issued": stock,
        "dividends_paid": divs,
        "cash_from_financing": fin,
        "net_change_in_cash": ops + capex + fin,
        "beginning_cash": begin,
        "ending_cash": begin + ops + capex + fin,
    }


def articulation_check(ledger: Any, period_end: str) -> dict[str, int]:
    end = _month_end(period_end)
    bs = balance_sheet(ledger, period_end)
    prev_bs = balance_sheet(ledger, (end.replace(day=1) - timedelta(days=1)).strftime("%Y-%m-%d"))
    cf = cash_flow_statement(ledger, period_end)
    inc = income_statement(ledger, period_end)
    re_gap = bs["retained_earnings"] - prev_bs["retained_earnings"] - (inc["net_income"] + cf["dividends_paid"])
    dep_gap = bs["accumulated_depreciation"] - prev_bs["accumulated_depreciation"] - inc["depreciation_expense"]
    return {
        "balance_gap": bs["total_assets"] - bs["total_liabilities_and_equity"],
        "cash_gap": bs["cash"] - cf["ending_cash"],
        "retained_earnings_gap": re_gap,
        "depreciation_gap": dep_gap,
    }
