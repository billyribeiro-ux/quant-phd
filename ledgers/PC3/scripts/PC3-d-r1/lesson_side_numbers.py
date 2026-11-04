"""Re-derive lesson-side numbers that the cards depend on or that sit next to them (PC3-d round 1, notes only).

Run: python3 -I ledgers/PC3/scripts/PC3-d-r1/lesson_side_numbers.py
"""
import math
import random
from collections import deque
from fractions import Fraction as F

print("L01 line 140 ratio remainder/bound:", f"{0.0046221254 / 0.0048728552:.6f}")
print("L01 line 140 bound/remainder - 1:", f"{0.0048728552 / 0.0046221254 - 1:.6f}")

# c085 Remark 3.4: step k removes k-1 entries in one loop for x=(k,...,2,100)
for k in (3, 6, 9):
    xs = list(range(k, 1, -1)) + [100]
    dq: deque[int] = deque(); removed_at_step_k = None
    for i, v in enumerate(xs, 1):
        cnt = 0
        while dq and xs[dq[-1]] <= v:
            dq.pop(); cnt += 1
        if i == k:
            removed_at_step_k = cnt
        dq.append(i - 1)
        if dq[0] <= i - 1 - k:
            dq.popleft()
    print(f"c085 k={k}: pops in the while loop at step k = {removed_at_step_k} (expect k-1 = {k-1})")

# E2 of L05 (seed 6)
r6 = random.Random(6)
xs6 = [r6.randint(0, 999) for _ in range(200)]
comps = pushes = pops = 0
dq = deque()
for i, v in enumerate(xs6):
    while dq:
        comps += 1
        if xs6[dq[-1]] > v:
            break
        dq.pop(); pops += 1
    dq.append(i); pushes += 1
    if dq[0] <= i - 8:
        dq.popleft(); pops += 1
print(f"L05 E2 seed 6 k=8: deque comparisons {comps}, pushes {pushes}, pops {pops} (lesson says 350, 200, 197)")

# L04 E2 seed 0 informed count (20 arrivals)
r0 = random.Random(0)
arr = []
for _ in range(20):
    r0.random()
    d = r0.random()
    arr.append("ub" if d < 0.25 else "us" if d < 0.5 else "inf")
print("L04 E2 informed arrivals on seed 0:", arr.count("inf"), "(lesson says 13)")

# L06 E2 NPV at 1200 and 1300 units, 10 percent
def npv(u: F) -> F:
    return -F(15_000_000) + sum((F(u * 5000) / F(11, 10) ** t for t in (1, 2, 3)), F(0))
print("L06 E2 NPV(1200) cents:", float(npv(F(1200))), "(lesson says -78888.05)")
print("L06 E2 NPV(1300) cents:", float(npv(F(1300))), "(lesson says 1164537.94)")

# L04 E1 seed 1 path (lesson says 16 fills, cash 20100, inventory -2, settle 10020, P&L 60)
r1 = random.Random(1)
path = [10000]; arrivals = []
for _ in range(20):
    mv = 5 if r1.random() < 0.5 else -5
    path.append(path[-1] + mv)
    d = r1.random()
    arrivals.append("ub" if d < 0.25 else "us" if d < 0.5 else "inf")
inv = cash = 0; last = None; fills = 0; cflow = 0
for t in range(1, 21):
    mid = 10000 if last is None else last
    bid, ask = mid - 10, mid + 10
    a = arrivals[t - 1]; fair = path[t]
    side = -1 if a == "ub" else 1 if a == "us" else (-1 if fair > ask else 1 if fair < bid else 0)
    if side and abs(inv + side) <= 10:
        price = ask if side < 0 else bid
        cf = -side * price
        inv += side; cash += cf; cflow += cf; fills += 1; last = price
print(f"L04 E1 seed 1: fills {fills}, cash flow {cflow}, inventory {inv}, settle {path[20]}, P&L {cash + inv*path[20]} (lesson says 16, 20100, -2, 10020, 60)")
