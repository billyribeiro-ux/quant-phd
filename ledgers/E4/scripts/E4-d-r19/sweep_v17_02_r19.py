"""Round 19 re-run of the round-18 sweep (paths moved to the r19 checkout): actual (not bounded) discrepancy |mut_gap(lam_m) - reference_formula(lam_m)| of mutant_v17_02 over
(a) the autograder box sd in [0.5,0.75], cost in [0.12,0.15] (200 x 200), (b) the page domain sd in [1e-50, 1e2],
cost in [0, 0.34] (log-spaced sd, 300 x 300). Reports the maxima and the locations."""
import importlib.util, math, sys
import os; sys.path.insert(0, os.environ["SOLVER_DIR"])
import solver as ref
spec = importlib.util.spec_from_file_location("mut", "/Users/billyribeiro/.fanout/wt/verifyE19-E4-d/ledgers/E4/mutants/mutant_v17_02_price_slope_drops_uninformed_term.py")
mut = importlib.util.module_from_spec(spec); spec.loader.exec_module(mut)

def scan(sds, cs, label):
    best = (0.0, None); n = 0; over = 0
    for sd in sds:
        for c in cs:
            m = mut.solve_model(sd, c)
            lam = m["informed_fraction"]
            if not (0.0 < lam < 1.0):
                continue
            n += 1
            rf = ref.indifference_gap(lam, sd, c)
            d = abs(m["indifference_gap"] - rf) / max(1.0, abs(rf))
            if d > 1e-14:
                over += 1
            if d > best[0]:
                best = (d, (sd, c, lam, m["indifference_gap"], rf))
    print(label, "interior", n, "over_1e-14", over, "max_rel", best[0], best[1])

N = 200
box_sd = [0.5 + 0.25 * i / (N - 1) for i in range(N)]
box_c = [0.12 + 0.03 * j / (N - 1) for j in range(N)]
scan(box_sd, box_c, "BOX")
dom_sd = [10 ** (-50 + 52 * i / 299) for i in range(300)]
dom_c = [0.34 * j / 299 for j in range(300)]
scan(dom_sd, dom_c, "DOMAIN")
