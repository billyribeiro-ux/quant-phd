"""Alternative C: ledger is a frozen dataclass of entries; dates compared as ISO strings; flows from Counter diffs."""

from __future__ import annotations

import calendar
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date
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


@dataclass(frozen=True)
class Ledger:
    entries: tuple[tuple[str, tuple[tuple[str, int], ...]], ...]


def _iso(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("date must be a string")
    if len(value) != 10 or value[4] != "-" or value[7] != "-" or not value.replace("-", "").isdigit():
        raise ValueError("date must be YYYY-MM-DD")
    try:
        date.fromisoformat(value)
    except ValueError as error:
        raise ValueError("not a real date") from error
    return value


def _money(value: Any) -> int:
    if type(value) is bool or not isinstance(value, int):
        raise ValueError("amount must be integer cents")
    if value < 0:
        raise ValueError("negative amount")
    return value


def post(transactions: Sequence[Mapping[str, Any]]) -> Ledger:
    entries = []
    for tx in transactions:
        if not isinstance(tx, Mapping) or "date" not in tx or "lines" not in tx:
            raise ValueError("transaction needs date and lines")
        day = _iso(tx["date"])
        lines = tx["lines"]
        if not isinstance(lines, (list, tuple)) or not lines:
            raise ValueError("needs lines")
        parts = []
        total = 0
        for ln in lines:
            if not isinstance(ln, Mapping):
                raise ValueError("line must be a mapping")
            for key in ("account", "debit", "credit"):
                if key not in ln:
                    raise ValueError("line incomplete")
            acct = ln["account"]
            if acct not in ACCOUNTS:
                raise ValueError("unknown account")
            dr = _money(ln["debit"])
            cr = _money(ln["credit"])
            if (dr > 0 and cr > 0) or (dr == 0 and cr == 0):
                raise ValueError("exactly one side")
            parts.append((acct, dr - cr))
            total += dr - cr
        if total:
            raise ValueError("unbalanced")
        entries.append((day, tuple(parts)))
    return Ledger(tuple(entries))


def _month_end(value: Any) -> str:
    text = _iso(value)
    d = date.fromisoformat(text)
    if d.day != calendar.monthrange(d.year, d.month)[1]:
        raise ValueError("not a month end")
    return text


def _prior_month_end(text: str) -> str:
    d = date.fromisoformat(text)
    return date(d.year, d.month, 1).fromordinal(date(d.year, d.month, 1).toordinal() - 1).isoformat()


def _cum(ledger: Ledger, end: str) -> Counter[str]:
    c: Counter[str] = Counter({a: 0 for a in ACCOUNTS})
    for day, parts in ledger.entries:
        if day <= end:
            for acct, s in parts:
                c[acct] += s
    return c


def _diff(ledger: Ledger, end: str) -> dict[str, int]:
    prior = _prior_month_end(end)
    now, before = _cum(ledger, end), _cum(ledger, prior)
    return {a: now[a] - before[a] for a in ACCOUNTS}


def balance_sheet(ledger: Ledger, period_end: str) -> dict[str, int]:
    end = _month_end(period_end)
    c = _cum(ledger, end)
    acc = -c["accumulated_depreciation"]
    net = c["equipment"] - acc
    assets = c["cash"] + c["accounts_receivable"] + c["inventory"] + net
    ap = -c["accounts_payable"]
    debt = -c["long_term_debt"]
    liab = ap + debt
    stock = -c["common_stock"]
    profit = -(c["sales"] + c["cost_of_goods_sold"] + c["operating_expenses"] + c["depreciation_expense"])
    retained = profit - c["dividends"]
    equity = stock + retained
    return {
        "cash": c["cash"],
        "accounts_receivable": c["accounts_receivable"],
        "inventory": c["inventory"],
        "equipment": c["equipment"],
        "accumulated_depreciation": acc,
        "net_equipment": net,
        "total_assets": assets,
        "accounts_payable": ap,
        "long_term_debt": debt,
        "total_liabilities": liab,
        "common_stock": stock,
        "retained_earnings": retained,
        "total_equity": equity,
        "total_liabilities_and_equity": liab + equity,
    }


def income_statement(ledger: Ledger, period_end: str) -> dict[str, int]:
    f = _diff(ledger, _month_end(period_end))
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


def cash_flow_statement(ledger: Ledger, period_end: str) -> dict[str, int]:
    end = _month_end(period_end)
    f = _diff(ledger, end)
    begin = _cum(ledger, _prior_month_end(end))["cash"]
    ni = income_statement(ledger, end)["net_income"]
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


def articulation_check(ledger: Ledger, period_end: str) -> dict[str, int]:
    end = _month_end(period_end)
    now = balance_sheet(ledger, end)
    before = balance_sheet(ledger, _prior_month_end(end))
    cf = cash_flow_statement(ledger, end)
    inc = income_statement(ledger, end)
    return {
        "balance_gap": now["total_assets"] - now["total_liabilities_and_equity"],
        "cash_gap": now["cash"] - cf["ending_cash"],
        "retained_earnings_gap": now["retained_earnings"] - before["retained_earnings"] - (inc["net_income"] + cf["dividends_paid"]),
        "depreciation_gap": now["accumulated_depreciation"] - before["accumulated_depreciation"] - inc["depreciation_expense"],
    }
