"""Recompute the L03 Lab 1 standard errors unrounded (same seed, same draw order) and the SE gaps."""
import importlib.util
import math
import random
import sys

LAB = sys.argv[1]
spec = importlib.util.spec_from_file_location("l03lab", LAB)
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)

rng = random.Random(lab.SEED)
rows = []
for horizon in lab.HORIZONS:
    for k in lab.LEVELS:
        steps = 2**k
        vals = lab.squared_increment_sums(horizon, steps, lab.PATHS, rng)
        mean, se = lab.mean_and_standard_error(vals)
        z = (mean - horizon) / se
        ref = horizon * math.sqrt(2 / steps) / 20
        rows.append((horizon, steps, round(mean, 4), round(se, 4), se, ref, z, mean))
worst_printed = max(rows, key=lambda r: abs(round(r[3], 4) / r[5] - 1))
worst_unr = max(rows, key=lambda r: abs(r[4] / r[5] - 1))
for r in rows:
    print(f"H={r[0]:g} N={r[1]:3d} printed_se={r[3]:.4f} unrounded_se={r[4]:.10f} ref={r[5]:.6f} "
          f"gap_printed={100*(r[3]/r[5]-1):+.2f}% gap_unrounded={100*(r[4]/r[5]-1):+.3f}% z={r[6]:+.3f}")
print("max |z| =", max(abs(r[6]) for r in rows))
print("worst printed gap at H=%g N=%d: %+.3f%%" % (worst_printed[0], worst_printed[1], 100*(worst_printed[3]/worst_printed[5]-1)))
print("worst unrounded gap at H=%g N=%d: %+.3f%%" % (worst_unr[0], worst_unr[1], 100*(worst_unr[4]/worst_unr[5]-1)))
print("max |printed gap| <= 14 percent:", max(abs(r[3]/r[5]-1) for r in rows) <= 0.14)
print("0.1601/(2*sqrt2/20)-1 =", 100*(0.1601/(2*math.sqrt(2)/20)-1))
