"""Recompute the L08 lab cosines and shares unrounded (uses the lab's own functions)."""
import runpy, sys, io, contextlib
import numpy as np
src = open("tests/labs/M3/lab-M3-L08-1.py").read().replace("\nmain()", "\n")
ns = {}
exec(compile(src, "lab-M3-L08-1.py", "exec"), ns)
rng = np.random.default_rng(8)
panel = ns["simulate_panel"](rng)
lam, v = ns["pca"](panel)
level, slope, curv = ns["planted_shapes"]()
cs = []
for shape in (level, slope, curv):
    c = np.abs(v[:, :3].T @ shape)
    cs.append(float(np.max(c)))
    print("best cosine", repr(float(np.max(c))), "best index", int(np.argmax(c)))
print("min of best cosines (unrounded):", repr(min(cs)))
sh = lam / lam.sum()
print("shares unrounded:", [100*x for x in sh[:3]])
m = ns["pca"]  # unused
