"""Out-of-slice spot checks, recorded for the unit's other verifiers: L04 E1 (seed 1 game) and L05 E2 (seed 6, window 8).

Usage: python -I ledgers/PC3/scripts/PC3-d-r6/out_of_slice_problem_checks_r6.py <checkout>
"""
import contextlib
import importlib.util
import io
import pathlib
import random
import sys

root = pathlib.Path(sys.argv[1])


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, root / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


l05 = load("lab05b", "tests/labs/PC3/lab-PC3-L05-1.py")
xs6 = l05.make_sequence(6, 200)
out6, ops6 = l05.deque_maxima(xs6, 8)
naive6, cmp6 = l05.naive_maxima(xs6, 8)
print("L05 E2 seed 6 k=8: outputs equal", out6 == naive6, "naive", cmp6, "deque comparisons", ops6.comparisons,
      "pushes", ops6.pushes, "pops", ops6.pops)
print("L05 E2 claims: naive 1351, deque 350, pushes 200, pops 197")
l04 = load("lab04b", "tests/labs/PC3/lab-PC3-L04-1.py")
print("L04 module functions:", [n for n in dir(l04) if not n.startswith("_")][:30])
path, turns = l04.play(1)
fills = [t for t in turns if t.filled]
cash = sum(t.cash_flow_cents for t in fills)
settle = path[l04.HORIZON]
inv = turns[-1].inventory_after
print("L04 E1 seed 1: fills", len(fills), "cash flow", cash, "final inventory", inv, "settlement", settle,
      "mark", inv * settle, "P&L", turns[-1].cash_after_cents + inv * settle)
print("L04 E1 claims: fills 16, cash flow 20100, inventory -2, settlement 10020, mark -20040, P&L 60")
