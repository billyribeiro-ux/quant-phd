"""Alternative r13 C: strict type checks (type(v) is int), regex date check, ledger as a list of (date, account, signed) tuples,
and a fresh statement dict each call; the reference's balance-difference flows are kept."""

from __future__ import annotations

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
ISO = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")


def _iso(value: Any) -> str:
    if type(value) is not str or ISO.fullmatch(value) is None:
        raise ValueError("date")
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("date") from exc
    return value


def _end(value: Any) -> str:
    text = _iso(value)
    d = date.fromisoformat(text)
    if d.day != calendar.monthrange(d.year, d.month)[1]:
        raise ValueError("period end")
    return text


def _prev(text: str) -> str:
    return (date.fromisoformat(text).replace(day=1) - timedelta(days=1)).isoformat()


def post(transactions: Any) -> tuple[tuple[str, str, int], ...]:
    rows: list[tuple[str, str, int]] = []
    for entry in transactions:
        day = _iso(entry["date"]) if isinstance(entry, dict) and "date" in entry else None
        if day is None or "lines" not in entry:
            raise ValueError("transaction")
        lines = list(entry["lines"]) if isinstance(entry["lines"], (list, tuple)) else []
        if not lines:
            raise ValueError("lines")
        bal = 0
        block: list[tuple[str, str, int]] = []
        for line in lines:
            acct = line.get("account") if isinstance(line, dict) else None
            if acct not in ACCOUNTS:
                raise ValueError("account")
            if "debit" not in line or "credit" not in line:
                raise ValueError("line")
            dr, cr = line["debit"], line["credit"]
            if type(dr) is not int or type(cr) is not int or dr < 0 or cr < 0:
                raise ValueError("amount")
            if (dr > 0) + (cr > 0) != 1:
                raise ValueError("debit or credit")
            block.append((day, acct, dr - cr))
            bal += dr - cr
        if bal != 0:
            raise ValueError("balance")
        rows.extend(block)
    return tuple(rows)


def _totals(ledger: Any, end: str) -> dict[str, int]:
    out = dict.fromkeys(ACCOUNTS, 0)
    for d, a, s in ledger:
        if d <= end:
            out[a] += s
    return out


def balance_sheet(ledger: Any, period_end: str) -> dict[str, int]:
    end = _end(period_end)
    b = _totals(ledger, end)
    acc = -b["accumulated_depreciation"]
    neteq = b["equipment"] - acc
    ta = b["cash"] + b["accounts_receivable"] + b["inventory"] + neteq
    ap, ltd = -b["accounts_payable"], -b["long_term_debt"]
    tl = ap + ltd
    cs = -b["common_stock"]
    re_ = -(b["sales"] + b["cost_of_goods_sold"] + b["operating_expenses"] + b["depreciation_expense"]) - b["dividends"]
    te = cs + re_
    return {"cash": b["cash"], "accounts_receivable": b["accounts_receivable"], "inventory": b["inventory"],
            "equipment": b["equipment"], "accumulated_depreciation": acc, "net_equipment": neteq,
            "total_assets": ta, "accounts_payable": ap, "long_term_debt": ltd, "total_liabilities": tl,
            "common_stock": cs, "retained_earnings": re_, "total_equity": te, "total_liabilities_and_equity": tl + te}


def _flow(ledger: Any, period_end: str) -> tuple[dict[str, int], dict[str, int]]:
    end = _end(period_end)
    now, before = _totals(ledger, end), _totals(ledger, _prev(end))
    return now, {a: now[a] - before[a] for a in ACCOUNTS}


def income_statement(ledger: Any, period_end: str) -> dict[str, int]:
    _, f = _flow(ledger, period_end)
    s = -f["sales"]
    c = f["cost_of_goods_sold"]
    o = f["operating_expenses"]
    d = f["depreciation_expense"]
    return {"sales": s, "cost_of_goods_sold": c, "gross_profit": s - c, "operating_expenses": o,
            "depreciation_expense": d, "net_income": s - c - o - d}


def cash_flow_statement(ledger: Any, period_end: str) -> dict[str, int]:
    now, f = _flow(ledger, period_end)
    before_cash = now["cash"] - f["cash"]
    end = _end(period_end)
    _, prev_flow = _flow(ledger, end)
    ni = income_statement(ledger, end)["net_income"]
    old_now, old_before = _totals(ledger, end), _totals(ledger, _prev(end))
    ops = ni + f["depreciation_expense"] - (old_now["accounts_receivable"] - old_before["accounts_receivable"]) \
        - (old_now["inventory"] - old_before["inventory"]) - (old_now["accounts_payable"] - old_before["accounts_payable"])
    capex = -f["equipment"]
    divs = -f["dividends"]
    fin = -f["long_term_debt"] - f["common_stock"] + divs
    _ = prev_flow
    return {"net_income": ni, "depreciation": f["depreciation_expense"],
            "receivables": -(old_now["accounts_receivable"] - old_before["accounts_receivable"]),
            "inventory": -(old_now["inventory"] - old_before["inventory"]),
            "payables": -(old_now["accounts_payable"] - old_before["accounts_payable"]),
            "cash_from_operations": ops, "capital_expenditure": capex, "cash_from_investing": capex,
            "net_borrowing": -f["long_term_debt"], "stock_issued": -f["common_stock"], "dividends_paid": divs,
            "cash_from_financing": fin, "net_change_in_cash": ops + capex + fin, "beginning_cash": before_cash,
            "ending_cash": before_cash + ops + capex + fin}


def articulation_check(ledger: Any, period_end: str) -> dict[str, int]:
    end = _end(period_end)
    now = balance_sheet(ledger, end)
    before = balance_sheet(ledger, _prev(end))
    cf = cash_flow_statement(ledger, end)
    ni = income_statement(ledger, end)
    return {"balance_gap": now["total_assets"] - now["total_liabilities_and_equity"],
            "cash_gap": now["cash"] - cf["ending_cash"],
            "retained_earnings_gap": (now["retained_earnings"] - before["retained_earnings"]) - (ni["net_income"] + cf["dividends_paid"]),
            "depreciation_gap": (now["accumulated_depreciation"] - before["accumulated_depreciation"]) - ni["depreciation_expense"]}
