import re, sys, types
import numpy as np
src = open(sys.argv[1], encoding="utf-8").read()
src = re.sub(r"^main\(\)\s*$", "", src, flags=re.M)
mod = types.ModuleType("twin_L04"); sys.modules["twin_L04"] = mod
exec(compile(src, "twin", "exec"), mod.__dict__)
for seed in (2604, 2605, 2606):
    p = mod.build_panel(np.random.default_rng(seed), 400, moving=True)
    cf = (p.ni - mod.cfo_from_balance_sheet(p)) / mod.average_total_assets(p)
    bs = ((p.ca_other1 - p.ca_other0) - (p.cl1 - p.cl0) - p.dep) / mod.average_total_assets(p)
    print(seed, round(float(np.mean(np.abs(cf - bs) > 0.01)), 4))
