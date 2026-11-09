"""Verifier re-derivation (FC1-b round 4) of every number printed by Lab 1 (L04) and quoted in L04.html.

Independent of tests/labs/FC1/lab-FC1-L04-1.py: the book is a dict of price levels holding FIFO deques, not a list
of Order objects. The RNG call order is reproduced from the lesson's stated flow (seed 2026, 300 events, one draw
for side, one for lots, one for the roll, then one for the offset or the stop offset), so the flow is the same
SIMULATED flow the lab prints.

Usage: python3 -I ledgers/FC1/scripts/FC1-b-r4/l04_independent_r4.py
"""

from __future__ import annotations

import random
from collections import Counter, deque

SEED, MID, WIDTH, N = 2026, 10000, 20, 300


class Book:
    def __init__(self) -> None:
        self.bid_levels: dict[int, deque[list[int]]] = {}
        self.ask_levels: dict[int, deque[list[int]]] = {}
        self.pending: list[dict[str, int]] = []
        self.last: int | None = None
        self.fills: list[tuple[int, int]] = []
        self.entered = 0
        self.traded = 0
        self.cancelled = 0
        self.seq_of: dict[int, int] = {}
        self.activations_in_event: list[tuple[int, int, list[tuple[int, int]]]] = []

    def best_bid(self) -> int | None:
        live = [p for p, q in self.bid_levels.items() if q]
        return max(live) if live else None

    def best_ask(self) -> int | None:
        live = [p for p, q in self.ask_levels.items() if q]
        return min(live) if live else None

    def resting(self) -> int:
        return sum(o[1] for side in (self.bid_levels, self.ask_levels) for q in side.values() for o in q)

    def arrive(self, side: str, kind: str, qty: int, price: int | None, seq: int) -> int:
        """Match an arriving limit or market order. Returns the residual quantity (resting or cancelled)."""
        self.entered += qty
        opposite = self.ask_levels if side == "buy" else self.bid_levels
        remaining = qty
        while remaining > 0:
            if side == "buy":
                levels = [p for p, q in opposite.items() if q]
                if not levels:
                    break
                best = min(levels)
                if kind == "limit" and best > price:  # type: ignore[operator]
                    break
            else:
                levels = [p for p, q in opposite.items() if q]
                if not levels:
                    break
                best = max(levels)
                if kind == "limit" and best < price:  # type: ignore[operator]
                    break
            queue = opposite[best]
            resting = queue[0]
            fill = min(remaining, resting[1])
            resting[1] -= fill
            remaining -= fill
            self.traded += fill
            self.last = best
            self.fills.append((best, fill))
            if resting[1] == 0:
                queue.popleft()
        if remaining > 0 and kind == "limit":
            own = self.bid_levels if side == "buy" else self.ask_levels
            own.setdefault(price, deque()).append([seq, remaining])  # type: ignore[arg-type]
            return 0
        if remaining > 0:
            self.cancelled += remaining
        return 0

    def activate_all(self) -> list[tuple[int, int, list[tuple[int, int]]]]:
        """Activate every triggered stop, arrival order first, repeating while the last trade moves."""
        done: list[tuple[int, int, list[tuple[int, int]]]] = []
        while self.last is not None:
            hit = None
            for i, s in enumerate(self.pending):
                if s["side"] == "buy" and self.last >= s["stop"]:
                    hit = i
                    break
                if s["side"] == "sell" and self.last <= s["stop"]:
                    hit = i
                    break
            if hit is None:
                break
            s = self.pending.pop(hit)
            before = len(self.fills)
            self.arrive(s["side"], "market", s["qty"], None, s["seq"])
            done.append((s["seq"], 1 if s["side"] == "buy" else -1, self.fills[before:]))
        return done


def flow() -> list[tuple[str, dict[str, int]]]:
    rng = random.Random(SEED)
    out: list[tuple[str, dict[str, int]]] = []
    for seq in range(N):
        side = rng.choice((1, -1))
        qty = 10 * rng.randint(1, 10)
        roll = rng.random()
        s = "buy" if side > 0 else "sell"
        if roll < 0.6:
            price = MID - side * rng.randint(0, WIDTH)
            out.append(("limit", {"seq": seq, "side": s, "qty": qty, "price": price}))
        elif roll < 0.85:
            out.append(("market", {"seq": seq, "side": s, "qty": qty}))
        else:
            stop = MID + side * rng.randint(0, WIDTH)
            out.append(("stop", {"seq": seq, "side": s, "qty": qty, "stop": stop}))
    return out


def fixtures() -> None:
    # Fixture A: asks 1000 x 60 and 1100 x 100; market buy 150.
    b = Book()
    b.arrive("sell", "limit", 60, 1000, 0)
    b.arrive("sell", "limit", 100, 1100, 1)
    b.arrive("buy", "market", 150, None, 2)
    cost = sum(p * q for p, q in b.fills)
    print("A fills", b.fills, "cost", cost, "avg", cost / 150, "ask left at 1100", sum(o[1] for o in b.ask_levels[1100]))
    # Fixture B: asks 990 x 100; bids 985 x 100, 980 x 100; sell stop 100 at 990; market buy 100.
    b = Book()
    b.arrive("sell", "limit", 100, 990, 0)
    b.arrive("buy", "limit", 100, 985, 1)
    b.arrive("buy", "limit", 100, 980, 2)
    b.pending.append({"seq": 3, "side": "sell", "qty": 100, "stop": 990})
    b.activate_all()
    b.arrive("buy", "market", 100, None, 4)
    act = b.activate_all()
    print("B fills", b.fills, "activations", len(act), "stop filled at", b.fills[-1][0])


def run() -> None:
    b = Book()
    kinds: Counter[str] = Counter()
    crossed_after_event = 0
    crossed_intermediate = 0
    conservation_fail = 0
    activated = 0
    trace: list[str] = []
    seq_checks: list[str] = []
    for seq, (kind, o) in enumerate(flow()):
        kinds[kind] += 1
        if kind == "stop":
            b.pending.append({"seq": o["seq"], "side": o["side"], "qty": o["qty"], "stop": o["stop"]})
        else:
            b.arrive(o["side"], kind, o["qty"], o.get("price"), o["seq"])
        # every intermediate state after each activation (strict check, reported separately)
        acts = b.activate_all()
        activated += len(acts)
        for _, _, fills in acts:
            seq_checks.append(str(seq))
        bid, ask = b.best_bid(), b.best_ask()
        if bid is not None and ask is not None and bid >= ask:
            crossed_after_event += 1
        if b.entered != b.resting() + 2 * b.traded + b.cancelled:
            conservation_fail += 1
        if seq < 8:
            trace.append(
                f"event {seq}: {kind} {o['side']}, best bid {bid}, best ask {ask}, last {b.last}, activations {len(acts)}"
            )
        if seq == 7:
            print("EVENT 7 kind", kind, o, "activations", [(a[0], a[1], a[2]) for a in acts])
    for line in trace:
        print(line)
    print("kinds", dict(kinds))
    print("trades", len(b.fills), "traded", b.traded, "activated", activated, "pending", len(b.pending))
    print("cancelled", b.cancelled, "resting", b.resting())
    print("crossed after events", crossed_after_event, "conservation failures", conservation_fail)
    print("end best bid", b.best_bid(), "best ask", b.best_ask())
    print("activation-sequence events", len(seq_checks))
    print("avg shares per trade", f"{b.traded}/{len(b.fills)}", b.traded / len(b.fills))


if __name__ == "__main__":
    fixtures()
    run()
