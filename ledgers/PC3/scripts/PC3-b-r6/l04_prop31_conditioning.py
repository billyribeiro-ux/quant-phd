"""Exact enumeration: does Proposition 3.1 hold when conditioning only on (v_t = v, I_{t-1} = 0), i.e. with the
quote a_t, b_t NOT fixed? PC3-b round 6. Own implementation of the page's game rule (Example 1.3, A1, A4, A5).
Turn outcome probabilities: move +5/-5 each 1/2; arrival uninformed-buy 1/4, uninformed-sell 1/4, informed 1/2.
"""
from fractions import Fraction as F
from collections import defaultdict
import sys

H = 10  # half spread
L = 10

def formula(v, a, b, p=F(1, 2)):
    return (1 - p) * F(a - b, 2) - p * (max(v - a, 0) + max(b - v, 0))

def run(T):
    # state: (v_prev, last_fill_price or None, inventory, cash) with probability weight; track path info needed
    # Enumerate turns 1..T; record at turn T: v_T, inventory before T, quote at T, trade term at T.
    states = [(F(1), 10000, None, 0)]  # (prob, v_{t-1}, last_fill, inventory)
    records = defaultdict(F)  # key (v_T, quote(a,b), inv_before) -> prob mass
    trade_sum = defaultdict(F)  # key (v_T, quote, inv) -> sum prob*term
    for t in range(1, T + 1):
        new = []
        for prob, vprev, last, inv in states:
            for mv in (5, -5):
                v = vprev + mv
                mid = 10000 if last is None else last
                a, b = mid + H, mid - H
                for arr, pa in (("ub", F(1, 4)), ("us", F(1, 4)), ("inf", F(1, 2))):
                    pr = prob * F(1, 2) * pa
                    if arr == "ub":
                        side = -1
                    elif arr == "us":
                        side = 1
                    else:
                        side = -1 if v > a else (1 if v < b else 0)
                    filled = side != 0 and abs(inv + side) <= L
                    price = None
                    term = F(0)
                    if filled:
                        price = a if side < 0 else b
                        term = -side * price + side * v  # c_t + sigma_t v_t
                    if t == T:
                        key = (v, (a, b), inv)
                        records[key] += pr
                        trade_sum[key] += pr * term
                    new.append((pr, v, price if filled else last, inv + (side if filled else 0)))
        states = new
    return records, trade_sum

if __name__ == "__main__":
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    rec, ts = run(T)
    bad = []
    for v in sorted({k[0] for k in rec}):
        # condition on v_T = v and inventory before T equal 0
        mass = sum(p for k, p in rec.items() if k[0] == v and k[2] == 0)
        if mass == 0:
            continue
        mix = sum(ts[k] for k in rec if k[0] == v and k[2] == 0) / mass
        quotes = {k[1] for k in rec if k[0] == v and k[2] == 0}
        fixed_ok = all(
            (sum(ts[k] for k in rec if k[0] == v and k[2] == 0 and k[1] == q) /
             sum(rec[k] for k in rec if k[0] == v and k[2] == 0 and k[1] == q)) == formula(v, q[0], q[1])
            for q in quotes if sum(rec[k] for k in rec if k[0] == v and k[2] == 0 and k[1] == q) > 0
        )
        if mix != formula(v, *next(iter(quotes))) or len(quotes) > 1:
            bad.append((v, float(mix), sorted((q, float(formula(v, *q))) for q in quotes), fixed_ok))
    print("T =", T, "values v with >1 quote or mismatch (v, E over quotes, [(quote, formula)], formula ok per quote):")
    for row in bad[:12]:
        print(" ", row)
    print("count of v values with quote mixture:", len(bad))
