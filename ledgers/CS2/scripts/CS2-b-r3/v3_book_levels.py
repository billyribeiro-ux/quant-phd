"""Independent level-structure model for the L08 lab stream (seed 20261029), to re-derive the Part C counts.

Usage: python -I -W error v3_book_levels.py   (standard library only; writes nothing)
Model, from the lesson text (Definition 1.1 and Proposition 3.2): per side a sorted list of prices with at least
one live order; per price a FIFO list of entries with a head index that passes only dead entries, and only when
an incoming order examines the best level of the opposite side; a level is deleted when its last live order goes.
Counts: queue steps (head passes), levels created, levels removed, halving searches and their comparisons.
"""

from collections import deque


class Lcg:
    def __init__(self, s):
        self.s = s % 2**31

    def below(self, n):
        self.s = (1103515245 * self.s + 12345) % 2**31
        return (self.s >> 16) % n


def halving(prices, p):
    lo, hi, comps = 0, len(prices), 0
    while lo < hi:
        mid = lo + (hi - lo) // 2
        comps += 1
        if prices[mid] < p:
            lo = mid + 1
        else:
            hi = mid
    return lo, comps


def main():
    gen = Lcg(20261029)
    prices = {"B": [], "S": []}  # sorted ascending
    levels = {"B": {}, "S": {}}  # price -> {"q": deque of [oid, qty], "head": int, "live": int}
    where = {}  # oid -> (side, price, entry)
    queue_steps = created = removed = searches = 0
    max_comps = 0
    comps_log = []
    next_id = 1
    orders_added = 0
    cancels = 0

    def drop_if_empty(side, price):
        nonlocal removed, searches, max_comps
        lv = levels[side][price]
        if lv["live"] == 0:
            idx, c = halving(prices[side], price)
            searches += 1
            comps_log.append((len(prices[side]), c))
            max_comps = max(max_comps, c)
            assert prices[side][idx] == price
            del prices[side][idx]
            del levels[side][price]
            removed += 1

    for step in range(400):
        live = sorted(where)
        if live and gen.below(100) < 25:
            oid = live[gen.below(len(live))]
            side, price, entry = where.pop(oid)
            entry[1] = 0
            levels[side][price]["live"] -= 1
            drop_if_empty(side, price)
            cancels += 1
            continue
        side = "B" if gen.below(2) == 0 else "S"
        price = 10000 - 20 + gen.below(41)
        qty = 1 + gen.below(20)
        orders_added += 1
        opp = "S" if side == "B" else "B"
        remaining = qty
        while remaining > 0:
            if not prices[opp]:
                break
            best = prices[opp][-1] if opp == "B" else prices[opp][0]
            if (side == "B" and best > price) or (side == "S" and best < price):
                break
            lv = levels[opp][best]
            q, head = lv["q"], lv["head"]
            while head < len(q) and q[head][1] == 0:
                head += 1
                queue_steps += 1
            lv["head"] = head
            front = q[head]
            fill = min(remaining, front[1])
            front[1] -= fill
            remaining -= fill
            if front[1] == 0:
                lv["live"] -= 1
                del where[front[0]]
            drop_if_empty(opp, best)
        if remaining > 0:
            if price not in levels[side]:
                idx, c = halving(prices[side], price)
                searches += 1
                comps_log.append((len(prices[side]), c))
                max_comps = max(max_comps, c)
                prices[side].insert(idx, price)
                levels[side][price] = {"q": deque(), "head": 0, "live": 0}
                created += 1
            entry = [next_id, remaining]
            levels[side][price]["q"].append(entry)
            levels[side][price]["live"] += 1
            where[next_id] = (side, price, entry)
        next_id += 1

    bound_ok = all(c <= L.bit_length() for L, c in comps_log)
    print(f"orders_added={orders_added} cancels={cancels} live_orders_end={len(where)}")
    print(f"queue_steps={queue_steps} levels_created={created} levels_removed={removed}")
    print(f"searches={searches} (created+removed={created + removed}) max_comparisons={max_comps}")
    print(f"every_search_within_bit_length_bound={bound_ok}")
    print(f"levels_left={sum(len(levels[s]) for s in levels)} sides_prices_end={ {s: len(prices[s]) for s in prices} }")


main()
