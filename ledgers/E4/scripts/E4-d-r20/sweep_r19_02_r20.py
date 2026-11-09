"""Round-20 check of the equivalence claim for mutant_r19_02 over the page's whole domain (not a new mutant).

Runs the reference solve_model and the r19_02 variant (ledgers/E4/equivalent/...) on a log-spaced grid of noise volumes
from 1e-50 to 1e2 and costs from 0 to 0.34, and compares each reported gap with the suite's 60-digit Proposition 3 gap
(prop3_gap_exact, copied verbatim from grader/test_project.py) at the fraction that solver reports.
Usage: python3 -I sweep_r19_02_r20.py <checkout-root>
"""
import importlib.util
import math
import sys
from decimal import Decimal, localcontext

root = sys.argv[1]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ref = load(root + "/course/modules/E/E4/grader/reference.py", "ref")
mut = load(root + "/ledgers/E4/equivalent/mutant_r19_02_price_denominator_drops_uninformed_posterior_precision.py", "mut")
A_CARA, TAU_V, TAU_E = 2.0, 1.0, 1.0


def prop3_gap_exact(lam, sd, cost):
    with localcontext() as ctx:
        ctx.prec = 60
        lam_d, sd_d, cost_d = Decimal(lam), Decimal(sd), Decimal(cost)
        a, tv, te = Decimal(A_CARA), Decimal(TAU_V), Decimal(TAU_E)
        tau_y = lam_d * lam_d * te * te / (lam_d * lam_d * te + a * a * sd_d * sd_d)
        b_s = (lam_d * te + (1 - lam_d) * tau_y) / (lam_d * (tv + te) + (1 - lam_d) * (tv + tau_y))
        b_u = -a * b_s / (lam_d * te)
        omega = 1 / tv + b_s * b_s * (1 / tv + 1 / te) + b_u * b_u * sd_d * sd_d - 2 * b_s / tv
        v_i, v_u = 1 / (tv + te), 1 / (tv + tau_y)
        return (v_u.sqrt() - (a * cost_d).exp() * v_i.sqrt()) / omega.sqrt()


def worst(mod, sds, costs):
    n_int = 0
    n_over = 0
    worst_err = (0.0, None)
    for sd in sds:
        for c in costs:
            out = mod.solve_model(sd, c)
            lam = out["informed_fraction"]
            if not (0.0 < lam < 1.0):
                continue
            n_int += 1
            ex = float(prop3_gap_exact(lam, sd, c))
            err = abs(out["indifference_gap"] - ex) / max(1.0, abs(ex))
            if err > 1e-14:
                n_over += 1
            if err > worst_err[0]:
                worst_err = (err, (sd, c, lam))
    return n_int, n_over, worst_err


N_SD = int(sys.argv[2]) if len(sys.argv) > 2 else 400
sds = [10 ** (-50 + 52 * i / (N_SD - 1)) for i in range(N_SD)]
costs = [0.34 * j / 39 for j in range(40)] + [1e-9, 0.059130434782608696]
for name, mod in (("reference", ref), ("r19_02_variant", mut)):
    n_int, n_over, (err, where) = worst(mod, sds, costs)
    print(f"{name}: interior points {n_int}, error above 1e-14: {n_over}, worst error {err:.4e} at sd, cost, lam = {where}")
