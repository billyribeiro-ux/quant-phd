"""p29: beneish_m_score reads the period's current liabilities by direct indexing, so a missing item raises KeyError."""

from __future__ import annotations

import datetime as dt
import math
from collections.abc import Mapping, Sequence
from numbers import Real
from typing import Any

import numpy as np

ITEMS: tuple[str, ...] = (
    "revenue",
    "cogs",
    "sga",
    "depreciation",
    "operating_income",
    "net_income",
    "cfo",
    "total_assets",
    "current_assets",
    "cash",
    "receivables",
    "ppe",
    "total_liabilities",
    "current_liabilities",
    "long_term_debt",
    "equity",
    "shares_outstanding",
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
# The Beneish (1999) constants are UNCONFIRMED: ONE secondary source (the Wikipedia page
# 'Beneish M-score', read 2026-10-27) reproduces them; nothing else could be read.
BENEISH_INTERCEPT: float = -4.84
BENEISH_COEFFICIENTS: Mapping[str, float] = {
    "DSRI": 0.920,
    "GMI": 0.528,
    "AQI": 0.404,
    "SGI": 0.892,
    "DEPI": 0.115,
    "SGAI": -0.172,
    "LVGI": -0.327,
    "TATA": 4.679,
}

__all__ = [
    "BENEISH_COEFFICIENTS",
    "BENEISH_INTERCEPT",
    "ITEMS",
    "TAG_PRIORITY",
    "accruals_balance_sheet",
    "accruals_cash_flow",
    "beneish_m_score",
    "current_ratio",
    "days_sales_outstanding",
    "debt_to_assets",
    "dupont",
    "gross_margin",
    "modified_jones",
    "piotroski_f_score",
    "roic",
    "standardize",
]

Facts = Mapping[str, Any]
Statements = Mapping[str, Mapping[str, float]]

_RANK_TOL = 1e-10
_YEAR_MIN, _YEAR_MAX = 350, 380
_DAYS_PER_YEAR = 365


# ---------------------------------------------------------------- validation helpers


def _date(value: Any, name: str) -> dt.date:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be an ISO date string, not {type(value).__name__}")
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{name} is not an ISO date: {value!r}") from exc


def _number(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a number, not {type(value).__name__}")
    x = float(value)
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x


def _div(numerator: float, denominator: float, name: str) -> float:
    if denominator == 0.0:
        raise ValueError(f"{name} is zero: the ratio is undefined")
    result = numerator / denominator
    if not math.isfinite(result):
        raise ValueError(f"the result for {name} is not finite")
    return result


def _period(period_end: Any) -> str:
    return _date(period_end, "period_end").isoformat()


def _statements(statements: Any) -> Statements:
    if not isinstance(statements, Mapping):
        raise ValueError("statements must be a mapping from period end to items")
    return statements


def _get(statements: Any, end: str, item: str) -> float:
    row = _statements(statements).get(end)
    if row is None:
        raise ValueError(f"the statements have no period end {end}")
    if item not in row:
        raise ValueError(f"{item} is missing for period end {end}: nothing is imputed")
    return _number(row[item], f"{item} at {end}")


def _previous(statements: Any, end: str) -> str:
    """The latest period end in the statements 350 to 380 days before ``end``."""
    t = dt.date.fromisoformat(end)
    best: dt.date | None = None
    for key in _statements(statements):
        e = _date(key, "period end in the statements")
        if _YEAR_MIN <= (t - e).days <= _YEAR_MAX and (best is None or e > best):
            best = e
    if best is None:
        raise ValueError(f"the statements have no previous year (350 to 380 days before {end})")
    return best.isoformat()


def _average(a: float, b: float) -> float:
    return (a + b) / 2.0


# ---------------------------------------------------------------- standardization


def _observation(obs: Any, tag: str) -> tuple[dt.date, dt.date, str, str, bool, dt.date | None, float]:
    """Validate one observation and return (end, filed, form, fp, has_start, start, value)."""
    if not isinstance(obs, Mapping):
        raise ValueError(f"an observation of {tag} must be a mapping")
    for key in ("end", "val", "filed", "form"):
        if key not in obs:
            raise ValueError(f"an observation of {tag} lacks {key!r}")
    end = _date(obs["end"], f"end of an observation of {tag}")
    filed = _date(obs["filed"], f"filed of an observation of {tag}")
    value = _number(obs["val"], f"val of an observation of {tag}")
    form = obs["form"]
    if not isinstance(form, str):
        raise ValueError(f"form of an observation of {tag} must be a string")
    fp = obs.get("fp", "")
    start = _date(obs["start"], f"start of an observation of {tag}") if "start" in obs else None
    return end, filed, form, str(fp), start is not None, start, value


def _is_annual(item: str, form: str, fp: str, start: dt.date | None, end: dt.date) -> bool:
    if not form.startswith("10-K") or fp != "FY":
        return False
    if item in _FLOW:
        return start is not None and _YEAR_MIN <= (end - start).days <= _YEAR_MAX
    return start is None


_FLOW = frozenset({"revenue", "cogs", "sga", "depreciation", "operating_income", "net_income", "cfo"})


def standardize(facts: Facts, as_of: str | None = None) -> dict[str, dict[str, float]]:
    """Standardized statements {period_end: {item: value}} from a company-facts mapping, as known on ``as_of``."""
    cutoff = None if as_of is None else _date(as_of, "as_of")
    if not isinstance(facts, Mapping) or "facts" not in facts:
        raise ValueError("facts must be a company-facts mapping with a 'facts' key")
    body = facts["facts"]
    if not isinstance(body, Mapping):
        raise ValueError("facts['facts'] must be a mapping of taxonomies")
    gaap = body.get("us-gaap", {})
    if not isinstance(gaap, Mapping):
        raise ValueError("facts['facts']['us-gaap'] must be a mapping of tags")

    chosen: dict[str, dict[str, tuple[dt.date, str, float]]] = {}  # item -> end -> best candidate
    values: dict[str, dict[str, float]] = {}
    for item in ITEMS:
        unit = "shares" if item == "shares_outstanding" else "USD"
        best_by_tag: dict[str, dict[str, tuple[dt.date, str, float]]] = {}
        for tag in TAG_PRIORITY[item]:
            entry = gaap.get(tag)
            if entry is None:
                continue
            if not isinstance(entry, Mapping) or not isinstance(entry.get("units", {}), Mapping):
                raise ValueError(f"the tag {tag} must map units to observation lists")
            observations = entry.get("units", {}).get(unit, [])
            if not isinstance(observations, Sequence) or isinstance(observations, str):
                raise ValueError(f"the observations of {tag} in {unit} must be a list")
            candidates: dict[str, list[tuple[dt.date, str, float]]] = {}
            for obs in observations:
                end, filed, form, fp, _, start, value = _observation(obs, tag)
                if not _is_annual(item, form, fp, start, end):
                    continue
                if cutoff is not None and filed > cutoff:
                    continue
                accn = str(obs.get("accn", "") or "")
                candidates.setdefault(end.isoformat(), []).append((filed, accn, value))
            best: dict[str, tuple[dt.date, str, float]] = {}
            for key, options in candidates.items():
                options.sort(key=lambda c: (c[0], c[1]), reverse=True)
                top, runner_up = options[0], options[1] if len(options) > 1 else None
                if (
                    runner_up is not None
                    and (top[0], top[1]) == (runner_up[0], runner_up[1])
                    and top[2] != runner_up[2]
                ):
                    raise ValueError(
                        f"the facts are inconsistent: two annual observations of {tag} for {key} tie on (filed, accn) "
                        "with different values"
                    )
                best[key] = top
            best_by_tag[tag] = best
        chosen[item] = {}
        for tag in TAG_PRIORITY[item]:
            for key, candidate in best_by_tag.get(tag, {}).items():
                if key not in chosen[item]:
                    chosen[item][key] = candidate
    for item in ITEMS:
        for key, candidate in chosen[item].items():
            values.setdefault(key, {})[item] = candidate[2]
    return {key: dict(values[key]) for key in sorted(values)}


# ---------------------------------------------------------------- ratios


def dupont(statements: Statements, period_end: str) -> dict[str, float]:
    """DuPont decomposition on average assets and equity; roe equals net_margin * asset_turnover * leverage."""
    end = _period(period_end)
    prev = _previous(statements, end)
    revenue = _get(statements, end, "revenue")
    net_income = _get(statements, end, "net_income")
    avg_assets = _average(_get(statements, end, "total_assets"), _get(statements, prev, "total_assets"))
    avg_equity = _average(_get(statements, end, "equity"), _get(statements, prev, "equity"))
    return {
        "net_margin": _div(net_income, revenue, "revenue"),
        "asset_turnover": _div(revenue, avg_assets, "average total assets"),
        "leverage": _div(avg_assets, avg_equity, "average equity"),
        "roe": _div(net_income, avg_equity, "average equity"),
        "roa": _div(net_income, avg_assets, "average total assets"),
    }


def _invested_capital(statements: Statements, end: str) -> float:
    return _get(statements, end, "equity") + _get(statements, end, "long_term_debt") - _get(statements, end, "cash")


def roic(statements: Statements, period_end: str, tax_rate: float) -> float:
    """NOPAT over average invested capital, with invested capital = equity + long-term debt - cash."""
    end = _period(period_end)
    rate = _number(tax_rate, "tax_rate")
    if not 0.0 <= rate < 1.0:
        raise ValueError("tax_rate must satisfy 0 <= tax_rate < 1")
    prev = _previous(statements, end)
    nopat = _get(statements, end, "operating_income") * (1.0 - rate)
    avg_capital = _average(_invested_capital(statements, end), _invested_capital(statements, prev))
    if avg_capital <= 0.0:
        raise ValueError("average invested capital must be positive for ROIC to be defined")
    return _div(nopat, avg_capital, "average invested capital")


def current_ratio(statements: Statements, period_end: str) -> float:
    """Current assets over current liabilities at the period end."""
    end = _period(period_end)
    return _div(_get(statements, end, "current_assets"), _get(statements, end, "current_liabilities"), "liabilities")


def gross_margin(statements: Statements, period_end: str) -> float:
    """Gross margin: (revenue - cogs) / revenue."""
    end = _period(period_end)
    revenue = _get(statements, end, "revenue")
    return _div(revenue - _get(statements, end, "cogs"), revenue, "revenue")


def debt_to_assets(statements: Statements, period_end: str) -> float:
    """Long-term debt over total assets at the period end."""
    end = _period(period_end)
    return _div(_get(statements, end, "long_term_debt"), _get(statements, end, "total_assets"), "total assets")


def days_sales_outstanding(statements: Statements, period_end: str) -> float:
    """Receivables over revenue, times 365."""
    end = _period(period_end)
    revenue = _get(statements, end, "revenue")
    return _div(_get(statements, end, "receivables"), revenue, "revenue") * _DAYS_PER_YEAR


# ---------------------------------------------------------------- earnings quality


def accruals_cash_flow(statements: Statements, period_end: str) -> float:
    """Cash-flow accruals: (net income - cfo) over average total assets."""
    end = _period(period_end)
    prev = _previous(statements, end)
    avg_assets = _average(_get(statements, end, "total_assets"), _get(statements, prev, "total_assets"))
    return _div(_get(statements, end, "net_income") - _get(statements, end, "cfo"), avg_assets, "average assets")


def accruals_balance_sheet(statements: Statements, period_end: str) -> float:
    """Sloan (1996) balance-sheet accruals over average total assets.

    [(d current assets - d cash) - d current liabilities - depreciation] / average total assets, where d is the
    change from the previous year end. Short-term debt and taxes payable are not separate items in this contract.
    """
    end = _period(period_end)
    prev = _previous(statements, end)
    d_current_assets = _get(statements, end, "current_assets") - _get(statements, prev, "current_assets")
    d_cash = _get(statements, end, "cash") - _get(statements, prev, "cash")
    d_current_liabilities = _get(statements, end, "current_liabilities") - _get(statements, prev, "current_liabilities")
    depreciation = _get(statements, end, "depreciation")
    avg_assets = _average(_get(statements, end, "total_assets"), _get(statements, prev, "total_assets"))
    numerator = (d_current_assets - d_cash) - d_current_liabilities - depreciation
    return _div(numerator, avg_assets, "average assets")


_MJ_KEYS = ("total_accruals", "lag_assets", "d_revenue", "d_receivables", "ppe")


def modified_jones(sample: Sequence[Mapping[str, float]]) -> dict[str, Any]:
    """Modified Jones model (registry key dechow1995detecting, 'Detecting Earnings Management').

    Estimated by OLS without an intercept.
    """
    if not isinstance(sample, Sequence) or isinstance(sample, str):
        raise ValueError("sample must be a sequence of firm-year mappings")
    rows: list[list[float]] = []
    for i, row in enumerate(sample):
        if not isinstance(row, Mapping):
            raise ValueError(f"firm-year {i} must be a mapping")
        for key in _MJ_KEYS:
            if key not in row:
                raise ValueError(f"firm-year {i} lacks {key!r}")
        vals = {key: _number(row[key], f"{key} of firm-year {i}") for key in _MJ_KEYS}
        if vals["lag_assets"] <= 0.0:
            raise ValueError(f"lag_assets must be positive (firm-year {i})")
        rows.append([vals[key] for key in _MJ_KEYS])
    if len(rows) < 4:
        raise ValueError("the modified Jones model needs at least 4 firm-years")
    data = np.array(rows, dtype=np.float64)
    lag = data[:, 1]
    y = data[:, 0] / lag
    design = np.column_stack([1.0 / lag, (data[:, 2] - data[:, 3]) / lag, data[:, 4] / lag])
    if not (np.all(np.isfinite(y)) and np.all(np.isfinite(design))):
        raise ValueError("the regression inputs must be finite")
    norms = np.linalg.norm(design, axis=0)
    if np.any(norms == 0.0):
        raise ValueError("the design matrix is rank-deficient: a regressor is identically zero")
    unit_columns = design / norms  # the rank test must not depend on the regressors' units
    s = np.linalg.svd(unit_columns, compute_uv=False)
    if s[-1] <= _RANK_TOL * s[0]:
        raise ValueError("the design matrix is rank-deficient: the three regressors must be linearly independent")
    coef = np.linalg.lstsq(design, y, rcond=None)[0]
    fitted = design @ coef
    return {
        "coefficients": tuple(float(c) for c in coef),
        "nondiscretionary": [float(v) for v in fitted],
        "discretionary": [float(v) for v in (y - fitted)],
    }


# ---------------------------------------------------------------- scores


def piotroski_f_score(statements: Statements, period_end: str) -> dict[str, Any]:
    """Piotroski (2000) F-score: nine binary signals on the period end and its two preceding year ends."""
    t = _period(period_end)
    t1 = _previous(statements, t)
    t2 = _previous(statements, t1)
    ta_t, ta_t1, ta_t2 = (_get(statements, e, "total_assets") for e in (t, t1, t2))
    roa = _div(_get(statements, t, "net_income"), ta_t1, "total assets of the previous year")
    roa_prev = _div(_get(statements, t1, "net_income"), ta_t2, "total assets two years back")
    cfo = _div(_get(statements, t, "cfo"), ta_t1, "total assets of the previous year")
    lev = _div(_get(statements, t, "long_term_debt"), _average(ta_t, ta_t1), "average total assets")
    lev_prev = _div(_get(statements, t1, "long_term_debt"), _average(ta_t1, ta_t2), "average total assets")
    cr = _div(_get(statements, t, "current_assets"), _get(statements, t, "current_liabilities"), "liabilities")
    cr_prev = _div(_get(statements, t1, "current_assets"), _get(statements, t1, "current_liabilities"), "liabilities")
    rev_t, rev_t1 = _get(statements, t, "revenue"), _get(statements, t1, "revenue")
    gm = _div(rev_t - _get(statements, t, "cogs"), rev_t, "revenue")
    gm_prev = _div(rev_t1 - _get(statements, t1, "cogs"), rev_t1, "revenue")
    ato = _div(rev_t, ta_t1, "total assets of the previous year")
    ato_prev = _div(rev_t1, ta_t2, "total assets two years back")
    shares = _get(statements, t, "shares_outstanding")
    shares_prev = _get(statements, t1, "shares_outstanding")
    signals = (
        int(roa > 0.0),
        int(cfo > 0.0),
        int(roa > roa_prev),
        int(cfo > roa),
        int(lev < lev_prev),
        int(cr > cr_prev),
        int(shares <= shares_prev),
        int(gm > gm_prev),
        int(ato > ato_prev),
    )
    return {"signals": signals, "score": sum(signals)}


def beneish_m_score(statements: Statements, period_end: str) -> dict[str, float]:
    """Beneish (1999) eight-variable M-score on the period end and the previous year end.

    The constants are UNCONFIRMED (see instance.BENEISH_STATUS).
    """
    t = _period(period_end)
    t1 = _previous(statements, t)

    def g(end: str, item: str) -> float:
        return _get(statements, end, item)

    rev, rev1 = g(t, "revenue"), g(t1, "revenue")
    gm = _div(rev - g(t, "cogs"), rev, "revenue")
    gm1 = _div(rev1 - g(t1, "cogs"), rev1, "revenue")
    ta, ta1 = g(t, "total_assets"), g(t1, "total_assets")
    ppe, ppe1 = g(t, "ppe"), g(t1, "ppe")
    dep, dep1 = g(t, "depreciation"), g(t1, "depreciation")
    dsri = _div(_div(g(t, "receivables"), rev, "revenue"), _div(g(t1, "receivables"), rev1, "revenue"), "DSRI base")
    gmi = _div(gm1, gm, "gross margin")
    aqi = _div(
        1.0 - _div(g(t, "current_assets") + ppe, ta, "total assets"),
        1.0 - _div(g(t1, "current_assets") + ppe1, ta1, "total assets"),
        "AQI base",
    )
    sgi = _div(rev, rev1, "revenue")
    depi = _div(
        _div(dep1, dep1 + ppe1, "depreciation plus PP&E"),
        _div(dep, dep + ppe, "depreciation plus PP&E"),
        "DEPI base",
    )
    sgai = _div(_div(g(t, "sga"), rev, "revenue"), _div(g(t1, "sga"), rev1, "revenue"), "SGAI base")
    lvgi = _div(
        _div(statements[t]["current_liabilities"] + g(t, "long_term_debt"), ta, "total assets"),
        _div(g(t1, "current_liabilities") + g(t1, "long_term_debt"), ta1, "total assets"),
        "LVGI base",
    )
    tata = _div(g(t, "net_income") - g(t, "cfo"), ta, "total assets")
    variables = {
        "DSRI": dsri,
        "GMI": gmi,
        "AQI": aqi,
        "SGI": sgi,
        "DEPI": depi,
        "SGAI": sgai,
        "LVGI": lvgi,
        "TATA": tata,
    }
    m = BENEISH_INTERCEPT + sum(BENEISH_COEFFICIENTS[name] * value for name, value in variables.items())
    if not math.isfinite(m):
        raise ValueError("the M-score is not finite")
    return {**variables, "m_score": m}
