import sys
from fractions import Fraction
src = open(sys.argv[1], encoding="utf-8").read()
src = src.rsplit("\nmain()", 1)[0]
ns: dict = {"__name__": "twin_l05"}
exec(compile(src, sys.argv[1], "exec"), ns)
strikes = ns["STRIKES_CENTS"]
for D in [Fraction(0), Fraction(1, 100), Fraction(1, 2), Fraction(9, 10), Fraction(1), Fraction(3, 2)]:
    ns["DISCOUNT"] = D
    calls = []
    for k in strikes:
        price = max(ns["SPOT_CENTS"] - D * k, Fraction(0)) + Fraction(max(10_000 - k, 0), 10)
        calls.append(price)
    if any(c.denominator != 1 for c in calls):
        print("D", D, "non-integer call cents", calls)
        continue
    calls = tuple(int(c) for c in calls)
    puts = tuple(int(c - 10_000 + D * k) for k, c in zip(strikes, calls))
    bv = [(k, b) for k, c, p in zip(strikes, calls, puts) for b in ns["bounds_violations"](k, c, p)]
    cv = ns["convexity_violations"](strikes, calls)
    print("D", D, "calls", calls, "bound_violations", len(bv), "convexity_violations", len(cv))
    if D == Fraction(1, 100):
        print("  D=1/100 breaks:", bv)
