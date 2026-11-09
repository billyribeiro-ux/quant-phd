"""Round-16 fixer probe: locate random page-valid cases whose complementary slackness exceeds 1e-8 under the fixed
reference, and tally the refusal reasons. Same generator as probe_fix_r16.py (seeded). Run from the repository root:
.venv/bin/python -I ledgers/M7/scripts/M7-d-r16/probe_bad_r16.py"""
import collections, importlib.util, os, random, sys

ROOT = os.getcwd()
spec = importlib.util.spec_from_file_location("ref_bad_r16", ROOT + "/course/modules/M/M7/grader/reference.py")
ref = importlib.util.module_from_spec(spec)
sys.modules["ref_bad_r16"] = ref
spec.loader.exec_module(ref)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from probe_fix_r16 import recompute  # noqa: E402  (re-runs the hand section; harmless)

rng = random.Random(16)
reasons = collections.Counter()
bad = []
for trial in range(400):
    n = rng.choice([2, 3, 4])
    scale = rng.choice([0.04, 1.0, 1000.0])
    mu = [round(rng.uniform(-1, 1) * scale, 6) for _ in range(n)]
    A = [[rng.randint(-2, 2) for _ in range(n)] for _ in range(n)]
    sigma = [[sum(A[k][i] * A[k][j] for k in range(n)) + (1 if i == j else 0) for j in range(n)] for i in range(n)]
    w0 = [rng.randint(0, 100) / 100 for _ in range(n - 1)]
    w0.append(round(1 - sum(w0), 12))
    tau = rng.choice([0.0, 1e-10, 1e-9, 1e-3, 0.2])
    lower = [round(-0.5 + rng.random() * 0.3, 12) for _ in range(n)]
    upper = [round(max(w0[i], 1.0) + rng.random() * 0.5, 12) for i in range(n)]
    for i in range(n):
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
        reasons[f"{type(exc).__name__}: {str(exc)[:70]}"] += 1
        continue
    rec = recompute(c, out["weights"], out["multipliers"])
    if rec["complementary_slackness"] > 1e-8:
        bad.append((trial, c, out, rec))
print("refusals:")
for k, v in reasons.most_common():
    print(f"  {v:4d}  {k}")
print(f"complementary > 1e-8: {len(bad)} cases")
for trial, c, out, rec in bad[:6]:
    print(f"trial {trial}: n={len(c['mu'])} mu={c['mu']} tau={c['turnover_limit']} caps={c['sector_caps']} sector={c['sector']}")
    print(f"   w0={c['w0']} lower={c['lower']} upper={c['upper']}")
    print(f"   w={out['weights']} comp_rec={rec['complementary_slackness']:.3e}")
    print(f"   lower_m={out['multipliers']['lower']} upper_m={out['multipliers']['upper']} sector_m={out['multipliers']['sector']}")
