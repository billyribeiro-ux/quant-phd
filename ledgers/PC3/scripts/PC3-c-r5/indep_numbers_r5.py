"""Round-5 independent re-derivation of every number on project.html (Labs 1-3, Exemplars A and B, Lab 3 counterfactual,
and the arrival-sensitivity sentence). Written from the page's Conventions text and Lesson 4 A1/A2 only, not from the
grader or the lab code. Run: python3 -I indep_numbers_r5.py"""
from fractions import Fraction


def game(seed, p_buy=Fraction(1, 4), p_sell=Fraction(1, 4), moves_first=True):
    import random
    rng = random.Random(seed)
    v = [10000]
    arr = []
    for _ in range(20):
        eps = 5 if rng.random() < 0.5 else -5
        v.append(v[-1] + eps)
        u = rng.random()
        if u < p_buy:
            arr.append("ub")
        elif u < p_buy + p_sell:
            arr.append("us")
        else:
            arr.append("inf")
    return v, arr


def run(seed, half=10, p_buy=Fraction(1, 4), p_sell=Fraction(1, 4)):
    v, arr = game(seed, p_buy, p_sell)
    inv = 0
    cash = 0
    last = None
    fills = []
    maxabs = 0
    for t in range(1, 21):
        mid = 10000 if last is None else last
        b, a = mid - half, mid + half
        x = arr[t - 1]
        if x == "ub":
            side = -1
        elif x == "us":
            side = 1
        elif v[t] > a:
            side = -1
        elif v[t] < b:
            side = 1
        else:
            side = 0
        if side != 0 and abs(inv + side) <= 10:
            price = a if side == -1 else b
            inv += side
            cash += -side * price
            last = price
            fills.append((t, side, price))
            maxabs = max(maxabs, abs(inv))
    s = v[20]
    return {"fills": len(fills), "cash": cash, "inv": inv, "mark": inv * s, "pnl": cash + inv * s,
            "maxabs": maxabs, "settlement": s, "fill_list": fills}


ref = run(0)
print("seed0 reference:", {k: ref[k] for k in ("fills", "cash", "inv", "mark", "pnl", "maxabs", "settlement")})
print("fill turns:", [t for t, _, _ in ref["fill_list"]])
print("fill prices:", [p for _, _, p in ref["fill_list"]])
print("identity:", ref["pnl"] == ref["cash"] + ref["inv"] * ref["settlement"])
wide = run(0, half=15)
print("counterfactual half 15:", {k: wide[k] for k in ("fills", "pnl")}, "change", wide["pnl"] - ref["pnl"])
ex_b_buys = [p for t, s, p in ref["fill_list"] if s == 1]
ex_b_sells = [p for t, s, p in ref["fill_list"] if s == -1]
print("Exemplar B: bids-bought turns:", [t for t, s, p in ref["fill_list"] if s == 1], "sum", sum(ex_b_buys))
print("Exemplar B: asks-sold turns:", [t for t, s, p in ref["fill_list"] if s == -1], "sum", sum(ex_b_sells))
print("sum check -9950:", sum(ex_b_sells) - sum(ex_b_buys))
for label, kw in [("p_buy 0.20", dict(p_buy=Fraction(1, 5))), ("p_buy 0.30", dict(p_buy=Fraction(3, 10))),
                  ("p_sell 0.26", dict(p_sell=Fraction(13, 50)))]:
    r = run(0, **kw)
    print("sensitivity", label, "fills", r["fills"], "pnl", r["pnl"])
# seed 7919 is the second seed of the autograder: report only its reference numbers
r2 = run(7919)
print("seed 7919 reference:", {k: r2[k] for k in ("fills", "cash", "inv", "mark", "pnl")})
