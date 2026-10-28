"""Alternative r13 A: date objects in the ledger, windowed flows (prev < day <= end) instead of balance differences."""

from __future__ import annotations

import calendar
from datetime import date, timedelta
from numbers import Integral
from typing import Any

ACCOUNTS: dict[str, str] = {
    "cash": "asset", "accounts_receivable": "asset", "inventory": "asset", "equipment": "asset",
    "accumulated_depreciation": "contra_asset", "accounts_payable": "liability", "long_term_debt": "liability",
    "common_stock": "equity", "dividends": "distribution", "sales": "revenue", "cost_of_goods_sold": "expense",
    "operating_expenses": "expense", "depreciation_expense": "expense",
}

Ledger = tuple[tuple[date, str, int], ...]


def _day(value: object) -> date:
    if not isinstance(value, str) or len(value) != 10 or value[4] != "-" or value[7] != "-":
        raise ValueError("date")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as error:
        raise ValueError("date") from error
    return parsed


def _amount(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, Integral):
        raise ValueError("amount")
    if int(value) < 0:
        raise ValueError("amount")
    return int(value)


def _end(value: object) -> date:
    parsed = _day(value)
    if parsed.day != calendar.monthrange(parsed.year, parsed.month)[1]:
        raise ValueError("period end")
    return parsed


def _prev(end: date) -> date:
    return end.replace(day=1) - timedelta(days=1)


def post(transactions: Any) -> Ledger:
    out: list[tuple[date, str, int]] = []
    for entry in transactions:
        if not isinstance(entry, dict) or "date" not in entry or "lines" not in entry:
            raise ValueError("entry")
        day = _day(entry["date"])
        lines = entry["lines"]
        if isinstance(lines, str) or len(lines) == 0:
            raise ValueError("lines")
        net = 0
        for line in lines:
            if not isinstance(line, dict) or not {"account", "debit", "credit"} <= set(line):
                raise ValueError("line")
            account = line["account"]
            if account not in ACCOUNTS:
                raise ValueError("account")
            d, c = _amount(line["debit"]), _amount(line["credit"])
            if (d > 0) == (c > 0):
                raise ValueError("debit or credit")
            out.append((day, account, d - c))
            net += d - c
        if net != 0:
            raise ValueError("balance")
    return tuple(out)


def _bal(ledger: Ledger, end: date) -> dict[str, int]:
    totals = dict.fromkeys(ACCOUNTS, 0)
    for day, account, signed in ledger:
        if day <= end:
            totals[account] += signed
    return totals


def _win(ledger: Ledger, end: date) -> dict[str, int]:
    prev = _prev(end)
    totals = dict.fromkeys(ACCOUNTS, 0)
    for day, account, signed in ledger:
        if prev < day <= end:
            totals[account] += signed
    return totals


def balance_sheet(ledger: Ledger, period_end: str) -> dict[str, int]:
    end = _end(period_end)
    b = _bal(ledger, end)
    acc = -b["accumulated_depreciation"]
    net_eq = b["equipment"] - acc
    ta = b["cash"] + b["accounts_receivable"] + b["inventory"] + net_eq
    pay = -b["accounts_payable"]
    debt = -b["long_term_debt"]
    tl = pay + debt
    common = -b["common_stock"]
    retained = -(b["sales"] + b["cost_of_goods_sold"] + b["operating_expenses"] + b["depreciation_expense"]) - b["dividends"]
    te = common + retained
    return {
        "cash": b["cash"], "accounts_receivable": b["accounts_receivable"], "inventory": b["inventory"],
        "equipment": b["equipment"], "accumulated_depreciation": acc, "net_equipment": net_eq,
        "total_assets": ta, "accounts_payable": pay, "long_term_debt": debt, "total_liabilities": tl,
        "common_stock": common, "retained_earnings": retained, "total_equity": te,
        "total_liabilities_and_equity": tl + te,
    }


def income_statement(ledger: Ledger, period_end: str) -> dict[str, int]:
    w = _win(ledger, _end(period_end))
    sales = -w["sales"]
    cost = w["cost_of_goods_sold"]
    gross = sales - cost
    op = w["operating_expenses"]
    dep = w["depreciation_expense"]
    return {"sales": sales, "cost_of_goods_sold": cost, "gross_profit": gross, "operating_expenses": op,
            "depreciation_expense": dep, "net_income": gross - op - dep}


def cash_flow_statement(ledger: Ledger, period_end: str) -> dict[str, int]:
    end = _end(period_end)
    w = _win(ledger, end)
    prev_bal = _bal(ledger, _prev(end))
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
    beginning = prev_bal["cash"]
    return {
        "net_income": ni, "depreciation": dep, "receivables": rec, "inventory": inv, "payables": pay,
        "cash_from_operations": ops, "capital_expenditure": capex, "cash_from_investing": capex,
        "net_borrowing": borrow, "stock_issued": stock, "dividends_paid": divs, "cash_from_financing": fin,
        "net_change_in_cash": ops + capex + fin, "beginning_cash": beginning,
        "ending_cash": beginning + ops + capex + fin,
    }


def articulation_check(ledger: Ledger, period_end: str) -> dict[str, int]:
    end = _end(period_end)
    now, before = balance_sheet(ledger, period_end), balance_sheet(ledger, _prev(end).isoformat())
    cf = cash_flow_statement(ledger, period_end)
    ni = income_statement(ledger, period_end)
    return {
        "balance_gap": now["total_assets"] - now["total_liabilities_and_equity"],
        "cash_gap": now["cash"] - cf["ending_cash"],
        "retained_earnings_gap": (now["retained_earnings"] - before["retained_earnings"]) - (ni["net_income"] + cf["dividends_paid"]),
        "depreciation_gap": (now["accumulated_depreciation"] - before["accumulated_depreciation"]) - ni["depreciation_expense"],
    }
