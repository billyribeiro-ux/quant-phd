"""Re-run the lab twins' own functions for the seeds the lessons quote but the labs do not print.

usage: python -I extra_seed_checks.py <repo-root>
"""
import sys
from pathlib import Path

root = Path(sys.argv[1])


def load(name: str) -> dict:  # type: ignore[type-arg]
    src = (root / "tests/labs/PC3" / name).read_text(encoding="utf-8")
    body = src.rsplit("\nmain()", 1)[0]
    ns: dict = {"__name__": "twin"}  # type: ignore[type-arg]
    exec(compile(body, name, "exec"), ns)
    return ns


l4 = load("lab-PC3-L04-1.py")
path, turns = l4["play"](1)
fills = [t for t in turns if t.filled]
cash = sum(t.cash_flow_cents for t in fills)
inv = turns[-1].inventory_after
settle = path[l4["HORIZON"]]
pnl = turns[-1].cash_after_cents + inv * settle
print(f"L04 seed 1: fills={len(fills)} cash_flow={cash} inventory={inv} settlement={settle} mark={inv * settle} pnl={pnl}")

l5 = load("lab-PC3-L05-1.py")
xs = l5["make_sequence"](6, 200)
out, ops = l5["deque_maxima"](xs, 8)
naive, nc = l5["naive_maxima"](xs, 8)
print(f"L05 seed 6 k=8: equal={out == naive} naive={nc} deque_comparisons={ops.comparisons} pushes={ops.pushes} pops={ops.pops}")
