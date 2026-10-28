"""Count boundary cases (equality) that the L07 and L08 lab checks would have to exercise, over seeds 1..40 and the lab seed."""
import re
import sys

root = sys.argv[1]
ns = {}
src7 = open(f"{root}/tests/labs/AC4/lab-AC4-L07-1.py", encoding="utf-8").read()
src8 = open(f"{root}/tests/labs/AC4/lab-AC4-L08-1.py", encoding="utf-8").read()
import importlib.util
import types


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    src = open(path, encoding="utf-8").read().replace("\nmain()", "\n")
    exec(compile(src, path, "exec"), mod.__dict__)
    return mod.__dict__


g7 = load("l07mod", f"{root}/tests/labs/AC4/lab-AC4-L07-1.py")
g8 = load("l08mod", f"{root}/tests/labs/AC4/lab-AC4-L08-1.py")
for seed in [20261027] + list(range(1, 41)):
    cases = g7["generate"](seed, 200)
    fits = [c for c in cases if c.q <= c.capacity]
    tie = sum(1 for c in fits if g7["t_min"](c) == g7["t_max"](c))
    s0 = sum(1 for c in fits if g7["firm_surplus"](c) == 0)
    divs = g8["generate"](seed, 8)
    rzero = sum(1 for d in divs if g8["residual_income"](d) == 0)
    rate_eq = sum(1 for d in divs if g8["return_ratio"](d) == g8["Fraction"](900, 10000))
    tie_rank = 0
    for a in divs:
        for b in divs:
            if a.name < b.name and (g8["residual_income"](a) == g8["residual_income"](b) or g8["return_ratio"](a) == g8["return_ratio"](b)):
                tie_rank += 1
    if seed == 20261027 or tie or s0 or rzero or rate_eq or tie_rank:
        print(f"seed {seed}: L07 fits {len(fits)} t_min==t_max {tie} surplus==0 {s0}; L08 RI==0 {rzero} OI/C==r {rate_eq} rank ties {tie_rank}")
print("scan done")
