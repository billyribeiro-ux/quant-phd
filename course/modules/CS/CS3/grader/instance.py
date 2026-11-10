"""Per-learner instances for the CS3 Atlas A2 data layer autograder.

make_instance(seed) is deterministic: the same seed always produces the same instance,
and different seeds produce different simulated fixture payloads and timestamps.
All payloads are SIMULATED: synthetic test fixtures, no issuer licence applies.
"""

from __future__ import annotations

import hashlib
import json
import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic test instance for a given workspace seed."""
    rng = random.Random(seed)

    # 1. Base dates
    base_year = 2020 + (seed % 3)
    dates = [
        f"{base_year}-01-10",
        f"{base_year}-01-15",
        f"{base_year}-01-20",
        f"{base_year}-01-25",
        f"{base_year}-01-30",
    ]

    # 2. FRED simulated CSV
    fred_val1 = round(1.50 + rng.uniform(0.01, 0.50), 2)
    fred_val2 = round(fred_val1 + rng.uniform(-0.10, 0.10), 2)
    fred_val3 = round(fred_val2 + rng.uniform(-0.10, 0.10), 2)
    fred_val4 = round(fred_val3 + rng.uniform(-0.10, 0.10), 2)
    fred_val5 = round(fred_val4 + rng.uniform(-0.10, 0.10), 2)

    fred_lines = [
        "date,DGS10,FEDFUNDS",
        f"{dates[0]},{fred_val1:.2f},{fred_val1 - 0.25:.2f}",
        f"{dates[1]},{fred_val2:.2f},{fred_val2 - 0.25:.2f}",
        f"{dates[2]},{fred_val3:.2f},{fred_val3 - 0.25:.2f}",
        f"{dates[3]},{fred_val4:.2f},{fred_val4 - 0.25:.2f}",
        f"{dates[4]},{fred_val5:.2f},{fred_val5 - 0.25:.2f}",
    ]
    fred_csv = ("\n".join(fred_lines) + "\n").encode("utf-8")
    fred_retrieved = f"{base_year}-02-01T12:00:00Z"

    # 3. FRED revision simulated CSV (revised values for dates[3] and dates[4], released later)
    rev_fred_val4 = round(fred_val4 + 0.05, 2)
    rev_fred_val5 = round(fred_val5 + 0.08, 2)
    rev_lines = [
        "date,DGS10,FEDFUNDS",
        f"{dates[3]},{rev_fred_val4:.2f},{rev_fred_val4 - 0.25:.2f}",
        f"{dates[4]},{rev_fred_val5:.2f},{rev_fred_val5 - 0.25:.2f}",
    ]
    fred_rev_csv = ("\n".join(rev_lines) + "\n").encode("utf-8")
    fred_rev_retrieved = f"{base_year}-02-15T12:00:00Z"

    # 4. Treasury simulated CSV
    ust_val1 = round(2.00 + rng.uniform(0.01, 0.50), 2)
    ust_lines = [
        "date,BC_10YEAR,BC_3MONTH",
        f"{dates[0]},{ust_val1:.2f},{ust_val1 - 0.50:.2f}",
        f"{dates[1]},{ust_val1 + 0.02:.2f},{ust_val1 - 0.48:.2f}",
    ]
    treasury_csv = ("\n".join(ust_lines) + "\n").encode("utf-8")
    treasury_retrieved = f"{base_year}-02-05T08:00:00Z"

    # 5. French simulated CSV
    french_lines = [
        "date,Mkt_RF,SMB,HML",
        f"{dates[0]},0.12,-0.05,0.08",
        f"{dates[1]},-0.45,0.10,-0.15",
    ]
    french_csv = ("\n".join(french_lines) + "\n").encode("utf-8")
    french_retrieved = f"{base_year}-02-06T09:00:00Z"

    # 6. Shiller simulated CSV
    shiller_p = round(3000.0 + rng.uniform(10.0, 500.0), 1)
    shiller_lines = [
        "date,P,DIV,CPI",
        f"{dates[0]},{shiller_p:.1f},55.2,258.1",
        f"{dates[1]},{shiller_p + 15.0:.1f},55.4,258.4",
    ]
    shiller_csv = ("\n".join(shiller_lines) + "\n").encode("utf-8")
    shiller_retrieved = f"{base_year}-02-07T10:00:00Z"

    # 7. EDGAR raw payload
    cik = f"{100000 + (seed % 899999):010d}"
    edgar_dict = {"cik": cik, "entityName": f"SIMULATED Corp {seed}", "facts": {"revenues": 125000000}}
    edgar_raw = json.dumps(edgar_dict, sort_keys=True).encode("utf-8")
    edgar_retrieved = f"{base_year}-02-08T18:00:00Z"

    # Precomputed expectations
    expected_asof_queries = [
        {
            "desc": "fred_before_any_observation",
            "source": "fred",
            "series": "DGS10",
            "t": f"{base_year}-01-05T00:00:00Z",
            "expected": None,
        },
        {
            "desc": "fred_point_in_time_before_first_retrieval",
            "source": "fred",
            "series": "DGS10",
            "t": f"{base_year}-01-20T12:00:00Z",  # date is valid, but retrieved is later
            "expected": None,
        },
        {
            "desc": "fred_after_first_retrieval_before_revision",
            "source": "fred",
            "series": "DGS10",
            "t": f"{base_year}-02-05T00:00:00Z",
            "expected": {
                "source": "fred",
                "series": "DGS10",
                "date": dates[4],
                "value": f"{fred_val5:.2f}",
                "retrieved": fred_retrieved,
            },
        },
        {
            "desc": "fred_after_revision_point_in_time",
            "source": "fred",
            "series": "DGS10",
            "t": f"{base_year}-02-20T00:00:00Z",
            "expected": {
                "source": "fred",
                "series": "DGS10",
                "date": dates[4],
                "value": f"{rev_fred_val5:.2f}",
                "retrieved": fred_rev_retrieved,
            },
        },
        {
            "desc": "treasury_lookup",
            "source": "treasury",
            "series": "BC_10YEAR",
            "t": f"{base_year}-02-10T00:00:00Z",
            "expected": {
                "source": "treasury",
                "series": "BC_10YEAR",
                "date": dates[1],
                "value": f"{ust_val1 + 0.02:.2f}",
                "retrieved": treasury_retrieved,
            },
        },
    ]

    payload = {
        "seed": seed,
        "base_year": base_year,
        "fred_csv_hex": fred_csv.hex(),
        "fred_retrieved": fred_retrieved,
        "fred_sha256": hashlib.sha256(fred_csv).hexdigest(),
        "fred_rows": 5,
        "fred_rev_csv_hex": fred_rev_csv.hex(),
        "fred_rev_retrieved": fred_rev_retrieved,
        "fred_rev_sha256": hashlib.sha256(fred_rev_csv).hexdigest(),
        "fred_rev_rows": 2,
        "treasury_csv_hex": treasury_csv.hex(),
        "treasury_retrieved": treasury_retrieved,
        "treasury_sha256": hashlib.sha256(treasury_csv).hexdigest(),
        "treasury_rows": 2,
        "french_csv_hex": french_csv.hex(),
        "french_retrieved": french_retrieved,
        "french_sha256": hashlib.sha256(french_csv).hexdigest(),
        "french_rows": 2,
        "shiller_csv_hex": shiller_csv.hex(),
        "shiller_retrieved": shiller_retrieved,
        "shiller_sha256": hashlib.sha256(shiller_csv).hexdigest(),
        "shiller_rows": 2,
        "edgar_raw_hex": edgar_raw.hex(),
        "edgar_retrieved": edgar_retrieved,
        "edgar_sha256": hashlib.sha256(edgar_raw).hexdigest(),
        "expected_asof_queries": expected_asof_queries,
    }

    return {
        "seed": seed,
        "label": f"SIMULATED data layer instance {seed}",
        "payload": json.dumps(payload, sort_keys=True),
    }
