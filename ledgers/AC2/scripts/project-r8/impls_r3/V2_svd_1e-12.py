"""Fresh implementation of the A15 contract (candidate V2_svd_1e-12), written for round 3 of the AC2 verification."""

from __future__ import annotations

import datetime as dt
import math
from collections.abc import Mapping, Sequence
from numbers import Real
from typing import Any

import numpy as np

ITEMS: tuple[str, ...] = (
    "revenue", "cogs", "sga", "depreciation", "operating_income", "net_income", "cfo",
    "total_assets", "current_assets", "cash", "receivables", "ppe", "total_liabilities",
    "current_liabilities", "long_term_debt", "equity", "shares_outstanding",
)
TAG_PRIORITY: Mapping[str, tuple[str, ...]] = {
    "revenue": ("Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet"),
    "cogs": ("CostOfRevenue", "CostOfGoodsAndServicesSold"),
    "sga": ("SellingGeneralAndAdministrativeExpense",),
    "depreciation": ("DepreciationDepletionAndAmortization", "DepreciationAndAmortization", "Depreciation"),
    "operating_income": ("OperatingIncomeLoss",),
    "net_income": ("NetIncomeLoss",),
    "cfo": ("NetCashProvidedByUsedInOperatingActivities",),
    "total_assets": ("Assets",),
    "current_assets": ("AssetsCurrent",),
    "cash": ("CashAndCashEquivalentsAtCarryingValue",),
    "receivables": ("AccountsReceivableNetCurrent",),
    "ppe": ("PropertyPlantAndEquipmentNet",),
    "total_liabilities": ("Liabilities",),
    "current_liabilities": ("LiabilitiesCurrent",),
    "long_term_debt": ("LongTermDebtNoncurrent",),
    "equity": ("StockholdersEquity",),
    "shares_outstanding": ("CommonStockSharesOutstanding",),
}
BENEISH_INTERCEPT: float = -4.84
BENEISH_COEFFICIENTS: Mapping[str, float] = {
    "DSRI": 0.920, "GMI": 0.528, "AQI": 0.404, "SGI": 0.892,
    "DEPI": 0.115, "SGAI": -0.172, "LVGI": -0.327, "TATA": 4.679,
}
__all__ = ["ITEMS", "TAG_PRIORITY", "BENEISH_INTERCEPT", "BENEISH_COEFFICIENTS", "standardize", "dupont", "roic",
           "current_ratio", "gross_margin", "debt_to_assets", "days_sales_outstanding", "accruals_cash_flow",
           "accruals_balance_sheet", "modified_jones", "piotroski_f_score", "beneish_m_score"]

_FLOW = frozenset({"revenue", "cogs", "sga", "depreciation", "operating_income", "net_income", "cfo"})



def _iso(value: Any, what: str) -> dt.date:
    if not isinstance(value, str):
        raise ValueError(f"{what} must be a string date")
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        raise ValueError(f"{what} is not an ISO date") from None


def _num(value: Any, what: str) -> float:
    if not isinstance(value, Real) or not math.isfinite(float(value)):
        raise ValueError(f"{what} must be a finite number")
    return float(value)


def _quot(a: float, b: float, what: str) -> float:
    if b == 0.0:
        raise ValueError(f"zero denominator: {what}")
    q = a / b
    if not math.isfinite(q):
        raise ValueError(f"non-finite result: {what}")
    return q


def _need(st: Mapping[str, Mapping[str, float]], end: str, item: str) -> float:
    if end not in st:
        raise ValueError(f"no period end {end} in the statements")
    if item not in st[end]:
        raise ValueError(f"missing item {item} at {end}")
    return _num(st[end][item], item)


def _prev(st: Mapping[str, Any], end: str) -> str:
    t = _iso(end, "period end")
    found = None
    for k in st:
        e = _iso(k, "statement period end")
        if 350 <= (t - e).days <= 380 and (found is None or e > found):
            found = e
    if found is None:
        raise ValueError(f"no previous year for {end}")
    return found.isoformat()


def standardize(facts: Any, as_of: str | None = None) -> dict[str, dict[str, float]]:
    cut = None if as_of is None else _iso(as_of, "as_of")
    if not isinstance(facts, Mapping) or "facts" not in facts:
        raise ValueError("no facts key")
    gaap = facts["facts"].get("us-gaap", {})
    out: dict[str, dict[str, float]] = {}
    for item in ITEMS:
        unit = "shares" if item == "shares_outstanding" else "USD"
        taken: dict[str, float] = {}
        for tag in TAG_PRIORITY[item]:
            seen: dict[str, list[tuple[str, str, float]]] = {}
            for obs in gaap.get(tag, {}).get("units", {}).get(unit, []):
                if not isinstance(obs, Mapping):
                    raise ValueError("observation must be a mapping")
                for key in ("end", "val", "filed", "form"):
                    if key not in obs:
                        raise ValueError(f"observation lacks {key}")
                end = _iso(obs["end"], "end")
                filed = _iso(obs["filed"], "filed")
                val = _num(obs["val"], "val")
                form = obs["form"]
                if not isinstance(form, str):
                    raise ValueError("form must be a string")
                start = _iso(obs["start"], "start") if "start" in obs else None
                fp = obs.get("fp")
                if not form.startswith("10-K") or fp != "FY":
                    continue
                if item in _FLOW:
                    if start is None or not (350 <= (end - start).days <= 380):
                        continue
                elif start is not None:
                    continue
                if cut is not None and filed > cut:
                    continue
                accn = obs.get("accn") or ""
                seen.setdefault(end.isoformat(), []).append((filed.isoformat(), str(accn), val))
            for end_iso, cands in seen.items():
                cands.sort(key=lambda c: (c[0], c[1]), reverse=True)
                if len(cands) > 1 and cands[0][:2] == cands[1][:2] and cands[0][2] != cands[1][2]:
                    raise ValueError("inconsistent facts: a tie with different values")
                if end_iso not in taken:
                    taken[end_iso] = cands[0][2]
        for end_iso, v in taken.items():
            out.setdefault(end_iso, {})[item] = v
    return {k: out[k] for k in sorted(out)}


def _avg(a: float, b: float) -> float:
    return (a + b) / 2.0


def _ic(st: Mapping[str, Mapping[str, float]], end: str) -> float:
    return _need(st, end, "equity") + _need(st, end, "long_term_debt") - _need(st, end, "cash")


def dupont(statements: Any, period_end: str) -> dict[str, float]:
    p = _prev(statements, period_end)
    e = period_end
    ta = _avg(_need(statements, e, "total_assets"), _need(statements, p, "total_assets"))
    eq = _avg(_need(statements, e, "equity"), _need(statements, p, "equity"))
    rev, ni = _need(statements, e, "revenue"), _need(statements, e, "net_income")
    return {
        "net_margin": _quot(ni, rev, "net margin"),
        "asset_turnover": _quot(rev, ta, "asset turnover"),
        "leverage": _quot(ta, eq, "leverage"),
        "roe": _quot(ni, eq, "roe"),
        "roa": _quot(ni, ta, "roa"),
    }


def roic(statements: Any, period_end: str, tax_rate: float) -> float:
    rate = _num(tax_rate, "tax_rate")
    if not (0.0 <= rate < 1.0):
        raise ValueError("tax rate outside [0, 1)")
    p = _prev(statements, period_end)
    nopat = _need(statements, period_end, "operating_income") * (1.0 - rate)
    avg_ic = _avg(_ic(statements, period_end), _ic(statements, p))
    if not avg_ic > 0.0:
        raise ValueError("non-positive invested capital")
    return _quot(nopat, avg_ic, "roic")


def current_ratio(statements: Any, period_end: str) -> float:
    return _quot(_need(statements, period_end, "current_assets"), _need(statements, period_end, "current_liabilities"), "CR")


def gross_margin(statements: Any, period_end: str) -> float:
    rev = _need(statements, period_end, "revenue")
    return _quot(rev - _need(statements, period_end, "cogs"), rev, "gross margin")


def debt_to_assets(statements: Any, period_end: str) -> float:
    return _quot(_need(statements, period_end, "long_term_debt"), _need(statements, period_end, "total_assets"), "D/A")


def days_sales_outstanding(statements: Any, period_end: str) -> float:
    rev = _need(statements, period_end, "revenue")
    return _quot(_need(statements, period_end, "receivables"), rev, "DSO") * 365.0


def accruals_cash_flow(statements: Any, period_end: str) -> float:
    p = _prev(statements, period_end)
    ta = _avg(_need(statements, period_end, "total_assets"), _need(statements, p, "total_assets"))
    return _quot(_need(statements, period_end, "net_income") - _need(statements, period_end, "cfo"), ta, "accruals")


def accruals_balance_sheet(statements: Any, period_end: str) -> float:
    p = _prev(statements, period_end)
    e = period_end
    d_ca = _need(statements, e, "current_assets") - _need(statements, p, "current_assets")
    d_cash = _need(statements, e, "cash") - _need(statements, p, "cash")
    d_cl = _need(statements, e, "current_liabilities") - _need(statements, p, "current_liabilities")
    dep = _need(statements, e, "depreciation")
    ta = _avg(_need(statements, e, "total_assets"), _need(statements, p, "total_assets"))
    return _quot((d_ca - d_cash) - d_cl - dep, ta, "balance-sheet accruals")


def _rows(sample: Any) -> list[list[float]]:
    if isinstance(sample, (str, bytes)) or not isinstance(sample, Sequence):
        raise ValueError("sample must be a sequence")
    out: list[list[float]] = []
    for row in sample:
        if not isinstance(row, Mapping):
            raise ValueError("firm-year must be a mapping")
        vals = []
        for key in ("total_accruals", "lag_assets", "d_revenue", "d_receivables", "ppe"):
            if key not in row:
                raise ValueError(f"firm-year lacks {key}")
            vals.append(_num(row[key], key))
        if vals[1] <= 0.0:
            raise ValueError("lag_assets must be positive")
        out.append(vals)
    if len(out) < 4:
        raise ValueError("fewer than four firm-years")
    return out


def _norm_cols(design):
    norms = np.linalg.norm(design, axis=0)
    if np.any(norms == 0.0):
        raise ValueError("rank-deficient: a regressor is identically zero")
    return design / norms


def _rank_check(design):
    x = _norm_cols(design)
    s = np.linalg.svd(x, compute_uv=False)
    if s[-1] <= 1e-12 * s[0]:
        raise ValueError("rank-deficient design")



def modified_jones(sample: Any) -> dict[str, Any]:
    rows = _rows(sample)
    arr = np.array(rows, dtype=np.float64)
    lag = arr[:, 1]
    y = arr[:, 0] / lag
    design = np.column_stack([1.0 / lag, (arr[:, 2] - arr[:, 3]) / lag, arr[:, 4] / lag])
    if not (np.all(np.isfinite(y)) and np.all(np.isfinite(design))):
        raise ValueError("non-finite regression input")
    _rank_check(design)
    coef = np.linalg.lstsq(design, y, rcond=None)[0]
    fit = design @ coef
    return {
        "coefficients": tuple(float(c) for c in coef),
        "nondiscretionary": [float(v) for v in fit],
        "discretionary": [float(v) for v in y - fit],
    }


def piotroski_f_score(statements: Any, period_end: str) -> dict[str, Any]:
    t = period_end
    t1 = _prev(statements, t)
    t2 = _prev(statements, t1)
    n = lambda e, k: _need(statements, e, k)  # noqa: E731
    roa = _quot(n(t, "net_income"), n(t1, "total_assets"), "ROA")
    roa_p = _quot(n(t1, "net_income"), n(t2, "total_assets"), "ROA prev")
    cfo = _quot(n(t, "cfo"), n(t1, "total_assets"), "CFO")
    lev = _quot(n(t, "long_term_debt"), _avg(n(t, "total_assets"), n(t1, "total_assets")), "LEV")
    lev_p = _quot(n(t1, "long_term_debt"), _avg(n(t1, "total_assets"), n(t2, "total_assets")), "LEV prev")
    cr = _quot(n(t, "current_assets"), n(t, "current_liabilities"), "CR")
    cr_p = _quot(n(t1, "current_assets"), n(t1, "current_liabilities"), "CR prev")
    gm = _quot(n(t, "revenue") - n(t, "cogs"), n(t, "revenue"), "GM")
    gm_p = _quot(n(t1, "revenue") - n(t1, "cogs"), n(t1, "revenue"), "GM prev")
    ato = _quot(n(t, "revenue"), n(t1, "total_assets"), "ATO")
    ato_p = _quot(n(t1, "revenue"), n(t2, "total_assets"), "ATO prev")
    sig = (
        int(roa > 0), int(cfo > 0), int(roa > roa_p), int(cfo > roa), int(lev < lev_p),
        int(cr > cr_p), int(n(t, "shares_outstanding") <= n(t1, "shares_outstanding")),
        int(gm > gm_p), int(ato > ato_p),
    )
    return {"signals": sig, "score": sum(sig)}


def beneish_m_score(statements: Any, period_end: str) -> dict[str, float]:
    t = period_end
    p = _prev(statements, t)
    n = lambda e, k: _need(statements, e, k)  # noqa: E731
    v = {
        "DSRI": _quot(_quot(n(t, "receivables"), n(t, "revenue"), "r"), _quot(n(p, "receivables"), n(p, "revenue"), "r"), "DSRI"),
        "GMI": _quot(_quot(n(p, "revenue") - n(p, "cogs"), n(p, "revenue"), "g"), _quot(n(t, "revenue") - n(t, "cogs"), n(t, "revenue"), "g"), "GMI"),
        "AQI": _quot(1 - _quot(n(t, "current_assets") + n(t, "ppe"), n(t, "total_assets"), "a"),
                     1 - _quot(n(p, "current_assets") + n(p, "ppe"), n(p, "total_assets"), "a"), "AQI"),
        "SGI": _quot(n(t, "revenue"), n(p, "revenue"), "SGI"),
        "DEPI": _quot(_quot(n(p, "depreciation"), n(p, "depreciation") + n(p, "ppe"), "d"),
                      _quot(n(t, "depreciation"), n(t, "depreciation") + n(t, "ppe"), "d"), "DEPI"),
        "SGAI": _quot(_quot(n(t, "sga"), n(t, "revenue"), "s"), _quot(n(p, "sga"), n(p, "revenue"), "s"), "SGAI"),
        "LVGI": _quot(_quot(n(t, "current_liabilities") + n(t, "long_term_debt"), n(t, "total_assets"), "l"),
                      _quot(n(p, "current_liabilities") + n(p, "long_term_debt"), n(p, "total_assets"), "l"), "LVGI"),
        "TATA": _quot(n(t, "net_income") - n(t, "cfo"), n(t, "total_assets"), "TATA"),
    }
    m = BENEISH_INTERCEPT + sum(BENEISH_COEFFICIENTS[k] * x for k, x in v.items())
    if not math.isfinite(m):
        raise ValueError("non-finite M-score")
    return {**v, "m_score": m}
