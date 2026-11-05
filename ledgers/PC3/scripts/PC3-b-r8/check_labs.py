import sys
import types
from fractions import Fraction as F


def load(path):
    src = open(path, encoding="utf-8").read()
    assert src.rstrip().endswith("main()")
    src = src.rstrip()[: -len("main()")]
    mod = types.ModuleType("twin_import")
    sys.modules["twin_import"] = mod
    exec(compile(src, path, "exec"), mod.__dict__)
    return mod.__dict__


l4 = load("tests/labs/PC3/lab-PC3-L04-1.py")
path, turns = l4["play"](1)
fills = [r for r in turns if r.filled]
cf = sum(r.cash_flow_cents for r in fills)
inv = turns[-1].inventory_after
settle = path[l4["HORIZON"]]
print("L04 seed1 fills", len(fills), "cash flow", cf, "inv", inv, "settle", settle,
      "mark", inv * settle, "pnl", turns[-1].cash_after_cents + inv * settle,
      "maxabs", max(abs(r.inventory_after) for r in turns))

l5 = load("tests/labs/PC3/lab-PC3-L05-1.py")
xs = l5["make_sequence"](6, 200)
naive, nc = l5["naive_maxima"](xs, 8)
fast, ops = l5["deque_maxima"](xs, 8)
print("L05 seed6 outputs equal", naive == fast, "naive", nc, "deque cmp", ops.comparisons,
      "pushes", ops.pushes, "pops", ops.pops, "<=400", ops.comparisons <= 400)
