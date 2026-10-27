"""Round-3 check of L02 E2 and Lab 1 shares: unrounded log changes from the L02 twin's own functions.

Usage: .venv/bin/python -I ledgers/AC2/scripts/L01-L02-r3/l02_e2_unrounded.py tests/labs/AC2/lab-AC2-L02-1.py
The twin's final main() call is removed before exec; the twin is not changed.
"""
import math
import sys
import types

src = open(sys.argv[1], encoding="utf-8").read().rstrip()
assert src.endswith("main()")
src = src[: -len("main()")]
mod = types.ModuleType("twin")
sys.modules["twin"] = mod
ns = mod.__dict__
exec(compile(src, sys.argv[1], "exec"), ns)
filer = ns["make_filer"]()
st = ns["standardize"](filer)
d23 = ns["dupont"](st, "2023-12-31")
d24 = ns["dupont"](st, "2024-12-31")
tot = math.log(d24["roe"] / d23["roe"])
print("total log change:", round(tot, 6))
for f in ("net_margin", "asset_turnover", "leverage"):
    lc = math.log(d24[f] / d23[f])
    print(f, round(lc, 6), "share %", round(100 * lc / tot, 3))
print("from printed 4-digit values: nm", round(math.log(0.0874 / 0.1179), 6), "roe", round(math.log(0.1237 / 0.1738), 6))
