"""Round-15 probe (repository script). Page-valid hand inputs with a turnover limit in (0, 1e-9] or a bound 1e-9 above
the start, and large expected returns. Reports, for the reference and for the equivalence candidates r05, v10_02 and r04:
the certificate the suite would recompute from the page's definitions, the agreement with the reported fields (1e-9),
and an exact-Fraction comparison of the reference's objective with a feasible point moved by tau/2 along (+1,-1).
Run from the repository root: .venv/bin/python -I ledgers/M7/scripts/M7-d-r15/tiny_tau_probe_r15.py"""
import importlib.util, os, sys
from fractions import Fraction as F
ROOT = os.getcwd()
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m; spec.loader.exec_module(m); return m
ref = load(ROOT + "/course/modules/M/M7/grader/reference.py", "ref_probe")
EQ = ROOT + "/ledgers/M7/equivalent/"
cands = {"r05": load(EQ + "r05_turnover_total_slackness_term_zeroed.py", "c_r05"),
         "v10_02": load(EQ + "v10_02_complementary_slackness_signed_not_absolute.py", "c_v10_02"),
         "r04": load(EQ + "r04_budget_left_out_of_primal_residual.py", "c_r04")}

def recompute(c, w, m):
    n = len(c["mu"]); d = [w[i] - c["w0"][i] for i in range(n)]; t = [abs(x) for x in d]
    ineq = [(m["lower"][i], c["lower"][i] - w[i]) for i in range(n)] + [(m["upper"][i], w[i] - c["upper"][i]) for i in range(n)]
    ineq += [(m["sector"][k], sum(w[i] for i in range(n) if c["sector"][i] == k) - c["sector_caps"][k]) for k in range(len(c["sector_caps"]))]
    ineq += [(m["turnover_plus"][i], d[i] - t[i]) for i in range(n)] + [(m["turnover_minus"][i], -d[i] - t[i]) for i in range(n)]
    ineq += [(m["turnover_total"], sum(t) - c["turnover_limit"])]
    return {"primal_residual": max([0.0, abs(sum(w) - 1)] + [g for _, g in ineq]),
            "dual_residual": max(0.0, -min(x for x, _ in ineq)),
            "complementary_slackness": max(abs(x * g) for x, g in ineq)}

def case(mu, tau, upper0=2.0):
    return {"label": "SIMULATED probe", "gamma": 1.0, "mu": mu, "sigma": [[1.0, 0.0], [0.0, 1.0]], "w0": [0.5, 0.5],
            "lower": [-1.0, -1.0], "upper": [upper0, 2.0], "sector": [0, 0], "sector_caps": [2.0], "turnover_limit": tau}

def f_exact(w, mu):  # gamma = 1, Sigma = I, exact Fractions
    return F(1, 2) * sum(x * x for x in w) - sum(mu[i] * w[i] for i in range(2))

cases = [("A mu=[1000,0] tau=1e-9", case([1000.0, 0.0], 1e-9)),
         ("B mu=[100,0] tau=1e-10", case([100.0, 0.0], 1e-10)),
         ("C mu=[10,0] tau=0", case([10.0, 0.0], 0.0)),
         ("D mu=[1,0] tau=1e-9", case([1.0, 0.0], 1e-9)),
         ("E mu=[1000,0] upper0=0.5+1e-9 tau=2", case([1000.0, 0.0], 2.0, upper0=0.5 + 1e-9))]
for label, c in cases:
    out = ref.allocate(c)
    rec = recompute(c, out["weights"], out["multipliers"])
    cert = out["certificate"]
    print(label, "| reference w =", [str(F(x).limit_denominator(10**12)) for x in out["weights"]],
          "| reported complementary =", "%.3g" % cert["complementary_slackness"], "| recomputed complementary =", "%.3g" % rec["complementary_slackness"],
          "| above page tolerance 1e-8:", rec["complementary_slackness"] > 1e-8)
    for name, mod in cands.items():
        o = mod.allocate(c)
        diff = max(abs(o["certificate"][k] - rec[k]) for k in rec)
        print("    candidate %-6s reported complementary = %.3g, agrees with recomputed within 1e-9: %s" % (name, o["certificate"]["complementary_slackness"], diff <= 1e-9))
# exact optimality check, case A and case E
mu = [F(1000), F(0)]
d = F(1, 2) * F(1, 10**9)
moved = [F(1, 2) + d, F(1, 2) - d]
print("case A: f(moved) - f(reference) =", float(f_exact(moved, mu) - f_exact([F(1, 2), F(1, 2)], mu)), "(exact; negative means the reference is not optimal)")
moved_e = [F(1, 2) + F(1, 10**9), F(1, 2) - F(1, 10**9)]
print("case E: f(moved) - f(reference) =", float(f_exact(moved_e, mu) - f_exact([F(1, 2), F(1, 2)], mu)))
