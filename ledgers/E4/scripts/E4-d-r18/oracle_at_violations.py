"""Round 18: at mutant_v17_02 violation points (page domain), compare the grader oracle with the reference formula and
with the mutant's reported gap, so the violation is not an artefact of the reference formula."""
import importlib.util, math, sys
sys.path.insert(0, "/Users/billyribeiro/.fanout/scratch-E4-d-r18/probe")
import solver as ref
import test_project as tp
spec = importlib.util.spec_from_file_location("mut", "/Users/billyribeiro/.fanout/wt/verifyE18-E4-d/ledgers/E4/equivalent/mutant_v17_02_price_slope_drops_uninformed_term.py")
mut = importlib.util.module_from_spec(spec); spec.loader.exec_module(mut)
pts = [(3.3245979322709314e-22, 0.059130434782608696), (1e-6, 0.0598), (1e-3, 0.0598), (1e-2, 0.0598), (0.1, 0.0598), (1.0, 0.0598), (1.0, 0.1), (0.6, 0.02)]
for sd, c in pts:
    m = mut.solve_model(sd, c); r = ref.solve_model(sd, c)
    lam = m["informed_fraction"]
    if not (0 < lam < 1):
        print("not interior", sd, c, lam); continue
    orc = tp.oracle_gap(lam, sd, c)
    rf = ref.indifference_gap(lam, sd, c)
    print(f"sd={sd:.3e} c={c} lam={lam:.6e} mut_gap-oracle={m['indifference_gap']-orc:+.3e} "
          f"ref_gap-oracle={r['indifference_gap']-orc:+.3e} mut_gap-refformula={m['indifference_gap']-rf:+.3e} ref_formula-oracle={rf-orc:+.3e}")
