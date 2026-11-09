"""Round-16 fixer: candidate hand cases for the new mutants. For each candidate, reports whether the fixed reference
returns the worked answer with the certificate inside 1e-8 (the suite's standard), and which mutants fail it.
Run from the repository root: .venv/bin/python ledgers/M7/scripts/M7-d-r16/candidates_r16.py"""
import glob, importlib.util, io, contextlib, os, sys
ROOT = os.getcwd()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


sys.path.insert(0, ROOT + "/ledgers/M7/scripts/M7-d-r16")
with contextlib.redirect_stdout(io.StringIO()):
    from probe_fix_r16 import recompute


def cert_ok(c, out):
    rec = recompute(c, out["weights"], out["multipliers"])
    return max(rec["primal_residual"], rec["dual_residual"], rec["complementary_slackness"]) <= 1e-8


def base(**kw):
    d = {"label": "SIMULATED hand case for the acceptance suite, not a real portfolio", "gamma": 1.0, "sector": [0, 0],
         "sector_caps": [2.0], "turnover_limit": 2.0, "sigma": [[1.0, 0.0], [0.0, 1.0]], "lower": [-1.0, -1.0],
         "upper": [2.0, 2.0]}
    d.update(kw)
    return d


CANDIDATES = {
    "C1 lower binding, one billionth above start": (base(mu=[-1000.0, 0.0], w0=[0.5, 0.5], lower=[0.5 + 5e-10, -1.0]),
                                                    [0.5 + 5e-10, 0.5 - 5e-10]),
    "C2 lower binding, one billionth above start, tau 1e-9": (
        base(mu=[-1000.0, 0.0], w0=[0.5, 0.5], lower=[0.5 + 5e-10, -1.0], turnover_limit=1e-9),
        [0.5 + 5e-10, 0.5 - 5e-10]),
    "C3 three assets, sector cap breached by one billionth, first member at its bound": (
        {"label": "SIMULATED", "gamma": 1.0, "mu": [-1000.0, 0.0, 0.0], "w0": [0.3, 0.3, 0.4],
         "sigma": [[1.0, 0, 0], [0, 1.0, 0], [0, 0, 1.0]], "lower": [0.3, -1.0, -1.0], "upper": [2.0, 2.0, 2.0],
         "sector": [0, 0, 1], "sector_caps": [0.6 - 5e-10, 1.0], "turnover_limit": 2.0},
        [0.3, 0.3 - 5e-10, 0.4 + 5e-10]),
}
MUTANT_DIR = ROOT + "/ledgers/M7/mutants/"
mutants = {os.path.basename(p)[:-3]: p for p in sorted(glob.glob(MUTANT_DIR + "r16_*.py"))}
ref = load(ROOT + "/course/modules/M/M7/grader/reference.py", "ref_cand")
mods = {k: load(p, "m_" + k[:6]) for k, p in mutants.items()}
for label, (c, expected) in CANDIDATES.items():
    row = []
    try:
        out = ref.allocate(dict(c))
        ok = all(abs(out["weights"][i] - expected[i]) <= 1e-8 for i in range(len(expected))) and cert_ok(c, out)
        row.append(f"reference={'PASS' if ok else 'FAIL'} w={[round(v, 12) for v in out['weights']]}")
    except Exception as exc:  # report, do not hide
        row.append(f"reference=ERROR {type(exc).__name__}: {exc}")
    failing = []
    for k, m in mods.items():
        try:
            o = m.allocate(dict(c))
            good = all(abs(o["weights"][i] - expected[i]) <= 1e-8 for i in range(len(expected))) and cert_ok(c, o)
        except Exception:
            good = False
        if not good:
            failing.append(k[:6])
    print(label, "|", row[0], "| mutants failing:", failing)
