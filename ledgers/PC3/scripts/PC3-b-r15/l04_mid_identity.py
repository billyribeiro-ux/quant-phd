"""Checks the L04 'where the canon breaks' claim: under the Example 1.3 rule the mid at turn t equals
10000 - 10 * I_{t-1}, for every seed tested; also the Remark 4.2 I=10 case by enumeration, and the 3.4 quarter claim.
Run: python3 -I l04_mid_identity.py
"""
import random
from fractions import Fraction as F

def run(seed):
    rng = random.Random(seed)
    path = [10000]
    arr = []
    for _ in range(20):
        path.append(path[-1] + (5 if rng.random() < 0.5 else -5))
        d = rng.random()
        arr.append("ub" if d < 0.25 else ("us" if d < 0.5 else "inf"))
    inv, last, bad, checked = 0, None, 0, 0
    for t in range(1, 21):
        mid = 10000 if last is None else last
        checked += 1
        if mid != 10000 - 10 * inv:
            bad += 1
        bid, ask = mid - 10, mid + 10
        fv = path[t]
        a = arr[t - 1]
        side = -1 if a == "ub" else (1 if a == "us" else (-1 if fv > ask else (1 if fv < bid else 0)))
        if side != 0 and abs(inv + side) <= 10:
            price = ask if side < 0 else bid
            inv += side
            last = price
    return checked, bad

tot_checked = tot_bad = 0
for s in range(2000):
    c, b = run(s)
    tot_checked += c
    tot_bad += b
print("mid == 10000 - 10*I_{t-1} checks:", tot_checked, "failures:", tot_bad)

# Remark 4.2 at I=10: quote 9990/10010, v=10000, p=1/2; uninformed buy (1/4) contributes 10; others 0
E = F(1, 4) * (10010 - 10000) + F(1, 4) * 0 + F(1, 4) * 0 + F(1, 4) * 0
print("Remark 4.2 I=10 enumerated E:", E, "(I=0 value 5)")
# Remark 3.4: (1-p)h as a fraction of 2h at p=1/2
h = 10
print("uninformed term / quoted spread at p=1/2:", F(1, 2) * h / (2 * h))
