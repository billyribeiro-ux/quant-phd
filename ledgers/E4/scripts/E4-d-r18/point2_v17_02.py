import importlib.util, math, sys
sys.path.insert(0, "/Users/billyribeiro/.fanout/scratch-E4-d-r18/probe")
import solver as ref
spec = importlib.util.spec_from_file_location("mut", "/Users/billyribeiro/.fanout/wt/verifyE18-E4-d/ledgers/E4/equivalent/mutant_v17_02_price_slope_drops_uninformed_term.py")
mut = importlib.util.module_from_spec(spec); spec.loader.exec_module(mut)
A, TV, TE, P = 2.0, 1.0, 1.0, 2.0
def H(lam, sd, c):
    t = lam*lam*TE*TE/(lam*lam*TE + A*A*sd*sd)
    return (TV + t) ** -0.5 - math.exp(A*c)*P ** -0.5
def run(sd, c, label):
    m = mut.solve_model(sd, c); r = ref.solve_model(sd, c)
    lam = m["informed_fraction"]
    ref_formula = ref.indifference_gap(lam, sd, c)
    d_mut_vs_refformula = abs(m["indifference_gap"] - ref_formula) / max(1.0, abs(ref_formula))
    print(f"{label}: sd={sd!r} c={c!r} lam_mut={lam!r} lam_ref={r['informed_fraction']!r} "
          f"same_lam={lam == r['informed_fraction']} gap_mut={m['indifference_gap']!r} gap_ref_formula={ref_formula!r} "
          f"rel_diff_mut_vs_ref_formula={d_mut_vs_refformula:.3e} ref_reported_gap_minus_formula={r['indifference_gap'] - ref.indifference_gap(r['informed_fraction'], sd, c)!r}")
run(3.135710839812719e-50, 0.05977124999999999, "scan_worst")
for sd in (1e-50, 1e-49, 3e-50, 1e-45, 1e-40, 1e-20, 1e-6):
    for c in (0.0, 0.01, 0.0598, 0.13, 0.2):
        m = mut.solve_model(sd, c)
        if 0 < m["informed_fraction"] < 1:
            run(sd, c, "grid")
