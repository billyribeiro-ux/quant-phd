"""Lab MS2-project-1: Rung 1 worked example for batch-auction counterfactual.

Simulates an order stream under continuous trading (CLOB) and frequent batch auctions (FBA),
computing latency arbitrage rents, market maker PnL, and investor welfare.
"""

from __future__ import annotations

import math
import random
from typing import Any


def run_worked_example() -> None:
    rng = random.Random(42)
    initial_price = 100.0
    half_spread = 0.05
    mm_latency = 2.5
    sniper_latencies = [0.8, 1.2, 1.5]
    batch_interval = 100.0

    print("Step 1 | Generating order stream: 60 events (jumps and investor orders)")
    events: list[dict[str, Any]] = []
    current_time = 0.0
    for _ in range(60):
        current_time += round(rng.expovariate(0.05) + 0.1, 2)
        u = rng.random()
        if u < 0.25:
            delta = round(rng.choice([-1.0, 1.0]) * rng.uniform(0.10, 0.25), 4)
            events.append({"time": round(current_time, 2), "type": "jump", "price_delta": delta, "size": 1})
        elif u < 0.625:
            events.append({"time": round(current_time, 2), "type": "investor_buy", "price_delta": 0.0, "size": 1})
        else:
            events.append({"time": round(current_time, 2), "type": "investor_sell", "price_delta": 0.0, "size": 1})

    t0 = events[0]["time"]
    t_end = events[-1]["time"]
    print(f"Step 1 | Generated {len(events)} events. First event at t={t0}ms, last at t={t_end}ms")

    # Step 2: Continuous limit order book simulation
    mid_clob = initial_price
    fastest_sniper = min(sniper_latencies)
    clob_rents = 0.0
    clob_snipe_count = 0
    clob_trades = 0
    mm_cash_clob = 0.0
    mm_inv_clob = 0

    for e in events:
        t = e["type"]
        sz = e["size"]
        if t == "jump":
            d = e["price_delta"]
            if fastest_sniper < mm_latency:
                if d > half_spread:
                    p = mid_clob + half_spread
                    new_m = mid_clob + d
                    r = (new_m - p) * sz
                    clob_rents += r
                    clob_snipe_count += 1
                    clob_trades += 1
                    mm_cash_clob += p * sz
                    mm_inv_clob -= sz
                elif d < -half_spread:
                    p = mid_clob - half_spread
                    new_m = mid_clob + d
                    r = (p - new_m) * sz
                    clob_rents += r
                    clob_snipe_count += 1
                    clob_trades += 1
                    mm_cash_clob -= p * sz
                    mm_inv_clob += sz
            mid_clob += d
        elif t == "investor_buy":
            p = mid_clob + half_spread
            mm_cash_clob += p * sz
            mm_inv_clob -= sz
            clob_trades += 1
        elif t == "investor_sell":
            p = mid_clob - half_spread
            mm_cash_clob -= p * sz
            mm_inv_clob += sz
            clob_trades += 1

    mm_pnl_clob = mm_cash_clob + mm_inv_clob * mid_clob

    print("Step 2 | Continuous Trading (CLOB) Results:")
    print(f"       | Total Trades:                {clob_trades:d}")
    print(f"       | Latency Arbitrage Trades:    {clob_snipe_count:d}")
    print(f"       | Latency Arbitrage Rents ($): {clob_rents:.4f}")
    print(f"       | Market Maker PnL ($):        {mm_pnl_clob:.4f}")
    print(f"       | Final Mid-Price ($):         {mid_clob:.4f}")

    # Step 3: Frequent Batch Auction simulation
    mid_fba = initial_price
    fba_trades = 0
    mm_cash_fba = 0.0
    mm_inv_fba = 0
    spread_savings = 0.0

    max_t = max(float(e["time"]) for e in events)
    n_batches = math.ceil(max_t / batch_interval) + 1
    batches: list[list[dict[str, Any]]] = [[] for _ in range(n_batches)]
    for e in events:
        batches[int(float(e["time"]) // batch_interval)].append(e)

    for b in batches:
        if not b:
            continue
        buys = 0
        sells = 0
        for e in b:
            if e["type"] == "jump":
                mid_fba += float(e["price_delta"])
            elif e["type"] == "investor_buy":
                buys += int(e["size"])
            elif e["type"] == "investor_sell":
                sells += int(e["size"])

        cross = min(buys, sells)
        if cross > 0:
            spread_savings += cross * half_spread * 2.0
            fba_trades += 1

        imbalance = buys - sells
        if imbalance > 0:
            p = mid_fba + half_spread
            mm_cash_fba += p * imbalance
            mm_inv_fba -= imbalance
            fba_trades += 1
        elif imbalance < 0:
            p = mid_fba - half_spread
            mm_cash_fba -= p * (-imbalance)
            mm_inv_fba += -imbalance
            fba_trades += 1

    mm_pnl_fba = mm_cash_fba + mm_inv_fba * mid_fba

    print("Step 3 | Frequent Batch Auction (FBA, delta=100ms) Results:")
    print(f"       | Batch Clearing Events:       {fba_trades:d}")
    print("       | Latency Arbitrage Trades:    0")
    print("       | Latency Arbitrage Rents ($): 0.0000")
    print(f"       | Multilateral Spread Savings: ${spread_savings:.4f}")
    print(f"       | Market Maker PnL ($):        {mm_pnl_fba:.4f}")
    print(f"       | Final Mid-Price ($):         {mid_fba:.4f}")

    print("Step 4 | Welfare Comparison:")
    print(f"       | Latency Rent Elimination:    ${clob_rents:.4f}")
    print(f"       | Market Maker PnL Gain:       ${mm_pnl_fba - mm_pnl_clob:.4f}")


def main() -> None:
    run_worked_example()


main()
