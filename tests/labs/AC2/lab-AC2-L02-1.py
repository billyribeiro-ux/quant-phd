"""AC2 lab L02: ratio analysis and the DuPont identity on a SIMULATED generated filer.

SIMULATED: the filer is generated from a seeded RNG (make_filer, as in Lesson 1's lab). Nothing here is a real
company's data. The ratios follow atlas/A15.contract.md (Ratios, Conventions). The lab checks the identity
roe == net_margin * asset_turnover * leverage to relative 1e-12 in every year that has a previous year, and shows
how the choice of denominator (year-end or average) moves ROE. Standard library only; no network.
"""

from __future__ import annotations

import math
import random
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date
from typing import Any

SEED = 20261027
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
FLOW_ITEMS: frozenset[str] = frozenset(
    {"revenue", "cogs", "sga", "depreciation", "operating_income", "net_income", "cfo"}
)


@dataclass(frozen=True)
class Observation:
    """One parsed observation. Dates are datetime.date; val is a finite float in the filing's unit."""

    end: date
    val: float
    filed: date
    form: str
    fp: str
    accn: str
    start: date | None


def _date(value: object, where: str) -> date:
    """Parse an ISO date with date.fromisoformat; anything else raises ValueError."""
    if not isinstance(value, str):
        raise ValueError(f"{where} must be an ISO date string, not {type(value).__name__}")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{where} is not an ISO date: {value!r}") from exc


def _observation(raw: object, tag: str, unit: str) -> Observation:
    """Validate one raw observation; a missing or malformed required key raises ValueError."""
    where = f"{tag} [{unit}]"
    if not isinstance(raw, Mapping):
        raise ValueError(f"{where}: an observation must be a mapping")
    for key in ("end", "val", "filed", "form"):
        if key not in raw:
            raise ValueError(f"{where}: observation lacks {key!r}")
    value = raw["val"]
    if isinstance(value, bool) or not isinstance(value, int | float) or not math.isfinite(value):
        raise ValueError(f"{where}: val must be a finite number, not {value!r}")
    form = raw["form"]
    if not isinstance(form, str):
        raise ValueError(f"{where}: form must be a string")
    fp = raw.get("fp", "")
    accn = raw.get("accn", "")
    if not isinstance(fp, str) or not isinstance(accn, str):
        raise ValueError(f"{where}: fp and accn must be strings when present")
    start = _date(raw["start"], f"{where}: start") if "start" in raw else None
    return Observation(
        end=_date(raw["end"], f"{where}: end"),
        val=float(value),
        filed=_date(raw["filed"], f"{where}: filed"),
        form=form,
        fp=fp,
        accn=accn,
        start=start,
    )


def _is_annual(obs: Observation, flow: bool) -> bool:
    """Annual: form 10-K*, fp FY, and a 350-380 day duration (flow) or no start date (instant)."""
    if not obs.form.startswith("10-K") or obs.fp != "FY":
        return False
    if flow:
        return obs.start is not None and 350 <= (obs.end - obs.start).days <= 380
    return obs.start is None


def _us_gaap(facts: Mapping[str, Any]) -> Mapping[str, Any]:
    """Return the us-gaap block; a mapping without 'facts' raises ValueError."""
    if not isinstance(facts, Mapping) or "facts" not in facts:
        raise ValueError("the company-facts mapping lacks 'facts'")
    block = facts["facts"]
    if not isinstance(block, Mapping):
        raise ValueError("'facts' must be a mapping")
    gaap = block.get("us-gaap", {})
    if not isinstance(gaap, Mapping):
        raise ValueError("'facts[us-gaap]' must be a mapping")
    return gaap


def _as_of_pick(
    gaap: Mapping[str, Any], tag: str, unit: str, flow: bool, cutoff: date | None
) -> dict[date, Observation]:
    """For one tag: per period end, the annual observation with the greatest (filed, accn) among filed <= cutoff."""
    block = gaap.get(tag)
    if block is None:
        return {}
    if not isinstance(block, Mapping) or not isinstance(block.get("units", {}), Mapping):
        raise ValueError(f"{tag}: must be a mapping with a 'units' mapping")
    rows = block.get("units", {}).get(unit, [])
    if not isinstance(rows, list):
        raise ValueError(f"{tag} [{unit}]: observations must be a list")
    candidates: dict[date, list[Observation]] = {}
    for raw in rows:
        obs = _observation(raw, tag, unit)
        if not _is_annual(obs, flow):
            continue
        if cutoff is not None and obs.filed > cutoff:
            continue
        candidates.setdefault(obs.end, []).append(obs)
    best: dict[date, Observation] = {}
    for end, group in candidates.items():
        # Rank by (filed, accn or ""), best first. Contract: if the two best tie on that key and carry different
        # val, the facts are inconsistent and standardize raises ValueError. Equal values are not a conflict.
        ranked = sorted(group, key=lambda o: (o.filed, o.accn), reverse=True)
        top = ranked[0]
        if len(ranked) > 1:
            runner = ranked[1]
            if (top.filed, top.accn) == (runner.filed, runner.accn) and top.val != runner.val:
                raise ValueError(
                    f"{tag} at period end {end.isoformat()}: two annual observations tie on "
                    f"(filed {top.filed.isoformat()}, accn {top.accn!r}) with different values "
                    f"{top.val!r} and {runner.val!r}"
                )
        best[end] = top
    return best


def select(facts: Mapping[str, Any], as_of: str | None = None) -> dict[str, dict[date, tuple[str, Observation]]]:
    """Per item and period end, the winning (tag, observation) under the tag priority and the as-of rule."""
    cutoff = None if as_of is None else _date(as_of, "as_of")
    gaap = _us_gaap(facts)
    out: dict[str, dict[date, tuple[str, Observation]]] = {}
    for item in ITEMS:
        flow = item in FLOW_ITEMS
        unit = "shares" if item == "shares_outstanding" else "USD"
        per_tag = {tag: _as_of_pick(gaap, tag, unit, flow, cutoff) for tag in TAG_PRIORITY[item]}
        ends: set[date] = set()
        for picks in per_tag.values():
            ends.update(picks)
        winners: dict[date, tuple[str, Observation]] = {}
        for end in ends:
            for tag in TAG_PRIORITY[item]:
                if end in per_tag[tag]:
                    winners[end] = (tag, per_tag[tag][end])
                    break
        out[item] = winners
    return out


def standardize(facts: Mapping[str, Any], as_of: str | None = None) -> dict[str, dict[str, float]]:
    """{period_end_iso: {item: value}}, period ends ascending; absent items are absent (nothing imputed)."""
    picked = select(facts, as_of)
    table: dict[date, dict[str, float]] = {}
    for item in ITEMS:
        for end, (_tag, obs) in picked[item].items():
            table.setdefault(end, {})[item] = obs.val
    return {end.isoformat(): table[end] for end in sorted(table)}


def make_filer(seed: int = SEED) -> dict[str, Any]:
    """A SIMULATED company-facts mapping: five fiscal years, 10-K comparatives, a restatement, a 10-Q, a Q4 row."""
    rng = random.Random(seed)
    years = (2020, 2021, 2022, 2023, 2024)
    rev = {2020: 1_000_000_000}
    for y in years[1:]:
        rev[y] = round(rev[y - 1] * (1 + rng.uniform(0.04, 0.09)))
    cogs = {y: round(rev[y] * rng.uniform(0.58, 0.64)) for y in years}
    sga = {y: round(rev[y] * rng.uniform(0.18, 0.22)) for y in years}
    noise = {y: round(rev[y] * rng.uniform(-0.03, 0.03)) for y in years}
    dep: dict[int, int] = {2020: 38_000_000}
    ppe: dict[int, int] = {2020: 400_000_000}
    for y in years[1:]:
        dep[y] = round(ppe[y - 1] * 0.10)
        ppe[y] = ppe[y - 1] + round(rev[y] * 0.06) - dep[y]
    oi = {y: rev[y] - cogs[y] - sga[y] - dep[y] for y in years}
    ni = {y: round(oi[y] * 0.75) for y in years}
    cfo = {y: ni[y] + dep[y] + noise[y] for y in years}
    eq: dict[int, int] = {2020: 600_000_000}
    for y in years[1:]:
        eq[y] = eq[y - 1] + ni[y] - round(0.4 * ni[y])
    ltd = {y: 300_000_000 + 10_000_000 * (y - 2020) for y in years}
    cash = {y: round(rev[y] * 0.08) for y in years}
    recv = {y: round(rev[y] * 0.12) for y in years}
    inv = {y: round(cogs[y] * 0.15) for y in years}
    other_ca = {y: round(rev[y] * 0.03) for y in years}
    ca = {y: cash[y] + recv[y] + inv[y] + other_ca[y] for y in years}
    cl = {y: round(cogs[y] * 0.25) for y in years}
    ol = {y: round(rev[y] * 0.05) for y in years}
    tl = {y: cl[y] + ltd[y] + ol[y] for y in years}
    ta = {y: tl[y] + eq[y] for y in years}
    shares = {y: 50_000_000 if y < 2024 else 52_000_000 for y in years}

    def fy_tag(item: str, fy: int) -> str:
        if item == "revenue":
            return "Revenues" if fy <= 2021 else "RevenueFromContractWithCustomerExcludingAssessedTax"
        if item == "cogs":
            return "CostOfRevenue" if fy <= 2022 else "CostOfGoodsAndServicesSold"
        return TAG_PRIORITY[item][0]

    truth: dict[str, dict[int, int]] = {
        "revenue": rev,
        "cogs": cogs,
        "sga": sga,
        "depreciation": dep,
        "operating_income": oi,
        "net_income": ni,
        "cfo": cfo,
        "total_assets": ta,
        "current_assets": ca,
        "cash": cash,
        "receivables": recv,
        "ppe": ppe,
        "total_liabilities": tl,
        "current_liabilities": cl,
        "long_term_debt": ltd,
        "equity": eq,
        "shares_outstanding": shares,
    }
    flows = {"revenue", "cogs", "sga", "depreciation", "operating_income", "net_income", "cfo"}
    gaap: dict[str, dict[str, dict[str, list[dict[str, Any]]]]] = {}

    def add(item: str, fy: int, end_year: int, val: int, form: str, fp: str, accn: str, filed: str) -> None:
        tag = fy_tag(item, fy)
        unit = "shares" if item == "shares_outstanding" else "USD"
        obs: dict[str, Any] = {"end": f"{end_year}-12-31", "val": val, "filed": filed, "form": form, "fp": fp}
        if item in flows:
            obs["start"] = f"{end_year}-01-01"  # a full fiscal year, 365 days
            if fp == "Q1":
                obs["end"] = f"{end_year}-03-31"
            if fp == "Q4":
                obs["start"] = f"{end_year}-10-01"
        obs["accn"] = accn
        units: dict[str, list[dict[str, Any]]] = gaap.setdefault(tag, {"units": {}})["units"]
        units.setdefault(unit, []).append(obs)

    for fy in years:
        filed = f"{fy + 1}-02-15"
        accn = f"SIM-{fy}-K"
        for end_year in (fy, fy - 1):
            if end_year < 2020:
                continue
            for item in truth:
                if item == "long_term_debt" and end_year == 2020:
                    continue  # never published: the 2020 long-term debt is absent from the file
                add(item, fy, end_year, truth[item][end_year], "10-K", "FY", accn, filed)
        if fy == 2023:
            add("revenue", fy, 2023, rev[2023] // 4, "10-K", "Q4", accn, filed)
    # Restatement of FY2022 revenue, filed later as a 10-K/A.
    add("revenue", 2023, 2022, round(rev[2022] * 1.012), "10-K/A", "FY", "SIM-2023-KA", "2024-03-01")
    # Quarterly revenue from 10-Q filings: never annual, so the rules ignore them.
    for fy in years[1:]:
        add("revenue", fy, fy, rev[fy] // 4, "10-Q", "Q1", f"SIM-{fy}-Q1", f"{fy}-05-10")
    return {
        "cik": 1,
        "entityName": "SIMULATED FILER 1 (generated; not a real company)",
        "facts": {"us-gaap": gaap},
    }


Statements = Mapping[str, Mapping[str, float]]


def _previous_year(statements: Statements, period_end: str) -> str:
    """The latest period end 350 to 380 days before period_end; none raises ValueError."""
    end = _date(period_end, "period_end")
    earlier = [e for e in statements if 350 <= (end - date.fromisoformat(e)).days <= 380]
    if not earlier:
        raise ValueError(f"no previous year for {period_end}: no period end 350 to 380 days earlier")
    return max(earlier, key=date.fromisoformat)


def _item(statements: Statements, period_end: str, item: str) -> float:
    row = statements.get(period_end)
    if row is None:
        raise ValueError(f"no statement for period end {period_end}")
    if item not in row:
        raise ValueError(f"{item} is missing for period end {period_end}")
    return row[item]


def _average(statements: Statements, period_end: str, item: str) -> float:
    """(x_t + x_{t-1}) / 2 of year-end balances."""
    previous = _previous_year(statements, period_end)
    return (_item(statements, period_end, item) + _item(statements, previous, item)) / 2


def _ratio(numerator: float, denominator: float, name: str) -> float:
    """A zero denominator or a non-finite result raises ValueError."""
    if denominator == 0:
        raise ValueError(f"{name}: zero denominator")
    value = numerator / denominator
    if not math.isfinite(value):
        raise ValueError(f"{name}: non-finite result")
    return value


def dupont(statements: Statements, period_end: str) -> dict[str, float]:
    """net_margin, asset_turnover, leverage, roe, roa on average balances (A15 contract, Ratios)."""
    net_income = _item(statements, period_end, "net_income")
    revenue = _item(statements, period_end, "revenue")
    avg_assets = _average(statements, period_end, "total_assets")
    avg_equity = _average(statements, period_end, "equity")
    net_margin = _ratio(net_income, revenue, "net_margin")
    asset_turnover = _ratio(revenue, avg_assets, "asset_turnover")
    leverage = _ratio(avg_assets, avg_equity, "leverage")
    return {
        "net_margin": net_margin,
        "asset_turnover": asset_turnover,
        "leverage": leverage,
        "roe": _ratio(net_income, avg_equity, "roe"),
        "roa": _ratio(net_income, avg_assets, "roa"),
    }


def current_ratio(statements: Statements, period_end: str) -> float:
    return _ratio(
        _item(statements, period_end, "current_assets"),
        _item(statements, period_end, "current_liabilities"),
        "current_ratio",
    )


def gross_margin(statements: Statements, period_end: str) -> float:
    revenue = _item(statements, period_end, "revenue")
    return _ratio(revenue - _item(statements, period_end, "cogs"), revenue, "gross_margin")


def debt_to_assets(statements: Statements, period_end: str) -> float:
    return _ratio(
        _item(statements, period_end, "long_term_debt"),
        _item(statements, period_end, "total_assets"),
        "debt_to_assets",
    )


def days_sales_outstanding(statements: Statements, period_end: str) -> float:
    revenue = _item(statements, period_end, "revenue")
    return _ratio(_item(statements, period_end, "receivables"), revenue, "dso") * 365


def scaled(statements: Statements, factor: float) -> dict[str, dict[str, float]]:
    """Every money item times factor; shares are left alone. Ratios must not change."""
    return {
        end: {k: (v if k == "shares_outstanding" else v * factor) for k, v in row.items()}
        for end, row in statements.items()
    }


def tie_filer(first: float, second: float) -> dict[str, Any]:
    """A SIMULATED one-tag mapping with two annual observations filed the same day under the same accession."""
    row = {"end": "2023-12-31", "filed": "2024-02-15", "form": "10-K", "fp": "FY", "accn": "SIM-2023-K"}
    rows = [{**row, "val": first}, {**row, "val": second}]
    return {"facts": {"us-gaap": {"Assets": {"units": {"USD": rows}}}}}


def millions(value: float) -> str:
    return f"{value / 1e6:,.1f}"


def main() -> None:
    filer = make_filer()
    statements = standardize(filer)
    ends = list(statements)
    print("DuPont decomposition, average balances (SIMULATED filer 1)")
    print("period_end  net_margin  asset_turn  leverage     roe      roa  identity_ok")
    for end in ends[1:]:
        d = dupont(statements, end)
        product = d["net_margin"] * d["asset_turnover"] * d["leverage"]
        identity_ok = abs(d["roe"] - product) <= 1e-12 * abs(d["roe"])
        print(
            f"{end}  {d['net_margin']:10.4f}  {d['asset_turnover']:10.4f}  {d['leverage']:8.4f}"
            f"  {d['roe']:7.4f}  {d['roa']:7.4f}  {identity_ok}"
        )

    print("other ratios (SIMULATED): year-end balances, except gross margin, which uses only the year's flows")
    print("period_end  current_ratio  gross_margin  debt_to_assets  dso_days")
    for end in ends:
        ltd = "absent" if "long_term_debt" not in statements[end] else f"{debt_to_assets(statements, end):.4f}"
        print(
            f"{end}  {current_ratio(statements, end):13.4f}  {gross_margin(statements, end):12.4f}"
            f"  {ltd:>14}  {days_sales_outstanding(statements, end):8.2f}"
        )

    y2022 = "2022-12-31"
    avg_eq = _average(statements, y2022, "equity")
    year_end_roe = _item(statements, y2022, "net_income") / _item(statements, y2022, "equity")
    print(
        f"FY2022 ROE: average equity {avg_eq / 1e6:,.1f} USD m gives {dupont(statements, y2022)['roe']:.4f};"
        f" year-end equity gives {year_end_roe:.4f}"
    )

    restated = dupont(standardize(filer), y2022)
    original = dupont(standardize(filer, as_of="2023-06-30"), y2022)
    print(f"FY2022 net margin: as filed {original['net_margin']:.4f}, restated {restated['net_margin']:.4f}")

    end = "2022-12-31"
    d = dupont(statements, end)
    year_end_assets = _item(statements, end, "total_assets")
    mismatched = d["net_margin"] * (_item(statements, end, "revenue") / year_end_assets) * d["leverage"]
    print(
        f"identity with year-end assets in turnover but average in leverage: {mismatched:.4f}"
        f" against roe {d['roe']:.4f}"
    )

    earlier, later = dupont(statements, "2023-12-31"), dupont(statements, "2024-12-31")
    log_total = math.log(later["roe"] / earlier["roe"])
    print(f"log change in ROE, 2023 to 2024: {log_total:.4f}")
    for factor in ("net_margin", "asset_turnover", "leverage"):
        share = math.log(later[factor] / earlier[factor])
        print(f"  {factor}: log change {share:.4f}, share of the change {100 * share / log_total:.1f}%")

    for label, payload in (
        ("conflicting tie", tie_filer(1.0, 2.0)),
        ("equal-valued tie", tie_filer(1.0, 1.0)),
    ):
        try:
            standardize(payload)
        except ValueError as exc:
            print(f"ValueError ({label}): {exc}")
        else:
            print(f"no error ({label})")
    scaled_stmt = scaled(statements, 1000.0)
    same = all(
        abs(dupont(scaled_stmt, end)[k] - dupont(statements, end)[k]) <= 1e-12 * abs(dupont(statements, end)[k])
        for end in ends[1:]
        for k in ("net_margin", "asset_turnover", "leverage", "roe", "roa")
    )
    print("ratios unchanged when every money item is multiplied by 1000:", same)

    for label, call in (
        ("dupont at the first period end (no previous year)", lambda: dupont(statements, ends[0])),
        ("debt_to_assets at 2020-12-31 (long_term_debt not published)", lambda: debt_to_assets(statements, ends[0])),
        (
            "dupont with zero revenue",
            lambda: dupont(
                {
                    "2021-12-31": {"net_income": 1.0, "revenue": 0.0, "total_assets": 2.0, "equity": 1.0},
                    "2020-12-31": {"net_income": 1.0, "revenue": 1.0, "total_assets": 2.0, "equity": 1.0},
                },
                "2021-12-31",
            ),
        ),
    ):
        try:
            call()
        except ValueError as exc:
            print(f"ValueError ({label}): {exc}")
        else:
            print(f"no error ({label})")


main()
