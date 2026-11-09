"""Round-16 fixer probe (repository script). Runs the fixed reference on the verifier's hand inputs and on random
page-valid cases, including starts inside the 1e-9 tolerance. Recomputes the four certificate fields from the page's
definitions (as the suite does) and reports the largest residual per field, plus the reference's agreement with its
own reported fields. Run from the repository root: .venv/bin/python -I ledgers/M7/scripts/M7-d-r16/probe_fix_r16.py"""
import importlib.util, os, random, sys

ROOT = os.getcwd()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


ref = load(ROOT + "/course/modules/M/M7/grader/reference.py", "ref_probe_r16")


def recompute(c, w, m):
    n = len(c["mu"])
    d = [w[i] - c["w0"][i] for i in range(n)]
    t = [abs(x) for x in d]
    ineq = [(m["lower"][i], c["lower"][i] - w[i]) for i in range(n)]
    ineq += [(m["upper"][i], w[i] - c["upper"][i]) for i in range(n)]
    ineq += [(m["sector"][k], sum(w[i] for i in range(n) if c["sector"][i] == k) - c["sector_caps"][k])
             for k in range(len(c["sector_caps"]))]
    ineq += [(m["turnover_plus"][i], d[i] - t[i]) for i in range(n)]
    ineq += [(m["turnover_minus"][i], -d[i] - t[i]) for i in range(n)]
    ineq += [(m["turnover_total"], sum(t) - c["turnover_limit"])]
    return {"primal_residual": max([0.0, abs(sum(w) - 1)] + [g for _, g in ineq]),
            "dual_residual": max(0.0, -min(x for x, _ in ineq)),
            "complementary_slackness": max(abs(x * g) for x, g in ineq)}


def hand(mu, w0, tau, lower=(-1.0, -1.0), upper=(2.0, 2.0), sigma=((1.0, 0.0), (0.0, 1.0))):
    return {"label": "SIMULATED probe", "gamma": 1.0, "mu": list(mu), "sigma": [list(r) for r in sigma],
            "w0": list(w0), "lower": list(lower), "upper": list(upper), "sector": [0, 0],
            "sector_caps": [2.0], "turnover_limit": tau}


def report(label, c):
    out = ref.allocate(dict(c))
    rec = recompute(c, out["weights"], out["multipliers"])
    rep = out["certificate"]
    gap = max(abs(rep[k] - rec[k]) for k in rec)
    print(f"{label}: w={out['weights']} comp_rep={rep['complementary_slackness']:.3e} "
          f"comp_rec={rec['complementary_slackness']:.3e} primal_rec={rec['primal_residual']:.3e} "
          f"agree={gap:.1e} kappa={out['multipliers']['turnover_total']:.3e}")
    return rec, gap


print("== hand inputs (PRJ-R15-01)")
rA, _ = report("A mu=[1000,0] w0=(1/2,1/2) tau=1e-9", hand([1000.0, 0.0], [0.5, 0.5], 1e-9))
rE, _ = report("E mu=[1000,0] upper=(1/2+1e-9,2) tau=2", hand([1000.0, 0.0], [0.5, 0.5], 2.0,
                                                          upper=(0.5 + 1e-9, 2.0)))
report("B mu=[100,0] tau=1e-10", hand([100.0, 0.0], [0.5, 0.5], 1e-10))
report("C mu=[10,0] tau=0", hand([10.0, 0.0], [0.5, 0.5], 0.0))

print("== random page-valid cases")
rng = random.Random(16)
worst = {"primal_residual": 0.0, "stationarity_residual": 0.0, "dual_residual": 0.0, "complementary_slackness": 0.0}
worst_agree = 0.0
answered = refused = 0
for trial in range(int(os.environ.get("TRIALS", "400"))):
    n = rng.choice([2, 3, 4])
    scale = rng.choice([0.04, 1.0, 1000.0])
    mu = [round(rng.uniform(-1, 1) * scale, 6) for _ in range(n)]
    # SPD sigma: A'A + I with small integers, exact in decimal
    A = [[rng.randint(-2, 2) for _ in range(n)] for _ in range(n)]
    sigma = [[sum(A[k][i] * A[k][j] for k in range(n)) + (1 if i == j else 0) for j in range(n)] for i in range(n)]
    w0 = [rng.randint(0, 100) / 100 for _ in range(n - 1)]
    w0.append(round(1 - sum(w0), 12))
    tau = rng.choice([0.0, 1e-10, 1e-9, 1e-3, 0.2])
    lower = [round(-0.5 + rng.random() * 0.3, 12) for _ in range(n)]
    upper = [round(max(w0[i], 1.0) + rng.random() * 0.5, 12) for i in range(n)]
    for i in range(n):  # a start on or inside its bounds, or a start within the tolerance outside them
        jitter = rng.choice([0.0, 5e-10, -5e-10, 2e-10])
        if rng.random() < 0.5:
            lower[i] = round(w0[i] + jitter, 12) if rng.random() < 0.5 else lower[i]
    sector = [0] * n
    for i in range(n):
        sector[i] = rng.choice([0, 1])
    sector[0], sector[-1] = 0, 1
    caps = []
    for k in range(2):
        s = sum(w0[i] for i in range(n) if sector[i] == k)
        caps.append(round(s + rng.choice([0.0, 5e-10, -5e-10, 0.3]), 12))
    c = {"label": "SIMULATED probe", "gamma": rng.choice([1.0, 0.5, 2.0]), "mu": mu, "sigma": sigma, "w0": w0,
         "lower": lower, "upper": upper, "sector": sector, "sector_caps": caps, "turnover_limit": tau}
    try:
        out = ref.allocate(dict(c))
    except (ValueError, RuntimeError, TypeError) as exc:
        refused += 1
        continue
    answered += 1
    rec = recompute(c, out["weights"], out["multipliers"])
    rep = out["certificate"]
    worst_agree = max(worst_agree, max(abs(rep[k] - rec[k]) for k in rec))
    for k in worst:
        if k in rec:
            worst[k] = max(worst[k], rec[k])
print(f"answered={answered} refused={refused}")
print("worst recomputed residuals:", {k: f"{v:.3e}" for k, v in worst.items() if k in ('primal_residual', 'dual_residual', 'complementary_slackness')})
print(f"worst agreement reported vs recomputed (excluding stationarity): {worst_agree:.3e}")
