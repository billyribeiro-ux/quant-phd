"""Round-16 fixer (ruling 35): compare each proof file with the reference on exactly feasible starts, and separately
count the cases only a proof file answers (tolerance-level breaches the reference refuses), with their largest breach."""
import glob, importlib.util, json, os, random, sys
from fractions import Fraction
ROOT = os.getcwd()
sys.path.insert(0, ROOT + "/course/modules/M/M7/grader")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


ref = load(ROOT + "/course/modules/M/M7/grader/reference.py", "ref_x")
inst = load(ROOT + "/course/modules/M/M7/grader/instance.py", "inst_x")


def flat(out):
    v = list(out["weights"])
    for key in sorted(out["multipliers"]):
        val = out["multipliers"][key]
        v.extend(val if isinstance(val, list) else [val])
    v.extend(out["certificate"][k] for k in sorted(out["certificate"]))
    return v


def start_breach(c):
    """Largest exact breach of the starting portfolio (budget, bounds, sector caps), read from the decimal text."""
    F = lambda v: Fraction(repr(float(v)))
    w0 = [F(v) for v in c["w0"]]
    lo = [F(v) for v in c["lower"]]
    up = [F(v) for v in c["upper"]]
    caps = [F(v) for v in c["sector_caps"]]
    sec = c["sector"]
    b = [abs(sum(w0) - 1)]
    b += [max(lo[i] - w0[i], w0[i] - up[i], Fraction(0)) for i in range(len(w0))]
    b += [max(sum((w0[i] for i in range(len(w0)) if sec[i] == k), Fraction(0)) - caps[k], Fraction(0)) for k in range(len(caps))]
    return float(max(b))


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
        sector = [rng.choice([0, 1]) for _ in range(n)]
        sector[0], sector[-1] = 0, 1
        caps = []
        for k in range(2):
            s = sum(w0[i] for i in range(n) if sector[i] == k)
            caps.append(round(s + rng.choice([0.0, 5e-10, -5e-10, 0.3]), 12))
        yield {"label": "SIMULATED probe", "gamma": rng.choice([1.0, 0.5, 2.0]), "mu": mu, "sigma": sigma, "w0": w0,
               "lower": lower, "upper": upper, "sector": sector, "sector_caps": caps, "turnover_limit": tau}


cases = [("gen%d" % s, json.loads(inst.make_instance(s)["payload"])) for s in range(50)]
cases += [("rand%d" % i, c) for i, c in enumerate(random_cases(400))]
base = {}
for name, c in cases:
    try:
        base[name] = flat(ref.allocate(dict(c)))
    except (ValueError, RuntimeError, TypeError):
        base[name] = None
for path in sorted(glob.glob(ROOT + "/ledgers/M7/equivalent/*.py")):
    mod = load(path, "eq_" + os.path.basename(path)[:-3])
    exact_answered = exact_differ = refused_only = 0
    worst_exact = 0.0
    max_breach_mutant_only = 0.0
    for name, c in cases:
        b = base[name]
        try:
            o = flat(mod.allocate(dict(c)))
        except (ValueError, RuntimeError, TypeError):
            o = None
        if b is None and o is None:
            continue
        if b is None:
            refused_only += 1
            max_breach_mutant_only = max(max_breach_mutant_only, start_breach(c))
            continue
        if o is None:
            exact_differ += 1
            continue
        exact_answered += 1
        d = max(abs(x - y) for x, y in zip(b, o))
        worst_exact = max(worst_exact, d)
        if d > 1e-9:
            exact_differ += 1
    print(f"{os.path.basename(path)}: exact-start answered={exact_answered} differ_over_1e-9={exact_differ} "
          f"largest_diff={worst_exact:.3e} | answered_only_by_file (reference refuses)={refused_only} "
          f"largest_start_breach={max_breach_mutant_only:.3e}")
