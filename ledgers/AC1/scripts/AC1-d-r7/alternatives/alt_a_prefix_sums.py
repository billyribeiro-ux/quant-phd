"""Alternative correct solution A: ledger is (sorted dates, postings in date order); balances use bisect prefix cutoffs."""

from __future__ import annotations

import bisect
import calendar
import datetime
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
_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
Ledger = tuple[tuple[str, ...], tuple[tuple[str, int], ...]]


def _iso_date(value: Any) -> str:
    if not isinstance(value, str) or _DATE.fullmatch(value) is None:
        raise ValueError("date must be YYYY-MM-DD")
    datetime.date.fromisoformat(value)  # raises ValueError for 2024-02-30
    return value


def _amount(value: Any) -> int:
    if type(value) is not int:
        raise ValueError("amount must be an integer number of cents")
    if value < 0:
        raise ValueError("amount must not be negative")
    return value


def post(transactions: Sequence[Mapping[str, Any]]) -> Ledger:
    dated: list[tuple[str, str, int]] = []
    if not isinstance(transactions, Sequence):
        raise ValueError("transactions must be a list")
    for txn in transactions:
        if not isinstance(txn, Mapping) or "date" not in txn or "lines" not in txn:
            raise ValueError("a transaction needs a date and lines")
        date = _iso_date(txn["date"])
        lines = txn["lines"]
        if not isinstance(lines, Sequence) or len(lines) == 0:
            raise ValueError("a transaction needs at least one line")
        total = 0
        rows = []
        for line in lines:
            if not isinstance(line, Mapping) or "account" not in line or "debit" not in line or "credit" not in line:
                raise ValueError("a line needs an account, a debit and a credit")
            account = line["account"]
            if account not in ACCOUNTS:
                raise ValueError("account is outside the chart")
            d, c = _amount(line["debit"]), _amount(line["credit"])
            if (d > 0) == (c > 0):
                raise ValueError("a line carries a debit or a credit, and exactly one")
            total += d - c
            rows.append((date, account, d - c))
        if total != 0:
            raise ValueError("unbalanced entry")
        dated.extend(rows)
    dated.sort(key=lambda row: row[0])  # stable: keeps entry order within a date
    dates = tuple(row[0] for row in dated)
    return (dates, tuple((row[1], row[2]) for row in dated))


def _month_end(period_end: Any) -> str:
    text = _iso_date(period_end)
    year, month, day = int(text[:4]), int(text[5:7]), int(text[8:])
    if day != calendar.monthrange(year, month)[1]:
        raise ValueError("period end must be a month end")
    return text


def _previous_end(period_end: str) -> str:
    year, month = int(period_end[:4]), int(period_end[5:7])
    year, month = (year - 1, 12) if month == 1 else (year, month - 1)
    return f"{year:04d}-{month:02d}-{calendar.monthrange(year, month)[1]:02d}"


def _through(ledger: Ledger, end: str) -> dict[str, int]:
    dates, postings = ledger
    cut = bisect.bisect_right(dates, end)
    out = dict.fromkeys(ACCOUNTS, 0)
    for account, signed in postings[:cut]:
        out[account] += signed
    return out


def _flows(ledger: Ledger, end: str) -> dict[str, int]:
    now, before = _through(ledger, end), _through(ledger, _previous_end(end))
    return {a: now[a] - before[a] for a in ACCOUNTS}


def balance_sheet(ledger: Ledger, period_end: str) -> dict[str, int]:
    end = _month_end(period_end)
    b = _through(ledger, end)
    acc = -b["accumulated_depreciation"]
    net_eq = b["equipment"] - acc
    assets = b["cash"] + b["accounts_receivable"] + b["inventory"] + net_eq
    ap, ltd, cs = -b["accounts_payable"], -b["long_term_debt"], -b["common_stock"]
    retained = -(b["sales"] + b["cost_of_goods_sold"] + b["operating_expenses"] + b["depreciation_expense"]) - b["dividends"]
    liab = ap + ltd
    equity = cs + retained
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
        "common_stock": cs,
        "retained_earnings": retained,
        "total_equity": equity,
        "total_liabilities_and_equity": liab + equity,
    }


def income_statement(ledger: Ledger, period_end: str) -> dict[str, int]:
    end = _month_end(period_end)
    f = _flows(ledger, end)
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
    end = _month_end(period_end)
    f = _flows(ledger, end)
    ni = income_statement(ledger, end)["net_income"]
    dep = f["depreciation_expense"]
    rec, inv, pay = -f["accounts_receivable"], -f["inventory"], -f["accounts_payable"]
    cfo = ni + dep + rec + inv + pay
    capex = -f["equipment"]
    borrow, stock, divs = -f["long_term_debt"], -f["common_stock"], -f["dividends"]
    cff = borrow + stock + divs
    beginning = _through(ledger, _previous_end(end))["cash"]
    ending = beginning + cfo + capex + cff
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
        "beginning_cash": beginning,
        "ending_cash": ending,
    }


def articulation_check(ledger: Ledger, period_end: str) -> dict[str, int]:
    end = _month_end(period_end)
    bs = balance_sheet(ledger, end)
    cf = cash_flow_statement(ledger, end)
    bal_before = _through(ledger, _previous_end(end))
    f = _flows(ledger, end)
    balance_gap = bs["total_assets"] - bs["total_liabilities_and_equity"]
    cash_gap = bs["cash"] - cf["ending_cash"]
    re_now = bs["retained_earnings"]
    re_before = balance_sheet(ledger, _previous_end(end))["retained_earnings"]
    retained_gap = (re_now - re_before) - (cf["net_income"] + cf["dividends_paid"])
    ad_before = -bal_before["accumulated_depreciation"]
    ad_now = -_through(ledger, end)["accumulated_depreciation"]
    depreciation_gap = (ad_now - ad_before) - f["depreciation_expense"]
    return {
        "balance_gap": balance_gap,
        "cash_gap": cash_gap,
        "retained_earnings_gap": retained_gap,
        "depreciation_gap": depreciation_gap,
    }
