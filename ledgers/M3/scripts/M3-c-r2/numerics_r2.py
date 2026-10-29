# Independent recomputation for M3-c round 2 (L08 lab numbers, L09 bounds).
import sys
import numpy as np
src = open("/tmp/verifyB2-M3-c/tests/labs/M3/lab-M3-L08-1.py").read().split("def main()")[0]
exec(src)
rng = np.random.default_rng(8)
panel = simulate_panel(rng)
T = panel.shape[0]
xc = panel - panel.mean(axis=0)
m = xc.T @ xc / (T - 1)
lam, v = pca(panel)
sh = lam / lam.sum()
print("unrounded shares %", 100 * sh[:3])
level, slope, curv = planted_shapes()
for name, s in zip(("level", "slope", "curv"), (level, slope, curv)):
    c = np.abs(v[:, :3].T @ s)
    print(name, "abs cosines to PC1..3 (unrounded):", c, "max", c.max())
M11 = m[0, 0]; T0 = np.trace(m)
print("M11", repr(M11), "T0", repr(T0))
bound = 100 * M11 / (T0 + 99 * M11)
print("bound unrounded", bound, "old share", lam[0] / T0)
r = panel.copy(); r[:, 0] *= 10
lam3, _ = pca(r)
print("new share", lam3[0] / lam3.sum(), "new trace", lam3.sum(), "T0+99M11", T0 + 99 * M11)
print("check new M11 = 100*M11:", np.trace(np.cov(r.T)) if False else "")
mr = r - r.mean(axis=0); mr = mr.T @ mr / (T - 1)
print("rescaled M11", mr[0, 0], 100 * M11, "rescaled trace", np.trace(mr), "T0+99M11", T0 + 99 * M11)
print("lam1' >= 100 M11 ?", lam3[0] >= 100 * M11)
# rounding of printed digits
print("printed bound from displayed inputs:", 100 * 13.6818 / (88.2028 + 99 * 13.6818))
print("printed shares sum unrounded", 100 * sh[:3].sum(), "printed sum 99.2")
