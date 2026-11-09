"""PC3-b round 16: independent re-implementation of the L04 game rules (not copied from the twin).

Checks the seed-0 and seed-1 totals printed in L04 Lab 1 / Problems E1-E3, the canon-breaks claim that the mid at
turn t equals 10000 - 10*I_{t-1} under the Example 1.3 rule (for many seeds), the A5 inventory limit, and the
P&L identity. Draw order is taken from the page text: per turn, first the fair move, then the arrival.
Usage: python -I ledgers/PC3/scripts/PC3-b-r16/sim_game_independent.py
"""
import random

HOR, V0, LIM, HS = 20, 10000, 10, 10


def run(seed):
    rng = random.Random(seed)
    v = V0
    moves, arrs = [v], []
    for _ in range(HOR):
        v += 5 if rng.random() < 0.5 else -5
        moves.append(v)
        u = rng.random()
        arrs.append("ub" if u < 0.25 else ("us" if u < 0.5 else "inf"))
    inv, cash, last = 0, 0, None
    mid_ok = True
    fills, informed, maxabs = 0, 0, 0
    cf = 0
    for t in range(1, HOR + 1):
        mid = V0 if last is None else last
        if mid != V0 - 10 * inv:
            mid_ok = False
        bid, ask = mid - HS, mid + HS
        arr = arrs[t - 1]
        fv = moves[t]
        if arr == "inf":
            informed += 1
        if arr == "ub":
            side = -1
        elif arr == "us":
            side = 1
        else:
            side = -1 if fv > ask else (1 if fv < bid else 0)
        if side != 0 and abs(inv + side) <= LIM:
            price = ask if side < 0 else bid
            cf += -side * price
            cash += -side * price
            inv += side
            last = price
            fills += 1
        maxabs = max(maxabs, abs(inv))
    settle = moves[HOR]
    pnl = cash + inv * settle
    return dict(fills=fills, cash_flow=cf, inv=inv, settle=settle, pnl=pnl, informed=informed,
                maxabs=maxabs, mid_ok=mid_ok, identity=(pnl == cf + inv * settle))


r0 = run(0)
r1 = run(1)
print("seed 0:", r0)
print("seed 1:", r1)
print("expected seed 0: fills 9, cash_flow -9950, inv 1, settle 9980, pnl 30, informed 13, maxabs 3")
print("expected seed 1: fills 16, cash_flow 20100, inv -2, settle 10020, pnl 60")
ok0 = (r0["fills"], r0["cash_flow"], r0["inv"], r0["settle"], r0["pnl"], r0["informed"], r0["maxabs"]) == (9, -9950, 1, 9980, 30, 13, 3)
ok1 = (r1["fills"], r1["cash_flow"], r1["inv"], r1["settle"], r1["pnl"]) == (16, 20100, -2, 10020, 60)
print("seed0 matches:", ok0, "seed1 matches:", ok1)
allmid = all(run(s)["mid_ok"] for s in range(500))
allid = all(run(s)["identity"] for s in range(500))
maxlim = max(run(s)["maxabs"] for s in range(500))
print("mid == 10000 - 10*I_{t-1} at every turn, seeds 0..499:", allmid)
print("P&L identity, seeds 0..499:", allid)
print("largest |inventory| over seeds 0..499:", maxlim, "(limit 10)")
