"""Round-16 fixer: output comparison of the fixed reference with each proof file in ledgers/M7/equivalent/.
Cases: the generator's instances for seeds 0-49, and a seeded random sweep of 400 page-valid cases that includes
starts inside the 1e-9 tolerance. For each file, reports the number of cases whose weights, multipliers or
certificate fields differ from the reference's by more than 1e-9 (the page's agreement tolerance), and the largest
difference. Run from the repository root: .venv/bin/python -I ledgers/M7/scripts/M7-d-r16/equiv_recheck_r16.py"""
import glob, importlib.util, os, random, sys
ROOT = os.getcwd()
sys.path.insert(0, ROOT + "/course/modules/M/M7/grader")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


ref = load(ROOT + "/course/modules/M/M7/grader/reference.py", "ref_eq_r16")
inst = load(ROOT + "/course/modules/M/M7/grader/instance.py", "inst_eq_r16")


def flat(out):
    v = list(out["weights"])
    for key in sorted(out["multipliers"]):
        val = out["multipliers"][key]
        v.extend(val if isinstance(val, list) else [val])
    v.extend(out["certificate"][k] for k in sorted(out["certificate"]))
    return v


def random_cases(trials):
    rng = random.Random(16)
    for _ in range(trials):
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
        yield {"label": "SIMULATED probe", "gamma": rng.choice([1.0, 0.5, 2.0]), "mu": mu, "sigma": sigma, "w0": w0,
               "lower": lower, "upper": upper, "sector": sector, "sector_caps": caps, "turnover_limit": tau}


cases = []
import json
for seed in range(50):
    cases.append(("gen%d" % seed, json.loads(inst.make_instance(seed)["payload"])))
cases += [("rand%d" % i, c) for i, c in enumerate(random_cases(400))]
base_out = {}
for name, c in cases:
    try:
        base_out[name] = flat(ref.allocate(dict(c)))
    except (ValueError, RuntimeError, TypeError):
        base_out[name] = None
for path in sorted(glob.glob(ROOT + "/ledgers/M7/equivalent/*.py")):
    mod = load(path, "eq_" + os.path.basename(path)[:-3])
    mism, worst, answered = 0, 0.0, 0
    for name, c in cases:
        b = base_out[name]
        try:
            o = flat(mod.allocate(dict(c)))
        except (ValueError, RuntimeError, TypeError):
            o = None
        if b is None or o is None:
            if (b is None) != (o is None):
                mism += 1
            continue
        answered += 1
        d = max(abs(x - y) for x, y in zip(b, o))
        worst = max(worst, d)
        if d > 1e-9:
            mism += 1
    print(f"{os.path.basename(path)}: answered={answered} cases_differ_over_1e-9={mism} largest_difference={worst:.3e}")
