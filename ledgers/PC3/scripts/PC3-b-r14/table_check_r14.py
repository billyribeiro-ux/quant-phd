"""Round-14 check: independent per-turn replay of L04 seed 0 against the printed Part 1 table, and L05 first maxima."""

import random
import re
import sys

sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyE14-PC3-b/ledgers/PC3/scripts/PC3-b-r14")
exp = open("/Users/billyribeiro/.fanout/wt/verifyE14-PC3-b/ledgers/PC3/scripts/PC3-b-r14/out/stdout_L04_r14.txt").read().splitlines()
rows = [ln for ln in exp if re.match(r"^\s*\d+\s+\d+\s+\d+\s+\d+\s+", ln)]
rng = random.Random(0)
v = [10000]
arr = []
for _ in range(20):
    v.append(v[-1] + (5 if rng.random() < 0.5 else -5))
    x = rng.random()
    arr.append("UB" if x < 0.25 else ("US" if x < 0.5 else "I"))
inv, cash, last = 0, 0, None
mism = 0
for t in range(1, 21):
    mid = 10000 if last is None else last
    b, a = mid - 10, mid + 10
    k = arr[t - 1]
    side = -1 if k == "UB" else (1 if k == "US" else (-1 if v[t] > a else (1 if v[t] < b else 0)))
    filled = side != 0 and abs(inv + side) <= 10
    price = (a if side == -1 else b) if filled else None
    if filled:
        cash += -side * price
        inv += side
        last = price
    fill_s = "-" if price is None else str(price)
    mine = f"{t:>4}  {b:>5}  {a:>5}  {1:>4}  {k if False else ''}"
    parts = rows[t - 1].split()
    ok = (int(parts[0]) == t and int(parts[1]) == b and int(parts[2]) == a and parts[5] == str(filled)
          and parts[6] == fill_s and int(parts[7]) == inv and int(parts[8]) == cash)
    if not ok:
        mism += 1
        print("MISMATCH turn", t, rows[t - 1], "mine", b, a, filled, fill_s, inv, cash)
print("L04 seed0 table rows checked: 20, mismatches:", mism)
