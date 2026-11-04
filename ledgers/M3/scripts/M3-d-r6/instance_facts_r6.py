"""Round-6 verifier: re-derive the instance claims of project.html (line 231-233) on seeds 0-199 from instance.py."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "course/modules/M/M3/grader"))
import instance as inst
ks, bad, worst, lo_v, hi_v, sp_bad, pd_bad, sym_bad = {}, [], -9.0, 9.0, 0.0, 0, 0, 0
for seed in range(200):
    d = inst.make_instance(seed)
    k = d["k"]; ks[k] = ks.get(k, 0) + 1
    c = d["corr"]
    if any(abs(c[i][i] - 1.0) > 0 for i in range(k)): bad.append(("diag", seed))
    if any(abs(c[i][j] - c[j][i]) > 0 for i in range(k) for j in range(k)): sym_bad += 1
    me = inst._min_eigenvalue(c)
    worst = max(worst, me)
    if not me < -0.02: bad.append(("margin", seed, me))
    for v in d["vols"]:
        lo_v = min(lo_v, v); hi_v = max(hi_v, v)
    if len(d["vols"]) != k: bad.append(("vols-len", seed))
    if inst._min_eigenvalue(d["psd_corr"]) <= 0: pd_bad += 1
    if d["psd_spectrum"][0] != 0.0 or any(x < 0 for x in d["psd_spectrum"]): sp_bad += 1
    if len(d["eigenvectors"]) != k: bad.append(("evec", seed))
print("k counts", ks, "| asymmetric", sym_bad, "| bad", bad[:5], "| max min-eig over seeds", round(worst, 6))
print("vols range", lo_v, hi_v, "| psd_corr not PD", pd_bad, "| psd_spectrum violations", sp_bad)
