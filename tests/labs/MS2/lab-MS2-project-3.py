"""Lab MS2-project-3: Rung 3 benchmark parameter grid for research memo.

Evaluates counterfactual continuous trading vs frequent batch auctions
across batch intervals delta in {10.0, 50.0, 100.0, 250.0, 500.0} ms.
Produces the reference output table required for the student report.
"""

from __future__ import annotations

import math
import random
from typing import Any


def simulate_continuous_book(
    events: list[dict[str, Any]],
    initial_price: float,
    half_spread: float,
    mm_latency: float,
    sniper_latencies: list[float],
) -> dict[str, Any]:
    mid_price = float(initial_price)
    fastest_sniper = min(sniper_latencies)

    latency_arbitrage_count = 0
    latency_arbitrage_rents = 0.0
    investor_volume = 0

    mm_cash = 0.0
    mm_inventory = 0

    trades = 0

    for e in events:
        etype = e["type"]
        size = int(e["size"])

        if etype == "jump":
            delta = float(e["price_delta"])
            if fastest_sniper < mm_latency:
                if delta > half_spread:
                    exec_price = mid_price + half_spread
                    new_mid = mid_price + delta
                    rent = (new_mid - exec_price) * size
                    latency_arbitrage_count += 1
                    latency_arbitrage_rents += rent
                    mm_cash += exec_price * size
                    mm_inventory -= size
                    trades += 1
                elif delta < -half_spread:
                    exec_price = mid_price - half_spread
                    new_mid = mid_price + delta
                    rent = (exec_price - new_mid) * size
                    latency_arbitrage_count += 1
                    latency_arbitrage_rents += rent
                    mm_cash -= exec_price * size
                    mm_inventory += size
                    trades += 1
            mid_price += delta

        elif etype == "investor_buy":
            exec_price = mid_price + half_spread
            mm_cash += exec_price * size
            mm_inventory -= size
            investor_volume += size
            trades += 1

        elif etype == "investor_sell":
            exec_price = mid_price - half_spread
            mm_cash -= exec_price * size
            mm_inventory += size
            investor_volume += size
            trades += 1

    mm_pnl = mm_cash + mm_inventory * mid_price

    return {
        "trade_count": trades,
        "latency_arbitrage_count": latency_arbitrage_count,
        "latency_arbitrage_rents": round(latency_arbitrage_rents, 4),
        "mm_pnl": round(mm_pnl, 4),
    }


def simulate_batch_auction(
    events: list[dict[str, Any]],
    initial_price: float,
    half_spread: float,
    batch_interval: float,
) -> dict[str, Any]:
    mid_price = float(initial_price)
    spread_savings = 0.0
    mm_cash = 0.0
    mm_inventory = 0
    trade_count = 0

    max_time = max(float(e["time"]) for e in events)
    num_batches = math.ceil(max_time / batch_interval) + 1
    batches: list[list[dict[str, Any]]] = [[] for _ in range(num_batches)]

    for e in events:
        b_idx = int(float(e["time"]) // batch_interval)
        batches[b_idx].append(e)

    for b_events in batches:
        if not b_events:
            continue

        buy_orders = 0
        sell_orders = 0

        for e in b_events:
            etype = e["type"]
            size = int(e["size"])
            if etype == "jump":
                mid_price += float(e["price_delta"])
            elif etype == "investor_buy":
                buy_orders += size
            elif etype == "investor_sell":
                sell_orders += size

        crossed = min(buy_orders, sell_orders)
        if crossed > 0:
            spread_savings += crossed * half_spread * 2.0
            trade_count += 1

        net = buy_orders - sell_orders
        if net > 0:
            exec_price = mid_price + half_spread
            mm_cash += exec_price * net
            mm_inventory -= net
            trade_count += 1
        elif net < 0:
            exec_price = mid_price - half_spread
            mm_cash -= exec_price * (-net)
            mm_inventory += -net
            trade_count += 1

    mm_pnl = mm_cash + mm_inventory * mid_price

    return {
        "trade_count": trade_count,
        "latency_arbitrage_count": 0,
        "latency_arbitrage_rents": 0.0,
        "spread_savings": round(spread_savings, 4),
        "mm_pnl": round(mm_pnl, 4),
    }


def make_benchmark_instance(seed: int) -> dict[str, Any]:
    rng = random.Random(seed)
    n_events = 120
    initial_price = 100.0
    half_spread = 0.05
    mm_latency = 2.5
    sniper_latencies = [0.8, 1.2, 1.5]
    batch_intervals = [10.0, 50.0, 100.0, 250.0, 500.0]

    events: list[dict[str, Any]] = []
    current_time = 0.0
    for _ in range(n_events):
        current_time += round(rng.expovariate(0.04) + 0.1, 2)
        u = rng.random()
        if u < 0.25:
            delta = round(rng.choice([-1.0, 1.0]) * rng.uniform(0.10, 0.30), 4)
            events.append({"time": round(current_time, 2), "type": "jump", "price_delta": delta, "size": 1})
        elif u < 0.625:
            events.append({"time": round(current_time, 2), "type": "investor_buy", "price_delta": 0.0, "size": 1})
        else:
            events.append({"time": round(current_time, 2), "type": "investor_sell", "price_delta": 0.0, "size": 1})

    return {
        "events": events,
        "initial_price": initial_price,
        "half_spread": half_spread,
        "mm_latency": mm_latency,
        "sniper_latencies": sniper_latencies,
        "batch_intervals": batch_intervals,
    }


def main() -> None:
    inst = make_benchmark_instance(1)
    clob = simulate_continuous_book(
        events=inst["events"],
        initial_price=inst["initial_price"],
        half_spread=inst["half_spread"],
        mm_latency=inst["mm_latency"],
        sniper_latencies=inst["sniper_latencies"],
    )

    print("MS2 Project Report Benchmark Grid (Seed 1, N=120 events, half_spread=0.05):")
    print("Venue / Delta   | Trades | Snipes | Latency Rent ($) | Spread Savings ($) | MM PnL ($)")
    print("--------------------------------------------------------------------------------------")
    print(
        f"Continuous CLOB | {clob['trade_count']:6d} | {clob['latency_arbitrage_count']:6d} | "
        f"${clob['latency_arbitrage_rents']:16.4f} | $            0.0000 | ${clob['mm_pnl']:10.4f}"
    )

    for delta in inst["batch_intervals"]:
        fba = simulate_batch_auction(
            events=inst["events"],
            initial_price=inst["initial_price"],
            half_spread=inst["half_spread"],
            batch_interval=delta,
        )
        print(
            f"FBA delta={delta:4.0f}ms | {fba['trade_count']:6d} | {fba['latency_arbitrage_count']:6d} | "
            f"${fba['latency_arbitrage_rents']:16.4f} | ${fba['spread_savings']:18.4f} | ${fba['mm_pnl']:10.4f}"
        )


main()
