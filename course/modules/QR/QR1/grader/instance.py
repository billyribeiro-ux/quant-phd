"""Per-learner instances for the QR1 research data engineering autograder.

make_instance(seed) is deterministic: the same seed always produces the identical instance,
and different seeds produce distinct simulated revision trajectories, ticks, and split events.
All payloads are SIMULATED: synthetic test fixtures, no real issuer licence applies.
"""

from __future__ import annotations

import json
import random
from typing import Any

SOURCES: tuple[str, ...] = ("fred", "french", "shiller", "treasury", "edgar")


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic test instance for a given workspace seed."""
    rng = random.Random(seed)

    base_year = 2024 + (seed % 3)

    # 1. Macro Data Vintages (FRED & Treasury)
    obs_dates = [
        f"{base_year}-01-01",
        f"{base_year}-02-01",
        f"{base_year}-03-01",
        f"{base_year}-04-01",
        f"{base_year}-05-01",
    ]

    vintages: list[dict[str, str]] = []
    # Initial advance releases
    base_val = round(100.0 + rng.uniform(5.0, 50.0), 2)
    for i, od in enumerate(obs_dates):
        pub_month = i + 2
        val = round(base_val + i * 1.5 + rng.uniform(-0.5, 0.5), 2)
        vintages.append(
            {
                "source": "fred",
                "series": "CORE_CPI",
                "obs_date": od,
                "value": f"{val:.2f}",
                "published": f"{base_year}-{pub_month:02d}-15T13:30:00Z",
                "retrieved": f"{base_year}-{pub_month:02d}-15T13:35:00Z",
            }
        )

    # Revisions published later for earlier observation dates
    for i in range(3):
        od = obs_dates[i]
        orig_val = float(vintages[i]["value"])
        rev_val = round(orig_val + rng.uniform(0.1, 0.8), 2)
        rev_pub_month = i + 4
        vintages.append(
            {
                "source": "fred",
                "series": "CORE_CPI",
                "obs_date": od,
                "value": f"{rev_val:.2f}",
                "published": f"{base_year}-{rev_pub_month:02d}-15T13:30:00Z",
                "retrieved": f"{base_year}-{rev_pub_month:02d}-15T13:40:00Z",
            }
        )

    # Treasury series (BC_10YEAR)
    ust_val = round(3.50 + rng.uniform(0.1, 1.5), 2)
    for i, od in enumerate(obs_dates[:3]):
        pub_month = i + 2
        vintages.append(
            {
                "source": "treasury",
                "series": "BC_10YEAR",
                "obs_date": od,
                "value": f"{ust_val + i * 0.1:.2f}",
                "published": f"{base_year}-{pub_month:02d}-10T15:00:00Z",
                "retrieved": f"{base_year}-{pub_month:02d}-10T15:01:00Z",
            }
        )

    # Cutoffs for testing visible queries
    cutoffs = [
        f"{base_year}-01-15T00:00:00Z",  # Before any published
        f"{base_year}-02-20T00:00:00Z",  # Post first release
        f"{base_year}-04-20T00:00:00Z",  # Post first revision
        f"{base_year}-08-01T00:00:00Z",  # Post all revisions
    ]

    # 2. Tick Stream Data
    # 20 to 40 ticks with jittered arrival order and a timestamp tie
    n_ticks = 20 + (seed % 15)
    base_price = round(150.0 + rng.uniform(10.0, 50.0), 2)
    tick_records: list[tuple[str, int, float]] = []

    for s in range(1, n_ticks + 1):
        sec = s // 2
        ms = (s % 2) * 500
        ts = f"{base_year}-06-01T09:30:{sec:02d}.{ms:03d}Z"
        px = round(base_price + rng.uniform(-1.0, 1.0), 2)
        tick_records.append((ts, s, px))

    # Add deliberate tie at sequence n_ticks + 1
    tie_ts = f"{base_year}-06-01T09:30:10.000Z"
    tick_records.append((tie_ts, n_ticks + 1, round(base_price + 2.50, 2)))

    # Permute tick order to simulate out-of-order network arrival
    shuffled_ticks = list(tick_records)
    rng.shuffle(shuffled_ticks)

    tick_cutoffs = [
        f"{base_year}-06-01T09:29:59.000Z",
        f"{base_year}-06-01T09:30:05.000Z",
        tie_ts,
        f"{base_year}-06-01T09:31:00.000Z",
    ]

    # 3. Stock Closes & Corporate Action Splits
    dates = [
        f"{base_year}-07-01",
        f"{base_year}-07-02",
        f"{base_year}-07-03",
        f"{base_year}-07-06",
        f"{base_year}-07-07",
        f"{base_year}-07-08",
        f"{base_year}-07-09",
        f"{base_year}-07-10",
    ]

    # 2-for-1 split on 2024/2025/2026-07-06
    split_ex_date = dates[3]
    split_ratio = 2.0
    splits = [(split_ex_date, split_ratio)]

    pre_split_px = round(200.0 + rng.uniform(10.0, 40.0), 2)
    closes: list[float] = []
    for i, d in enumerate(dates):
        if d < split_ex_date:
            closes.append(round(pre_split_px + i * 1.5, 2))
        elif d == split_ex_date:
            # Pure split at ex-date: price divides exactly by split_ratio
            closes.append(closes[-1] / split_ratio)
        else:
            offset = i - dates.index(split_ex_date)
            closes.append(round(closes[dates.index(split_ex_date)] + offset * 1.0, 2))

    # 4. Invalid Case: Selected deterministically from E1..E6 based on seed % 6
    invalid_category = seed % 6
    invalid_case: dict[str, Any]
    if invalid_category == 0:
        # E1: Spring gap in Eastern wall time
        invalid_case = {
            "type": "E1",
            "func": "et_to_utc",
            "kwargs": {"wall": "2026-03-08 02:30"},
            "error_msg": "spring DST gap",
        }
    elif invalid_category == 1:
        # E2: Empty path for VintageIndex
        invalid_case = {
            "type": "E2",
            "func": "VintageIndex",
            "kwargs": {"path": ""},
            "error_msg": "empty path",
        }
    elif invalid_category == 2:
        # E3: Unknown source
        invalid_case = {
            "type": "E3",
            "func": "record",
            "kwargs": {
                "source": "unknown_provider",
                "series": "GDP",
                "obs_date": f"{base_year}-01-01",
                "value": "100.0",
                "published": f"{base_year}-02-01T12:00:00Z",
                "retrieved": f"{base_year}-02-01T12:00:00Z",
            },
            "error_msg": "unknown source",
        }
    elif invalid_category == 3:
        # E4: Naive timestamp in visible
        invalid_case = {
            "type": "E4",
            "func": "visible",
            "kwargs": {
                "source": "fred",
                "series": "CORE_CPI",
                "obs_date": obs_dates[0],
                "t": f"{base_year}-02-01 12:00:00",  # Missing Z
            },
            "error_msg": "naive or malformed timestamp",
        }
    elif invalid_category == 4:
        # E5: Naive timestamp in last_trade_at
        invalid_case = {
            "type": "E5",
            "func": "last_trade_at",
            "kwargs": {
                "ticks": [("2026-01-01T09:30:00Z", 1, 100.0)],
                "t": "2026-01-01 09:30:00",
            },
            "error_msg": "naive or malformed timestamp",
        }
    else:
        # E6: Negative split ratio in adjust_closes
        invalid_case = {
            "type": "E6",
            "func": "adjust_closes",
            "kwargs": {
                "dates": ["2026-01-01", "2026-01-02"],
                "closes": [100.0, 100.0],
                "events": [("2026-01-02", -2.0)],
            },
            "error_msg": "non-positive ratio",
        }

    payload = {
        "seed": seed,
        "base_year": base_year,
        "vintages": vintages,
        "cutoffs": cutoffs,
        "ticks": shuffled_ticks,
        "tick_cutoffs": tick_cutoffs,
        "stock_dates": dates,
        "stock_closes": closes,
        "stock_splits": splits,
        "invalid": invalid_case,
    }

    return {
        "seed": seed,
        "label": f"SIMULATED research data engineering instance {seed}",
        "payload": json.dumps(payload, sort_keys=True),
    }
