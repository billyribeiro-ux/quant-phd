"""CS2 slice b, round 2: independent recount of L08 queue steps, steps with no live order, and binary-search total.

Own implementation: each price level is a FIFO list of order records with a head index. The head advances past
records whose remaining quantity is 0 (filled or cancelled); each advance is one queue step. The head is consulted
only when a fill is attempted at the best opposite price, as Definition 1.1 and the pseudocode describe.
Seeded stream: LCG seed 20261029, the same draw order as the lab docstring specifies (cancel draw, then side,
price, quantity).
Usage: python -I -W error recompute_l08_queue_r2.py
"""

from __future__ import annotations


class LCG:
    def __init__(self, seed: int) -> None:
        self.s = seed % (2**31)

    def draw(self, n: int) -> int:
        self.s = (1103515245 * self.s + 12345) % (2**31)
        return (self.s >> 16) % n


class Rec:
    def __init__(self, oid: int, side: str, price: int, q: int) -> None:
        self.oid, self.side, self.price, self.q = oid, side, price, q


def main() -> None:
    g = LCG(20261029)
    MID, HALF, MAXQ, CANCEL, MESSAGES = 10000, 20, 20, 25, 400
    queues: dict[str, dict[int, list[Rec]]] = {"B": {}, "S": {}}
    heads: dict[str, dict[int, int]] = {"B": {}, "S": {}}
    prices: dict[str, list[int]] = {"B": [], "S": []}
    live: dict[int, Rec] = {}
    steps = 0
    added = 0
    no_live_steps: list[int] = []
    cancels = 0
    traded_msgs = 0
    executions = 0
    created = removed = 0
    next_id = 1

    def best(side: str) -> int | None:
        if not prices[side]:
            return None
        return prices[side][-1] if side == "B" else prices[side][0]

    def front(side: str, p: int) -> Rec | None:
        nonlocal steps
        q = queues[side][p]
        h = heads[side][p]
        while h < len(q) and q[h].q == 0:
            h += 1
            steps += 1
        heads[side][p] = h
        return q[h] if h < len(q) else None

    def drop(side: str, p: int) -> None:
        nonlocal removed
        if any(r.q > 0 for r in queues[side][p]):
            return
        prices[side].remove(p)
        del queues[side][p]
        del heads[side][p]
        removed += 1

    def insert_price(side: str, p: int) -> None:
        nonlocal created
        lst = prices[side]
        i = 0
        while i < len(lst) and lst[i] < p:
            i += 1
        lst.insert(i, p)
        queues[side][p] = []
        heads[side][p] = 0
        created += 1

    for step in range(MESSAGES):
        if not live:
            no_live_steps.append(step)
        live_ids = sorted(live)
        if live_ids and g.draw(100) < CANCEL:
            oid = live_ids[g.draw(len(live_ids))]
            r = live.pop(oid)
            r.q = 0
            cancels += 1
            drop(r.side, r.price)
            continue
        side = "B" if g.draw(2) == 0 else "S"
        price = MID - HALF + g.draw(2 * HALF + 1)
        qty = 1 + g.draw(MAXQ)
        added += 1
        opp = "S" if side == "B" else "B"
        remaining = qty
        trades = 0
        while remaining > 0:
            b = best(opp)
            if b is None or (side == "B" and b > price) or (side == "S" and b < price):
                break
            r = front(opp, b)
            assert r is not None
            fill = min(remaining, r.q)
            r.q -= fill
            remaining -= fill
            trades += 1
            if r.q == 0:
                live.pop(r.oid, None)
            drop(opp, b)
        if trades:
            traded_msgs += 1
            executions += trades
        if remaining > 0:
            if price not in queues[side]:
                insert_price(side, price)
            rec = Rec(next_id, side, price, remaining)
            queues[side][price].append(rec)
            live[next_id] = rec
        next_id += 1
    print(f"orders added {added}; cancels {cancels}; traded messages {traded_msgs}; executions {executions}")
    print(f"queue steps {steps} (orders added {added})")
    print(f"levels created {created}; removed {removed}; levels left {created - removed}; live orders {len(live)}")
    print(f"steps with no live order before the message: {no_live_steps}")
    live_steps = MESSAGES - len(no_live_steps)
    print(f"steps with a live order: {live_steps}; cancel share {cancels}/{live_steps} = {100 * cancels / live_steps:.1f}%")
    bids = [r.price for r in live.values() if r.side == "B"]
    asks = [r.price for r in live.values() if r.side == "S"]
    print(f"best bid {max(bids) if bids else None}; best ask {min(asks) if asks else None}")


if __name__ == "__main__":
    main()
