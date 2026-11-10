"""Mutant: FBA incorrectly awards latency-arbitrage rents by using continuous speed priority inside batches."""

from __future__ import annotations

from typing import Any


def _parse_event(e: Any) -> tuple[float, str, float, int]:
    if isinstance(e, dict):
        return float(e["time"]), str(e["type"]), float(e.get("price_delta", 0.0)), int(e["size"])
    return float(e[0]), str(e[1]), float(e[2]), int(e[3])


def simulate_continuous_book(
    events: list[dict[str, Any]],
    initial_price: float,
    half_spread: float,
    mm_latency: float,
    sniper_latencies: list[float],
) -> dict[str, Any]:
    if initial_price <= 0.0:
        raise ValueError("initial_price must be positive")
    if half_spread <= 0.0:
        raise ValueError("half_spread must be positive")
    if mm_latency <= 0.0:
        raise ValueError("mm_latency must be positive")
    if not sniper_latencies or any(sl <= 0.0 for sl in sniper_latencies):
        raise ValueError("sniper_latencies must be non-empty and strictly positive")
    if not events:
        raise ValueError("events list cannot be empty")

    mid_price = float(initial_price)
    fastest_sniper = min(sniper_latencies)

    latency_arbitrage_count = 0
    latency_arbitrage_volume = 0
    latency_arbitrage_rents = 0.0
    investor_volume = 0

    mm_cash = 0.0
    mm_inventory = 0
    investor_cash = 0.0
    investor_inventory = 0

    trades: list[dict[str, Any]] = []

    last_time = -1.0
    for e in events:
        t, etype, delta, size = _parse_event(e)
        if t < last_time:
            raise ValueError("events must be strictly ordered by timestamp")
        last_time = t

        if size <= 0:
            raise ValueError("order size must be positive")

        if etype == "jump":
            if fastest_sniper < mm_latency:
                if delta > half_spread:
                    exec_price = mid_price + half_spread
                    new_mid = mid_price + delta
                    rent = (new_mid - exec_price) * size
                    latency_arbitrage_count += 1
                    latency_arbitrage_volume += size
                    latency_arbitrage_rents += rent
                    mm_cash += exec_price * size
                    mm_inventory -= size
                    trades.append(
                        {
                            "time": round(t + fastest_sniper, 4),
                            "price": exec_price,
                            "size": size,
                            "type": "latency_arbitrage_buy",
                            "rent": rent,
                        }
                    )
                elif delta < -half_spread:
                    exec_price = mid_price - half_spread
                    new_mid = mid_price + delta
                    rent = (exec_price - new_mid) * size
                    latency_arbitrage_count += 1
                    latency_arbitrage_volume += size
                    latency_arbitrage_rents += rent
                    mm_cash -= exec_price * size
                    mm_inventory += size
                    trades.append(
                        {
                            "time": round(t + fastest_sniper, 4),
                            "price": exec_price,
                            "size": size,
                            "type": "latency_arbitrage_sell",
                            "rent": rent,
                        }
                    )
            mid_price += delta

        elif etype == "investor_buy":
            exec_price = mid_price + half_spread
            mm_cash += exec_price * size
            mm_inventory -= size
            investor_cash -= exec_price * size
            investor_inventory += size
            investor_volume += size
            trades.append({"time": t, "price": exec_price, "size": size, "type": "investor_buy", "rent": 0.0})

        elif etype == "investor_sell":
            exec_price = mid_price - half_spread
            mm_cash -= exec_price * size
            mm_inventory += size
            investor_cash += exec_price * size
            investor_inventory -= size
            investor_volume += size
            trades.append({"time": t, "price": exec_price, "size": size, "type": "investor_sell", "rent": 0.0})
        else:
            raise ValueError(f"unknown event type: {etype}")

    mm_pnl = mm_cash + mm_inventory * mid_price
    investor_pnl = investor_cash + investor_inventory * mid_price

    return {
        "trades": trades,
        "trade_count": len(trades),
        "latency_arbitrage_count": latency_arbitrage_count,
        "latency_arbitrage_volume": latency_arbitrage_volume,
        "latency_arbitrage_rents": round(latency_arbitrage_rents, 6),
        "investor_volume": investor_volume,
        "mm_pnl": round(mm_pnl, 6),
        "investor_pnl": round(investor_pnl, 6),
        "final_price": round(mid_price, 6),
    }


def simulate_batch_auction(
    events: list[dict[str, Any]],
    initial_price: float,
    half_spread: float,
    batch_interval: float,
    mm_latency: float,
    sniper_latencies: list[float],
) -> dict[str, Any]:
    # WRONG: Mutant re-introduces continuous speed priority inside the batch
    clob = simulate_continuous_book(events, initial_price, half_spread, mm_latency, sniper_latencies)
    clob["spread_savings"] = 0.0
    return clob


def run_counterfactual(
    events: list[dict[str, Any]],
    initial_price: float,
    half_spread: float,
    batch_intervals: list[float],
    mm_latency: float,
    sniper_latencies: list[float],
) -> dict[str, Any]:
    clob = simulate_continuous_book(events, initial_price, half_spread, mm_latency, sniper_latencies)
    fba_results: dict[str, Any] = {}
    for delta in batch_intervals:
        fba_results[f"delta_{delta:g}"] = simulate_batch_auction(
            events, initial_price, half_spread, delta, mm_latency, sniper_latencies
        )
    return {"continuous": clob, "batch_auctions": fba_results, "rent_savings": clob["latency_arbitrage_rents"]}
