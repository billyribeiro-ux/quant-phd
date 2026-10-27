import importlib.util, sys
import numpy as np
sys.path.insert(0, "/tmp/ap1-r5/project-r10/ref")
from instance import make_instance
def load(name):
    spec = importlib.util.spec_from_file_location(name, f"/tmp/ap1-r5/project-r10/{name}/sdf_recovery.py")
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m
names = ["ref", "a_lstsq", "b_pinv", "c_cov_solve"]
mods = {n: load(n) for n in names}
worst = {}
minstd = []
for seed in range(50):
    I = make_instance(seed)
    rf = I["riskless"]
    RISKY = I["train"][:, 1:] if rf else I["train"]
    RP = I["prices"][1:] if rf else I["prices"]
    for n, sol in mods.items():
        ua, ub = sol.min_variance_sdf(RISKY, RP, 0.97)
        mu_ = ua + RISKY @ np.asarray(ub)
        std_unit = sol.min_sdf_std(RISKY, RP, 0.97)
        for scale in (1e-11, 1e11):
            a, b = sol.min_variance_sdf(scale * RISKY, scale * RP, 0.97)
            m_ = a + (scale * RISKY) @ np.asarray(b)
            dm = float(np.max(np.abs(m_ - mu_) / (1e-7 + 1e-7 * np.abs(mu_))))
            da = abs(a - ua) / (1e-9 + 1e-7 * abs(ua))
            bb = np.asarray(b) * scale
            db = float(np.max(np.abs(bb - np.asarray(ub)) / (1e-7 + 1e-7 * np.abs(np.asarray(ub)))))
            ds = abs(sol.min_sdf_std(scale * RISKY, scale * RP, 0.97) - std_unit) / (1e-7 * abs(std_unit))
            for k, v in (("m", dm), ("a", da), ("b", db), ("std", ds)):
                worst[(n, scale, k)] = max(worst.get((n, scale, k), 0.0), v)
    minstd.append(std_unit)
for k in sorted(worst, key=str):
    print(k, f"worst fraction of tolerance used: {worst[k]:.3e}")
print("min-std value over seeds (ref, unit scale):", f"{min(minstd):.4g}", "max:", f"{max(minstd):.4g}")
