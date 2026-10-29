# Re-run L06 twin's own functions without the printing step (round 23). Run as: python -I this.py <twin path>
import sys, random, math
src = open(sys.argv[1], encoding="utf-8").read()
src = src.rsplit("\nmain()", 1)[0]
ns: dict = {"__name__": "lab_noprint"}
exec(compile(src, sys.argv[1], "exec"), ns)
rng = random.Random(ns["SEED"])
npvs = [ns["npv_of"]([rng.randint(ns["LOW"], ns["HIGH"]) for _ in range(ns["YEARS"])]) for _ in range(ns["N_MAX"])]
o = sorted(npvs)
q10, q90 = ns["quantile"](o, 0.10), ns["quantile"](o, 0.90)
print(repr(q10), repr(q90), repr(q90 - q10))
neg = sum(1 for x in npvs if x < 0)
print("negative_count", neg, "share", neg / ns["N_MAX"], "se", math.sqrt((neg/ns["N_MAX"])*(1-neg/ns["N_MAX"])/ns["N_MAX"]))
print("median", repr(ns["quantile"](o, 0.5)))
