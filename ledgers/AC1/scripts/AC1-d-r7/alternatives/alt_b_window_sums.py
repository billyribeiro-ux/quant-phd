"""Alternative correct solution B: ledger is a list of signed postings; flows are direct sums over the month window."""

from __future__ import annotations

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
ISO = re.compile(r"(\d{4})-(\d{2})-(\d{2})")


class Ledger:
    """Opaque to callers: a list of (date, account, signed cents)."""

    def __init__(self, postings: list[tuple[str, str, int]]) -> None:
        self.postings = postings


def _date(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("a date is a string")
    match = ISO.fullmatch(value)
    if match is None:
        raise ValueError("a date is YYYY-MM-DD")
    datetime.date(*(int(g) for g in match.groups()))  # ValueError for a day that does not exist
    return value


def _cents(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("an amount is an integer number of cents")
    if value < 0:
        raise ValueError("an amount is never negative")
    return value


def post(transactions: Sequence[Mapping[str, Any]]) -> Ledger:
    out: list[tuple[str, str, int]] = []
    for entry in transactions:
        if "date" not in entry:
            raise ValueError("a transaction has a date")
        date = _date(entry["date"])
        if "lines" not in entry or not entry["lines"]:
            raise ValueError("a transaction has lines")
        staged: list[tuple[str, str, int]] = []
        net = 0
        for line in entry["lines"]:
            for key in ("account", "debit", "credit"):
                if key not in line:
                    raise ValueError(f"a line has a {key}")
            if line["account"] not in ACCOUNTS:
                raise ValueError("an account is in the chart")
            debit, credit = _cents(line["debit"]), _cents(line["credit"])
            if (debit == 0) == (credit == 0):
                raise ValueError("a line has exactly one of a debit and a credit")
            net += debit - credit
            staged.append((date, line["account"], debit - credit))
        if net:
            raise ValueError("debits must equal credits")
        out.extend(staged)
    return Ledger(out)


def _end(period_end: Any) -> str:
    text = _date(period_end)
    y, m, d = (int(x) for x in text.split("-"))
    if d != calendar.monthrange(y, m)[1]:
        raise ValueError("period end is a month end")
    return text


def _prev(end: str) -> str:
    y, m = int(end[:4]), int(end[5:7]) - 1
    if m == 0:
        y, m = y - 1, 12
    return "%04d-%02d-%02d" % (y, m, calendar.monthrange(y, m)[1])


def _sum(ledger: Ledger, lo: str | None, hi: str) -> dict[str, int]:
    """Signed totals of postings with lo < date <= hi (lo None means from the beginning)."""
    out = dict.fromkeys(ACCOUNTS, 0)
    for date, account, signed in ledger.postings:
        if date <= hi and (lo is None or date > lo):
            out[account] += signed
    return out


def _balance(ledger: Ledger, end: str) -> dict[str, int]:
    return _sum(ledger, None, end)


def _month(ledger: Ledger, end: str) -> dict[str, int]:
    return _sum(ledger, _prev(end), end)


def balance_sheet(ledger: Ledger, period_end: str) -> dict[str, int]:
    end = _end(period_end)
    b = _balance(ledger, end)
    net_equipment = b["equipment"] - (-b["accumulated_depreciation"])
    total_assets = b["cash"] + b["accounts_receivable"] + b["inventory"] + net_equipment
    total_liabilities = -b["accounts_payable"] - b["long_term_debt"]
    retained = -(b["sales"] + b["cost_of_goods_sold"] + b["operating_expenses"] + b["depreciation_expense"]) - b["dividends"]
    total_equity = -b["common_stock"] + retained
    return {
        "cash": b["cash"],
        "accounts_receivable": b["accounts_receivable"],
        "inventory": b["inventory"],
        "equipment": b["equipment"],
        "accumulated_depreciation": -b["accumulated_depreciation"],
        "net_equipment": net_equipment,
        "total_assets": total_assets,
        "accounts_payable": -b["accounts_payable"],
        "long_term_debt": -b["long_term_debt"],
        "total_liabilities": total_liabilities,
        "common_stock": -b["common_stock"],
        "retained_earnings": retained,
        "total_equity": total_equity,
        "total_liabilities_and_equity": total_liabilities + total_equity,
    }


def income_statement(ledger: Ledger, period_end: str) -> dict[str, int]:
    end = _end(period_end)
    m = _month(ledger, end)
    sales = -m["sales"]
    gross = sales - m["cost_of_goods_sold"]
    return {
        "sales": sales,
        "cost_of_goods_sold": m["cost_of_goods_sold"],
        "gross_profit": gross,
        "operating_expenses": m["operating_expenses"],
        "depreciation_expense": m["depreciation_expense"],
        "net_income": gross - m["operating_expenses"] - m["depreciation_expense"],
    }


def cash_flow_statement(ledger: Ledger, period_end: str) -> dict[str, int]:
    end = _end(period_end)
    m = _month(ledger, end)
    ni = income_statement(ledger, end)["net_income"]
    receivables = -m["accounts_receivable"]
    inventory = -m["inventory"]
    payables = -m["accounts_payable"]
    cfo = ni + m["depreciation_expense"] + receivables + inventory + payables
    capex = -m["equipment"]
    borrowing = -m["long_term_debt"]
    stock = -m["common_stock"]
    dividends_paid = -m["dividends"]
    cff = borrowing + stock + dividends_paid
    beginning = _balance(ledger, _prev(end))["cash"]
    return {
        "net_income": ni,
        "depreciation": m["depreciation_expense"],
        "receivables": receivables,
        "inventory": inventory,
        "payables": payables,
        "cash_from_operations": cfo,
        "capital_expenditure": capex,
        "cash_from_investing": capex,
        "net_borrowing": borrowing,
        "stock_issued": stock,
        "dividends_paid": dividends_paid,
        "cash_from_financing": cff,
        "net_change_in_cash": cfo + capex + cff,
        "beginning_cash": beginning,
        "ending_cash": beginning + cfo + capex + cff,
    }


def articulation_check(ledger: Ledger, period_end: str) -> dict[str, int]:
    end = _end(period_end)
    bs = balance_sheet(ledger, end)
    prev_bs = balance_sheet(ledger, _prev(end))
    cf = cash_flow_statement(ledger, end)
    m = _month(ledger, end)
    return {
        "balance_gap": bs["total_assets"] - bs["total_liabilities_and_equity"],
        "cash_gap": bs["cash"] - cf["ending_cash"],
        "retained_earnings_gap": bs["retained_earnings"] - prev_bs["retained_earnings"] - (cf["net_income"] + cf["dividends_paid"]),
        "depreciation_gap": bs["accumulated_depreciation"] - prev_bs["accumulated_depreciation"] - m["depreciation_expense"],
    }
