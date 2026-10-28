import sys, runpy, math
sys.path.insert(0, "/tmp/verify14-CF1-d/ledgers/CF1/scripts/CF1-d-r14")
g = runpy.run_path("/tmp/verify14-CF1-d/tests/labs/CF1/lab-CF1-L06-1.py", run_name="lab")
import random
rng = random.Random(g["SEED"])
npvs = [g["npv_of"]([rng.randint(g["LOW"], g["HIGH"]) for _ in range(g["YEARS"])]) for _ in range(g["N_MAX"])]
o = sorted(npvs)
q10, q90 = g["quantile"](o, 0.1), g["quantile"](o, 0.9)
print(repr(q10), repr(q90), repr(q90 - q10), f"{q90-q10:.2f}", f"{143406.13-14896.62:.2f}", 143406.13-14896.62)
print("min/max",min(npvs),max(npvs), "neg share", sum(1 for x in npvs if x<0)/len(npvs))
