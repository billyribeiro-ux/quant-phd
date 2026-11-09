"""Round-15 re-check of the nine equivalence candidates in ledgers/M7/equivalent against the reference.
For each random page-valid case (instance-shaped, plus hand-scale cases with large returns and tiny turnover limits),
compares each candidate's output with the reference: a candidate is distinguished when a certificate field differs by
more than the page's agreement tolerance 1e-9 from the field recomputed (page definitions) from the same weights and
multipliers. Also checks F2 (smallest inequality multiplier exactly 0). Run from the repository root with python -I."""
import glob, importlib.util, os, random, sys
from fractions import Fraction
ROOT = os.getcwd()
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m; spec.loader.exec_module(m); return m
ref = load(ROOT + "/course/modules/M/M7/grader/reference.py", "ref_mod")
cands = sorted(glob.glob(ROOT + "/ledgers/M7/equivalent/*.py"))
mods = {os.path.basename(p): load(p, "cand_%d" % i) for i, p in enumerate(cands)}

def recompute(c, w, m):
    n = len(c["mu"]); d = [w[i] - c["w0"][i] for i in range(n)]; t = [abs(x) for x in d]
    ineq = [(m["lower"][i], c["lower"][i] - w[i]) for i in range(n)] + [(m["upper"][i], w[i] - c["upper"][i]) for i in range(n)]
    ineq += [(m["sector"][k], sum(w[i] for i in range(n) if c["sector"][i] == k) - c["sector_caps"][k]) for k in range(len(c["sector_caps"]))]
    ineq += [(m["turnover_plus"][i], d[i] - t[i]) for i in range(n)] + [(m["turnover_minus"][i], -d[i] - t[i]) for i in range(n)]
    ineq += [(m["turnover_total"], sum(t) - c["turnover_limit"])]
    rec = {"primal_residual": max([0.0, abs(sum(w) - 1)] + [g for _, g in ineq]),
           "dual_residual": max(0.0, -min(x for x, _ in ineq)),
           "complementary_slackness": max(abs(x * g) for x, g in ineq)}
    return rec, min(x for x, _ in ineq)

rng = random.Random(15)
def rand_case(scale, tau_choice):
    n = rng.choice([2, 3, 4])
    A = [[rng.randint(-2, 2) for _ in range(n)] for _ in range(n)]
    sig = [[(sum(A[k][i] * A[k][j] for k in range(n)) + (1 if i == j else 0)) / 1000 for j in range(n)] for i in range(n)]
    mu = [round(rng.uniform(-1, 1) * scale, 6) for _ in range(n)]
    w0 = [rng.random() for _ in range(n)]; s = sum(w0); w0 = [round(x / s, 6) for x in w0]
    w0[-1] = round(1 - sum(w0[:-1]), 6)
    lower = [-0.1] * n; upper = [max(w0[i], 1.0) for i in range(n)]
    sector = [i % 2 for i in range(n)]; caps = [round(sum(w0[i] for i in range(n) if sector[i] == k) + rng.choice([0, 0.05]), 6) for k in range(2)]
    tau = {"zero": 0.0, "tiny": 1e-9, "small": 0.05, "mid": 0.3}[tau_choice]
    return {"label": "SIMULATED recheck", "gamma": rng.choice([0.5, 1.0, 4.0]), "mu": mu, "sigma": sig, "w0": w0,
            "lower": lower, "upper": upper, "sector": sector, "sector_caps": caps, "turnover_limit": tau}

stats = {name: {"distinguished": 0, "answered": 0, "max_diff": 0.0} for name in mods}
f2_bad = 0; answered = 0; refused = 0
for trial in range(400):
    scale = rng.choice([0.04, 1.0, 100.0, 1000.0])
    c = rand_case(scale, rng.choice(["zero", "tiny", "small", "mid"]))
    try:
        base = ref.allocate(c)
    except Exception:
        refused += 1; continue
    answered += 1
    w = base["weights"]; m = base["multipliers"]
    rec, mn = recompute(c, w, m)
    if mn != 0:
        f2_bad += 1
    for name, mod in mods.items():
        out = mod.allocate(c)
        cert = out["certificate"]
        worst = max(abs(cert[k] - rec[k]) for k in ("primal_residual", "dual_residual", "complementary_slackness"))
        worst = max(worst, abs(cert["stationarity_residual"] - base["certificate"]["stationarity_residual"]))
        stats[name]["answered"] += 1
        stats[name]["max_diff"] = max(stats[name]["max_diff"], worst)
        if worst > 1e-9:
            stats[name]["distinguished"] += 1
print("random cases answered by reference:", answered, "refused:", refused)
print("reference smallest inequality multiplier != 0 on", f2_bad, "answers (F2 check)")
for name in sorted(stats):
    s = stats[name]
    print("%-70s answered=%d distinguished_beyond_1e-9=%d max_diff_vs_recomputed=%.3g" % (name, s["answered"], s["distinguished"], s["max_diff"]))
