"""Round-16 fixer probe: case-by-case comparison of the committed reference (git HEAD, copied to a scratch file
outside the repository) with the fixed reference, on the seeded random page-valid sweep of probe_fix_r16.py.
Run from the repository root: .venv/bin/python -I ledgers/M7/scripts/M7-d-r16/compare_old_new_r16.py OLD_PATH"""
import importlib.util, random, sys
sys.path.insert(0, "/Users/billyribeiro/dev/quant-phd/ledgers/M7/scripts/M7-d-r16")
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    from probe_fix_r16 import recompute


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


new = load("course/modules/M/M7/grader/reference.py", "new_r16")
old = load(sys.argv[1], "old_r16")
rng = random.Random(16)
tally = {"old_bad_new_ok": 0, "new_bad_old_ok": 0, "both_bad": 0, "both_ok": 0, "refused_by_both": 0}
regress = []
for trial in range(400):
    n = rng.choice([2, 3, 4]); scale = rng.choice([0.04, 1.0, 1000.0])
    mu = [round(rng.uniform(-1, 1) * scale, 6) for _ in range(n)]
    A = [[rng.randint(-2, 2) for _ in range(n)] for _ in range(n)]
    sigma = [[sum(A[k][i] * A[k][j] for k in range(n)) + (1 if i == j else 0) for j in range(n)] for i in range(n)]
    w0 = [rng.randint(0, 100) / 100 for _ in range(n - 1)]; w0.append(round(1 - sum(w0), 12))
    tau = rng.choice([0.0, 1e-10, 1e-9, 1e-3, 0.2])
    lower = [round(-0.5 + rng.random() * 0.3, 12) for _ in range(n)]
    upper = [round(max(w0[i], 1.0) + rng.random() * 0.5, 12) for i in range(n)]
    for i in range(n):
        jitter = rng.choice([0.0, 5e-10, -5e-10, 2e-10])
        if rng.random() < 0.5:
            lower[i] = round(w0[i] + jitter, 12) if rng.random() < 0.5 else lower[i]
    sector = [0] * n
    for i in range(n): sector[i] = rng.choice([0, 1])
    sector[0], sector[-1] = 0, 1
    caps = []
    for k in range(2):
        s = sum(w0[i] for i in range(n) if sector[i] == k)
        caps.append(round(s + rng.choice([0.0, 5e-10, -5e-10, 0.3]), 12))
    c = {"label": "SIMULATED probe", "gamma": rng.choice([1.0, 0.5, 2.0]), "mu": mu, "sigma": sigma, "w0": w0,
         "lower": lower, "upper": upper, "sector": sector, "sector_caps": caps, "turnover_limit": tau}
    res = {}
    for tag, mod in (("old", old), ("new", new)):
        try:
            out = mod.allocate(dict(c))
            res[tag] = recompute(c, out["weights"], out["multipliers"])["complementary_slackness"] <= 1e-8
        except (ValueError, RuntimeError, TypeError):
            res[tag] = None
    if res["old"] is None and res["new"] is None:
        tally["refused_by_both"] += 1
    elif res["old"] is None or res["new"] is None:
        tally["refusal_differs"] = tally.get("refusal_differs", 0) + 1
    elif res["old"] and not res["new"]:
        tally["new_bad_old_ok"] += 1; regress.append((trial, c["turnover_limit"]))
    elif res["new"] and not res["old"]:
        tally["old_bad_new_ok"] += 1
    elif res["new"]:
        tally["both_ok"] += 1
    else:
        tally["both_bad"] += 1
print(tally)
print("regressions (trial, tau):", regress)
