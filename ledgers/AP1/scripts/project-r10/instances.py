import sys, numpy as np
sys.path.insert(0, "/tmp/verify-ap1-r10-m/course/modules/AP/AP1/grader")
import importlib.util
spec = importlib.util.spec_from_file_location("inst", "/tmp/verify-ap1-r10-m/course/modules/AP/AP1/grader/instance.py")
inst = importlib.util.module_from_spec(spec); sys.modules["inst"] = inst; spec.loader.exec_module(inst)
rows = []; weights = []
for s in range(20):
    I = inst.make_instance(s)
    S, N = I["probs"].size, I["prices"].size
    ok = (abs(I["probs"].sum() - 1) < 1e-12 and (I["probs"] > 0).all() and (I["m_true"] > 0).all()
          and N <= S - 2 and np.allclose(I["prices"], I["payoffs"].T @ (I["probs"] * I["m_true"]))
          and (I["prices"] >= 0.3).all() and np.all(np.isfinite(I["train"])) and np.all(np.isfinite(I["test"])))
    if I["riskless"]: ok = ok and np.all(I["payoffs"][:, 0] == 1.0)
    w = np.linalg.solve(I["train"].T @ I["train"] / len(I["train"]), I["prices"])
    weights.append(w[:1].round(6).tolist())
    rows.append((s, S, N, I["riskless"], len(I["train"]), len(I["test"]), ok))
for r in rows: print("seed %2d states %2d assets %d riskless %-5s train %3d test %3d valid %s" % r)
print("distinct first weights:", len({tuple(w) for w in weights}), "of 20")
