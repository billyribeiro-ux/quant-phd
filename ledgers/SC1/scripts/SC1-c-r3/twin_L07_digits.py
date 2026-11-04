"""Execute the L07 twin without its final main() call and print unrounded Part B/C values (boundary check)."""
import random
import sys
src = open(sys.argv[1], encoding="utf-8").read()
src = src.rsplit("\nmain()", 1)[0]
ns = {"__name__": "twin_module"}
exec(compile(src, sys.argv[1], "exec"), ns)
maxima = ns["simulate_maxima"](random.Random(ns["SEED"]))
import math
for n in ns["GRID_STEPS"]:
    mean, se = ns["mean_and_standard_error"](maxima[n])
    ind = [1.0 if m >= 1.0 else 0.0 for m in maxima[n]]
    p, pse = ns["mean_and_standard_error"](ind)
    print("N=%d mean=%.12f se=%.12f | p=%.12f pse=%.12f" % (n, mean, se, p, pse))
