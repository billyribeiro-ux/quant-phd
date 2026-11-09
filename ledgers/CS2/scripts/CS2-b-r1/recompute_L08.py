"""Independent re-run of the L08 order-book stream (seed and draw order from the lesson's lab description).

Written separately from the twin: the book is a dict of price levels with explicit head indices, the
reference is a flat list sorted per match, and the halving search is re-implemented. Prints the numbers
the L08 prose and cards state, and checks the live-order claim of problem E1.
Run: python -I -W error recompute_L08.py
"""
from __future__ import annotations


class LCG:
    def __init__(self, s: int) -> None:
        self.s = s % (2**31)

    def below(self, n: int) -> int:
        self.s = (1103515245 * self.s + 12345) % (2**31)
        return (self.s >> 16) % n


class Level:
    def __init__(self) -> None:
        self.entries: list[list[int]] = []  # [oid, qty]
        self.head = 0


def run() -> None:
    g = LCG(20261029)
    bids: dict[int, Level] = {}
    asks: dict[int, Level] = {}
    bid_prices: list[int] = []  # sorted ascending
    ask_prices: list[int] = []
    where: dict[int, tuple[str, int]] = {}  # live oid -> (side, price)
    ref: list[tuple[str, int, int, int]] = []  # (side, price, oid, qty) flat
    queue_steps = 0
    orders_added = 0
    levels_created = 0
    levels_removed = 0
    searches: list[int] = []
    trades_msgs = 0
    executions = 0
    cancels = 0
    live_empty_steps: list[int] = []
    cancel_draw_steps = 0
    next_id = 1

    def halving(lst: list[int], p: int) -> int:
        lo, hi, c = 0, len(lst), 0
        while lo < hi:
            mid = (lo + hi) // 2
            c += 1
            if lst[mid] < p:
                lo = mid + 1
            else:
                hi = mid
        searches.append(c)
        return lo

    def level_live(lv: Level) -> int:
        return sum(1 for e in lv.entries if e[1] > 0)

    for step in range(400):
        live_ids = sorted(oid for (_, _, oid, qty) in ref if qty > 0)
        if not live_ids:
            live_empty_steps.append(step)
        if live_ids and g.below(100) < 25:
            cancel_draw_steps += 1
            oid = live_ids[g.below(len(live_ids))]
            cancels += 1
            side, price = where.pop(oid)
            lv = (bids if side == "B" else asks)[price]
            for e in lv.entries:
                if e[0] == oid:
                    e[1] = 0
            # reference
            ref = [r if r[2] != oid else (r[0], r[1], r[2], 0) for r in ref]
            if level_live(lv) == 0:
                plist = bid_prices if side == "B" else ask_prices
                idx = halving(plist, price)
                assert plist[idx] == price
                del plist[idx]
                del (bids if side == "B" else asks)[price]
                levels_removed += 1
            continue
        side = "B" if g.below(2) == 0 else "S"
        price = 9980 + g.below(41)
        qty = 1 + g.below(20)
        oid = next_id
        next_id += 1
        orders_added += 1
        # reference: flat scan
        if side == "B":
            cands = sorted([r for r in ref if r[0] == "S" and r[3] > 0 and r[1] <= price], key=lambda r: (r[1], r[2]))
        else:
            cands = sorted([r for r in ref if r[0] == "B" and r[3] > 0 and r[1] >= price], key=lambda r: (-r[1], r[2]))
        rem = qty
        ref_trades = []
        newref = []
        fills: dict[int, int] = {}
        for c in cands:
            if rem == 0:
                break
            f = min(rem, c[3])
            ref_trades.append((c[1], f, c[2]))
            fills[c[2]] = f
            rem -= f
        ref = [(r[0], r[1], r[2], r[3] - fills.get(r[2], 0)) for r in ref]
        if rem > 0:
            ref.append((side, price, oid, rem))
        # book
        opp_levels = asks if side == "B" else bids
        opp_prices = ask_prices if side == "B" else bid_prices
        book_trades = []
        q = qty
        while q > 0:
            if not opp_prices:
                break
            best = opp_prices[0] if side == "B" else opp_prices[-1]
            if side == "B" and best > price:
                break
            if side == "S" and best < price:
                break
            lv = opp_levels[best]
            while lv.head < len(lv.entries) and lv.entries[lv.head][1] == 0:
                lv.head += 1
                queue_steps += 1
            assert lv.head < len(lv.entries), "level without live order"
            e = lv.entries[lv.head]
            f = min(q, e[1])
            e[1] -= f
            q -= f
            book_trades.append((best, f, e[0]))
            if e[1] == 0:
                where.pop(e[0], None)
            if level_live(lv) == 0:
                idx = halving(opp_prices, best)
                assert opp_prices[idx] == best
                del opp_prices[idx]
                del opp_levels[best]
                levels_removed += 1
        if q > 0:
            own_levels = bids if side == "B" else asks
            own_prices = bid_prices if side == "B" else ask_prices
            if price not in own_levels:
                idx = halving(own_prices, price)
                own_prices.insert(idx, price)
                own_levels[price] = Level()
                levels_created += 1
            own_levels[price].entries.append([oid, q])
            where[oid] = (side, price)
        if book_trades:
            trades_msgs += 1
            executions += len(book_trades)
        assert [(p, f, o) for (p, f, o) in book_trades] == ref_trades, f"step {step} trades differ"
        bb = bid_prices[-1] if bid_prices else None
        ba = ask_prices[0] if ask_prices else None
        rb = max([r[1] for r in ref if r[0] == "B" and r[3] > 0], default=None)
        ra = min([r[1] for r in ref if r[0] == "S" and r[3] > 0], default=None)
        assert (bb, ba) == (rb, ra), f"step {step} best differs"
        if bb is not None and ba is not None:
            assert bb < ba, f"crossed at step {step}"
    final_live = sum(1 for r in ref if r[3] > 0)
    print(f"orders_added={orders_added} cancels={cancels} messages_traded={trades_msgs} executions={executions}")
    print(f"queue_steps={queue_steps} levels_created={levels_created} levels_removed={levels_removed} searches={len(searches)} max_cmp={max(searches)}")
    print(f"final best bid={bid_prices[-1] if bid_prices else None} best ask={ask_prices[0] if ask_prices else None} resting={final_live} levels_left={len(bid_prices)+len(ask_prices)}")
    print(f"steps_with_no_live_order={live_empty_steps[:6]} count={len(live_empty_steps)} steps_with_draw={cancel_draw_steps}")
    print(f"cancel_share_of_messages={cancels/400:.4f}  cancel_share_of_steps_with_live={cancels/(400-len(live_empty_steps)):.4f}")
    print(f"searches_bound_check={all(c <= (k).bit_length() for c, k in [(c, 1) for c in searches]) if False else max(searches) <= 4}")


if __name__ == "__main__":
    run()
