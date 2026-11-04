"""Independent re-derivation of the L04 page numbers (does not import the twin).

Usage: python -I recompute_L04.py. Stdlib only. Implements the page's rules directly from the text:
A1 arrivals (1/4 uninformed buy, 1/4 uninformed sell, 1/2 informed), A2 moves +-5, A4 informed trades when
v>a (buy at ask) or v<b (sell at bid), A5 fill iff q>=1 and |I after| <= 10, quote = last fill mid +-10, size 1.
Draw order per turn (Lab 1 text): move draw first, then arrival draw.
"""
import random
from fractions import Fraction as F

def game(seed):
    rng = random.Random(seed)
    v = [10000]
    arr = []
    for _ in range(20):
        mv = 5 if rng.random() < 0.5 else -5
        v.append(v[-1] + mv)
        u = rng.random()
        arr.append("ub" if u < 0.25 else ("us" if u < 0.5 else "inf"))
    return v, arr

def run(seed):
    v, arr = game(seed)
    I = 0; C = 0; last = None; fills = 0; cashflow = 0
    for t in range(1, 21):
        mid = 10000 if last is None else last
        b, a = mid - 10, mid + 10
        ar = arr[t-1]; fv = v[t]
        if ar == "ub": side = -1
        elif ar == "us": side = 1
        else:
            side = -1 if fv > a else (1 if fv < b else 0)
        if side != 0 and abs(I + side) <= 10:
            price = a if side < 0 else b
            cf = -side * price
            I += side; C += cf; cashflow += cf; fills += 1; last = price
    settle = v[20]
    return dict(fills=fills, cashflow=cashflow, inv=I, settle=settle, mark=I*settle, pnl=C + I*settle)

print("seed 0:", run(0))
print("seed 1:", run(1))

def trade_term(inv, fv, b=9990, a=10010):
    # expected trade term c + sigma*v from inventory inv, size 1, page rules
    tot = F(0)
    for prob, kind in ((F(1,4),"ub"),(F(1,4),"us"),(F(1,2),"inf")):
        if kind == "ub": side = -1
        elif kind == "us": side = 1
        else:
            side = -1 if fv > a else (1 if fv < b else 0)
        if side == 0: continue
        if abs(inv + side) > 10: continue
        price = a if side < 0 else b
        tot += prob * (-side * price + side * fv)
    return tot

print("Remark 4.2 trade term at v=10000 by inventory:")
for inv in (0, 1, 3, 9, 10, -10):
    print(" I=", inv, trade_term(inv, 10000))
grid = list(range(9900, 10101))
same = all(trade_term(i, f) == trade_term(0, f) for i in range(-9, 10) for f in grid)
print("|I|<=9 equals I=0 at every integer fair value 9900..10100:", same)
print("I=10 equals I=0 at every grid point:", all(trade_term(10, f) == trade_term(0, f) for f in grid))
print("I=10 at v=10000 differs from I=0:", trade_term(10,10000) != trade_term(0,10000))
