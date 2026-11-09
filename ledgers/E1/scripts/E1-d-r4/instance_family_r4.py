"""Exhaustive check of the instance family in grader/instance.py: b in 1..3, c in 5..60, gap d in 60..400."""
from fractions import Fraction as F
import math

def hu(x):
    return math.floor(x + F(1, 2))

def out(s, a, b, c):
    d = F(a - b * c)
    Q = {"monopoly": d / 2, "cournot": 2 * d / 3, "bertrand": d}[s]
    fee = F(a - Q) / b
    profit = (fee - c) * Q
    cs = Q * Q / (2 * b)
    w = F(a) * Q / b - Q * Q / (2 * b) - c * Q
    dwl = (d - Q) ** 2 / (2 * b)
    return {"volume": hu(Q), "fee": hu(fee), "profit": hu(profit), "welfare": hu(w), "dwl": hu(dwl), "cs": hu(cs)}, Q, fee, profit, w, dwl

n = 0
bad = []
for b in range(1, 4):
    for c in range(5, 61):
        for d in range(60, 401):
            n += 1
            a = b * c + d
            P, *_ = out("monopoly", a, b, c), None
            m = out("monopoly", a, b, c)[0]; k = out("cournot", a, b, c)[0]; t = out("bertrand", a, b, c)[0]
            ok = (m["volume"] < k["volume"] < t["volume"] and m["fee"] > k["fee"] > c
                  and m["welfare"] < k["welfare"] < t["welfare"] and m["dwl"] > k["dwl"] > t["dwl"] == 0
                  and m["profit"] > k["profit"] > t["profit"] == 0)
            if not ok:
                bad.append((a, b, c))
print("family cases", n, "order violations", len(bad), bad[:3])
