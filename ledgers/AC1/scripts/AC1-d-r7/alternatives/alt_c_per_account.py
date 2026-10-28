"""Alternative correct solution C: ledger is a dict of account -> sorted (date, signed) list; previous month end by date arithmetic."""

from __future__ import annotations

import datetime
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
Ledger = dict[str, list[tuple[str, int]]]
_KEYS = ("date", "lines")


def _date_text(value: Any) -> datetime.date:
    if type(value) is not str or len(value) != 10 or value[4] != "-" or value[7] != "-":
        raise ValueError("date must be written YYYY-MM-DD")
    if not (value[:4] + value[5:7] + value[8:]).isdigit():
        raise ValueError("date must be written YYYY-MM-DD")
    return datetime.date.fromisoformat(value)


def _money(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("amount must be an integer")
    if value < 0:
        raise ValueError("amount must not be negative")
    return value


def post(transactions: Sequence[Mapping[str, Any]]) -> Ledger:
    ledger: Ledger = {account: [] for account in ACCOUNTS}
    for transaction in transactions:
        for key in _KEYS:
            if key not in transaction:
                raise ValueError(f"transaction needs {key}")
        day = _date_text(transaction["date"]).isoformat()
        lines = transaction["lines"]
        if len(lines) == 0:
            raise ValueError("no lines")
        pending: list[tuple[str, int]] = []
        balance = 0
        for line in lines:
            if "account" not in line or "debit" not in line or "credit" not in line:
                raise ValueError("line is incomplete")
            if line["account"] not in ACCOUNTS:
                raise ValueError("account not in chart")
            d = _money(line["debit"])
            c = _money(line["credit"])
            if bool(d) is bool(c):
                raise ValueError("line must carry exactly one of debit and credit")
            balance += d - c
            pending.append((line["account"], d - c))
        if balance != 0:
            raise ValueError("entry does not balance")
        for account, signed in pending:
            ledger[account].append((day, signed))
    for account in ledger:
        ledger[account].sort()
    return ledger


def _end(period_end: Any) -> str:
    day = _date_text(period_end)
    if (day + datetime.timedelta(days=1)).day != 1:
        raise ValueError("period end must be a month end")
    return day.isoformat()


def _before(end: str) -> str:
    first = datetime.date.fromisoformat(end).replace(day=1)
    return (first - datetime.timedelta(days=1)).isoformat()


def _to(ledger: Ledger, end: str) -> dict[str, int]:
    return {a: sum(s for d, s in rows if d <= end) for a, rows in ledger.items()}


def _retained(b: dict[str, int]) -> int:
    income = -(b["sales"] + b["cost_of_goods_sold"] + b["operating_expenses"] + b["depreciation_expense"])
    return income - b["dividends"]


def balance_sheet(ledger: Ledger, period_end: str) -> dict[str, int]:
    end = _end(period_end)
    b = _to(ledger, end)
    acc_dep = -b["accumulated_depreciation"]
    equipment_net = b["equipment"] - acc_dep
    assets = b["cash"] + b["accounts_receivable"] + b["inventory"] + equipment_net
    liabilities = -b["accounts_payable"] - b["long_term_debt"]
    equity = -b["common_stock"] + _retained(b)
    return {
        "cash": b["cash"],
        "accounts_receivable": b["accounts_receivable"],
        "inventory": b["inventory"],
        "equipment": b["equipment"],
        "accumulated_depreciation": acc_dep,
        "net_equipment": equipment_net,
        "total_assets": assets,
        "accounts_payable": -b["accounts_payable"],
        "long_term_debt": -b["long_term_debt"],
        "total_liabilities": liabilities,
        "common_stock": -b["common_stock"],
        "retained_earnings": _retained(b),
        "total_equity": equity,
        "total_liabilities_and_equity": liabilities + equity,
    }


def _month_flow(ledger: Ledger, end: str) -> dict[str, int]:
    now, prev = _to(ledger, end), _to(ledger, _before(end))
    return {a: now[a] - prev[a] for a in ACCOUNTS}


def income_statement(ledger: Ledger, period_end: str) -> dict[str, int]:
    end = _end(period_end)
    f = _month_flow(ledger, end)
    sales = -f["sales"]
    gross = sales - f["cost_of_goods_sold"]
    return {
        "sales": sales,
        "cost_of_goods_sold": f["cost_of_goods_sold"],
        "gross_profit": gross,
        "operating_expenses": f["operating_expenses"],
        "depreciation_expense": f["depreciation_expense"],
        "net_income": gross - f["operating_expenses"] - f["depreciation_expense"],
    }


def cash_flow_statement(ledger: Ledger, period_end: str) -> dict[str, int]:
    end = _end(period_end)
    f = _month_flow(ledger, end)
    ni = income_statement(ledger, end)["net_income"]
    cfo = ni + f["depreciation_expense"] - f["accounts_receivable"] - f["inventory"] - f["accounts_payable"]
    capex = -f["equipment"]
    borrowing = -f["long_term_debt"]
    stock = -f["common_stock"]
    dividends = -f["dividends"]
    cff = borrowing + stock + dividends
    beginning = _to(ledger, _before(end))["cash"]
    return {
        "net_income": ni,
        "depreciation": f["depreciation_expense"],
        "receivables": -f["accounts_receivable"],
        "inventory": -f["inventory"],
        "payables": -f["accounts_payable"],
        "cash_from_operations": cfo,
        "capital_expenditure": capex,
        "cash_from_investing": capex,
        "net_borrowing": borrowing,
        "stock_issued": stock,
        "dividends_paid": dividends,
        "cash_from_financing": cff,
        "net_change_in_cash": cfo + capex + cff,
        "beginning_cash": beginning,
        "ending_cash": beginning + cfo + capex + cff,
    }


def articulation_check(ledger: Ledger, period_end: str) -> dict[str, int]:
    end = _end(period_end)
    bs, prev = balance_sheet(ledger, end), balance_sheet(ledger, _before(end))
    cf = cash_flow_statement(ledger, end)
    f = _month_flow(ledger, end)
    return {
        "balance_gap": bs["total_assets"] - bs["total_liabilities_and_equity"],
        "cash_gap": bs["cash"] - cf["ending_cash"],
        "retained_earnings_gap": bs["retained_earnings"] - prev["retained_earnings"] - cf["net_income"] - cf["dividends_paid"],
        "depreciation_gap": bs["accumulated_depreciation"] - prev["accumulated_depreciation"] - f["depreciation_expense"],
    }
