from typing import Any

# SIMULATED filer in the SEC company-facts shape (not a real company). Two fiscal years. The 2022 10-K repeats 2021
# under a different revenue tag, and the 2021 figure is restated by a 10-K/A filed later. A 10-Q fact is present.
FILER = {
    "entityName": "SIMULATED FILER 0001",
    "facts": {
        "us-gaap": {
            "Revenues": {
                "units": {
                    "USD": [
                        {
                            "end": "2021-12-31",
                            "start": "2021-01-01",
                            "val": 1000.0,
                            "filed": "2022-02-25",
                            "form": "10-K",
                            "fp": "FY",
                            "accn": "0000000001-22-000001",
                        },
                        {
                            "end": "2021-12-31",
                            "start": "2021-01-01",
                            "val": 990.0,
                            "filed": "2023-03-20",
                            "form": "10-K/A",
                            "fp": "FY",
                            "accn": "0000000001-23-000007",
                        },
                        {
                            "end": "2022-03-31",
                            "start": "2022-01-01",
                            "val": 300.0,
                            "filed": "2022-05-10",
                            "form": "10-Q",
                            "fp": "Q1",
                            "accn": "0000000001-22-000010",
                        },
                    ]
                }
            },
            "RevenueFromContractWithCustomerExcludingAssessedTax": {
                "units": {
                    "USD": [
                        {
                            "end": "2022-12-31",
                            "start": "2022-01-01",
                            "val": 1200.0,
                            "filed": "2023-02-24",
                            "form": "10-K",
                            "fp": "FY",
                            "accn": "0000000001-23-000002",
                        },
                        {
                            "end": "2021-12-31",
                            "start": "2021-01-01",
                            "val": 1000.0,
                            "filed": "2023-02-24",
                            "form": "10-K",
                            "fp": "FY",
                            "accn": "0000000001-23-000002",
                        },
                    ]
                }
            },
        }
    },
}

# The A15 tag priority for revenue: the first tag with an annual observation for a period end supplies it.
REVENUE_TAGS = ("Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet")


def is_annual(obs: dict[str, str | float], flow: bool) -> bool:
    # Annual: a 10-K for the fiscal year (fp == "FY"), and for a flow item a duration of 350 to 380 days.
    # The 10-Q quarter (fp == "Q1") and any other duration are not annual, so they are ignored.
    if not str(obs["form"]).startswith("10-K") or obs["fp"] != "FY":
        return False
    if not flow:
        return "start" not in obs
    from datetime import date

    days = (date.fromisoformat(str(obs["end"])) - date.fromisoformat(str(obs["start"]))).days
    return 350 <= days <= 380


def revenue_by_period(filer: dict[str, Any], as_of: str | None = None) -> dict[str, float]:
    # Step 1. For each tag, keep the annual observation per period end that is known on as_of (filed <= as_of)
    # and is the latest by (filed, accession number): a later 10-K/A supersedes the original.
    best: dict[str, dict[str, tuple[str, str, float]]] = {}
    for tag in REVENUE_TAGS:
        per_end: dict[str, tuple[str, str, float]] = {}
        for obs in filer["facts"]["us-gaap"].get(tag, {}).get("units", {}).get("USD", []):
            if not is_annual(obs, flow=True):
                continue
            if as_of is not None and obs["filed"] > as_of:
                continue
            key = (str(obs["filed"]), str(obs["accn"]))
            current = per_end.get(str(obs["end"]))
            if current is None or key > (current[0], current[1]):
                per_end[str(obs["end"])] = (key[0], key[1], float(obs["val"]))
        best[tag] = per_end
    # Step 2. Walk the tags in priority order: the first tag with a value for a period end supplies it.
    out: dict[str, float] = {}
    for tag in REVENUE_TAGS:
        for end, (_, _, value) in best[tag].items():
            out.setdefault(end, value)
    return dict(sorted(out.items()))


print("revenue, latest knowledge:", revenue_by_period(FILER))
print("revenue, known on 2023-03-01:", revenue_by_period(FILER, "2023-03-01"))
print("revenue, known on 2022-01-31:", revenue_by_period(FILER, "2022-01-31"))
