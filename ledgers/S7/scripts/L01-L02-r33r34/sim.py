import sys, importlib.util
import numpy as np
from scipy import stats
spec = importlib.util.spec_from_file_location("ks", "/tmp/verify-s7-r1-l12/tests/test_koning_spot.py")
ks = importlib.util.module_from_spec(spec); spec.loader.exec_module(ks)
phi, reject = ks._paths()
print("size (reject mean)", repr(float(reject.mean())))
print("max |phi_N - reject|", float(np.max(np.abs(phi[:, -1] - reject))))
m = phi.mean(axis=0)
print("martingale E[phi_n] min,max", float(m.min()), float(m.max()), "argmin", int(m.argmin()) + 1, "argmax", int(m.argmax()) + 1)
print("E[phi_n] all n:", [round(float(x), 5) for x in m])
for threshold in (0.5, 0.2, 0.05):
    hit = phi >= threshold
    first = np.where(hit.any(axis=1), hit.argmax(axis=1), ks.N - 1)
    stopped = phi[np.arange(ks.REPS), first]
    print("threshold", threshold, "E[phi_tau]", repr(float(stopped.mean())), "frac stopped early", float(hit.any(axis=1).mean()))
se = np.sqrt(0.05 * 0.95 / ks.REPS)
print("SE", se, "6SE", 6 * se, "TOLERANCE/SE", ks.TOLERANCE / se)
