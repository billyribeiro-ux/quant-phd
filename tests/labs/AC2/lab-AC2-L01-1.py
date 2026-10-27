"""AC2 lab L01: standardize a company-facts mapping under the A15 rules.

SIMULATED: the filer is generated from a seeded RNG. Its name, CIK and every figure are invented
for this lab and are not a real company's. The rules applied are those of atlas/A15.contract.md:
the annual-observation rule, the as-of rule, the tag priority per period end, and the input checks.
Standard library only; no network; every number printed is computed by the code below.
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


def observation_counts(gaap: Mapping[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for block in gaap.values():
        for rows in block["units"].values():
            for row in rows:
                counts[row["form"]] = counts.get(row["form"], 0) + 1
    return dict(sorted(counts.items()))


def as_of_monotone(facts: Mapping[str, Any], cutoffs: list[str], item: str) -> bool:
    """Proposition 3.1 in the lesson: a later cutoff never selects an earlier filing for a period end."""
    gaap = _us_gaap(facts)
    tag = TAG_PRIORITY[item][0]
    previous: dict[date, date] = {}
    for cut in cutoffs:
        current = {
            end: obs.filed for end, obs in _as_of_pick(gaap, tag, "USD", item in FLOW_ITEMS, _date(cut, "cut")).items()
        }
        for end, filed in previous.items():
            if end in current and current[end] < filed:
                return False
        previous = current
    return True


def tie_filer(first: float, second: float) -> dict[str, Any]:
    """A SIMULATED one-tag mapping with two annual observations filed the same day under the same accession."""
    row = {"end": "2023-12-31", "filed": "2024-02-15", "form": "10-K", "fp": "FY", "accn": "SIM-2023-K"}
    rows = [{**row, "val": first}, {**row, "val": second}]
    return {"facts": {"us-gaap": {"Assets": {"units": {"USD": rows}}}}}


def millions(value: float) -> str:
    return f"{value / 1e6:,.1f}"


def main() -> None:
    filer = make_filer()
    gaap = _us_gaap(filer)
    counts = observation_counts(gaap)
    print("SIMULATED filer: observations by form", counts)

    table = standardize(filer)
    print("standardize(as_of=None): USD millions; source of revenue in brackets")
    picked = select(filer)
    print("period_end  items  revenue  net_income  total_assets  equity  shares_m  revenue_tag")
    for end_iso, items in table.items():
        end = date.fromisoformat(end_iso)
        tag = picked["revenue"][end][0] if end in picked["revenue"] else "absent"
        print(
            f"{end_iso}  {len(items):5d}  {millions(items.get('revenue', math.nan)):>7}"
            f"  {millions(items.get('net_income', math.nan)):>10}  {millions(items.get('total_assets', math.nan)):>12}"
            f"  {millions(items.get('equity', math.nan)):>6}  {items.get('shares_outstanding', math.nan) / 1e6:>8.1f}"
            f"  {tag}"
        )

    before = standardize(filer, as_of="2023-06-30")
    after = standardize(filer)
    print(
        "FY2022 revenue, USD millions: as of 2023-06-30 =",
        millions(before["2022-12-31"]["revenue"]),
        "| as of today =",
        millions(after["2022-12-31"]["revenue"]),
    )
    print("period ends present as of 2023-06-30:", sorted(before))
    print(
        "items present for 2020-12-31 (no long-term debt published):",
        "long_term_debt" in table["2020-12-31"],
        "| 2021-12-31:",
        "long_term_debt" in table["2021-12-31"],
    )
    print(
        "as-of selection never moves to an earlier filing (revenue):",
        as_of_monotone(
            filer, ["2022-03-01", "2023-03-01", "2023-06-30", "2024-02-20", "2024-06-30", "2025-06-30"], "revenue"
        ),
    )

    malformed = {
        "facts": {
            "us-gaap": {"Assets": {"units": {"USD": [{"end": "2023-12-31", "val": 1.0, "form": "10-K", "fp": "FY"}]}}}
        }
    }
    cases: list[tuple[str, Any, str | None]] = [
        ("no 'facts' key", {"cik": 1}, None),
        ("observation without 'filed'", malformed, None),
        (
            "val is a string",
            {
                "facts": {
                    "us-gaap": {
                        "Assets": {
                            "units": {
                                "USD": [
                                    {
                                        "end": "2023-12-31",
                                        "val": "1.0",
                                        "filed": "2024-02-15",
                                        "form": "10-K",
                                        "fp": "FY",
                                    }
                                ]
                            }
                        }
                    }
                }
            },
            None,
        ),
        ("as_of is not a date", filer, "2023-13-01"),
        ("two filings tie on (filed, accn) with different values", tie_filer(1.0, 2.0), None),
        ("two filings tie on (filed, accn) with equal values", tie_filer(1.0, 1.0), None),
    ]
    for label, payload, as_of in cases:
        try:
            standardize(payload, as_of)
        except ValueError as exc:
            print(f"ValueError for {label}: {exc}")
        else:
            print(f"no error for {label}")


if __name__ == "__main__":
    main()
