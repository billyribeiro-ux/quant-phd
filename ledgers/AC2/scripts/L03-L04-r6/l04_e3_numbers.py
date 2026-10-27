# Recompute the L04 E3 figures from the twin's own functions at full precision (independent of the printed 4 dp).
import sys, types
import numpy as np
src = open(sys.argv[1], encoding="utf-8").read()
mod = types.ModuleType("twin"); sys.modules["twin"] = mod
exec(compile(src.split("\ndef main")[0], sys.argv[1], "exec"), mod.__dict__)
ns = mod.__dict__
n = 400
moving = ns["build_panel"](np.random.default_rng(2604), n, moving=True)
cf = ns["accruals_cash_flow"](moving); bs = ns["accruals_balance_sheet"](moving)
r = float(np.corrcoef(cf, bs)[0, 1])
print("r", r, "r2", r * r, "1-r2", 1 - r * r)
print("var(gap)/var(cf)", float(np.var(cf - bs, ddof=1) / np.var(cf, ddof=1)))
print("printed-check corr 4dp", f"{r:.4f}", "r2 4dp", f"{r*r:.4f}", "1-r2 4dp", f"{1-r*r:.4f}", "varratio 4dp", f"{float(np.var(cf-bs, ddof=1)/np.var(cf, ddof=1)):.4f}")
