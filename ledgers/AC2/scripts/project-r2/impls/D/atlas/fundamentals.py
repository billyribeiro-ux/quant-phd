"""Verifier candidate D (round 2): written from atlas/A15.contract.md with a validator-first structure, not from the reference."""

from __future__ import annotations

import datetime as dt
import math
from collections.abc import Mapping, Sequence
from numbers import Real
from typing import Any

import numpy as np

ITEMS: tuple[str, ...] = (
    "revenue", "cogs", "sga", "depreciation", "operating_income", "net_income", "cfo", "total_assets",
    "current_assets", "cash", "receivables", "ppe", "total_liabilities", "current_liabilities",
    "long_term_debt", "equity", "shares_outstanding",
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
    "DSRI": 0.920, "GMI": 0.528, "AQI": 0.404, "SGI": 0.892, "DEPI": 0.115, "SGAI": -0.172, "LVGI": -0.327,
    "TATA": 4.679,
}
FLOW = {"revenue", "cogs", "sga", "depreciation", "operating_income", "net_income", "cfo"}
MJ_FIELDS = ("total_accruals", "lag_assets", "d_revenue", "d_receivables", "ppe")


def _iso(value: Any) -> dt.date:
    if not isinstance(value, str):
        raise ValueError("a date must be an ISO string")
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("not an ISO date") from exc


def _num(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError("a value must be a number")
    out = float(value)
    if not math.isfinite(out):
        raise ValueError("a value must be finite")
    return out


def _ratio(num: float, den: float) -> float:
    if den == 0.0:
        raise ValueError("zero denominator")
    out = num / den
    if not math.isfinite(out):
        raise ValueError("non-finite result")
    return out


def _at(statements: Any, end: str, item: str) -> float:
    if not isinstance(statements, Mapping) or end not in statements:
        raise ValueError(f"no period end {end}")
    row = statements[end]
    if item not in row:
        raise ValueError(f"missing {item}")
    return _num(row[item])


def _prev(statements: Any, end: str) -> str:
    t = _iso(end)
    found = [k for k in statements if 350 <= (t - _iso(k)).days <= 380]
    if not found:
        raise ValueError("no previous year")
    return max(found, key=_iso)


def _avg(a: float, b: float) -> float:
    return (a + b) / 2.0


def standardize(facts: Any, as_of: str | None = None) -> dict[str, dict[str, float]]:
    cut = None if as_of is None else _iso(as_of)
    if not isinstance(facts, Mapping) or "facts" not in facts or not isinstance(facts["facts"], Mapping):
        raise ValueError("facts must be a company-facts mapping")
    gaap = facts["facts"].get("us-gaap", {})
    out: dict[str, dict[str, float]] = {}
    for item in ITEMS:
        unit = "shares" if item == "shares_outstanding" else "USD"
        per_tag: list[dict[str, tuple[tuple[dt.date, str], float]]] = []
        for tag in TAG_PRIORITY[item]:
            entry = gaap.get(tag)
            chosen: dict[str, tuple[tuple[dt.date, str], float]] = {}
            pool: dict[str, list[tuple[tuple[dt.date, str], float]]] = {}
            for obs in (entry or {}).get("units", {}).get(unit, []):
                if not isinstance(obs, Mapping):
                    raise ValueError("an observation must be a mapping")
                for field in ("end", "val", "filed", "form"):
                    if field not in obs:
                        raise ValueError(f"an observation lacks {field}")
                end = _iso(obs["end"]).isoformat()
                filed = _iso(obs["filed"])
                val = _num(obs["val"])
                form = obs["form"]
                if not isinstance(form, str):
                    raise ValueError("form must be a string")
                start = _iso(obs["start"]) if "start" in obs else None
                if not form.startswith("10-K") or obs.get("fp") != "FY":
                    continue
                if item in FLOW:
                    if start is None or not 350 <= (_iso(end) - start).days <= 380:
                        continue
                elif start is not None:
                    continue
                if cut is not None and filed > cut:
                    continue
                pool.setdefault(end, []).append(((filed, str(obs.get("accn") or "")), val))
            for end, cands in pool.items():
                top_key = max(k for k, _ in cands)
                tops = {v for k, v in cands if k == top_key}
                if len(tops) > 1:
                    raise ValueError("tied observations with different values")
                chosen[end] = (top_key, tops.pop())
            per_tag.append(chosen)
        for end in sorted({e for tag_map in per_tag for e in tag_map}):
            for tag_map in per_tag:
                if end in tag_map:
                    out.setdefault(end, {})[item] = tag_map[end][1]
                    break
    return {end: out[end] for end in sorted(out)}


def dupont(statements: Any, period_end: str) -> dict[str, float]:
    prev = _prev(statements, period_end)
    rev = _at(statements, period_end, "revenue")
    ni = _at(statements, period_end, "net_income")
    avg_ta = _avg(_at(statements, period_end, "total_assets"), _at(statements, prev, "total_assets"))
    avg_eq = _avg(_at(statements, period_end, "equity"), _at(statements, prev, "equity"))
    return {
        "net_margin": _ratio(ni, rev),
        "asset_turnover": _ratio(rev, avg_ta),
        "leverage": _ratio(avg_ta, avg_eq),
        "roe": _ratio(ni, avg_eq),
        "roa": _ratio(ni, avg_ta),
    }


def _ic(statements: Any, end: str) -> float:
    return _at(statements, end, "equity") + _at(statements, end, "long_term_debt") - _at(statements, end, "cash")


def roic(statements: Any, period_end: str, tax_rate: float) -> float:
    rate = _num(tax_rate)
    if not 0.0 <= rate < 1.0:
        raise ValueError("tax rate out of range")
    prev = _prev(statements, period_end)
    nopat = _at(statements, period_end, "operating_income") * (1.0 - rate)
    avg_ic = _avg(_ic(statements, period_end), _ic(statements, prev))
    if avg_ic <= 0.0:
        raise ValueError("non-positive invested capital")
    return _ratio(nopat, avg_ic)


def current_ratio(statements: Any, period_end: str) -> float:
    return _ratio(_at(statements, period_end, "current_assets"), _at(statements, period_end, "current_liabilities"))


def gross_margin(statements: Any, period_end: str) -> float:
    rev = _at(statements, period_end, "revenue")
    return _ratio(rev - _at(statements, period_end, "cogs"), rev)


def debt_to_assets(statements: Any, period_end: str) -> float:
    return _ratio(_at(statements, period_end, "long_term_debt"), _at(statements, period_end, "total_assets"))


def days_sales_outstanding(statements: Any, period_end: str) -> float:
    return _ratio(_at(statements, period_end, "receivables"), _at(statements, period_end, "revenue")) * 365.0


def accruals_cash_flow(statements: Any, period_end: str) -> float:
    prev = _prev(statements, period_end)
    avg_ta = _avg(_at(statements, period_end, "total_assets"), _at(statements, prev, "total_assets"))
    gap = _at(statements, period_end, "net_income") - _at(statements, period_end, "cfo")
    return _ratio(gap, avg_ta)


def accruals_balance_sheet(statements: Any, period_end: str) -> float:
    prev = _prev(statements, period_end)

    def d(item: str) -> float:
        return _at(statements, period_end, item) - _at(statements, prev, item)

    avg_ta = _avg(_at(statements, period_end, "total_assets"), _at(statements, prev, "total_assets"))
    num = (d("current_assets") - d("cash")) - d("current_liabilities") - _at(statements, period_end, "depreciation")
    return _ratio(num, avg_ta)


def modified_jones(sample: Any) -> dict[str, Any]:
    if isinstance(sample, str) or not isinstance(sample, Sequence):
        raise ValueError("sample must be a sequence")
    rows = []
    for row in sample:
        if not isinstance(row, Mapping):
            raise ValueError("a firm-year must be a mapping")
        vals = [_num(row[f]) if f in row else _raise(f) for f in MJ_FIELDS]
        if vals[1] <= 0.0:
            raise ValueError("lagged assets must be positive")
        rows.append(vals)
    if len(rows) < 4:
        raise ValueError("at least four firm-years")
    arr = np.array(rows, dtype=np.float64)
    lag = arr[:, 1]
    y = arr[:, 0] / lag
    x = np.column_stack([1.0 / lag, (arr[:, 2] - arr[:, 3]) / lag, arr[:, 4] / lag])
    if not (np.isfinite(x).all() and np.isfinite(y).all()):
        raise ValueError("non-finite regression input")
    if np.linalg.matrix_rank(x) < 3:  # unscaled rank test, a different route from the reference
        raise ValueError("rank-deficient design")
    coef = np.linalg.lstsq(x, y, rcond=None)[0]
    fit = x @ coef
    return {
        "coefficients": tuple(float(c) for c in coef),
        "nondiscretionary": [float(v) for v in fit],
        "discretionary": [float(v) for v in y - fit],
    }


def _raise(field: str) -> float:
    raise ValueError(f"a firm-year lacks {field}")


def piotroski_f_score(statements: Any, period_end: str) -> dict[str, Any]:
    t1 = _prev(statements, period_end)
    t2 = _prev(statements, t1)
    t = period_end
    ta = {k: _at(statements, k, "total_assets") for k in (t, t1, t2)}
    roa = _ratio(_at(statements, t, "net_income"), ta[t1])
    roa_p = _ratio(_at(statements, t1, "net_income"), ta[t2])
    cfo = _ratio(_at(statements, t, "cfo"), ta[t1])
    lev = _ratio(_at(statements, t, "long_term_debt"), _avg(ta[t], ta[t1]))
    lev_p = _ratio(_at(statements, t1, "long_term_debt"), _avg(ta[t1], ta[t2]))
    cr = _ratio(_at(statements, t, "current_assets"), _at(statements, t, "current_liabilities"))
    cr_p = _ratio(_at(statements, t1, "current_assets"), _at(statements, t1, "current_liabilities"))
    rev, rev_p = _at(statements, t, "revenue"), _at(statements, t1, "revenue")
    gm = _ratio(rev - _at(statements, t, "cogs"), rev)
    gm_p = _ratio(rev_p - _at(statements, t1, "cogs"), rev_p)
    ato = _ratio(rev, ta[t1])
    ato_p = _ratio(rev_p, ta[t2])
    sh, sh_p = _at(statements, t, "shares_outstanding"), _at(statements, t1, "shares_outstanding")
    flags = [roa > 0, cfo > 0, roa > roa_p, cfo > roa, lev < lev_p, cr > cr_p, sh <= sh_p, gm > gm_p, ato > ato_p]
    signals = tuple(1 if f else 0 for f in flags)
    return {"signals": signals, "score": sum(signals)}


def beneish_m_score(statements: Any, period_end: str) -> dict[str, float]:
    t = period_end
    p = _prev(statements, t)

    def v(end: str, item: str) -> float:
        return _at(statements, end, item)

    dsri = _ratio(_ratio(v(t, "receivables"), v(t, "revenue")), _ratio(v(p, "receivables"), v(p, "revenue")))
    gmt = _ratio(v(t, "revenue") - v(t, "cogs"), v(t, "revenue"))
    gmp = _ratio(v(p, "revenue") - v(p, "cogs"), v(p, "revenue"))
    gmi = _ratio(gmp, gmt)
    aqi = _ratio(
        1.0 - _ratio(v(t, "current_assets") + v(t, "ppe"), v(t, "total_assets")),
        1.0 - _ratio(v(p, "current_assets") + v(p, "ppe"), v(p, "total_assets")),
    )
    sgi = _ratio(v(t, "revenue"), v(p, "revenue"))
    depi = _ratio(
        _ratio(v(p, "depreciation"), v(p, "depreciation") + v(p, "ppe")),
        _ratio(v(t, "depreciation"), v(t, "depreciation") + v(t, "ppe")),
    )
    sgai = _ratio(_ratio(v(t, "sga"), v(t, "revenue")), _ratio(v(p, "sga"), v(p, "revenue")))
    lvgi = _ratio(
        _ratio(v(t, "current_liabilities") + v(t, "long_term_debt"), v(t, "total_assets")),
        _ratio(v(p, "current_liabilities") + v(p, "long_term_debt"), v(p, "total_assets")),
    )
    tata = _ratio(v(t, "net_income") - v(t, "cfo"), v(t, "total_assets"))
    out: dict[str, float] = {"DSRI": dsri, "GMI": gmi, "AQI": aqi, "SGI": sgi, "DEPI": depi, "SGAI": sgai,
                             "LVGI": lvgi, "TATA": tata}
    m = BENEISH_INTERCEPT + sum(BENEISH_COEFFICIENTS[k] * out[k] for k in out)
    if not math.isfinite(m):
        raise ValueError("non-finite M-score")
    out["m_score"] = m
    return out
