"""Recompute the seed-1 (L04 E1) and seed-6 (L05 E2) numbers by importing the lab twins' own functions.

Usage: python -I recompute_E_problems.py <checkout-root>. Each twin's main() is not run; its functions are loaded
from source with the module-level main() call stripped, so that only the functions are used.
"""
import sys
import types

root = sys.argv[1]


def load(path: str, name: str) -> types.ModuleType:
    src = open(path, encoding="utf-8").read()
    src = src.rsplit("\nmain()", 1)[0] if src.rstrip().endswith("main()") else src
    mod = types.ModuleType(name)
    sys.modules[name] = mod
    exec(compile(src, path, "exec"), mod.__dict__)
    return mod


# L04: seed 1 game
l4 = load(f"{root}/tests/labs/PC3/lab-PC3-L04-1.py", "l4")
path, turns = l4.play(1)
fills = [t for t in turns if t.filled]
cash_flow = sum(t.cash_flow_cents for t in fills)
inv = turns[-1].inventory_after
settle = path[l4.HORIZON]
print("L04 seed 1: fills", len(fills), "of", l4.HORIZON, "cash flow", cash_flow, "final inventory", inv,
      "settlement", settle, "mark", inv * settle, "P&L", turns[-1].cash_after_cents + inv * settle,
      "cash+mark identity", turns[-1].cash_after_cents + inv * settle == cash_flow + inv * settle)
# L04 seed 0 for E3 and E2 cross-checks
path0, turns0 = l4.play(0)
arr0 = [t.arrival for t in turns0]
print("L04 seed 0 informed arrivals:", arr0.count("informed"), "of", len(arr0))
print("L04 seed 0 last quote:", (turns0[-1].bid_cents, turns0[-1].ask_cents), "settlement", path0[-1])

# L05: seed 6 deque and naive
l5 = load(f"{root}/tests/labs/PC3/lab-PC3-L05-1.py", "l5")
xs6 = l5.make_sequence(6, 200)
naive6, nc6 = l5.naive_maxima(xs6, 8)
fast6, ops6 = l5.deque_maxima(xs6, 8)
print("L05 seed 6 k=8: outputs equal", naive6 == fast6, "naive comparisons", nc6,
      "deque comparisons", ops6.comparisons, "pushes", ops6.pushes, "pops", ops6.pops)
xs5 = l5.make_sequence(5, 200)
n5, nc5 = l5.naive_maxima(xs5, 8)
f5, o5 = l5.deque_maxima(xs5, 8)
print("L05 seed 5 k=8 (control): comparisons", o5.comparisons, "pops", o5.pops)
print("L05 seed 6 outputs equal for k=1..20:", all(l5.naive_maxima(xs6, k)[0] == l5.deque_maxima(xs6, k)[0] for k in range(1, 21)))
