"""AC3 project Lab 2: Rung 2 completed solution for the PEAD replication engine.

SIMULATED: the earnings histories, current realizations, and daily return sequences for 10 firms
are generated from fixed deterministic test data. Money and returns are pure floats.
The code executes each step of the PEAD pipeline: SUE computation, decile sorting,
drift CAR evaluation, hedge portfolio spread, and transaction-cost deduction.
"""

from __future__ import annotations

import math
from typing import Any

# SIMULATED panel of 10 firms: 8 quarters of history, quarter 9 actual, and daily returns around day 10
FIRMS_DATA: list[dict[str, Any]] = [
    {"firm_id": "F01", "history": [10.0, 11.0, 12.0, 13.0, 10.5, 11.6, 12.7, 13.8], "current": 10.2},
    {"firm_id": "F02", "history": [20.0, 22.0, 24.0, 26.0, 21.0, 23.1, 25.2, 27.3], "current": 22.5},
    {"firm_id": "F03", "history": [15.0, 15.5, 16.0, 16.5, 15.2, 15.8, 16.3, 16.9], "current": 15.1},
    {"firm_id": "F04", "history": [30.0, 31.0, 32.0, 33.0, 31.0, 32.1, 33.2, 34.3], "current": 33.5},
    {"firm_id": "F05", "history": [25.0, 26.0, 27.0, 28.0, 25.5, 26.6, 27.7, 28.8], "current": 26.0},
    {"firm_id": "F06", "history": [18.0, 19.0, 20.0, 21.0, 18.5, 19.6, 20.7, 21.8], "current": 18.2},
    {"firm_id": "F07", "history": [40.0, 42.0, 44.0, 46.0, 41.5, 43.6, 45.8, 48.0], "current": 44.5},
    {"firm_id": "F08", "history": [12.0, 12.5, 13.0, 13.5, 12.3, 12.9, 13.4, 14.0], "current": 12.1},
    {"firm_id": "F09", "history": [50.0, 52.0, 54.0, 56.0, 51.5, 53.7, 55.9, 58.2], "current": 55.0},
    {"firm_id": "F10", "history": [35.0, 36.0, 37.0, 38.0, 35.8, 36.9, 38.1, 39.3], "current": 37.0},
]

# Daily returns for days 0..15 (announcement at day 10, drift holding period days 12..15)
DAILY_RETURNS: dict[str, list[float]] = {
    "F01": [
        -0.005,
        -0.002,
        0.001,
        -0.003,
        0.000,
        -0.001,
        0.002,
        -0.004,
        0.001,
        -0.002,
        -0.020,
        -0.005,
        -0.008,
        -0.006,
        -0.007,
        -0.005,
    ],
    "F02": [
        0.002,
        0.001,
        0.003,
        -0.001,
        0.002,
        0.001,
        -0.002,
        0.003,
        0.001,
        0.002,
        0.015,
        0.004,
        0.005,
        0.006,
        0.004,
        0.005,
    ],
    "F03": [
        -0.001,
        -0.002,
        0.000,
        -0.001,
        0.001,
        -0.002,
        0.001,
        -0.001,
        0.000,
        -0.002,
        -0.015,
        -0.003,
        -0.006,
        -0.005,
        -0.004,
        -0.005,
    ],
    "F04": [
        0.001,
        0.002,
        -0.001,
        0.002,
        0.001,
        0.000,
        0.003,
        0.001,
        -0.001,
        0.002,
        0.018,
        0.005,
        0.007,
        0.008,
        0.006,
        0.007,
    ],
    "F05": [
        0.000,
        0.001,
        -0.001,
        0.000,
        0.002,
        -0.001,
        0.001,
        0.000,
        0.001,
        -0.001,
        0.002,
        0.001,
        0.001,
        0.000,
        0.001,
        -0.001,
    ],
    "F06": [
        -0.002,
        0.001,
        -0.003,
        0.000,
        -0.001,
        0.002,
        -0.002,
        0.001,
        -0.002,
        0.000,
        -0.012,
        -0.004,
        -0.005,
        -0.004,
        -0.003,
        -0.004,
    ],
    "F07": [
        0.003,
        0.001,
        0.002,
        0.000,
        0.001,
        0.003,
        -0.001,
        0.002,
        0.001,
        0.003,
        0.022,
        0.006,
        0.008,
        0.009,
        0.007,
        0.008,
    ],
    "F08": [
        -0.003,
        -0.001,
        0.000,
        -0.002,
        0.001,
        -0.003,
        0.000,
        -0.002,
        0.001,
        -0.001,
        -0.018,
        -0.005,
        -0.007,
        -0.006,
        -0.005,
        -0.006,
    ],
    "F09": [
        0.002,
        0.003,
        0.001,
        0.002,
        0.000,
        0.002,
        0.001,
        0.003,
        0.002,
        0.001,
        0.025,
        0.007,
        0.009,
        0.010,
        0.008,
        0.009,
    ],
    "F10": [
        0.001,
        0.000,
        0.002,
        -0.001,
        0.001,
        0.000,
        0.002,
        -0.001,
        0.001,
        0.002,
        0.005,
        0.002,
        0.002,
        0.003,
        0.002,
        0.002,
    ],
}


def compute_sue(history: list[float], current: float) -> float:
    """Step 1. Compute SUE under seasonal random walk with drift."""
    if len(history) < 8:
        raise ValueError("Need at least 8 quarters of history")
    diffs = [history[t] - history[t - 4] for t in range(4, len(history))]
    drift = sum(diffs) / len(diffs)
    expected = history[-4] + drift
    raw_error = current - expected

    errors = [d - drift for d in diffs]
    variance = sum(e**2 for e in errors) / (len(errors) - 1)
    std_dev = math.sqrt(variance)
    if std_dev <= 0:
        raise ValueError("Forecast error standard deviation must be positive")
    return raw_error / std_dev


def assign_deciles(scores: dict[str, float]) -> dict[str, int]:
    """Step 2. Sort firms into 10 deciles."""
    if len(scores) < 10:
        raise ValueError("Need at least 10 firms to form 10 deciles")
    sorted_firms = sorted(scores.keys(), key=lambda fid: (scores[fid], fid))
    n = len(sorted_firms)
    deciles: dict[str, int] = {}
    for rank, fid in enumerate(sorted_firms):
        d = min(10, (rank * 10) // n + 1)
        deciles[fid] = d
    return deciles


def compute_drift_returns(
    announcements: list[dict[str, Any]], holding_period: tuple[int, int] = (2, 5)
) -> dict[int, float]:
    """Step 3. Compute post-announcement cumulative abnormal returns per decile."""
    h_start, h_end = holding_period
    decile_cars: dict[int, list[float]] = {d: [] for d in range(1, 11)}

    for item in announcements:
        d = int(item["decile"])
        rets = list(item["daily_returns"])
        t0 = int(item["announcement_day"])

        car = sum(rets[t0 + k] for k in range(h_start, h_end + 1))
        decile_cars[d].append(car)

    return {d: (sum(cars) / len(cars) if cars else 0.0) for d, cars in decile_cars.items()}


def hedge_portfolio(decile_rets: dict[int, float], cost_bps: float = 20.0) -> dict[str, float]:
    """Step 4. Construct long Decile 10, short Decile 1 hedge portfolio net of costs."""
    gross = decile_rets[10] - decile_rets[1]
    cost_deduction = 2.0 * (cost_bps / 10000.0)
    net = gross - cost_deduction
    return {
        "gross_spread": gross,
        "cost_deduction": cost_deduction,
        "net_spread": net,
    }


def main() -> None:
    # 1. Compute SUE
    sue_dict = {f["firm_id"]: compute_sue(f["history"], f["current"]) for f in FIRMS_DATA}
    print("step 1 sue computed for", len(sue_dict), "firms")
    for fid in sorted(sue_dict.keys()):
        print(f"firm {fid} sue {sue_dict[fid]:+.4f}")

    # 2. Assign deciles
    deciles = assign_deciles(sue_dict)
    print("step 2 deciles assigned:")
    for d in range(1, 11):
        fids = [fid for fid, dec in deciles.items() if dec == d]
        print(f"decile {d:2d} : firms {fids}")

    # 3. Drift returns
    announcements = [
        {
            "firm_id": f["firm_id"],
            "decile": deciles[f["firm_id"]],
            "daily_returns": DAILY_RETURNS[f["firm_id"]],
            "announcement_day": 10,
        }
        for f in FIRMS_DATA
    ]
    drift = compute_drift_returns(announcements, holding_period=(2, 5))
    print("step 3 drift returns:")
    for d in range(1, 11):
        print(f"decile {d:2d} car {drift[d]:+.6f}")

    # 4. Hedge portfolio
    hedge = hedge_portfolio(drift, cost_bps=20.0)
    print("step 4 hedge portfolio:")
    print(f"gross_spread {hedge['gross_spread']:+.6f}")
    print(f"cost_deduction {hedge['cost_deduction']:.6f}")
    print(f"net_spread {hedge['net_spread']:+.6f}")
    print("step 4 net profitable:", hedge["net_spread"] > 0)


main()
