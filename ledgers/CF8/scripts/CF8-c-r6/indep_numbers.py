"""Independent recomputation of CF8 project numbers (day-by-day, exact Fractions). Verifier round 4."""
from fractions import Fraction
import math

def half_up(x):
    return math.floor(x + Fraction(1, 2))

def run(case, capped=True):
    H = 13
    def rate(weekly, day):
        w = 1 if day < 1 else (day - 1) // 7 + 1
        return Fraction(weekly[w - 1], 7)
    def flow(weekly, lag, w):
        return sum((rate(weekly, d - lag) for d in range(7 * (w - 1) + 1, 7 * w + 1)), Fraction(0))
    cash, drawn = case["cash"], case["drawn"]
    rows = []
    for w in range(1, H + 1):
        got = half_up(flow(case["sales"], case["lc"], w))
        out = half_up(flow(case["purch"], case["lp"], w)) + case["opex"][w - 1]
        before = cash + got - out
        need = max(0, case["min"] - before)
        avail = case["commit"] - drawn
        draw = min(need, avail) if capped else need
        repay = 0 if need > 0 else min(before - case["min"], drawn)
        cash = before + draw - repay
        drawn = drawn + draw - repay
        liq = cash + case["commit"] - drawn
        rows.append(dict(got=got, out=out, draw=draw, repay=repay, cash=cash, drawn=drawn, liq=liq, head=liq - case["thr"]))
    return rows

def cum(weekly, lag, upto):
    # sum of daily flows of sale days k (from -300) with k + lag <= upto
    def rate(day):
        w = 1 if day < 1 else (day - 1) // 7 + 1
        return Fraction(weekly[w - 1], 7)
    return sum((rate(k) for k in range(-300, upto - lag + 1)), Fraction(0))

def show(name, case):
    cap = run(case, True)
    free = run(case, False)
    print("==", name)
    for i, r in enumerate(cap, 1):
        print(f" w{i:2d} got {r['got']/100:.2f} out {r['out']/100:.2f} draw {r['draw']/100:.2f} repay {r['repay']/100:.2f} cash {r['cash']/100:.2f} drawn {r['drawn']/100:.2f} liq {r['liq']/100:.2f} head {r['head']/100:.2f}")
    peak = max([case["drawn"]] + [r["drawn"] for r in cap])
    req = max([case["drawn"]] + [r["drawn"] for r in free])
    short = max([0] + [max(0, case["min"] - r["cash"]) for r in cap])
    pinch = min(range(13), key=lambda i: (cap[i]["head"], i))
    print(" peak", peak, "required(cents)", req, "shortfall", short, "pinch week", pinch + 1, "headroom", cap[pinch]["head"])
    # DSO shortening by d: sales day k collected by 91 after change (k+lag-d <= 91) but not before (k+lag > 91)
    lc, lp = case["lc"], case["lp"]
    dso5 = half_up(cum(case["sales"], lc - 5, 91) - cum(case["sales"], lc, 91))
    dpo5 = half_up(cum(case["purch"], lp, 91) - cum(case["purch"], lp + 5, 91))
    print(" dso5", dso5, "dpo5", dpo5, "(dollars", dso5/100, dpo5/100, ")")

LAB1 = dict(sales=[1_000_000]*3 + [800_000]*10, purch=[700_000]*13, opex=[250_000]*13, lc=45, lp=30,
            cash=150_000, min=400_000, commit=1_000_000, drawn=0, thr=1_200_000)
LAB3 = dict(sales=[1_000_000]*5 + [700_000]*8, purch=[700_000]*13, opex=[250_000]*13, lc=30, lp=20,
            cash=100_000, min=300_000, commit=800_000, drawn=200_000, thr=400_000)
show("LAB1", LAB1)
show("LAB3", LAB3)
# Exemplar numbers
print("exA DSO5 cents exact", Fraction(5*800_000,7), half_up(Fraction(5*800_000,7)))
print("exB week10 receipts", half_up(Fraction(3*1_000_000+4*800_000,7)))
print("exB DPO5", half_up(Fraction(5*700_000,7)))
print("exB threshold min liquidity", min(r['liq'] for r in run(LAB1, True)) / 100)
print("exB Lab1 week-1 identity", (150_000 + 1_000_000 - 950_000 + 200_000 - 0) / 100)
